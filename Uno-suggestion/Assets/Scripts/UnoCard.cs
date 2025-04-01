using System;
using UnityEngine;
using UnityEngine.UI;
using DG.Tweening;
using Codice.CM.Common;

public class UnoCard : MonoBehaviour
{
    public enum CardType {
        Red,
        Green,
        Blue,
        Yellow

    }
    public enum SpecialCard
    {
        None,
        Skip = 10,
        Reverse = 11,
        Draw2 = 12,
        Wild = 13,
        Draw4Wild = 14
    }
    public int id;
    public string stringId;
    CardType Color;
    int Number;
    public int TurnChangeAmount = 1;
    public SpecialCard Type = SpecialCard.None;
    public int AccumulatedCards = 0;
    public Owner LastClicked;
    public bool IsAnimating = false;
    
    Image img;
    public Sprite BackImg;
    Sprite FrontImg;
    MoveObject moveComponent;

    private Vector3 initialScale;
    //public bool isAnimating = false;  // Toggle animation
    private Vector3 targetScale = new Vector3(1.25f, 1.25f, 1.25f); // Scale to reach
    private float speed = 3f;  // Speed of scaling
    private bool scalingUp = true; // Direction of scaling
    //private Tween tween;

    public event Action<UnoCard> OnSelected;
    void Awake()
    {
        img = GetComponent<Image>();
        moveComponent = GetComponent<MoveObject>();
        moveComponent.targetTransform = transform;
        
        Debug.Log("YAY: " + initialScale);
        
        //tween.Pause();
        //tweenSequence = DOTween.Sequence();
        //tweenSequence.Append(transform.DOScale(initialScale * 1.2f, 1f)
        //    .SetEase(Ease.InOutSine)
        //    .SetLoops(int.MaxValue, LoopType.Yoyo));
        //SuggestionAnimation();
    }

    private void Start()
    {
        //tweenSequence.Pause();
        transform.localScale = Vector3.one;
        initialScale = transform.localScale;
    }

    private void Update()
    {
        if (!IsAnimating) return; // Stop if animation is off
        print("we are here");
        // Determine target based on current scaling direction
        Vector3 target = scalingUp ? targetScale : initialScale;

        // Smoothly interpolate scale
        transform.localScale = Vector3.Lerp(transform.localScale, target, Time.deltaTime * speed);

        // Check if the object is close enough to the target scale
        if (Vector3.Distance(transform.localScale, target) < 0.05f)
        {
            scalingUp = !scalingUp; // Switch direction
        }
    }

    public void InitCard(int id,Sprite sprite, string stringId = null)
    {
        this.id = id;
        this.stringId = stringId;

        if (sprite !=null && img != null)
        {
            img.sprite =sprite;
            FrontImg = sprite;
        }
        ShowBackImg(true);
        SetNumberAndColor();
        
        TurnChangeAmount =  Type == SpecialCard.Skip? 2: Type == SpecialCard.Reverse ? -1:1;
        AccumulatedCards = Type == SpecialCard.Draw2 ? 2 : Type == SpecialCard.Draw4Wild ? 4 : 0;

    }

    public void AddStuffFromActualCard(UnoCard actualCard)
    {
        this.id = actualCard.id;
        this.stringId = actualCard.stringId;
        this.Color = actualCard.Color;
        this.Number = actualCard.Number;
        this.Type = actualCard.Type;
        this.TurnChangeAmount = actualCard.TurnChangeAmount;
        this.AccumulatedCards = actualCard.AccumulatedCards;
        this.LastClicked = actualCard.LastClicked;
        this.FrontImg = actualCard.FrontImg;
        this.transform.localScale = Vector3.one;
    }

    public void OnClick(int Player=-1)
    {
        if (Player == -1)
            LastClicked = (Owner)UnoGameManager.MainPlayer;//Owner.Player1;//TODO:multiplayer
        else
            LastClicked = (Owner)Player;
        OnSelected?.Invoke(this);
    }
    public void ShowBackImg(bool back)
    {
        if (back)
            img.sprite = BackImg;
        else
            img.sprite = FrontImg;
    }
    public void SetWildColor(CardType wildColor)
    {
        Color = wildColor;
    }
    //Move is called after Onclick is processed through manager
    public void Move(Vector3 EndPosition,Action callback)
    {
        moveComponent.Move(EndPosition, callback);
    }
    void SetNumberAndColor()
    {
        if (id < 56)
        {
            int row = (id / 14) % 4;
            Color = row == 0 ? CardType.Red : row == 1 ? CardType.Yellow : row == 2 ? CardType.Green : CardType.Blue;
            Number = id % 14;

            if (Number > 9)
                Type = (SpecialCard)Number;
        }
        else
        {
            int id2 = id - 56;
            int row = (id2 / 13) % 4;
            Color = row == 0 ? CardType.Red : row == 1 ? CardType.Yellow : row == 2 ? CardType.Green : CardType.Blue;

            Number = (id2 % 13) + 1;
            if (Number > 9)
                Type = Number == 13 ? SpecialCard.Draw4Wild : (SpecialCard)Number;
        }

       // DebugControl.Log(id+":"+ Number + " "+Color.ToString()+" "+Type,3);
    }

    public void SuggestionAnimation()
    {
        //tween = transform.DOScale(initialScale * 1.2f, 1f)
        //    .SetEase(Ease.InOutSine)
        //    .SetLoops(int.MaxValue, LoopType.Yoyo);
        //tween.Play();
        IsAnimating = true;
    }

    public void StopAnimation()
    {
        //tween.Kill();
        transform.localScale = initialScale;
        IsAnimating = false;
    }

    public bool AcceptsCard(UnoCard card)
    {
        //DebugControl.Log(Type + " " + card.Type, 3);
        if (card.Type == SpecialCard.Wild|| card.Type == SpecialCard.Draw4Wild)
            return true;

        return (card.Number == Number || card.Color == Color);
    }
    public CardType GetColor()
    {
        return Color;
    }
}
