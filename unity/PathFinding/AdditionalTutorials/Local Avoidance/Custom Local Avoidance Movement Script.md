# Custom Local Avoidance Movement Script

这个文档介绍如何将 Local Avoidance 集成到自己到移动脚本中，即在脚本中直接调用 Local Avoidance。

先构建一个简单的例子：

- 创建一个新的 scene
- 添加一个很大的平面，position=(0, 0, 0)，scale=(10, 10, 10)
- 添加一个新的 GameObject，称为 Simultor。在上面添加一个 RVOSimulator 组件，组件位于 Components > Local Avoidance > RVO Simultor
- RVOSimulator 组件上面有一些选项，现在先保留默认设置。但是这些选项的设置对性能有很大影响。这个组件将会处理 agents 的模拟，以及存储我们添加的任何动态 obstacles
- 添加一个简单的向前行走的 AI
  - 添加一个 Cylinder
  - 在 Cylinder 上添加组件 RVOController，Components > Local Avoidance > RVO Controller
  - RVOController 组件被设计为几乎是 drop-in 的 Unity Character Controller 的代替者，因此如果你使用过 character controller，就会很容易的使用它。处于明显的原因，它不支持一些碰撞特定的东西，例如 collision flags，但是它非常和 Character Controller 非常相似。
  - 设置 RVOController 的 height = 2

编写下面的组件

 ```C#
using UnityEngine;
using System.Collections;
using Pathfinding.RVO;

public class SimpleRVOAI : MonoBehaviour {
    RVOController controller;

    // Use this for initialization
    void Awake () {
        controller = GetComponent<RVOController>();
    }

    // Update is called once per frame
    public void Update () {
        // 只是获得移动方向上一个很远的位置
        var targetPoint = transform.position + transform.forward * 100;

        // 设置想要移动到的位置，想要的移动速度=10，但是如果必要，允许的最大移动速度=12
        controller.SetTarget(targetPoint, 10, 12);

        // 计算这一帧中移动多少。这个信息是基于之前的 frames 的移动命令的，因为 local avoidance 是被 RVOSimulator 以一个规律的间隔全局计算的。
        var delta = controller.CalculateMovementDelta(transform.position, Time.deltaTime);
        transform.position = transform.position + delta;
    }
}
```

RVOController 自己并不处理移动，因为一些游戏可能想要使用 CharacterController，一些只需要使用 transform.Translate，一些想要使用 Rigidbody，因此由移动脚本基于 RVOController 计算的 velocity 真实去移动 character。

现在是真正有趣的部分。复制 cylinder 并将它放在第一个前面的一定距离，并旋转 180 度使二者面面相对。因为它们都是简单地向前行走，因此一定会发生碰撞。点击 Play，这些 cylinders 应该彼此朝向对方移动，而就在发生碰撞之前，彼此避开了，awesome！

