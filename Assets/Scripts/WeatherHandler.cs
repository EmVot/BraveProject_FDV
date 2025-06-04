using System.Collections;
using UnityEngine;
using System.Collections.Generic;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;

public class WeatherHandler : MonoBehaviour
{
    [SerializeField] private ParticleSystem rainParticleSystem; // Sistema particellare della pioggia
    [SerializeField] private AudioSource rainAudioSource; // AudioSource collegato al GameObject della pioggia
    [SerializeField] private float rainEmissionDuration = 10.0f; // Durata transizione emissione pioggia
    [SerializeField] private float maxRainVolume = 0.018f; // Volume massimo della pioggia
    [SerializeField] private GameObject lightningParent; // GameObject del fulmine
    [SerializeField] private CameraShake cameraShake; // Riferimento al gestore del tremore della camera
    [SerializeField] private float cameraShakeIntensity = 0.5f; // Intensità del tremore della camera
    [SerializeField] private Volume skyAndFogVolume; // Volume globale per gestire Exposure

    private Exposure exposureComponent; // Componente Exposure per il flash di luce
    private bool rainStarted = false; // Flag per evitare avvio multiplo della pioggia
    private bool cameraShakeStarted = false; // Flag per avviare una sola volta il tremore continuo

    [SerializeField] private Material[] emissiveMaterials; // I due materiali da modificare
    [SerializeField] private float emissionStartIntensity = 5f;
    [SerializeField] private float emissionTargetIntensity = 5000f;
    [SerializeField] private AudioSource seatbeltSound; // Un AudioSource diverso da quello della pioggia
    [SerializeField] private AudioSource seatbeltFastenSound; // Un AudioSource diverso da quello della pioggia

    [SerializeField] private List<DoorMovement> doorMovements; // Lista degli oggetti con DoorMovement

    [SerializeField] private FlashHandler flashHandler;
    [SerializeField] private RandomBlinkingLights randomBlinkingLights;

    public ExposureHandler exposureHandler;


    void Start()
    {
        lightningParent.SetActive(false);
        rainAudioSource.volume = 0f;

        // Ottieni il componente Exposure dal Volume
        if (skyAndFogVolume.profile.TryGet(out exposureComponent) && exposureComponent != null)
        {
            Debug.Log("Componente Exposure trovato. Pronto per il flash di luce.");
        }
        else
        {
            Debug.LogWarning("Componente Exposure non trovato. Assicurati che il Volume abbia un override Exposure.");
        }

        // Imposta l'emissione iniziale dei materiali
        foreach (Material mat in emissiveMaterials)
        {
            if (mat.HasProperty("_EmissiveColor"))
            {
                Color emissiveColor = Color.white * emissionStartIntensity;
                mat.EnableKeyword("_EMISSION");
                mat.SetColor("_EmissiveColor", emissiveColor);
                mat.SetFloat("_EmissiveExposureWeight", 1.0f);
            }
        }

    }

    public void StartRainRoutine()
    {
        if (!rainStarted)
        {
            rainStarted = true;
            StartCoroutine(RainAndSoundTransition());
            Debug.Log("Routine maltempo avviata!");
        }
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

            yield return null;
        }

        lightningParent.SetActive(true);
        Debug.Log("Routine maltempo completata: pioggia massima e fulmini attivati!");

        StartCoroutine(SeatbeltRoutine());

        // Avvia effetti successivi (flash e tremore) dopo 15 secondi
        yield return new WaitForSeconds(15f);
        TriggerFlashAndShake();
    }

    private IEnumerator SeatbeltRoutine()
    {
        yield return new WaitForSeconds(5f); // Attesa prima dell’effetto

        Debug.Log("Cambio emissione e suono avviato dopo 5 secondi");

        if (seatbeltSound != null)
        {
            seatbeltSound.Play();
        }

        foreach (Material mat in emissiveMaterials)
        {
            if (mat.HasProperty("_EmissiveColor"))
            {
                Color emissiveColor = Color.white * emissionTargetIntensity;
                mat.EnableKeyword("_EMISSION");
                mat.SetColor("_EmissiveColor", emissiveColor);
                mat.SetFloat("_EmissiveExposureWeight", 1.0f); // Controllo HDR

                // Se vuoi aggiornare GI dinamica (opzionale):
                // DynamicGI.SetEmissive(renderer, emissiveColor);
            }
        }

        if (seatbeltFastenSound != null)
        {
            seatbeltFastenSound.Play();
        }
    }


    private void TriggerFlashAndShake()
    {
        Debug.Log("Avvio degli effetti: flash di luce e tremore continuo della camera!");

        // Avvia il flash di luce
        flashHandler.TriggerFlash(1.0f, 4.0f);

        // Avvia il tremore continuo della camera
        if (!cameraShakeStarted)
        {
            cameraShakeStarted = true;
            cameraShake.StartContinuousShake();
        }

        StartCoroutine(StartDoorMovementAfterDelay());

        randomBlinkingLights.StartBlinkingLights();
    }

    private IEnumerator StartDoorMovementAfterDelay()
    {
        yield return new WaitForSeconds(10f); // Attendi 10 secondi prima di far muovere gli sportelli

        Debug.Log("Avvio della rotazione degli sportelli dopo il tremore!");
        
        foreach (DoorMovement door in doorMovements)
        {
            if (door != null)
            {
                door.StartMoving();
                Debug.Log($"Movimento avviato per: {door.gameObject.name}");
            }
        }
    }

    public void StopWeatherEffects()
    {
        Debug.Log("Interruzione effetti meteo avviata.");
        lightningParent.SetActive(false);
        StartCoroutine(StopRainGradually());
        exposureHandler.RestoreExposure(10.0f,25.0f); 
    }

    private IEnumerator StopRainGradually()
    {
        float elapsedTime = 0f;
        float duration = rainEmissionDuration;

        float startVolume = rainAudioSource.volume;
        float startEmission = rainParticleSystem.emission.rateOverTime.constant;

        while (elapsedTime < duration)
        {
            float t = elapsedTime / duration;

            var emission = rainParticleSystem.emission;
            emission.rateOverTime = Mathf.Lerp(startEmission, 0f, t);
            rainAudioSource.volume = Mathf.Lerp(startVolume, 0f, t);

            elapsedTime += Time.deltaTime;
            yield return null;
        }

        // Assicurati che sia completamente spento
        var finalEmission = rainParticleSystem.emission;
        finalEmission.rateOverTime = 0f;
        rainAudioSource.volume = 0f;

        Debug.Log("Pioggia completamente interrotta.");
    }


}