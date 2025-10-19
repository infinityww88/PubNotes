# Behavior Designer

## Behavior Tree 组件

存储 behavior tree，作为 Behavior Designer 和 tasks 之间的接口。

- EnableBehavior()
- DisableBehavior(bool pause = false)
- TaskType FindTask<TaskType>()
- List<TaskType> FindTasks<TaskType>()
- Task FindTaskWithName(string taskName)
- List<Task> FindTasksWithName(string taskName)

behaviorTree.ExecutionStatus 是 tree 当前的执行状态
- Running
- Success
- Failure

可监听的事件

- OnBehaviorStart
- OnBehaviorRestart
- OnBehaviorEnd

属性

- Behavior Name
- Behavior Description
- External Behavior：引用要执行的外部的 behavior tree
- Group：数字 behavior tree group
- Start When Enabled：当 component enabled 时，behavior 开始运行
- Asynchronous Load：behavior 是否在单独的线程中加载。因为 Unity 不允许在非 main 线程使用 API calls，如果你使用 shared variables 属性映射应该关闭这个选项
- Pause When Disabled：如果为 true，behavior tree 在 component disable 时 暂停，否则 behavior tree 将会结束
- Restart When Complete：如果为 true，BT 在完成执行时重新开始，否则将会结束
- Reset Values On Restart：如果为 true，BT 变量和 task public 变量将重置为 BT 开始时的初始值
- Log Task Changes：用于调试，如果开启，BT 输出任何时候的 task status 改变，例如 starting 或 stopping

## 从脚本中创建 Behavior Tree

在一些情况下，可能想需要从脚本创建 Behavior Tree，而不是使用包含 behavior tree 的 BT prefab。例如加载一个 external behavior tree。

```C#
using UnityEngine;
using BehaviorDesigner.Runtime;

public class CreateTree : MonoBehaviour
{
    public ExternalBehaviorTree behaviorTree;

    private void Start()
    {
        var bt = gameObject.AddComponent<BehaviorTree>();
        bt.StartWhenEnabled = false;
        bt.ExternalBehavior = behaviorTree;
    }
}
```

bt.StartWhenEnabled = false 阻止 tree 立即开始执行，需要使用 bt.EnableBehavior() 手动开始。

## Behavior Manager

当 behavior tree 运行时，它将会创建一个带有 Behavior Manager 组件的新的 GameObject，如果还没有创建这样的 GameObject。这个组件管理场景中所有 behavior trees 的执行。

属性

- Interval property

  控制 BT tick 的频率

  - Every Frame：每个 frame Update loop tick
  - Specify Seconds：以指定 interval 时间 tick
  - Manual：调用 BehaviorManager.instance.Tick() 手动调用 tick

  还可以使用 BehaviorManager.instance.Tick(behaviorTree) 使每个 behavior tree 具有自己的 tick rate。例如，可以使用 DOTween 驱动。

- Task Execution Type

  指定 behavior tree 是否应该连续执行 tasks，直到在那个 tick 遇到一个在已经执行过的 task，或者它应该连续运行 tasks 直到在那个 tick 中执行了一个最大数量的 tasks。

  ![BTManagerTaskExecutionType](../Image/BTManagerTaskExecutionType.png)

  例如这个 BT 中，Repeater 设置为 repeat 5 times。如果 Behavior Manager 的 Task Execute Type 设置为 No Duplicates，Play Sound task 将会在每个 tick 执行一次。如果 Task Execution Type 设置为 Count，可以指定一个 maximum task execution count。如果指定为5，则 Play Sound task 将会在一个 tick 中执行5次

## Tasks

API

- void OnAwake()

  OnAwake 在 BT enabled 时调用一次，将其想象为一个 constructor

- void OnStart()

  在 task 开始执行前调用，用来从之前的 task 运行中重置任何变量。即每次 BT 求值进入这个 task，都会执行 OnStart

- TaskStatus OnUpdate()

  实际运行这个 task，返回求值状态（Running，Success，Failure）

- void OnEnd()

  对应 OnStart，每次求值结束（OnUpdate 返回 Success 或 Failure）调用

- void OnPause(bool paused)

  BT 暂停或恢复时调用

- float GetPriority()

  返回 task 的优先级，被 Priority Selector 使用

- float GetUtility

  返回 task 的 utility，被 Utility Selector 使用

- void OnBehaviorComplete()

  BehaviorTree 完成执行时调用

- void OnReset()

  被 inspector 调用，来重置 public properties

- void OnDrawGizmos()

  绘制 task 的 gizmos

- Behavior Owner

  拥有这个 task 的 Behavior 引用

属性

- name

- comment

- instant

  当一个 task 返回 success 或 fail，立刻在同一个 tick 移动到下一个 task（如果将 task 认为是 coroutine，则表示是否执行 await new WaitForTickEnd())，否则 task 将会等待当前 tick 执行完毕，在移动到下一个 task。这是一个非常容易的限流（throttle）behavior tree 的方法。

Task 生命周期

![BTTaskLifeCycle](../Image/BTTaskLifeCycle.png)

## Parent Tasks

Parent Tasks 是 composite 和 decorator task。

API

- public virtual int MaxChildren()

  一个 parent task 可以拥有的 children 的最大数量。通常是 1 或 int.MaxValue

- bool CanRunParallelChildren()

  这个 task 是否是 parallel task

- int CurrentChildIndex()

  当前 active child 的 index

- bool CanExecute()

  当前 task 是否可以执行

- TaskStatus Decorate(TaskStatus status)

  应用一个 decorator 到 executed status

- void OnChildExecuted(TaskStatus childStatus)

  通知 parent task，child 以及被执行完了，并且具有 childStatus 的状态码

- void ChildExecuted(int childIndex, TaskStatus childStatus)

  通知 parent task，位于 childIndex 的 task 执行完了，并且具有 childStatus 的状态码

- void OnChildStarted() / OnChildStarted(int childIndex)

  和 OnChildExecuted 对应，通知 parent child 或指定 index 的 child 开始执行

- TaskStatus OverrideStatue(TaskStatus status)

  一些 parrent task 需要能够覆盖 status，例如 parallel tasks

- TaskStatus OverrideStatus()

  一个 interrupt node 如果被中断将覆盖这个 status

- void OnConditionalAbort(int childIndex)

  通知 composite task 一个 conditional abort 被触发，以及应该重置的 child index

## 编写一个新的 Conditional Task

```C#
using UnityEngine;
using BehaviorDesigner.Runtime;
using BehaviorDesigner.Runtime.Tasks;
public class WithinSight : Conditional
{
    public float fieldOfViewAngle;
    public string targetTag;
    public SharedTransform target;
    private Transform[] possibleTargets;

    public override void OnAwake()
    {
        var targets = GameObject.FindGameObjectsWithTag(targetTag);
        possibleTargets = new Transform[targets.Length];
        for (int i = 0; i < targets.Length; ++i) {
            possibleTargets[i] = targets[i].transform;
        }
    }

    public bool WithinSight(Transform targetTransform, float fieldOfViewAngle)
    {
        Vector3 direction = targetTransform.position -
        transform.position;
        return Vector3.Angle(direction, transform.forward) < fieldOfViewAngle;
    }

    public override TaskStatus OnUpdate()
    {
        for (int i = 0; i < possibleTargets.Length; ++i) {
            if (WithinSight(possibleTargets[i], fieldOfViewAngle) {
                target.Value = possibleTargets[i];
                return TaskStatus.Success;
            }
        }
        return TaskStatus.Failure;
    }
}
```

## 编写一个新的 Action Task

```C#
using UnityEngine;
using BehaviorDesigner.Runtime;
using BehaviorDesigner.Runtime.Tasks;
public class MoveTowards : Action
{
    // The speed of the object
    public float speed = 0;
    // The transform that the object is moving towards public SharedTransform target;
    public override TaskStatus OnUpdate()
    {
        // Return a task status of success once we've reached the target
        if (Vector3.SqrMagnitude(transform.position - target.Value.position) < 0.1f) {
            return TaskStatus.Success;
        }
        // We haven't reached the target yet so keep moving towards it
        transform.position = Vector3.MoveTowards(transform.position, target.Value.position, speed * Time.deltaTime);
        return TaskStatus.Running;
    }
}
```

## Debugging

当 behavior tree 运行时，不同状态的 task 具有不同的颜色。

green：task 正在运行

gray：task 没有运行

右下角 check 符号：task 运行完毕并返回 Success

右下角 X 符号：task 运行完毕并返回 Failure

当 tasks 运行时，还可以在 inspector 改变 task 变量，改变的变量在游戏中实时反映。

右键点击 task 菜单允许设置 breakpoint。当 task 设置了 breakpoint，一旦它开始执行时，Behavior Designer 会暂停 Unity。这可以用于观察何时执行一个特定的 task。

当 task 被选中时，可以在 inspector 中点击变量左边的放大镜，这样可以在 graph 中观察这个变量，在 task 旁边。这是观察一个特定变量非常好的方法，而不必使 inspector 保持打开。

有时你只想关注一个特定 tasks 集合，而阻止剩余 tasks 执行。可以 disabling 一组 tasks。Hover task 并选择 task 左上角的橙色 X。Disabled tasks 不会运行并立刻返回 success。Disabled tasks 显示为被 enabled 更深的颜色。

还有一个 debugging 选项是任何时候 task 改变 state 时输出到 console。如果 Log Task Changes 开启，将会出现类似下面的日志：

```plaintext
GameObject - Behavior: Push task Sequence (index 0) at stack index 0
GameObject - Behavior: Push task Wait (index 1) at stack index 0
GameObject - Behavior: Pop task Wait (index 1) at stack index 0 with status Success
GameObject - Behavior: Push task Wait (index 2) at stack index 0
GameObject - Behavior: Pop task Wait (index 2) at stack index 0 with status Success
GameObject - Behavior: Pop task Sequence (index 0) at stack index 0 with status Success
Disabling GameObject - Behavior
```

每一条消息可以分解为以下部分：

{game object name } - {behavior name}: {task change} {task type} (index {task index}) at stack index {stack index} {optional status}

- {game object name}：behavior tree 附加到 gameobject 的名字
- {behavior name}：behavior tree 的名字
- {task change}：指示 task 的新 status。例如，一个 task 开始执行时被 push 到 stack，完成运行时从 stack pop
- {task type}：task 的 class type
- {stack index}：task 被 push 到的 stack 的索引。如果你有一个 parallel node，你将会使用多个 stacks。每个 parallel node 是一个子树，这个 BT 子树使用一个单独的 task 运行
- {optional status}：特定变化的额外状态信息。弹出 stack 的 task 将会输出 task status

## Variables

Behavior trees 的一个优势是它们非常灵活，所有的 tasks 都是低耦合的，意味着一个 task 不依赖于其他 task 来操作。这一点的缺陷是有时需要 task 之间共享信息。例如，你可能用一个 task 确定是视野内是否有一个 target。如果有 target 在视野内，你可能用另一个 task 移动到这个 target。这种情况下，两个 task 需要通信，共享 target 信息。

传统 behavior tree 实现中，这通过黑板技术实现（blackboard）。在 Behavior Designer 中，你可以方便地使用变量 variables。

public SharedTransform target;

SharedTransform 在 script 中创建一个共享变量的引用，它可以引用 Behavior Tree 上创建的一个变量。在 Behavior Designer 中创建真正的变量实体，它在整个 BT 的 tasks 中共享，只要 script 中声明 Shared 变量引用，然后在 Inspector 中将 BT 的变量设置到这个 task 的引用中。如果两个或多个 tasks 的 Shared 引用被设置为同一个 behavior tree 变量，它们就可以共享这个变量，通过它来传递信息。

Task Inspector 变量右上角三角形按钮用来设置这个变量的 Variable Mappings。

Variable Mappings 允许 SharedVariable 映射相同类型的属性（GameObject 组件上暴露的相同类型变量，而不必引用 behavior tree 的变量）。这允许你快速 get or set 一个 MonoBehavior 组件上的 value，这免于使用 Behavior Tree 上的变量。无论何时访问这个变量，它将去访问映射到的组件属性。这允许你 get or set Transform 的 position 而不需额外的 tasks。

Variable Mappings 是操作到 behavior tree 变量上，而不是 task SharedVariables 引用。

Behavior Tree 变量相当于所有 tasks 的 blackboard。

Behavior Designer 同时支持 local 和 global variables。

Local Variables 的 scope 就是 behavior tree，即所有 tasks 的 blackboard，被所有 tasks 共享。每个 behavior tree 都自己的 Local Variables。

Global Variables 是资源 assets，通过 Window > Behavior Designer > Global Variables 菜单或者 Behavior Designer Window 的 Variables Panel 中的 Global Variables 按钮创建。Behavior Designer 在 Resource 目录创建一个 BehaviorDesignerGlobalVariables 资源文件，所有 global variables 在其中保存。任何 BT 中的 tasks 的 SharedVariable 既可以引用 local blackboard 的变量，也可以引用 global variable。

![BTGlobalVariable](../Image/BTGlobalVariable.png)

Local Variables 可以被任何引用 behavior tree 的脚本通过 API 访问。

Global Variable 可以被 non-Task 派生的 objects 访问。

Dynamic Variables 允许创建限制于 scope 的临时变量。如果你想在受限数量的 tasks 之间共享数据，而不需要在这些 tasks 之外访问，这个功能非常有用。Dynamic variables 可以通过点击 variable field 右边的 circle，然后选择 “(Dynamic)” 来创建 Dynamic Variables。

当 dynamic variable 创建之后，你可以输入变量的名字。Dynamic Variable 现在可以用在你的 tree 中了。dynamic variable 和所有引用相同 dynamic variable 名字的 fields 具有相同的值。Dynamic Variable 的类型就是变量引用声明的类型。Dynamic Variables 名字是大小写敏感的，而且不应该和 tree 中的 Local Variables 相同。

变量本身就是数据，或者是在 Global Variables assset 中创建的，或者是在 Behavior Tree blackboard 中创建，或者Dynamic Variables 创建的临时变量。无论是 Global Variables，Local Variables，Dynamic Variables，都是在 Inspector 中创建，而在 Task 脚本中都是通过 SharedVariables 引用，SharedVariables 不管变量来自于何处。

Behavior Designer 默认支持以下 shared variable types。还可以创建自己的 shared variable 类型：
- SharedAnimationCurve
- SharedBool
- SharedColor
- SharedFloat
- SharedGameObject
- SharedGameObjectList
- SharedInt
- SharedMaterial
- SharedObject
- SharedObjectList
- SharedQuaternion
- SharedRect
- SharedString
- SharedTransform
- SharedTransformList
- SharedVector2
- SharedVector3Int
- SharedVector3
- SharedVector3Int
- SharedVector4


## 创建新的 Shared Variables 类型

继承 SharedVariable，实现以下方法

```C#
[System.Serializable]
public class SharedOBJECT_TYPE : SharedVariable<OBJECT_TYPE>
{
    public static implicit operator SharedOBJECT_TYPE(OBJECT_TYPE value)
    {
        return new SharedOBJECT_TYPE { Value = value };
    }
}
```

SharedVariables 可以保护任何类型的 object，包括 primitives，arrays，lists，自定义 objects 等等。

## 从 non-Task Objects 访问变量

Variables 通常通过在 Behavior Designer inspector panel 中为 task field 赋值变量名完成。

Local Variables 还可以被 non-Task 类访问：

- behaviorTree.GetVariable("MyVariable");
- behaviorTree.SetVariable("MyVariable", value);
- behaviorTree.SetVariableValue("MyVariableName", value);

```C#
var myIntVariable = (SharedInt)behaviorTree.GetVariable("MyVariable");
myIntVariable.Value = 42;
```

Global Variables 可以通过 GlobalVariable instance 访问：

- GlobalVariables.Instance.GetVariable("MyVariable");
- GlobalVariables.Instance.SetVariable("MyVariable", value);

## Conditional Aborts

Conditional aborts 允许 Behavior Tree 动态响应变化，而不需要在 behavior tree 堆积很多 Interrupt/Perform Interrupt tasks。

这个功能类似 Unreal Engine 4 的 Observer Aborts。绝大多数 behavior tree 实现在每个 tick 重新求值整个 tree。Conditional aborts 是一个优化，避免重新运行整个 tree。

Conditional aborts 可以从任何 Composite task 中访问。

conditional abort是一种中断机制

BT有两种实现方式

- 一种是每次 tick 都求值整个 tree，这样任何条件 task 的状态变化都会被感知，因此不需要中断机制，这是标准的 behavior tree 实现。

- 一种是每个 tick 只运行当前 Active 的 Task（返回Running），直到当前 Task 结束（返回非 Running 状态），并向下求值得到下一个 Active 的 Task。

第一种虽然更精确，但是每次 tick 求值整个 tree 很浪费，第二种是优化实现，但是如果当前 Active Task 持续很长时间，当前面的 condition 发生改变时就感知不到。

Conditional abort 是为第二种实现提供的中断当前 Active Task 的机制。Conditional Abort 只用在 Composites Task上。

一个 behavior tree 中，所有中间节点（parent task）都是 Composite Task 或者 Decorator Task。所有叶节点都是 Conditional Task 和 Action Task，它们不可能是中间节点，它们没有子节点。因此所有的 logic 都在叶节点，中间节点只是逻辑导航。Conditional Abort 用于所有 Composite Task 中间节点。

Behavior Designer 的求值方式，和标准的 behavior tree 非常相似，每个 tick 中，也是按照标准遍历顺序求值整个 tree。只是每次求值一个 Composite Task 时，比较这个 Composite Task 和 Active Action Task，决定是否求值这个 Composite Task 子树：

- 如果 Composite Task 的 Conditional Abort 为 Self，只有 Active Action Task 在 Composite Task 的子树上时，才会求值 Composite Task 子树
- 如果 Composite Task 的 Conditional Abort 为 Low Priority，只有 Active Action Task 在 Composite Task 的右边时，即按照先序遍历在 Composite Task 后面，才会求值 Composite Task 子树。如果 Active Action Task 在 Composite 子树上，不会求值 Composite Task 子树，因此会直接继续运行 Active Action Task。
- None：直接拒绝求值子树
- Both：组合 self 和 low priority

当决定求值 Composite Task 子树时，按照这个规则递归应用到每个遇到的 Composite Task，每个都和 Active Action Task 比较。

每次求值过程，都是要找到（陷入）一个 Action Task。

Conditional Abort 求值过程除了判断 Composite Task 和上一个Action Task，就是普通的求值过程，一旦求值到一个叶节点 Action Task，这个 Action Task 就替换了上一个 Action Task（刚才用于比较的）称为 Active Action Task，并开始运行它，这样刚才的 Action Task 就被 Abort 了。

每次 Behavior Designer 求值 tree 的过程，就像标准 tree 求值一样，唯一的区别就是 Composite Task 的 Abort Type 和 Active Action Task 进行判断，是否要执行这个子树。如果 Active Action Task 不存在（第一次运行），则直接求值子树；如果判断不执行 Composite Task 子树，则这个 Task 直接返回 Success，并继续向后求值。如果遇到新的 Action Task，它就成为 Active Action Task。如果新的 Active Action Task 和之前的不同，则之前的 Active Action Task 被 Abort。每次求值之后总是找到一个 Active Action Task，并在这个 tick 执行 它。

每个 tick，遍历 tree（比较 Composite Abort Type 和 Active Action Task），找到一个 Active Action Task，运行它。如果新的 Active Action Task 和之前的 Active Action Task 不同，则发送 Abort。

这样理解 Behavior Tree 的求值过程：每个 tick 从 root entry 求值整个 tree，每次求值到 Composite Task，查看它的 Abort Type：

- 如果是右箭头（low priority）且 Active Action Task 在 Composite Task 右边，则求值 Composite Task 子树
- 如果是下箭头（self）且 Active Action Task 在 Composite Task 子树上，则求值 Composite Task 子树
- 如果是 Both 则同时应用上面两个规则
- 如果是 None，或者上面的规则不成立，则 Composite Task 不继续向下求值，而是直接返回 Success
- 如果求值到一个叶节点，则这个 Task 就成为新的 Active Action Task。如果新旧 Active Action Task 不同，则原来的 Action Task 被称为 Abort
- 如果没有求值到任何叶节点（例如 Active Action Task 的 Parent Composite Task 是 None），则 Active Action Task 保持不变，并在这个 tick 中继续 Update

## Events

Behavior Designer 中的事件系统允许你的 behavior trees 很容易地相应变化。

事件系统可以使用 code 或者 task 触发一个事件。

使用 Task 处理事件：

- Send Event Task：发射事件

- Has Received Event：conditional task，一旦接收到事件，返回 Success

使用脚本处理事件：

发射事件

```C#
var behaviorTree = GetComponent<BehaviorTree>();
behaviorTree.SendEvent<object>("MyEvent", Vector3.zero);
```

接收事件

```C#
public void OnEnable()
{
    var behaviorTree = GetComponent<BehaviorTree>();
    behaviorTree.RegisterEvent<object>("MyEvent", ReceivedEvent);
}

public void ReceivedEvent(object arg1)
{

}

public void OnDisable()
{
    var behaviorTree = GetComponent<BehaviorTree>();
    behaviorTree.UnregisterEvent<object>("MyEvent", ReceivedEvent);
}
```

## External Behavior Trees

可复用的 tree，behavior tree 资源。在一个 BT 中使用 Behavior Tree Reference Task 引用一组 Behavior Tree 资源。引用的 Tree 称为 Parent 的子树。当parent tree 开始执行时，将引用的 tree 加载并在 parent tree graph 中完全展开，替换 Reference Task。子树中任何和 Parent Tree 中相同名字和类型的 SharedVariable 被 Parent 的覆盖。

Behavior Tree Reference Task 引用这一组 Behavior Tree，它们都被展开并连接到 Parent Composite Task，就像手动连接多个子树一样，至于它们是 selector 还是 sequence，依赖于 Parent Composite Task 的类型。如果 Parent Task 只允许一个 child，而 Reference Task 包含多个 tree，则只会展开一个，并且在 console 打印警告信息。

默认地，Parent Tree 的变量覆盖应用的子树的变量（相同名字相同类型）。如果 Reference Task 引用多个 tree，可以为每个子树指定不同的变量。

External Behavior Tree 也可以在 Behavior Tree 组件上直接替换原来的 tree。

## Pooling

External behavior trees 可以被 pooled，这样可以在多个 external trees 之间切换时，可以得到更好的性能。

当 external behavior tree 被实例化时，Init 应该被调用来反序列化 external behavior tree。然后 pooled external trees 可以被赋予 behavior tree component，就像没有被 pooled external behavior trees 一样。

```C#
using UnityEngine;
using BehaviorDesigner.Runtime;

public class ExternalPoolExample : MonoBehaviour {
    public BehaviorTree behaviorTree;
    public ExternalBehavior externalBehaviorTree;
    private ExternalBehavior[] externalPool;
    private int index;
    public void Awake()
    {
        // Instantiate five External Behavior Tree which will be reused. The Init method will deserialize the External Behavior Tree.
        externalPool = new ExternalBehavior[5];
        for (int i = 0; i < externalPool.Length; ++i) {
            externalPool[i] = Object.Instantiate(externalBehaviorTree);
            externalPool[i].Init();
        }
    }
    public void OnGUI()
    {
        // Assign the next External Behavior Tree within the simplified pool.
        if (GUILayout.Button("Assign")) {
            behaviorTree.DisableBehavior();
            behaviorTree.ExternalBehavior = externalPool[index];
            behaviorTree.EnableBehavior();
            index = (index + 1) % externalPool.Length;
        }
    }
}
```

## Referencing Tasks

当编写一个新 task 时，有时需要访问另一个 task。例如 TaskA 可能想得到 TaskB.SomeFloat 的值。因此 TaskA 需要引用 TaskB。

```C#
using UnityEngine;
using BehaviorDesigner.Runtime.Tasks;

public class TaskA : Action
{
    public TaskB referencedTask;
    public void OnAwake()
    {
        Debug.Log(referencedTask.SomeFloat);
    }
}
```

```C#
using UnityEngine;
using BehaviorDesigner.Runtime.Tasks;
public class TaskB : Action
{
    public float SomeFloat;
}
```

将 TaskA 和 TaskB 添加的 Tree 中。在 TaskA 的 inspector 中出现 Referenced Task。点击 Select 选择 TaskB，这样 TaskB 就被连接到 TaskA 的 referencedTask 上。然后 TaskA 中就可以访问 TaskB 的 SomeFloat。Inspector 中引用的 TaskB 右边：X 删除连接，i 高亮连接的 TaskB。

类似 SharedVariable 引用，但是为 Task 引用做了优化。

Task 也可以使用数组引用。

```C#
public class TaskA : Action
{
    public TaskB[] referencedTasks;
}

```

## Object Drawers

OnGUI

可以调用 Odin 的 Draw System 绘制 Task Inspector。

## Variable Synchronizer

这是一个链接组件，将一个 behavior tree 组件的 SharedVariable 连接到其他组件（不是 behavior tree）的某个相同类型的属性上，指定一个绑定方向。Variable Synchronizer 指定一个 Update Interval，每次 Update 按照 绑定方向 在 behavior tree 组件的 SharedVariable 和 非 behavior tree 组件的属性直接进行复制。

这是一个简单而常见的需求，可以自己实现，但是 Behavior Designer 提供了这个组件实现了这个功能。

## 引用 Scene Objects

创建 behavior tree 时，常见的实践是使用 一个 Shared Variable 或 task 引用 scene 中的 objects。

如果 behavior tree 引用 scene objects，将它拖拽到 Project 生成 Prefab 并从 scene 中移除之后，引用的属性就会变为 missing。这是因为 asset（prefab）不能引用 scene 中的 object。

这是 Unity 的限制，解决办法是在运行时实例化 prefab 之后手动设置这些引用。

有很多方法可以在 runtime 时设置 scene reference object。

一种方法是使用 Find Task，以及通过 name 查找场景中的物体。

另一种方法是拥有一个已经存在于 scene 中的引用 object 的组件。Prefab 实例化之后，这个组件可以为这个 tree 设置引用的 object。

```C#
using UnityEngine;
using BehaviorDesigner.Runtime;

public class Spawner : MonoBehaviour
{
    public GameObject m_Enemy;
    public void Start()
    {
        var behaviorTree = GetComponent<BehaviorTree>();
        behaviorTree.SetVariableValue("Enemy", m_Enemy);
    }
}
```

## Task Attributes

Behavior Designer 暴露以下属性：

- Help URL

  ```C#
  [HelpURL("http://www.example.com")] public class MyTask : Action
  {
  }
  ```

- Task Icon

  ```C#
  [TaskIcon("Assets/Path/To/{SkinColor}Icon.png")] public class MyTask : Action
  {
  }
  ```

  路径相对于 root project folder（Assets）。{SkinColor} 被 Unity skin color 替换，“Light” 或 “Dark”

- Task Category

  ```C#
  [TaskCategory("Common")] public class Seek : Action
  {
  }
  ```

  Seek Action 在 Behavior Designer 的 Task Panel 中被放到 “Common” 分类下面。

  分类 Categories 可以通过斜线创建嵌套分类

  ```C#
  [TaskCategory("RTS/Harvester")] public class HarvestGold : Action
  {
  }
  ```

- Task Description

  ```C#
  [TaskDescription("The sequence task is similar to an \"and\" operation. ..."]
  public class Sequence : Composite
  {
  }
  ```

  描述在 graph 的左下角区域显式

- Linked Task

  ```C#
  [LinkedTask]
  public TaskGuard[] linkedTaskGuards = null;
  ```

  有 SharedVariable，没有 SharedTask。当你想一组 tasks 共享同一个 task，使用 LinkedTask 属性。
