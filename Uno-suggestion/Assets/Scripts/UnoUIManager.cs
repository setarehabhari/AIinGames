using UnityEngine;
using UnityEngine.UI;

public class UnoUIManager : MonoBehaviour
{
    [SerializeField] private GameObject winPanel;
    [SerializeField] private Text winnerNameText;

    // Call this method to show the win panel with the winner's name
    public void ShowWinPanel(string winnerName)
    {
        winPanel.SetActive(true);
        winnerNameText.text = $"Winner: {winnerName}";
    }

    // Call this method to hide the win panel
    public void HideWinPanel()
    {
        winPanel.SetActive(false);
    }

    public void OnUnoButtonClicked()
    {
    }
}
