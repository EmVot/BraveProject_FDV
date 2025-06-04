using System;
using UnityEngine;

public class CharacterViewYaw : MonoBehaviour {
    [SerializeField] private float initialYaw = 90.0f; // Cambia questo valore per direzionare il player

    private float yaw = 0.0f;

    public Transform CameraPivot;

    [SerializeField] private float MinYaw = -45f;
    [SerializeField] private float MaxYaw = 45f;

    void Start() {
        Cursor.lockState = CursorLockMode.Locked;  // keep confined to center of screen
        
        yaw += Input.GetAxisRaw("Mouse X");
        CameraPivot.eulerAngles = new Vector3(0.0f, yaw, 0.0f);

    }

    void Update() {

        yaw += Input.GetAxisRaw("Mouse X");
        yaw = ClampAngle(yaw, MinYaw, MaxYaw);
        transform.eulerAngles = new Vector3(0.0f, yaw, 0.0f);

    }

    private float ClampAngle(float angle, float min, float max) {
        return Mathf.Clamp(angle, min, max);
    }

}
