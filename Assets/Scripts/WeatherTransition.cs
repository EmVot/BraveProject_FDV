using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;

public class WeatherTransition : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Riferimento al Volume globale
    [SerializeField] private float exposureStart = 17.0f; // Valore iniziale di Exposure Compensation
    [SerializeField] private float exposureEnd = 11.0f; // Valore finale di Exposure Compensation
    [SerializeField] private float exposureTransitionDuration = 5.0f; // Durata transizione Exposure Compensation

    [SerializeField] private ParticleSystem rainParticleSystem; // Sistema particellare della pioggia
    [SerializeField] private AudioSource rainAudioSource; // AudioSource collegato al GameObject della pioggia
    [SerializeField] private float rainEmissionDuration = 3.0f; // Durata transizione emissione pioggia
    [SerializeField] private float maxRainVolume = 0.018f; // Volume massimo della pioggia

    [SerializeField] private GameObject lightningParent; // GameObject del fulmine

    private HDRISky hdriSky; // Riferimento all'HDRI Sky
    private float exposureTransitionTime = 0f;
    private float rainEmissionTime = 0f;
    private bool exposureTransitionComplete = false;

    void Start()
    {
        // Ottieni il componente HDRISky dal Volume
        if (skyAndFogVolume.profile.TryGet(out hdriSky) && hdriSky != null)
        {
            // Imposta il valore iniziale di Exposure Compensation
            hdriSky.exposure.value = exposureStart;
            Debug.Log("HDRI Sky trovato! Pronto a iniziare la transizione dell'exposure.");
        }
        else
        {
            Debug.LogWarning("HDRI Sky non trovato. Assicurati che il Volume abbia un override HDRI Sky.");
            return;
        }

        // Inizializza Lightning parent disattivato e il volume dell'audio della pioggia a 0
        lightningParent.SetActive(false);
        rainAudioSource.volume = 0f;
    }

    void Update()
    {
        // **Transizione Graduale del Campo Exposure Compensation**
        if (!exposureTransitionComplete)
        {
            exposureTransitionTime += Time.deltaTime;
            float t = Mathf.Clamp01(exposureTransitionTime / exposureTransitionDuration); // Progresso della transizione

            // Cambia gradualmente il valore di Exposure Compensation
            hdriSky.exposure.value = Mathf.Lerp(exposureStart, exposureEnd, t);
            skyAndFogVolume.profile.isDirty = true; // Forza l'aggiornamento del Volume

            if (t >= 1f)
            {
                exposureTransitionComplete = true;
                Debug.Log("Transizione Exposure Compensation completata!");
            }
        }
        else
        {
            // **Transizione Graduale della Pioggia e dell'Audio**
            rainEmissionTime += Time.deltaTime;
            float t = Mathf.Clamp01(rainEmissionTime / rainEmissionDuration);

            // Modifica gradualmente l'emissione del Particle System
            var emission = rainParticleSystem.emission;
            emission.rateOverTime = Mathf.Lerp(0, 10000, t);

            // Modifica gradualmente il volume dell'AudioSource
            rainAudioSource.volume = Mathf.Lerp(0, maxRainVolume, t);

            if (t >= 1f)
            {
                // Attiva il GameObject dei fulmini quando la pioggia è al massimo
                lightningParent.SetActive(true);
                Debug.Log("Pioggia massima raggiunta, fulmine attivato!");
            }
        }
    }
}