using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class Utility 
{
    public static List<int> Shuffle(List<int> cards)
    {
        List<int> shuffledCards = new();
        while (cards.Count > 0)
        {
            int rand = Random.Range(0, cards.Count);
            shuffledCards.Add(cards[rand]);
            cards.RemoveAt(rand);
        }
        return shuffledCards;
    }
}
