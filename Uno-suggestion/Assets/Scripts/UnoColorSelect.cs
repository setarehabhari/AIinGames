using UnityEngine;

//Select player color in game menu
public class UnoColorSelect : MonoBehaviour
{
    public static UnoCard.CardType ColorSelected = UnoCard.CardType.Blue;

    private void Start()
    {
        ColorSelected = UnoCard.CardType.Blue;
    }

    public void SelectBlueColor(bool isOn)
    {
        if(isOn)
            ColorSelected = UnoCard.CardType.Blue;
    }
    public void SelectRedColor(bool isOn)
    {
        if (isOn)
            ColorSelected = UnoCard.CardType.Red;
    }
    public void SelectGreenColor(bool isOn)
    {
        if (isOn)
            ColorSelected = UnoCard.CardType.Green;
    }
    public void SelectYelloColor(bool isOn)
    {
        if (isOn)
            ColorSelected = UnoCard.CardType.Yellow;
    }
}
