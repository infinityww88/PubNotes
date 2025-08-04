InstanceFinder：这个 Game Instance 的有用信息 Finder。

你可以从 NetworkBehaviours 中获取大量有用信息，但在某些情况下，你的脚本可能未继承自 NetworkBehaviour。此时，InstanceFinder 可为你提供帮助。

InstanceFinder 能让你快速访问常用引用或信息，例如：SceneManager、IsClientStarted、TimeManager 等。

```C#
public class MyButton : MonoBehaviour
{
    public Image ButtonImage;
    
    /* It wouldn't make sense to update the UI
    * color on the server since it will have
    * no graphical interface. To save performance
    * we're only going to update color if client.
    * However, since this is a MonoBehaviour class
    * you do not have access to base.IsClientStarted.
    * Instead the InstanceFinder may be used. */
    private void SetColor(Color c)
    {
        if (InstanceFinder.IsClientStarted)
            ButtonImage.color = c;
    }
}
```