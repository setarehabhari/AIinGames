using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using DG.Tweening.Core.Easing;
using UnityEngine;
using Random = UnityEngine.Random;

public class UnoAI : MonoBehaviour
{
    List<UnoCard> cards;
    public Owner Owner;
    public UnoGameManager gameManager;


    void Play()
    {        
        if (cards.Count > 0)
        {
            cards[0].OnClick((int)Owner);
            cards.RemoveAt(0);
        }
    }
    void PrepareToPlay(UnoCardStack PlayerCardStack, List<UnoCard> DrawStackCards,int TryNumber)
    {
        cards =new List<UnoCard>(PlayerCardStack.GetAllCards().Count+ DrawStackCards.Count);
        List<UnoCard> AvailableCards= new List<UnoCard>();
        for (int i = 0; i < PlayerCardStack.GetAllCards().Count; i++)
        {
            if (i >= TryNumber)
            {
                AvailableCards.Add(PlayerCardStack.GetAllCards()[i]);
            }
        }

        cards.AddRange(AvailableCards);
        List<UnoCard> DrawCards = DrawStackCards;
        DrawCards.Reverse();
        cards.AddRange(DrawCards);
    }

    private IEnumerator GetAIMoveAsyncAsCoroutine(Action<String> onComplete)
    {
        var task = gameManager.GameServer.GetAIMoveAsync();
        yield return new WaitUntil(() => task.IsCompleted);

        // Call the callback with the result when the task completes
        onComplete?.Invoke(task.Result);
    }


    public void StartPlay( UnoCardStack PlayerCardStack = null, List<UnoCard> DrawStackCards = null,int TryNumber = 0)
    {
        if (!gameManager.DiscardPile.CanPlayOnUpCard())
        {
            
            int indexbegin = gameManager.DiscardPile.IndexOfDrawnCard();
            for (int j = 0; j < indexbegin; j++)
            {
                //print(indexbegin);
                //print("j");
                //print(j);
                //List<UnoCard> DrawCards = DrawStackCards;
                //DrawCards.Reverse();
                //DrawCards[0].OnClick((int)Owner);
                //DrawCards.RemoveAt(0);

                int id = gameManager.DrawPile.GetAllCards().Count - 1;
                UnoCard physicalCard = gameManager.DrawPile.GetAllCards()[id];
                physicalCard.transform.localScale = Vector3.one;

                //int CurrentID = j;
                //UnoCard card = MakeCardFromString(GameManager.CurrentGameState.hand[j]);
                //physicalCard.AddStuffFromActualCard(card);
                gameManager.DrawPile.RemoveFromDraw(physicalCard);
                //gameManager.DiscardPile.CardDrawn();

                gameManager.GetPlayer((Owner)1).DrawCard(physicalCard, false, true, () =>
                {//TODO:null exception when play again online game
                    physicalCard.ShowBackImg(true);
                }, true);
                //yield return new WaitForSeconds(UnoGameManager.WaitForOneMoveDuration * 3 / 4);
            }
            gameManager.ChangeTurn();
            //print(gameManager.DiscardPile.IndexOfDrawnCard());
        }
        else
        {
            StartCoroutine(GetAIMoveAsyncAsCoroutine((rawJson) =>
            {
                //print(rawJson);
                GameState CurrentGameState = JsonUtility.FromJson<GameState>(rawJson);
                //print(CurrentGameState.played_cards.Last());
                //print(CurrentGameState.played_cards);
                //print(CurrentGameState.ai_played_draw);
                //print(CurrentGameState.ai_played_draw == true);
                String playedCardString = CurrentGameState.played_cards.Last();
                playedCardString = playedCardString.Trim('\"');
                if (CurrentGameState.ai_played_draw == false)
                {
                    //print("fere");
                    UnoCard card = gameManager.DrawPile.MakeCardFromString(playedCardString);
                    PlayerCardStack.GetAllCards()[0].AddStuffFromActualCard(card);
                    PlayerCardStack.GetAllCards()[0].OnClick((int)Owner);
                    PlayerCardStack.GetAllCards().RemoveAt(0);
                }
                else
                {
                    List<UnoCard> DrawCards = DrawStackCards;
                    DrawCards.Reverse();
                    DrawCards[0].OnClick((int)Owner);
                    DrawCards.RemoveAt(0);
                }
            }));

        }
        int x = Random.Range(0, 10);
        if(x<2)
            StartCoroutine(CheckForUno());
    }
    public UnoCard.CardType SelectColorForWild(UnoCardStack PlayerCardStack)
    {
        List<int> colorCount = new List<int> { 0, 0, 0, 0 };

        foreach (var card in PlayerCardStack.GetAllCards()) {
            colorCount[(int)card.GetColor()]++;
        }

        int max = 0;
        UnoCard.CardType color = 0 ;
        for (int i = 0; i < 4; i++)
        {
            if(colorCount[i]>max)
            {
                color = (UnoCard.CardType)i;
                max = colorCount[i];
            }
        }
       
        return color;
    }
    IEnumerator CheckForUno()
    {
        yield return new WaitForSeconds(2*UnoGameManager.WaitForOneMoveDuration);

        for (int i = 0; i < gameManager.PlayerCount; i++)
        {
            UnoPlayer player = gameManager.GetPlayer((Owner)i);

            if (player.IsUno() && !player.IsImmune())
            {
                player.Uno((int)Owner);
            }
        }

    }

}
