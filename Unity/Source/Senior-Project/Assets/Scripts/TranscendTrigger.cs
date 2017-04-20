using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;
#endif

// ---------
public class TranscendTrigger : MonoBehaviour
{
    public GameObject transcendObject;
    public Color color;

    private int layerMask;
    private Collider objCollider;


    void Start()
    {
        objCollider = GetComponent<Collider>();
        color = gameObject.GetComponent<Renderer>().material.color;

        // Bit shift the index of the layer (8) to get a bit mask
        // Layer 8 is the button layer
        layerMask = 1 << 8;
    }

    void Update()
    {
        Vector3 center = new Vector3(Camera.main.pixelWidth / 2, Camera.main.pixelHeight / 2);
        Ray ray = Camera.main.ScreenPointToRay(center);
        RaycastHit hit;

        Physics.Raycast(ray, out hit, .6f, layerMask);

        if (hit.collider == objCollider && Input.GetMouseButtonDown(0))
        {
            transcendObject.BroadcastMessage("UpdateDevice", color);
        }
    }

}

#if UNITY_EDITOR
[CustomEditor(typeof(TranscendTrigger))]
[CanEditMultipleObjects]
public class TranscendTriggerEditor : Editor
{
    SerializedProperty transcendObject;
    SerializedProperty color;

    private void OnEnable()
    {
        transcendObject = serializedObject.FindProperty("transcendObject");
        color = serializedObject.FindProperty("color");
    }

    public override void OnInspectorGUI()
    {
        serializedObject.Update();

        // Show the custom GUI controls.
        EditorGUILayout.PropertyField(transcendObject);
        Color c = EditorGUILayout.ColorField("", color.colorValue);

        if (c != color.colorValue) {
            color.colorValue = c;
        }

        serializedObject.ApplyModifiedProperties();
    }
}
#endif
