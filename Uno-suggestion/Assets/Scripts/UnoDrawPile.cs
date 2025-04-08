using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using UnityEngine;
using ExitGames.Client.Photon;
using Photon.Realtime;
using Photon.Pun;
using UnityEngine.UIElements;
using System.Linq;

public class UnoDrawPile : MonoBehaviour
{
    public GameObject cardPrefab;

    Sprite[] CardSprites;
    const int TOTAL_CARDS = 108;
    const int CARD_STACK_NUMBERS = 14;
    private List<UnoCard> AllCards = new List<UnoCard>();
    UnoCardStack DrawStack;
    UnoCardStack UnusedStack;
    UnoGameManager GameManager;
    private void Awake()
    {
        DrawStack = GetComponent<UnoCardStack>();
        UnusedStack = GetComponent<UnoCardStack>();
        CardSprites = Resources.LoadAll<Sprite>("");
        DrawStack.OnCardSelected += OnCardSelected;//set a call back for it's stack

    }

    public void SetManager(UnoGameManager manager)
    {
        GameManager = manager;
        //if(PhotonNetwork.IsMasterClient)
        //    photonView.RPC("SendCardList", RpcTarget.All, "yo"+ PhotonNetwork.NickName);
    }
    public void RemoveFromDraw(UnoCard card)
    {
        DrawStack.Pop(card);
    }

    [PunRPC]
    public void SendCardList(string s)
    {
       // List<int> AllCardsInts = new List<int>(cards);
        Debug.LogError(s);
    }

    /// <summary>
    /// Draw a card to the player who's turn is now
    /// </summary>
    /// <param name="cardScript"></param>
    /// <param name="arg2"></param>
    /// <param name="owner"></param>
    private void OnCardSelected(UnoCard cardScript)
    {
        //print("finish game?");
        //print(GameManager.isGameLocked());
        //print(GameManager.GetTurn());
        //print((int)cardScript.LastClicked);
         if ( GameManager.isGameLocked() || GameManager.GetTurn() != (int)cardScript.LastClicked){//if its not the turn of the player clicked on this card,
            return;}
         //if (GameManager.DiscardPile.GetLastCard().Type == UnoCard.SpecialCard.Draw2 ||
         //   GameManager.DiscardPile.GetLastCard().Type == UnoCard.SpecialCard.Draw4Wild)
         //{
         //   print("yay -_-");
         //   return;
         //}
         GameManager.LockGame(true);
         DebugControl.LogTesting("drawing"+GameManager.isGameLocked()+" "+ GameManager.GetTurn());

        if (GameManager.GetTurn() == (int)Owner.Player1 && GameManager.DiscardPile.IndexOfDrawnCard() == 0)
        {
            StartCoroutine(GameManager.GetPlayer((Owner)GameManager.GetTurn()).PlayCardAsyncAsCoroutine("draw"));
        }
        //for (int i = 0; i <= GameManager.SpecialCardDrawAmount; i++) 
        //{// TODO this is the problem
        print("IndexOfDrawnCard");
        print(GameManager.DiscardPile.IndexOfDrawnCard());
            GameManager.GetPlayer((Owner)GameManager.GetTurn()).DrawCard(cardScript, false, false, () =>
            {
                //if (i == GameManager.SpecialCardDrawAmount)
                //{
                    if (DrawStack.IsEmpty())
                    {
                        GameManager.EmptyDrawPileShowWinner();
                    }
                    else
                    {
                        GameManager.DiscardPile.CardDrawn();

                        if (GameManager.OnlineGame && (Owner)UnoGameManager.MainPlayer == cardScript.LastClicked)
                        {
                            GameManager.EventSender.Online_OnDrawCardSelected(cardScript);
                        }

                        if (GameManager.DiscardPile.CanPlayOnUpCard())
                        {
                            print("whyyyy");
                            GameManager.ChangeTurn();
                        }
                        else
                        {
                            GameManager.GetPlayer((Owner)GameManager.GetTurn()).PlayAgain();
                        }
                    }
                //}
            });
        //}
    }
    public void ShuffleAndDistAllCards()
    {
       
        List<int> allNumbers = ShuffleAllCards();
        if (GameManager.OnlineGame && GameManager.isMasterClient)
        {
            const byte ShuffleAndDistAllCardsCode = 2;

            RaiseEventOptions raiseEventOptions = new RaiseEventOptions { Receivers = ReceiverGroup.Others }; // You would have to set the Receivers to All in order to receive this event on the local client as well
            PhotonNetwork.RaiseEvent(ShuffleAndDistAllCardsCode, allNumbers.ToArray(), raiseEventOptions, SendOptions.SendReliable);
            
            CreateAndDistCards(allNumbers);
        }
        else if(!GameManager.OnlineGame)
        {
            CreateAndDistCards(allNumbers);
        }
    }
    public void CreateAndDistCards(List<int> allNumbers)
    {
        for (int i = 0; i < TOTAL_CARDS; i++)
        {
            AllCards.Add(MakeCard(allNumbers[i]));
        }
        DistributeCards(GameManager.PlayerCount);
    }

    public void DistributeCards(int playerCount)
    {
        //push all cards to draw stack
        int j = 0;
        while (AllCards.Count > j)
        {
            DrawStack.PushAndMove(AllCards[j], true, () => { });
            j++;
        }

        UnoCard FirstCard = FindFirstCard();

        UnoCard ActualFirstCard = MakeCardFromString(GameManager.CurrentGameState.target);
        FirstCard.AddStuffFromActualCard(ActualFirstCard);
        StartCoroutine(DistCardtoPlayers(() =>
        {
            GameManager.GameStart(FirstCard);
        }));
    }


    IEnumerator DistCardtoPlayers(Action callback)
    {
        yield return new WaitForSeconds((5 / 2) * UnoGameManager.WaitForOneMoveDuration);

        for (int i = 0; i < GameManager.PlayerCount; i++)
        {
            for (int j = 0; j < GameManager.CurrentGameState.hand.Count; j++)
            {
                int id = DrawStack.GetAllCards().Count - 1;
                UnoCard physicalCard = DrawStack.GetAllCards()[id];
                
                int CurrentID = i;
                UnoCard card = MakeCardFromString(GameManager.CurrentGameState.hand[j]);
                physicalCard.AddStuffFromActualCard(card);
                RemoveFromDraw(physicalCard);
                GameManager.GetPlayer((Owner)i).DrawCard(physicalCard, false, true, () =>
                {//TODO:null exception when play again online game

                    if (CurrentID == UnoGameManager.MainPlayer)
                    {
                        physicalCard.ShowBackImg(false);
                    }
                    else
                    {
                        physicalCard.ShowBackImg(true);
                    }

                });
                yield return new WaitForSeconds(UnoGameManager.WaitForOneMoveDuration * 3 / 4);
            }
        }
        callback();
    }

    private UnoCard MakeCard(int id)
    {
        GameObject card = Instantiate(cardPrefab);
        UnoCard cardScript = card.GetComponent<UnoCard>();
        cardScript.InitCard(id, CardSprites[id]);
        return cardScript;
    }


    public UnoCard MakeCardFromString(string cardstring)
    {
        GameObject card = Instantiate(cardPrefab);
        UnoCard cardScript = card.GetComponent<UnoCard>();
        int id = ConvertStringIdToIntId(cardstring);
        cardScript.InitCard(id, CardSprites[id], cardstring);
        //print()
        if (cardScript.IsWildCard())
        {
            //print("HEre");
            cardScript.SetWildCardColor();
        }
        return cardScript;
    }

    public int ConvertStringIdToIntId(string cardstring)
    {
        cardstring = cardstring.Trim('\"');
        string[] parts = cardstring.Split('-');
        if (parts[1] == Server.CARD_STRING_DRAW4WILD)
        {
            return (int)Server.SpecialsIndex.Draw4Wild;
        }

        if (parts[1] == Server.CARD_STRING_WILD)
        {
            return (int)Server.SpecialsIndex.Wild;
        }
        int TypeNumber = parts[1] == Server.CARD_STRING_SKIP ? (int)Server.SpecialsIndex.Skip: 
            parts[1] == Server.CARD_STRING_REVERSE ? (int)Server.SpecialsIndex.Reverse :
            parts[1] == Server.CARD_STRING_DRAW2 ? (int)Server.SpecialsIndex.Draw2 :
            int.Parse(parts[1]);
        Enum.TryParse(parts[0], out Server.StringColors colorIndex);
        return TypeNumber + (int)colorIndex*CARD_STACK_NUMBERS;
    }

    public bool IsEmpty()
    {
        return DrawStack.IsEmpty();
    }
    public UnoCard GetaCard(int id = -1)
    {
        if (id != -1)
        {
            return DrawStack.GetCard(id);
        }
        else
        {
            if (DrawStack.IsEmpty())
            {
                GameManager.EmptyDrawPileShowWinner();
                return null;
            }
            else
                return DrawStack.GetAllCards()[0];
        }
    }
    public List<UnoCard> GetAllCards() {
        return DrawStack.GetAllCards();
    }
    private List<int> ShuffleAllCards()
    {
        List<int> allNumbers = new List<int>();
        for (int i = 0; i < TOTAL_CARDS; i++)
        {
            allNumbers.Add(i);
        }
        allNumbers = Utility.Shuffle(allNumbers);
        return allNumbers;

    }
    private UnoCard FindFirstCard()
    {
        int x = 0;
        while (!GameManager.IsCardAcceptableToStart(AllCards[x]))
        {
            x++;
        }
        UnoCard firstCard = AllCards[x];
        RemoveFromDraw(AllCards[x]);
        return firstCard;
    }

}
