using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class SliderController : MonoBehaviour
{
    public Slider calmSlider;
    public Slider fearSlider;
    public Slider angerSlider;

    void Start()
    {
        calmSlider.value = 0.8f;
        fearSlider.value = 0f;
        angerSlider.value = 0f;
        StartCoroutine(AnimatecalmSlider());
        StartCoroutine(AnimateFearSlider());
        StartCoroutine(AnimateAngerSlider());
    }

    IEnumerator AnimatecalmSlider()
    {
        yield return LerpSlider(calmSlider, 0.8f, 0.4f, 10f);
        yield return new WaitForSeconds(5f);
        yield return LerpSlider(calmSlider, 0.4f, 0.0f, 10f);
        yield return new WaitForSeconds(50f);
        yield return LerpSlider(calmSlider, 0.0f, 0.3f, 15f);
    }

    IEnumerator AnimateFearSlider()
    {
        yield return LerpSlider(fearSlider, 0f, 0.7f, 25f);
        yield return new WaitForSeconds(7f);
        yield return LerpSlider(fearSlider, 0.7f, 1f, 15f);
        yield return new WaitForSeconds(40f);
        yield return LerpSlider(fearSlider, 1f, 0.6f, 10f);
    }

    IEnumerator AnimateAngerSlider()
    {
        yield return new WaitForSeconds(10f);
        yield return LerpSlider(angerSlider, 0f, 0.1f, 10f);
        yield return new WaitForSeconds(10f);
        yield return LerpSlider(angerSlider, 0.5f, 0.3f, 5f);
        yield return new WaitForSeconds(40f);
        yield return LerpSlider(angerSlider, 0.3f, 0.2f, 10f);
    }


    IEnumerator LerpSlider(Slider slider, float startValue, float endValue, float duration)
    {
        float elapsed = 0f;
        while (elapsed < duration)
        {
            elapsed += Time.deltaTime;
            slider.value = Mathf.Lerp(startValue, endValue, elapsed / duration);
            yield return null;
        }
        slider.value = endValue;
    }
}