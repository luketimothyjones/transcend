using UnityEngine;


public class Crosshair : MonoBehaviour {
    GUIStyle style;

    private void Start()
    {
        Cursor.visible = false;
    }

    // http://answers.unity3d.com/questions/201103/c-crosshair.html
    void OnGUI() {
        Rect crossh = new Rect(Screen.width / 2, Screen.height / 2, 10, 10);
        GUI.Box(crossh, "");
    }

}

