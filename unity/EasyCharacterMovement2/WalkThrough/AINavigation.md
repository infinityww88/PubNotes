这个例子，使用新的 NavMeshCharacter 组件来实现 click-to-move 运动。

```C#
public class ClickToMove : MonoBehaviour
{
    public Camera mainCamera;
    public Character character;

    public LayerMask groundMask;

    private NavMeshCharacter _navMeshCharacter;

    private void Awake()
    {
        _navMeshCharacter = character.GetComponent<NavMeshCharacter>();
    }

    private void Update()
    {
        if (Input.GetMouseButton(0))
        {
            Ray ray = mainCamera.ScreenPointToRay(Input.mousePosition);
            if (Physics.Raycast(ray, out RaycastHit hitResult, Mathf.Infinity, groundMask))
                _navMeshCharacter.MoveToDestination(hitResult.point);
        }
    }
}
```

这里使用 NavMeshCharacter 指示 character 向玩家点击的 world position 移动，它使用 NavMeshAgent 在 world 中只能地移动。
