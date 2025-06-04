using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;

public class RotateHDRISky : MonoBehaviour
{
    [SerializeField] private Volume skyAndFogVolume; // Riferimento al Volume
    [SerializeField] private float rotationSpeed = 10.0f; // Velocità di rotazione

    private HDRISky hdriSky;

    void Start()
    {
        // Ottieni il componente HDRI Sky dal Volume
        if (skyAndFogVolume.profile.TryGet(out hdriSky) && hdriSky != null)
        {
            Debug.Log("HDRI Sky trovato! Pronto per ruotare il cielo.");
        }
        else
        {
            Debug.LogWarning("HDRI Sky non trovato. Assicurati che il Volume abbia un override HDRI Sky.");
        }
    }

    void Update()
    {
        if (hdriSky != null)
        {
            // Incrementa la rotazione in base alla velocità
            hdriSky.rotation.value += rotationSpeed * Time.deltaTime;

            // Applica le modifiche al profilo del Volume
            skyAndFogVolume.profile.isDirty = true; // Per garantire l'aggiornamento
        }
    }
}