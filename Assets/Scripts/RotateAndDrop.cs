using UnityEngine;
using System.Collections;

public class DoorMovement : MonoBehaviour
{
    private Vector3 startPosition;
    private Quaternion startRotation;
    private Vector3 targetPosition;
    private Quaternion targetRotation;

    public float moveDuration = 1f; 
    private float elapsedTime = 0f;
    private bool isMoving = false;

    // Mascherine
    public GameObject[] masks;
    private Vector3[] startMaskPositions;
    private Vector3 maskDisplacement = new Vector3(0f, -0.9f, 0f);
    public float maskMoveSpeed = 1f;

    // **Aggiunta audio**
    public AudioSource doorSound;
    public AudioSource screamingSound;

    //public CameraShake cameraShake; // Riferimento a CameraShake per accedere all'audio


    void Start()
    {
        startPosition = transform.position;
        startRotation = transform.rotation;

        targetPosition = new Vector3(startPosition.x, startPosition.y - 0.128f, startPosition.z + 0.145f);
        targetRotation = Quaternion.Euler(startRotation.eulerAngles.x, startRotation.eulerAngles.y, startRotation.eulerAngles.z - 90f);

        startMaskPositions = new Vector3[masks.Length];
        for (int i = 0; i < masks.Length; i++)
        {
            if (masks[i] != null)
                startMaskPositions[i] = masks[i].transform.position;
        }
    }

    void Update()
    {
        if (isMoving)
        {
            elapsedTime += Time.deltaTime;
            float t = elapsedTime / moveDuration;

            transform.position = Vector3.Lerp(startPosition, targetPosition, t);
            transform.rotation = Quaternion.Lerp(startRotation, targetRotation, t);

            StartCoroutine(MoveMasks(t));

            if (t >= 1f)
            {
                isMoving = false;
                Debug.Log("Movimento completato!");
            }
        }
    }

    private IEnumerator MoveMasks(float t)
    {
        yield return new WaitForSeconds(1f);

        for (int i = 0; i < masks.Length; i++)
        {
            if (masks[i] != null)
            {
                Vector3 targetMaskPos = startMaskPositions[i] + maskDisplacement;
                masks[i].transform.position = Vector3.Lerp(startMaskPositions[i], targetMaskPos, t * maskMoveSpeed);
            }
        }
    }

    public void StartMoving()
    {
        if (!isMoving)
        {
            isMoving = true;
            elapsedTime = 0f;

            if (doorSound != null)
            {
                doorSound.Play();
            }

            // Avvia screaming 
            StartCoroutine(PlayScreamingSoundDelayed(1f));
        }
    }


    private IEnumerator PlayScreamingSoundDelayed(float delay)
    {
        yield return new WaitForSeconds(delay); // Attesa prima di avviare il suono

        if (screamingSound != null)
        {
            screamingSound.volume = 0f;  // Inizia con volume a 0
            screamingSound.Play();

            float targetVolume = 1f;
            float fadeDuration = 2f; // Tempo in secondi per arrivare a volume 0.8
            float elapsedTime = 0f;

            while (elapsedTime < fadeDuration)
            {
                elapsedTime += Time.deltaTime;
                screamingSound.volume = Mathf.Lerp(0f, targetVolume, elapsedTime / fadeDuration);
                yield return null;
            }

            screamingSound.volume = targetVolume; // Assicurati che raggiunga esattamente 0.8
        }
    }

    public void ReturnMasksAndCloseDoors()
    {
        StartCoroutine(ReturnMasksThenClose());
    }

    private IEnumerator ReturnMasksThenClose()
    {
        Debug.Log("Rientro mascherine tra 5 secondi...");
        yield return new WaitForSeconds(5f);

        Debug.Log("Rientro mascherine iniziato.");
        float duration = 3.0f;    //1.5 prima
        float elapsed = 0f;

        while (elapsed < duration)
        {
            for (int i = 0; i < masks.Length; i++)
            {
                if (masks[i] != null)
                {
                    masks[i].transform.position = Vector3.Lerp(
                        masks[i].transform.position,
                        startMaskPositions[i],
                        elapsed / duration
                    );
                }
            }

            elapsed += Time.deltaTime;
            yield return null;
        }

        Debug.Log("Mascherine rientrate. Chiusura sportello...");
        CloseDoor();
    }

    private void CloseDoor()
    {
        // Inverti il movimento: vai da target a start
        StartCoroutine(CloseDoorCoroutine());
    }

    private IEnumerator CloseDoorCoroutine()
    {
        float elapsed = 0f;
        float duration = moveDuration;

        // Riproduci suono sportello anche in chiusura
        if (doorSound != null)
        {
            doorSound.Play();
        }

        while (elapsed < duration)
        {
            float t = elapsed / duration;

            transform.position = Vector3.Lerp(targetPosition, startPosition, t);
            transform.rotation = Quaternion.Lerp(targetRotation, startRotation, t);

            elapsed += Time.deltaTime;
            yield return null;
        }

        transform.position = startPosition;
        transform.rotation = startRotation;
        Debug.Log("Sportello richiuso.");
    }



}