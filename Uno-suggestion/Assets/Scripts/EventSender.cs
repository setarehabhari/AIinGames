using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using ExitGames.Client.Photon;
using Photon.Realtime;
using Photon.Pun;

public class EventSender : MonoBehaviour
{

    public void Online_OnPlayerHandCardSelected(UnoCard card)
    {
        object[] content = new object[] { card.id, (int)card.LastClicked };
        RaiseEvent(OnlinePlayer.OnCardSelectedPlayerHandEventCode, content);
    }

    public void Online_OnWildColorSelected(int color)
    {
        object[] content = new object[] { color };
        RaiseEvent(OnlinePlayer.OnWildColorSelectedEventCode, content);
    }  
    public void Online_OnDrawCardSelected(UnoCard card)
    {
        object[] content = new object[] { card.id, (int)card.LastClicked };
        RaiseEvent(OnlinePlayer.OnCardSelectedDrawEventCode, content);
    }   
    public void Online_OnUnoCalled(int sender,Owner target)//(sender is an owner type as well)
    {
        object[] content = new object[] { (int)sender, (int)target };
        RaiseEvent(OnlinePlayer.OnUnoEventCode, content);
    }

    public void RaiseEvent(byte EventCode, object[] content)
    {
            RaiseEventOptions raiseEventOptions = new RaiseEventOptions { Receivers = ReceiverGroup.Others };
            PhotonNetwork.RaiseEvent(EventCode, content, raiseEventOptions, SendOptions.SendReliable);
            Debug.LogError(EventCode);        
    }

}
