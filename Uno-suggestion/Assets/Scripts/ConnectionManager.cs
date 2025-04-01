using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using Photon.Realtime;
using Photon.Pun;

public class ConnectionManager : MonoBehaviourPunCallbacks
{
    [SerializeField]
    private TextMeshProUGUI StatusText;
    private bool isConnecting = false;
    private const string gameVersion = "v1";
    [SerializeField]
    private GameObject ConnectPanel;

    void Awake()
    {
        if (DontDestroy.TempData == 5)
        {
            ShowStatus("The other player left");

        }

    }

    public void SaveName(string name)
    {
        if (string.IsNullOrEmpty(name))
        {
            Debug.LogError("Player name is empty");
            return;
        }
        PhotonNetwork.NickName = name;
    }

    public void OnButtonClicked()//connect button
    {
        PhotonNetwork.AutomaticallySyncScene = true;
        Debug.Log(PhotonNetwork.NickName);
        Connect();
    }

    public void Connect()
    {
        DontDestroy.TempData = 1;//if not changed here, when other player leaves and were in lobby, it stays 5

        isConnecting = true;
        ConnectPanel.SetActive(false);
        ShowStatus("Connecting...");

        if (PhotonNetwork.IsConnected)
        {
            ShowStatus("Joining Random Room...");
            PhotonNetwork.JoinRandomRoom();
        }
        else
        {
            ShowStatus("Connecting...");
            PhotonNetwork.ConnectUsingSettings();
            PhotonNetwork.GameVersion = gameVersion;
        }
    }

    public override void OnConnectedToMaster()
    {
        if (isConnecting)
        {
            ShowStatus("Connected, joining room...");
            PhotonNetwork.JoinRandomRoom();
        }
    }

    public override void OnJoinRandomFailed(short returnCode, string message)
    {
        ShowStatus("Creating new room...");
        PhotonNetwork.CreateRoom(null, new Photon.Realtime.RoomOptions { MaxPlayers = 2 });
    }

    public override void OnDisconnected(DisconnectCause cause)
    {
        isConnecting = false;
        ConnectPanel.SetActive(true);
    }

    public override void OnJoinedRoom()
    {
        ShowStatus("Joined room - waiting for another player.");
    }

    public override void OnPlayerEnteredRoom(Player newPlayer)
    {
        base.OnPlayerEnteredRoom(newPlayer);
        if (PhotonNetwork.CurrentRoom.PlayerCount == 2 && PhotonNetwork.IsMasterClient)
        {
            PhotonNetwork.LoadLevel("GameScene");
            PhotonNetwork.AutomaticallySyncScene = false;//so it can go to menu and the othe would go to lobby after

        }
    }

    void ShowStatus(string status)
    {
        if (StatusText != null)
            StatusText.text = status;
        else
            DebugControl.LogError(status);
    }
    public override void OnPlayerLeftRoom(Player other)
    {
        // The other player left - might as well leave, too!
        DebugControl.LogError("im gone" + PhotonNetwork.NickName);
        PhotonNetwork.LeaveRoom();
        DontDestroy.TempData = 5;
    }
    public override void OnLeftRoom()
    {
        PhotonNetwork.LoadLevel("LobbyScene");
    }
}
