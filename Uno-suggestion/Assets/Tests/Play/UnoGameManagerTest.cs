using System.Collections;
using System.Collections.Generic;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public class UnoGameManagerTest
{
    private GameObject gameObject;
    private UnoGameManager gameManager;
    [SetUp]
    public void SetUp()
    {
        gameObject = new GameObject();
       // gameManager = gameObject.AddComponent<UnoGameManager>();
    }

    [TearDown]
    public void TearDown()
    {
        Object.Destroy(gameObject);
    }

    [UnityTest]
    public IEnumerator AddAllCardNumbersTest()
    {
     

        yield return null;
    }


}
