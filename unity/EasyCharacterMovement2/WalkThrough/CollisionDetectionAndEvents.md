Character类包含众多事件，可帮助你管理角色的各类交互行为。例如：  

- OnCollided事件：当角色在执行Move操作时与碰撞体（Collider）发生接触时触发，可用于处理碰撞后的逻辑（如停止移动、播放碰撞特效等）；  

- OnFoundGround事件：当角色检测到任何地面表面（无论是否可行走）时触发，可用于判断角色是否处于地面状态（如切换移动模式、触发落地动画等）。  

这些事件为角色与环境的交互提供了灵活的响应机制，开发者可根据需求选择继承Character类并重写对应事件方法（如OnCollided），或通过订阅事件（如Collided事件）来实现自定义逻辑。

在扩展Character类时，建议重写其对应的事件触发方法。例如，通过重写OnCollided方法来处理碰撞事件。

```C#
public class PlayerCharacter : Character
{
    protected override void OnCollided(ref CollisionResult collisionResult)
    {
        // Call base method implementation
        
        base.OnCollided(ref collisionResult);
        
        // Add your code here...
        
        Debug.Log($"Collided with {collisionResult.collider.name}");
    }
}
```

另一方面，如果通过组合来扩展 Character，建议监听暴露的事件。例如，订阅它的 Collided 事件来处理碰撞：

```C#
public class PlayerController : MonoBehaviour
{
    // The controlled Character

    private Character _character;

    protected void OnCollided(ref CollisionResult collisionResult)
    {
        Debug.Log($"Collided with {collisionResult.collider.name}");
    }

    private void OnEnable()
    {
        // Subscribe to Character events
        
        _character.Collided += OnCollided;
    }

    private void OnDisable()
    {
        // Un-subscribe from Character events
        
        _character.Collided -= OnCollided;
    }
}
```