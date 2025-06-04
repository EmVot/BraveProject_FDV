using UnityEngine;
using System.Collections.Generic;

public class DoorManager : MonoBehaviour
{
    public List<DoorMovement> doors; // Assegna tutti gli sportelli nell'inspector
    public AudioSource screamingSound;

    public void OnShakeEnded()
    {
        // Ferma screamingSound
        if (screamingSound != null && screamingSound.isPlaying)
        {
            screamingSound.Stop();
            Debug.Log("screamingSound interrotto da DoorManager");
        }

        // Fa rientrare e chiudere tutti gli sportelli
        foreach (DoorMovement door in doors)
        {
            if (door != null)
            {
                door.ReturnMasksAndCloseDoors();
            }
        }
    }
}
