using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using UnityEditor.Experimental.GraphView;
using UnityEngine;


public class GameState
{
    public List<string> hand;
    public string target;
    public List<string> played_cards;
    public List<string> legal_actions;
    public List<int> num_cards;
    public int num_players;
    public int current_player;
}


public class Server
{
    public enum StringColors
    {
        r,
        y,
        g,
        b,

    }
    public enum SpecialsIndex
    {
        Skip = 10,
        Reverse = 11,
        Draw2 = 12,
        Wild = 13,
        Draw4Wild = 70
    }
    public const string CARD_STRING_SKIP = "skip";
    public const string CARD_STRING_REVERSE = "reverse";
    public const string CARD_STRING_DRAW2 = "draw_2";
    public const string CARD_STRING_WILD = "wild";
    public const string CARD_STRING_DRAW4WILD = "wild_draw_4";

    private readonly string serverAddress;
    private readonly HttpClient httpClient;
    UnoGameManager GameManager;

    public Server(string ipAddress, string port , UnoGameManager manager)
    {
        serverAddress = ipAddress + ":" + port;
        httpClient = new HttpClient();
        GameManager = manager;
    }

    public async Task<String> DrawCardAsync()
    {
        try
        {
            HttpResponseMessage response = await httpClient.GetAsync($"http://{serverAddress}/draw_card");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"DrawCard request failed: {e.Message}");
            return null;
        }
    }

    public async Task<String> GetAIMoveAsync()
    {
        try
        {
            HttpResponseMessage response = await httpClient.GetAsync($"http://{serverAddress}/get_ai_move");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"DrawCard request failed: {e.Message}");
            return null;
        }
    }

    public async Task<String> GetSuggestionAsync()
    {
        try
        {
            HttpResponseMessage response = await httpClient.GetAsync($"http://{serverAddress}/suggestion");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"DrawCard request failed: {e.Message}");
            return null;
        }
    }

    public async Task<String> GetGameState()
    {
        try
        {
            HttpResponseMessage response = await httpClient.GetAsync($"http://{serverAddress}/get_human_game_state");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
        catch (Exception e)
        {
            Debug.LogError($"GetGameState request failed: {e.Message}");
            return null;
        }
    }

    public async Task PlayCardAsync(string card)
    {
        try
        {
            string url = $"http://{serverAddress}/play_card?card={card}";
            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, url);

            HttpResponseMessage response = await httpClient.SendAsync(request);
            response.EnsureSuccessStatusCode();
        }
        catch (Exception e)
        {
            Debug.LogError($"PlayCard request failed: {e.Message}");
        }
    }


    public async Task StartGameAsync()
    {
        try
        {
            HttpResponseMessage response = await httpClient.GetAsync($"http://{serverAddress}/start_game");

            if (!response.IsSuccessStatusCode)
            {
                Debug.LogError($"StartGame request failed with status code: {response.StatusCode}");
                return;
            }
        }
        catch (Exception e)
        {
            Debug.LogError($"StartGame request failed: {e.Message}");
        }
    }


}