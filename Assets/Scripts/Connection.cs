using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using System.Collections;

public class ExposureWeatherHandler : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Volume globale per Exposure e HDRI Sky
    private Exposure exposureComponent; // Riferimento alla proprietà Exposure del Volume

    [SerializeField] private ParticleSystem rainParticleSystem; // Sistema particellare della pioggia
    [SerializeField] private AudioSource rainAudioSource; // AudioSource collegato al GameObject della pioggia
    [SerializeField] private float rainEmissionDuration = 3.0f; // Durata transizione emissione pioggia
    [SerializeField] private float maxRainVolume = 0.018f; // Volume massimo della pioggia
    [SerializeField] private GameObject lightningParent; // GameObject del fulmine

    private TcpListener listener;
    public int port = 12345;
    private float targetExposure; // Valore di esposizione da raggiungere
    private bool isExposureUpdated = false; // Flag per segnalare l'aggiornamento dell'esposizione
    private bool exposureTransitionComplete = false; // Flag per segnalare il completamento della transizione di esposizione
    private bool rainStarted = false; // Evita avvio multiplo della routine

    void Start()
    {
        // Ottieni il componente Exposure dal Volume
        if (skyAndFogVolume.profile.TryGet(out exposureComponent) && exposureComponent != null)
        {
            Debug.Log("Componente Exposure trovato. Pronto a gestire l'esposizione e il meteo.");
        }
        else
        {
            Debug.LogWarning("Componente Exposure non trovato. Assicurati che il Volume abbia un override Exposure.");
            return;
        }

        // Avvia il listener socket
        listener = new TcpListener(IPAddress.Any, port);
        listener.Start();
        Debug.Log($"Server avviato sulla porta {port}. In attesa di connessioni...");
        listener.BeginAcceptTcpClient(OnClientConnect, null);

        // Inizializza i sistemi di pioggia e fulmini
        lightningParent.SetActive(false);
        rainAudioSource.volume = 0f;
    }

    private void OnClientConnect(IAsyncResult result)
    {
        try
        {
            TcpClient client = listener.EndAcceptTcpClient(result);
            NetworkStream stream = client.GetStream();
            byte[] buffer = new byte[1024];
            int byteCount = stream.Read(buffer, 0, buffer.Length); // Legge il messaggio inviato
            string receivedMessage = Encoding.UTF8.GetString(buffer, 0, byteCount);

            Debug.Log($"Messaggio ricevuto: {receivedMessage}");

            // Parsing del JSON per ottenere il valore di esposizione
            var message = JsonUtility.FromJson<ExposureMessage>(receivedMessage);
            targetExposure = message.exposure; // Valore di esposizione ricevuto
            isExposureUpdated = true; // Segnala che il valore deve essere aggiornato nel main thread

            // Chiudi lo stream e il client
            stream.Close();
            client.Close();

            // Continua ad accettare connessioni
            listener.BeginAcceptTcpClient(OnClientConnect, null);
        }
        catch (Exception e)
        {
            Debug.LogError($"Errore: {e.Message}");
        }
    }

    void Update()
    {
        // Controlla se il valore dell'esposizione deve essere aggiornato
        if (isExposureUpdated)
        {
            if (exposureComponent.mode.value == ExposureMode.Fixed)
            {
                // Avvia una transizione graduale
                StartCoroutine(TransitionExposure(targetExposure, 5.0f)); // Durata della transizione: 5 secondi
                Debug.Log($"Avvio della transizione di esposizione verso: {targetExposure}");
            }
            else
            {
                Debug.LogWarning("La modalità di Exposure non è impostata su Fixed. Nessuna modifica applicata.");
            }

            isExposureUpdated = false; // Reset flag
        }

        // Avvia la routine del maltempo se la transizione di esposizione è completata
        if (exposureTransitionComplete && !rainStarted)
        {
            Debug.Log("Transizione completata. Avvio routine di maltempo!");
            rainStarted = true; // Evita avvio multiplo della routine
            StartRainRoutine();
        }
    }

    private IEnumerator TransitionExposure(float newExposure, float duration)
    {
        float currentExposure = exposureComponent.fixedExposure.value;
        float elapsedTime = 0;

        while (elapsedTime < duration)
        {
            exposureComponent.fixedExposure.value = Mathf.Lerp(currentExposure, newExposure, elapsedTime / duration);
            elapsedTime += Time.deltaTime;
            yield return null; // Aspetta il frame successivo
        }

        exposureComponent.fixedExposure.value = newExposure;
        exposureTransitionComplete = true; // Segnala il completamento della transizione
        Debug.Log($"Transizione completata. Fixed Exposure impostato a: {newExposure}");
    }

    private void StartRainRoutine()
    {
        // Avvia la transizione graduale della pioggia e dell'audio
        StartCoroutine(RainAndSoundTransition());
    }

    private IEnumerator RainAndSoundTransition()
    {
        float rainEmissionTime = 0f;

        while (rainEmissionTime < rainEmissionDuration)
        {
            rainEmissionTime += Time.deltaTime;
            float t = Mathf.Clamp01(rainEmissionTime / rainEmissionDuration);

            // Modifica gradualmente l'emissione del Particle System
            var emission = rainParticleSystem.emission;
            emission.rateOverTime = Mathf.Lerp(0, 10000, t);

            // Modifica gradualmente il volume dell'AudioSource
            rainAudioSource.volume = Mathf.Lerp(0, maxRainVolume, t);

            yield return null; // Aspetta il frame successivo
        }

        lightningParent.SetActive(true); // Attiva i fulmini
        Debug.Log("Routine maltempo completata: pioggia massima e fulmini attivati!");
    }

    void OnDestroy()
    {
        if (listener != null)
        {
            listener.Stop();
            Debug.Log("Server socket chiuso.");
        }
    }

    [Serializable]
    public class ExposureMessage
    {
        public float exposure; // Valore di esposizione ricevuto dal JSON
    }
}

/*using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using System.Collections;

public class ExposureSocketHandler : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Volume globale per l'Exposure
    private Exposure exposureComponent; // Riferimento alla proprietà Exposure del Volume
    private TcpListener listener;
    public int port = 12345;
    private float targetExposure; // Valore di esposizione da raggiungere
    private bool isExposureUpdated = false; // Flag per segnalare l'aggiornamento

    void Start()
    {
        // Ottieni il componente Exposure dal Volume
        if (skyAndFogVolume.profile.TryGet(out exposureComponent) && exposureComponent != null)
        {
            Debug.Log("Componente Exposure trovato. Pronto per gestire l'esposizione tramite socket.");
        }
        else
        {
            Debug.LogWarning("Componente Exposure non trovato. Assicurati che il Volume abbia un override Exposure.");
            return;
        }

        // Avvia il listener socket
        listener = new TcpListener(IPAddress.Any, port);
        listener.Start();
        Debug.Log($"Server avviato sulla porta {port}. In attesa di connessioni...");
        listener.BeginAcceptTcpClient(OnClientConnect, null);
    }

    private void OnClientConnect(IAsyncResult result)
    {
        try
        {
            TcpClient client = listener.EndAcceptTcpClient(result);
            NetworkStream stream = client.GetStream(); // Stream di dati
            byte[] buffer = new byte[1024];
            int byteCount = stream.Read(buffer, 0, buffer.Length); // Legge il messaggio inviato
            string receivedMessage = Encoding.UTF8.GetString(buffer, 0, byteCount);

            Debug.Log($"Messaggio ricevuto: {receivedMessage}");

            // Parsing del JSON per ottenere il valore di esposizione
            var message = JsonUtility.FromJson<ExposureMessage>(receivedMessage);
            targetExposure = message.exposure; // Memorizza il valore ricevuto
            isExposureUpdated = true; // Segnala che il valore deve essere aggiornato nel main thread

            // Chiudi lo stream e il client
            stream.Close();
            client.Close();

            // Continua ad accettare connessioni
            listener.BeginAcceptTcpClient(OnClientConnect, null);
        }
        catch (Exception e)
        {
            Debug.LogError($"Errore: {e.Message}");
        }
    }

    void Update()
    {
        // Controlla se il valore dell'esposizione deve essere aggiornato
        if (isExposureUpdated)
        {
            if (exposureComponent.mode.value == ExposureMode.Fixed)
            {
                // Avvia una transizione graduale
                StartCoroutine(TransitionExposure(targetExposure, 5.0f)); // Durata 5 secondi
            }
            else
            {
                Debug.LogWarning("La modalità di Exposure non è impostata su Fixed. Nessuna modifica applicata.");
            }

            isExposureUpdated = false; // Reset flag
        }
    }

    private IEnumerator TransitionExposure(float newExposure, float duration)
    {
        float currentExposure = exposureComponent.fixedExposure.value;
        float elapsedTime = 0;

        while (elapsedTime < duration)
        {
            exposureComponent.fixedExposure.value = Mathf.Lerp(currentExposure, newExposure, elapsedTime / duration);
            elapsedTime += Time.deltaTime;
            yield return null; // Aspetta il frame successivo
        }

        // Assicura che il valore finale sia impostato correttamente
        exposureComponent.fixedExposure.value = newExposure;
        Debug.Log($"Transizione completata. Fixed Exposure impostato a: {newExposure}");
    }

    void OnDestroy()
    {
        if (listener != null)
        {
            listener.Stop();
            Debug.Log("Server socket chiuso.");
        }
    }

    [Serializable]
    public class ExposureMessage
    {
        public float exposure; // Valore di esposizione ricevuto dal JSON
    }
}*/