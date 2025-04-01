using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MenuControl : MonoBehaviour
{
    public string SceneName;
    public string LobbyName;
    public string MenuName;
    public Toggle MusicControlToggle;

    AudioSource Music;

    private void Awake()
    {
        GameObject temp = GameObject.FindWithTag("MUSIC");
        if (temp != null)
        {
            Music = temp.GetComponent<AudioSource>();
            if (Music.isPlaying)
            {
                MusicControlToggle.isOn = true;
            }
            else
            {
                MusicControlToggle.isOn = false;
            }
        }
    }
    public void OnGameClick(int idx)
    {
        DontDestroy.TempData = idx;
        if (idx == 1)
            SceneManager.LoadScene(LobbyName);

        else
            SceneManager.LoadScene(SceneName);
    }
    public void OnGoToMenuClick()
    {

        SceneManager.LoadScene(MenuName);
    }
    public void OnExitClicked()
    {
        DebugControl.LogTesting("quit called");
        Application.Quit();
    }
    public void PlayMusic(bool play)
    {
        if (play) Music.Play();
        else Music.Stop();
    }
}
