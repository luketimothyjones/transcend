using System.Collections;
using System.Collections.Generic;
using UnityEngine;


[RequireComponent(typeof(CharacterController))]
public class BasicPlayerController : MonoBehaviour {

    public float speed = 3.0F;

    void FixedUpdate() {
        CharacterController controller = GetComponent<CharacterController>();

        float moveHorizontal = Input.GetAxis("Horizontal");
        float moveVertical = Input.GetAxis("Vertical");

        Vector3 movement = new Vector3(moveHorizontal, 0f, moveVertical);
        movement = transform.TransformDirection(movement);

        controller.SimpleMove(movement * speed);
        
    }

}
