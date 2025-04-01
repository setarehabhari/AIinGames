using System.Collections;
using UnityEngine;
using TMPro;
public class NotifiControl : MonoBehaviour
{
    public enum NotificationCode
    {
        None,
        UNOF,
        DRAW2,
        REV,
        SKIP,
        DRAW4

    }
    public GameObject UI;
    public TMP_Text text;
    public Animator animator;
    public AudioSource Audio;
    public void ShowNotification(string message,NotificationCode type)//0 for no message only audio
    {       
        text.text = message;
        if(type!=NotificationCode.None)
             animator.SetTrigger(type.ToString());
        Audio.Play();

    }
}
