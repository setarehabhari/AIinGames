using UnityEngine;

public static class DebugControl 
{

    public static void LogTesting(string msg)
    {
            Debug.Log(msg);
    }

    public static void LogError(string msg)
    {
        Debug.LogError("Exeption:1374 "+msg);

    }  
    public static void Log(string msg)
    {
        Debug.LogError(msg);

    }
}
