using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RandomBlinkingLights : MonoBehaviour
{
    public Material blinkMaterial;
    private List<Renderer> lightObjects = new List<Renderer>();
    private Dictionary<Renderer, Material> originalMaterials = new Dictionary<Renderer, Material>();

    private Coroutine blinkingCoroutine;
    public bool isBlinking = false; // ✅ Nuovo flag di controllo

    void Start()
    {
        GameObject[] ceilingObjects = GameObject.FindGameObjectsWithTag("Ceiling");
        GameObject[] lightObjectsArray = GameObject.FindGameObjectsWithTag("Light");
        AddObjectsToList(ceilingObjects);
        AddObjectsToList(lightObjectsArray);
    }

    void AddObjectsToList(GameObject[] objects)
    {
        foreach (GameObject obj in objects)
        {
            Renderer rend = obj.GetComponent<Renderer>();
            if (rend != null && rend.materials.Length > 1)
            {
                lightObjects.Add(rend);
                originalMaterials[rend] = rend.materials[1];
            }
        }
    }

    public void StartBlinkingLights()
    {
        if (!isBlinking)
        {
            isBlinking = true;
            blinkingCoroutine = StartCoroutine(BlinkLights());
        }
    }

    public void StopBlinkingLights()
    {
        isBlinking = false;
        if (blinkingCoroutine != null)
        {
            StopCoroutine(blinkingCoroutine);
        }

        // ✅ Ripristina i materiali originali
        foreach (Renderer rend in lightObjects)
        {
            if (rend != null && originalMaterials.ContainsKey(rend))
            {
                Material[] newMaterials = rend.materials;
                newMaterials[1] = originalMaterials[rend];
                rend.materials = newMaterials;
            }
        }

        Debug.Log("Blinking disattivato e materiali ripristinati.");
    }

    IEnumerator BlinkLights()
    {
        yield return new WaitForSeconds(5f);

        while (isBlinking)
        {
            float randomInterval = Random.Range(0.05f, 0.2f);

            foreach (Renderer rend in lightObjects)
            {
                if (rend != null)
                {
                    Material[] newMaterials = rend.materials;
                    newMaterials[1] = blinkMaterial;
                    rend.materials = newMaterials;
                }
            }

            yield return new WaitForSeconds(randomInterval);

            foreach (Renderer rend in lightObjects)
            {
                if (rend != null)
                {
                    Material[] newMaterials = rend.materials;
                    newMaterials[1] = originalMaterials[rend];
                    rend.materials = newMaterials;
                }
            }

            yield return new WaitForSeconds(randomInterval);
        }
    }
}
