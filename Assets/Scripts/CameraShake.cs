using System.Collections;
using UnityEngine;

public class CameraShake : MonoBehaviour
{
    [SerializeField] private float shakeDuration = 1.0f; // Durata del tremore
    [SerializeField] private float shakeIntensity = 0.03f; // Intensità del tremore
    [SerializeField] private float intensityVariation = 0.2f; // Variazione casuale dell'intensità per ogni frame
    [SerializeField] public AudioSource peopleWorryingAudio;
    [SerializeField] private AudioSource rumblingAudio;
    [SerializeField] private float fadeInDuration = 1.0f;


    private Vector3 originalPosition;

    private Coroutine shakeCoroutine;

    public DoorManager doorManager; // Assegna nel campo dell’inspector

    public RandomBlinkingLights blinkingLights;

    public WeatherHandler weatherHandler;

    void Start()
    {
        // Salva la posizione iniziale della camera
        originalPosition = transform.localPosition;
    }


    public void StartContinuousShake()
    {
        shakeCoroutine = StartCoroutine(ContinuousShake());
        Debug.Log("Tremore continuo della visuale avviato!");
        rumblingAudio.Play();
        StartCoroutine(FadeInAudio());

        // Avvia spegnimento graduale dopo 30s
        StartCoroutine(StopShakeAfterDelay(30f));
    }

    private IEnumerator ContinuousShake()
    {
        float elapsedShakeTime = 0f;
        bool hasIncreased = false;

        while (true)
        {
            if (elapsedShakeTime > 10f && !hasIncreased)
            {
                shakeIntensity *= 1.5f;
                hasIncreased = true;
            }

            float currentIntensity = shakeIntensity + Random.Range(-intensityVariation, intensityVariation);

            Vector3 shakeOffset = new Vector3(
                Random.Range(-currentIntensity, currentIntensity),
                Random.Range(-currentIntensity, currentIntensity),
                Random.Range(-currentIntensity, currentIntensity)
            );

            transform.localPosition = originalPosition + shakeOffset;
            elapsedShakeTime += Time.deltaTime;
            yield return null;
        }
    }

    private IEnumerator FadeInAudio()
    {
        Debug.Log("Fade in iniziato!");
        if (peopleWorryingAudio == null) yield break;

        peopleWorryingAudio.volume = 0f;
        peopleWorryingAudio.Play();

        float elapsedTime = 0f;
        while (elapsedTime < fadeInDuration)
        {
            peopleWorryingAudio.volume = Mathf.Lerp(0f, 0.3f, elapsedTime / fadeInDuration);
            elapsedTime += Time.deltaTime;
            yield return null;
        }

        peopleWorryingAudio.volume = 0.3f; // Assicurati che arrivi al volume massimo
        Debug.Log("PeopleWorryingAudio fade in completato!");
    }

    private IEnumerator StopShakeAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        Debug.Log("Interruzione graduale dello shake...");
        StartCoroutine(GraduallyStopShake(7f)); // tempo di fade-out dello shake
    }

    private IEnumerator GraduallyStopShake(float duration)
    {
        float startIntensity = shakeIntensity;
        float timeElapsed = 0f;

        if (blinkingLights != null && blinkingLights.isBlinking)
        {
            blinkingLights.StopBlinkingLights();
        }


        while (timeElapsed < duration)
        {
            float t = timeElapsed / duration;
            shakeIntensity = Mathf.Lerp(startIntensity, 0f, t);

            timeElapsed += Time.deltaTime;
            yield return null;
        }

        shakeIntensity = 0f;
        transform.localPosition = originalPosition;

        if (shakeCoroutine != null)
            StopCoroutine(shakeCoroutine);

        // ✅ Notifica il DoorManager centrale
        if (doorManager != null)
        {
            doorManager.OnShakeEnded();
            Debug.Log("Notificato DoorManager: fine shaking.");
        }
        else
        {
            Debug.LogWarning("DoorManager non assegnato a CameraShake!");
        }

        Debug.Log("Shake terminato.");

        if (weatherHandler != null)
        {
            weatherHandler.StopWeatherEffects();
        }

    }


}