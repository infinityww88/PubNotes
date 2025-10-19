# SyncVar Hook

Hook 属性可以用于指定一个函数，在 SyncVar 修改时在 client 上调用。

- Hook method 必须有两个和 SyncVar 属性相同类型的参数，第一个是 old value，第二个是 new value
- Hook 在 property value 被设置时总是调用。你不必自己设置它。
- Hook 只在改变 values 时调用，而且在 inspector 改变 value 不会触发更新
- Hook 可以是虚方法，并在派生类调用

下面是一个简单例子，当每个 player 在 server 上生成时，为其赋予一个随机颜色。

```C#
using UnityEngine;
using Mirror;

public class PlayerController : NetworkBehaviour
{
    [SyncVar(hook = nameof(SetColor))]
    Color playerColor = Color.black;

    // Unity makes a clone of the Material every time GetComponent<Renderer>().material is used.
    // Cache it here and Destroy it in OnDestroy to prevent a memory leak.
    Material cachedMaterial;

    public override void OnStartServer()
    {
        base.OnStartServer();
        playerColor = Random.ColorHSV(0f, 1f, 1f, 1f, 0.5f, 1f);
    }

    void SetColor(Color oldColor, Color newColor)
    {
        if (cachedMaterial == null)
            cachedMaterial = GetComponent<Renderer>().material;

        cachedMaterial.color = newColor;
    }

    void OnDestroy()
    {
        Destroy(cachedMaterial);
    }
}
```

