using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using System.Collections;

public class ExposureHandler : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Volume globale per l'Exposure
    private Exposure exposureComponent; // Riferimento alla proprietà Exposure del Volume

    private TcpListener listener;
    public int port = 12345;
    private float targetExposure; // Valore di esposizione da raggiungere
    private bool isExposureUpdated = false; // Flag per segnalare l'aggiornamento dell'esposizione
    private bool exposureTransitionComplete = false; // Flag per segnalare il completamento della transizione

    public event Action OnExposureTransitionComplete; // Evento per segnalare il completamento della transizione

    [SerializeField] private AudioSource cheeringSound;

    void Start()
    {
        // Ottieni il componente Exposure dal Volume
        if (skyAndFogVolume.profile.TryGet(out exposureComponent) && exposureComponent != null)
        {
            Debug.Log("Componente Exposure trovato. Pronto a gestire l'esposizione.");
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
            NetworkStream stream = client.GetStream();
            byte[] buffer = new byte[1024];
            int byteCount = stream.Read(buffer, 0, buffer.Length);
            string receivedMessage = Encoding.UTF8.GetString(buffer, 0, byteCount);

            Debug.Log($"Messaggio ricevuto: {receivedMessage}");

            // Parsing del JSON per ottenere il valore di esposizione
            var message = JsonUtility.FromJson<ExposureMessage>(receivedMessage);
            targetExposure = message.exposure; // Valore di esposizione ricevuto
            isExposureUpdated = true;

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
                StartCoroutine(TransitionExposure(targetExposure, 5.0f));
                Debug.Log($"Avvio della transizione di esposizione verso: {targetExposure}");
            }
            else
            {
                Debug.LogWarning("La modalità di Exposure non è impostata su Fixed.");
            }

            isExposureUpdated = false;
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
            yield return null;
        }

        exposureComponent.fixedExposure.value = newExposure;
        exposureTransitionComplete = true;
        Debug.Log($"Transizione completata. Fixed Exposure impostato a: {newExposure}");

        // Segnala il completamento della transizione
        OnExposureTransitionComplete?.Invoke();
    }

    private WeatherHandler weatherHandler;

    void Awake()
    {
        weatherHandler = FindObjectOfType<WeatherHandler>();
        OnExposureTransitionComplete += weatherHandler.StartRainRoutine;
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

    public void RestoreExposure(float originalExposure, float duration)
    {
        if (exposureComponent == null) return;

        StartCoroutine(RestoreExposureCoroutine(originalExposure, duration));
    }

    private IEnumerator RestoreExposureCoroutine(float originalExposure, float duration)
    {
        float startExposure = exposureComponent.fixedExposure.value;
        float elapsed = 0f;

        while (elapsed < duration)
        {
            exposureComponent.fixedExposure.value = Mathf.Lerp(startExposure, originalExposure, elapsed / duration);
            elapsed += Time.deltaTime;
            yield return null;
        }

        exposureComponent.fixedExposure.value = originalExposure;
        Debug.Log($"Exposure ripristinata a {originalExposure}");

        // ✅ Avvia il cheeringSound con fade-in
        if (cheeringSound != null)
        {
            cheeringSound.volume = 0f;
            cheeringSound.Play();

            float fadeInDuration = 5.0f;
            float fadeInElapsed = 0f;
            float targetVolume = 0.8f;

            while (fadeInElapsed < fadeInDuration)
            {
                cheeringSound.volume = Mathf.Lerp(0f, targetVolume, fadeInElapsed / fadeInDuration);
                fadeInElapsed += Time.deltaTime;
                yield return null;
            }

            cheeringSound.volume = targetVolume;
            Debug.Log("CheeringSound portato al volume finale.");

            // ⏳ Attendi 7 secondi prima del fade-out
            yield return new WaitForSeconds(7f);

            // 🔇 Avvia fade-out
            float fadeOutDuration = 5.0f;
            float fadeOutElapsed = 0f;
            float startVolume = cheeringSound.volume;

            while (fadeOutElapsed < fadeOutDuration)
            {
                cheeringSound.volume = Mathf.Lerp(startVolume, 0f, fadeOutElapsed / fadeOutDuration);
                fadeOutElapsed += Time.deltaTime;
                yield return null;
            }

            cheeringSound.volume = 0f;
            cheeringSound.Stop();
            Debug.Log("CheeringSound interrotto gradualmente.");
        }
    }


}