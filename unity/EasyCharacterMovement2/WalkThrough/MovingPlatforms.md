CharacterMovement组件可以无缝处理移动平台，无论是动态刚体、脚本控制还是动画驱动的移动平台，都无需你进行任何额外操作。角色能够停留在移动平台上的唯一条件是该平台必须属于可行走表面。

例如，你可以跳上一个完全动态的车辆，角色会自动将其视为移动平台，无需任何额外操作或自定义脚本。

此外，你还可以选择将角色"绑定"到特定的移动平台上。这样，即使角色没有站立或接触该平台，它也会跟随所绑定的平台一起移动。

在实现脚本化动态平台时，其移动逻辑应当编写在FixedUpdate方法中。这样可以让角色准确感知平台的当前状态，例如：

```C#
public void FixedUpdate()
{
    float t = EaseInOut(Mathf.PingPong(Time.time, _moveTime), _moveTime);
    Vector3 p = Vector3.Lerp(_startPosition, _targetPosition, t);

    _rigidbody.MovePosition(p);
}
```

如果动态平台通过 Animator 动画，记得将它的 Animator Update Mode 设置为 Animate Physics，以获得正确的集成。

下面的例子显示如何实现一个 one-way 平台。这个例子使用 Character 类的 IgnoreCollision 函数，按需要在 character 和 platform 开启或关闭 collision。

```C#
public class OneWayPlatform : MonoBehaviour
{
    public Collider platformCollider;

    private void OnTriggerEnter(Collider other)
    {
        if (!other.CompareTag("Player"))
            return;

        Character character = other.GetComponent<Character>();
        if (character)
            character.IgnoreCollision(platformCollider);
    }

    private void OnTriggerExit(Collider other)
    {
        if (!other.CompareTag("Player"))
            return;
        
        Character character = other.GetComponent<Character>();
        if (character)
            character.IgnoreCollision(platformCollider, false);
    }
}
```