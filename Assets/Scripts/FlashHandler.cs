using System.Collections;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;

public class FlashHandler : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Volume globale per Exposure
    private Exposure exposureComponent;

    [SerializeField] private AudioSource flashSound; // Audio per il flash

    void Start()
    {
        // Ottieni il componente Exposure dal Volume
        if (skyAndFogVolume.profile.TryGet(out exposureComponent) && exposureComponent != null)
        {
            Debug.Log("Componente Exposure trovato! Pronto per gestire il flash di luce.");
        }
        else
        {
            Debug.LogWarning("Componente Exposure non trovato. Assicurati che il Volume abbia un override Exposure.");
        }
    }

    public void TriggerFlash(float flashDuration, float flashValue)
    {
        if (exposureComponent != null)
        {
            StartCoroutine(Flash(flashDuration, flashValue));
        }
    }

    private IEnumerator Flash(float duration, float flashValue)
    {
        float originalExposure = exposureComponent.fixedExposure.value;

        // **Riproduce il suono**
        if (flashSound != null)
        {
            flashSound.Play();
            Debug.Log("Suono del flash riprodotto!");
        }

        // Imposta l'esposizione temporanea
        exposureComponent.fixedExposure.value = flashValue;
        Debug.Log($"Flash di luce avviato! Valore esposizione: {flashValue}");

        yield return new WaitForSeconds(duration);

        // Ripristina l'esposizione originale
        exposureComponent.fixedExposure.value = originalExposure;
        Debug.Log($"Flash di luce completato! Valore esposizione ripristinato: {originalExposure}");
    }
}