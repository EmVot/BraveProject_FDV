using System.Collections;
using UnityEngine;
using System.Diagnostics; // Per eseguire processi esterni

public class PythonLauncher : MonoBehaviour
{
    [SerializeField] private string pythonScriptPath = @"C:\Users\asche\PycharmProjects\BraveProject\main.py"; 
    
    void Start()
    {
        StartCoroutine(RunPythonAfterDelay(10f));
    }

    private IEnumerator RunPythonAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay);
        RunPythonScript();
    }

    private void RunPythonScript()
    {
        try
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "py"; // Oppure il percorso completo a python.exe
            start.Arguments = $"\"{pythonScriptPath}\"";
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;
            start.CreateNoWindow = true;

            using (Process process = Process.Start(start))
            {
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                UnityEngine.Debug.Log("Output Python: " + output);
                if (!string.IsNullOrEmpty(error))
                    UnityEngine.Debug.LogError("Errore Python: " + error);

                process.WaitForExit();
            }
        }
        catch (System.Exception e) {
            UnityEngine.Debug.LogError($"Errore nell'avvio dello script Python: {e.Message}");
        }

    }
}
