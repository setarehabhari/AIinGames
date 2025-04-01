using UnityEngine;

public class DontDestroy : MonoBehaviour
{
    public static DontDestroy Instance;
    public static int TempData=2;
    private void Awake()
    {
        if (Instance != null)
            Destroy(gameObject);
        else
        {
            Instance = this;
            DontDestroyOnLoad(this.gameObject);
        }
    }
}
