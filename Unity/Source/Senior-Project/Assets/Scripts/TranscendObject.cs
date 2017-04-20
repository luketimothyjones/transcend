using UnityEngine;
using UnityEngine.Networking;

using System;
using System.Collections;


// ---------
[Serializable]
public class TranscendObjectMessage
{
    public string object_name;
    public string color;
    public string brightness = "50";

    public string jsonify() {
        return JsonUtility.ToJson(this);
    }
}

// ----
public class LightHandler
{
    public GameObject gameObject;

    private Renderer objRend;
    private Light objLightChild;

    public void init()
    {
        objRend = gameObject.GetComponent<Renderer>();
        objLightChild = gameObject.GetComponentInChildren<Light>();
    }

    // ----
    public void SetColor(Color newColor)
    {
        objRend.material.color = newColor;  // The lightbulb bulb color
        objLightChild.color = newColor;     // The lightbulb glow color
    }

    public void UpdateObject(string newInfo)
        // Input: JSON string of (R, G, B, Brightness), such that each is
        // a float representation of the value (val / 255)
    {
        float r, g, b, a;
        r = float.Parse(newInfo.Substring(6, 3));
        g = float.Parse(newInfo.Substring(16, 3));
        b = float.Parse(newInfo.Substring(26, 3));
        a = float.Parse(newInfo.Substring(36, 3));

        SetColor(new Color(r, g, b, a));
    }

    public TranscendObjectMessage ColorToMessage(Color color)
    {
        TranscendObjectMessage msg = new TranscendObjectMessage();

        double r, g, b, a;
        r = Math.Round(color.r * 255);
        g = Math.Round(color.g * 255);
        b = Math.Round(color.b * 255);
        a = Math.Round(color.a * 100);

        msg.object_name = gameObject.name;
        msg.color = String.Format("{0},{1},{2}", r, g, b);
        msg.brightness = Math.Round(a).ToString();

        return msg;
    }

    public void MessageToColor(TranscendObjectMessage msg)
    {
        Array color;
        float r, g, b, a;
        color = msg.color.Split(',');

        r = float.Parse((string) color.GetValue(0)) / 255;
        g = float.Parse((string) color.GetValue(1)) / 255;
        b = float.Parse((string) color.GetValue(2)) / 255;
        a = float.Parse(msg.brightness) / 255;

        SetColor(new Color(r, g, b, a));
    }
}

// ---------
public class TranscendObject : MonoBehaviour
{
    private static string ip = "127.0.0.1";
    private static string port = GetPort();
    private static string addr = "http://" + ip + ":" + port + '/';

    private LightHandler handler = new LightHandler();

    // ----
    private void Start()
    {
        handler.gameObject = gameObject;
        handler.init();
        InvokeRepeating("UpdateObject", 0.5f, 2.0f);
    }

    private static string GetPort()
    {
        string fname = "./transcend-broker/config/transcend.cfg";
        //string text = System.IO.File.ReadAllText(fname);
        //string port = text.Substring(text.LastIndexOf("port = ") + 7).Split('\n').GetValue(0).ToString();
        //return port.TrimEnd();
        return "22300";
    }

    // ----
    void UpdateObject() {
        // Update the gameobject's color
        StartCoroutine(QueryTranscendBroker());
    }

    void UpdateDevice(Color color)
    {
        // Update the device's color
        StartCoroutine(AlertTranscendBroker(handler.ColorToMessage(color)));
    }

    // ----
    IEnumerator QueryTranscendBroker() {
        // Get new device information from the broker

        // Change this to a post of the object name
        UnityWebRequest www = UnityWebRequest.Get(addr);

        yield return www.Send();
        
        if (www.isError)
        {
            Debug.Log(www.error);
        }

        else
        {
            String respText = www.downloadHandler.text;
            handler.UpdateObject(respText);
        }
    }
    
    // ----
    IEnumerator AlertTranscendBroker(TranscendObjectMessage msg) {  // Add function as param?
        /*
         * Spawn a coroutine
         *       Send object details to socket server
         *       Yield response code
         *       Print any errors
         */

        //TranscendObjectMessage msg = handler.GetObjectInfo();
        UnityWebRequest www = UnityWebRequest.Post(addr, msg.jsonify());

        yield return www.Send();

        if (www.isError) {
            Debug.Log(www.error);
        }

        else
        {
            handler.MessageToColor(msg);
        }

    }
    
}
