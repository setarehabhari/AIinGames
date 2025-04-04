using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DG.Tweening.Core.Easing;
using Photon.Realtime;
using Unity.Plastic.Newtonsoft.Json;
using UnityEngine;
using UnityEngine.UI;
using static UnoCard;

public class UnoPlayer : MonoBehaviour
{
    public UnoCardStack cardStack;
    public GameObject MyTurnImage;
    public GameObject SelectColorPanel;
    [NonSerialized]
    public UnoGameManager GameManager;
    [SerializeField]
    public Owner handOwner;
    private UnoAI AI;


    private int TryNumber = 0;
    private bool UnoImmune = false;
    private Button UnoButon;
    public List<Sprite> PlayerColorImg;
    public List<string> PlayerColorHex;
    public Image CardPlaceImage;
    public Image PlayerImg;
    public UnoCard.CardType PlayerColor;
    public UnoCard ColorDrawCard;
    public Animator animator;

    private UnoCard chosenCard = null;
    public void Init()
    {
        cardStack.OnCardSelected += OnCardSelected;
        if (GetComponent<UnoAI>() != null)
        {
            AI = GetComponent<UnoAI>();
            AI.gameManager = GameManager;
        }
        UnoButon = GetComponentInChildren<Button>();
        animator = GetComponent<Animator>();
        //PlayerColorHex = new List<string>();
        //PlayerColorHex.Add("EDD0BD");yello
        //PlayerColorHex.Add("88E0E8");blu
        //PlayerColorHex.Add("CCA9E5");red
        //PlayerColorHex.Add("82E894");green

    }

    //private void Update()
    //{
    //    if (chosenCard != null && !chosenCard.IsAnimating) {
    //        chosenCard.SuggestionAnimation();
    //        print("FUCK@!");
    //    }
    //}
    public void InteractableUnoButton(bool interactable)
    {
        UnoButon.interactable = interactable;
    }
    public bool AllCardsPlayed() {
        return cardStack.IsEmpty();
    }
    public void SetColor(UnoCard.CardType color)
    {
        Color temp;
        PlayerColor = color;
        if (ColorUtility.TryParseHtmlString(PlayerColorHex[(int)color]+"20", out temp))
        {
            CardPlaceImage.color = temp;
        }
        PlayerImg.sprite=PlayerColorImg[(int)color];
    }
    public void RemoveFromHand(UnoCard card)
    {
        cardStack.Pop(card);
    }
    public void SetOwner(Owner _owner)
    {
        handOwner = _owner; //stacks without player have assigned owners from editor.
    }
    public void DrawCard(UnoCard card,bool isForUno, bool isForInit, Action callback, bool isForAI=false)
    {
        GameManager.DrawPile.RemoveFromDraw(card);
        if(!isForUno)
            Immune(false);
        if (isForInit)
        {
            if (isForAI)
            {
                GameManager.DiscardPile.CardDrawn();
            }
            //GameDiscardPile.CardDrawn();
            cardStack.PushAndMove(card, false, () =>
            {
                if ((int)handOwner == UnoGameManager.MainPlayer)//TODO:Online
                    card.ShowBackImg(false);
                callback();
            });
        }
        else
        {
            StartCoroutine(DrawCardAsyncAsCoroutine((drawnCardString) =>
            {
                List<string> listOfDrawnCards = JsonConvert.DeserializeObject<List<string>>(drawnCardString);
                int index = GameManager.DiscardPile.IndexOfDrawnCard() - 1 < 0 ? 0 : (GameManager.DiscardPile.IndexOfDrawnCard() - 1);
                UnoCard drawnCard = GameManager.DrawPile.MakeCardFromString(listOfDrawnCards[index]);
                //GameManager.SpecialCardDrawAmount = GameManager.SpecialCardDrawAmount - 1;
                card.AddStuffFromActualCard(drawnCard);

                cardStack.PushAndMove(card, false, () =>
                {
                    if ((int)handOwner == UnoGameManager.MainPlayer) //TODO: Online
                        card.ShowBackImg(false);
                    callback();
                });
            }));
        }        
    }

    private IEnumerator DrawCardAsyncAsCoroutine(Action<String> onComplete)
    {
        var task = GameManager.GameServer.DrawCardAsync();
        yield return new WaitUntil(() => task.IsCompleted);

        // Call the callback with the result when the task completes
        onComplete?.Invoke(task.Result);
    }

    public void ChangeTurnToMe(bool isMyTurn)
    {
        MyTurnImage.SetActive(isMyTurn);
        TryNumber = 0;
        if(isMyTurn && handOwner == Owner.Player1)
        {
            StartCoroutine(GetSuggestionAsyncAsCoroutine((suggestionCardString) =>
            {
                if (suggestionCardString.Trim('\"') == "draw")
                {
                    GameManager.DrawPile.GetAllCards().Last().SuggestionAnimation();
                }
                else
                {
                    int suggestionId = GameManager.DrawPile.ConvertStringIdToIntId(suggestionCardString);
                    cardStack.GetAllCards().ForEach(card =>
                    {
                        if (card.id == suggestionId)
                        {
                            //print(card.id);
                            //chosenCard = card;
                            card.SuggestionAnimation();
                            //card.SuggestionAnimation();
                        }
                    });
                }
            }));
        }
        // DebugControl.Log("turn" + isMyTurn, 3);
        
        if( AI != null)
        {
            if (isMyTurn )
            {
                print("here");
                 StartCoroutine(AIPlay());
            }
        }
    }


    private IEnumerator GetSuggestionAsyncAsCoroutine(Action<String> onComplete)
    {
        var task = GameManager.GameServer.GetSuggestionAsync();
        yield return new WaitUntil(() => task.IsCompleted);

        // Call the callback with the result when the task completes
        onComplete?.Invoke(task.Result);
    }


    IEnumerator SelectWildCardColor(UnoCard cardScript)
    {
        if (GameManager.OnlineGame)
        {
            if (GameManager.GetTurn() == UnoGameManager.MainPlayer)
            {
                SelectColorPanel.SetActive(true);//then ColorSelected function will be called
            }
        }
        else
        {
            if (AI == null)
            {
                ColorDrawCard = cardScript;
                SelectColorPanel.SetActive(true);//then ColorSelected function will be called
            }
            else
            {
                print(cardScript.stringId);
                print(cardScript.GetColor());
                yield return new WaitForSeconds(UnoGameManager.WaitForOneMoveDuration);
                GameManager.DiscardPile.SetWildLastCardUIColor(cardScript.GetColor());
                GameManager.ContinueGame();
            }
        }
    }
    public void PlayAgain()
    {
        GameManager.LockGame(false);

        TryNumber++;
        //DebugControl.Log("play again", 3);
        if( AI != null ) 
            StartCoroutine(AIPlay());
    }
    public void ColorSelected(int color)//called from button clicked
    {

        GameManager.DiscardPile.SetWildLastCardUIColor((UnoCard.CardType)color);
        
        
        StringBuilder sb = new StringBuilder(ColorDrawCard.stringId);
        sb[0] = GetColorFromInt(color);
        string CardIdAFterColorpick = sb.ToString();


        StartCoroutine(PlayCardAsyncAsCoroutine(CardIdAFterColorpick));
        SelectColorPanel.SetActive(false);
        GameManager.ContinueGame();
        if (GameManager.OnlineGame)
        {
            GameManager.EventSender.Online_OnWildColorSelected(color);
        }
    }
    public char GetColorFromInt(int colorId)
    {
        if (colorId == ((int)CardType.Red))
        {
            return 'r';
        }
        if (colorId == ((int)CardType.Blue))
        {
            return 'b';
        }
        if (colorId == ((int)CardType.Green))
        {
            return 'g';
        }
        return 'y';
    }

    IEnumerator AIPlay()
    {
        AI.Owner = handOwner;
        yield return new WaitForSeconds(0.4f*UnoGameManager.WaitForOneMoveDuration);
        AI.StartPlay(cardStack, GameManager.DrawPile.GetAllCards(),TryNumber);
    }

    public IEnumerator PlayCardAsyncAsCoroutine(string stringId)
    {
        var task = GameManager.GameServer.PlayCardAsync(stringId); ;
        yield return new WaitUntil(() => task.IsCompleted);
    }

    public void OnCardSelected(UnoCard card)
    {
        if (GameManager.isGameLocked()){
            return;
        }
        if (GameManager.GetTurn() == (int)handOwner && GameManager.GetTurn() == (int)card.LastClicked)
        {
            //print("game edn");
            //print(GameManager.DiscardPile.CanPlayOnUpCard());
            //print(GameManager.DiscardPile.CanPlayThisCard(card));
            if (GameManager.DiscardPile.CanPlayOnUpCard() && GameManager.DiscardPile.CanPlayThisCard(card))
            {
                GameManager.LockGame(true);
                card.StopAnimation();
                RemoveFromHand(card);//TODO: move in discard in pile code
                Immune(false);
                if (!card.IsWildCard() && card.stringId is not null && GameManager.GetTurn() == (int)Owner.Player1)
                {
                    StartCoroutine(PlayCardAsyncAsCoroutine(card.stringId));
                }
                GameManager.DiscardPile.DiscardedCard(card, () => {

                    //if the card is mine, notify the other player in online game
                    if (GameManager.OnlineGame && (Owner)UnoGameManager.MainPlayer == card.LastClicked)
                    {
                        GameManager.EventSender.Online_OnPlayerHandCardSelected(card);
                    }
                    if (HasWon()) 
                    {
                         GameManager.ShowWinner((int)handOwner);
                            return;
                    }

                    if (GameManager.DiscardPile.ColorSelectIsNeeded())
                    {
                         StartCoroutine(SelectWildCardColor(card));
                    }
                    else
                    {
                        GameManager.ContinueGame(card);
                     }
                });

            }
            else
            {
                PlayAgain();
            }
        }
           // DebugControl.Log(globalCardIdx + " " + owner.ToString(), 3);

    }
    public bool HasWon()
    {
        return cardStack.IsEmpty();
    }

    public void Uno(int callerID)
    {
        animator.SetTrigger("UNOC");

        if (callerID != (int)handOwner)
        {
            if (IsUno()&& !IsImmune())
            {   
                Immune(true);
                GameManager.NotifiControl.ShowNotification("forgot uno!",NotifiControl.NotificationCode.UNOF);

                GetOnePenaltyCard(() =>
                {
                    GetOnePenaltyCard(() =>
                    {
                        if (GameManager.DrawPile.IsEmpty())
                        {
                            GameManager.EmptyDrawPileShowWinner();
                            return;
                        }
                    });
                });
            }
        }
        else
        {
            Immune(true);
        }
        

    }

    public void GetOnePenaltyCard(Action callback)
    {
        UnoCard PenaltyCard = GameManager.DrawPile.GetaCard();
        if (PenaltyCard != null)
            DrawCard(PenaltyCard, true, false, () =>
            {
                callback();
            });
    }
    public UnoCard GetaCard(int id = -1)
    {
        if (id != -1)
        {
            return cardStack.GetCard(id);
        }
        else//TODO:unused
        {
            if (cardStack.IsEmpty())
            {
               // GameManager.EmptyDrawPileShowWinner();
                Debug.LogError("Empty");
                return null;
            }
            else
                return cardStack.GetAllCards()[0];
        }
    }

    public void UnoClicked()
    {
        Uno(UnoGameManager.MainPlayer);
        if (GameManager.OnlineGame)
        {
            GameManager.EventSender.Online_OnUnoCalled(UnoGameManager.MainPlayer, handOwner);
        }
    }
    public bool IsUno()
    {
        return cardStack.HasOneCard();
    }

    public void Immune(bool immune)
    {
        UnoImmune = immune;
    }
    public bool IsImmune()
    {
        return UnoImmune;
    }

}
