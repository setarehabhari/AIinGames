using System;
using System.Collections.Generic;
using UnityEngine;

public class UnoDiscardPile : MonoBehaviour
{

    UnoGameManager GameManager;
    public GameObject WildColorGameObject;
    public List<GameObject> WildColors = new List<GameObject>();

    private Animation ChooseColorAnim;
    private UnoCard LastCard = null;
    private UnoCardStack cardStack;

    void Awake()
    {
        cardStack = GetComponent<UnoCardStack>();
        cardStack.SetAsDiscardStack();
        ChooseColorAnim = WildColorGameObject.GetComponent<Animation>();


    }
    public void SetManager(UnoGameManager manager)
    {
        GameManager = manager;
    }
    public void DiscardedCard(UnoCard card, Action callback)
    {
        GameManager.SpecialCardDrawAmount = 0;
        if (card.Type == UnoCard.SpecialCard.Reverse)
        {
            GameManager.NotifiControl.ShowNotification("Reverse!", NotifiControl.NotificationCode.REV);
        }
        else if (card.Type == UnoCard.SpecialCard.Skip)
        {
            GameManager.NotifiControl.ShowNotification("Skip!", NotifiControl.NotificationCode.SKIP);
        }
        else if (card.Type == UnoCard.SpecialCard.Draw2)
        {
            GameManager.NotifiControl.ShowNotification("draw 2 cards!", NotifiControl.NotificationCode.DRAW2);
            GameManager.SpecialCardDrawAmount = 1;
        }
        else if (card.Type == UnoCard.SpecialCard.Draw4Wild)
        {
            GameManager.NotifiControl.ShowNotification("draw 4 cards!", NotifiControl.NotificationCode.DRAW4);
            GameManager.SpecialCardDrawAmount = 3;
        }
        card.ShowBackImg(false);

        cardStack.PushAndMove(card,false, () => {
            callback();
        });
        LastCard = card;
    }
    public bool CanPlayOnUpCard() // This says you can never play on top of +2 or +4
    {
        return LastCard.AccumulatedCards <= 0;
    }
    public int IndexOfDrawnCard() // This says you can never play on top of +2 or +4
    {
        return LastCard.AccumulatedCards;
    }
    public bool CanPlayThisCard(UnoCard cardScript)
    {
        return (LastCard.AcceptsCard(cardScript) || (cardStack.HasOneCard()&&LastCard.Type==UnoCard.SpecialCard.Wild));
    }
    public bool ColorSelectIsNeeded()
    {
        return (LastCard.Type == UnoCard.SpecialCard.Wild || LastCard.Type == UnoCard.SpecialCard.Draw4Wild);
    }
    public void SetWildLastCardUIColor(UnoCard.CardType color)
    {
        LastCard.SetWildColor(color);
        //show the selected color on the wild card
        for (int i = 0; i < 4; i++)
        {
            WildColors[i].SetActive(i== (int)color);
        }
        
        WildColorGameObject.transform.SetAsLastSibling();
        ChooseColorAnim.Play();
        GameManager.NotifiControl.ShowNotification("", NotifiControl.NotificationCode.None);

    }

    public void CardDrawn()
    {
        if (LastCard.AccumulatedCards > 0)
        {

            LastCard.AccumulatedCards--;
        }
        print("New LastCard.AccumulatedCards:");
        print(LastCard.AccumulatedCards);
    }
    public UnoCard GetLastCard()
    {
        return LastCard;
    }

}
