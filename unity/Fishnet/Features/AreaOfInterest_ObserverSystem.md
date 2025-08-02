Fish-Networking 搭载了一套先进的网络兴趣区域 Area of interest 管理系统，用于精准控制每个户端接收哪些对象的相关信息。

观察者（Observer）是指能够查看对象并与之交互的客户端。您可以通过 NetworkObserver 和/或 ObserverManager 组件来配置哪些客户端有权观察特定对象。

若客户端未被设定为某对象的观察者，则该对象对其处于非激活状态——客户端既不会接收该对象的网络消息，也不会触发相关回调函数。对于场景对象而言，它将始终保持禁用状态，直至客户端获得观察权限；若是动态实例化的对象，则客户端在获得观察权之前根本不会加载该对象。

该观察者系统专为新手开发者设计了开箱即用的基础功能。当您需要自定义客户端观察对象的规则时，系统还提供了高度灵活的扩展能力——请注意这里存在多种条件判断类型，您甚至可以创建自定义条件。

Fish-Networking 提供的 NetworkManager 预制体已包含新项目开发所需的推荐基础组件。该预制体内置的 ObserverManager 组件预配置了场景条件（Scene Condition）。若您尚未熟悉 ObserverManager 和条件类型，请立即通过上方链接学习相关文档。

新手开发者常遇到的典型问题是场景对象无法为客户端启用：这通常发生在客户端未被认定为对象所在场景的成员，且场景条件阻止了该对象为客户端生成时。NetworkManager 预制体中的 PlayerSpawner 脚本会将玩家添加到当前场景，从而使客户端成为该场景内对象的观察者——但前提是玩家对象必须成功生成。如果您自行创建了 NetworkManager 对象或移除了 PlayerSpawner 脚本，则需要手动将客户端加载到目标观察场景中。

遇到此类问题时，您当然可以选择移除 ObserverManager 或其中的场景条件，但此举并不推荐——因为其他场景的对象可能会错误地尝试在未授权客户端上生成。另一种解决方案是将客户端添加到对象所在场景，具体实现方式多种多样。

假设您已移除 PlayerSpawner 组件或未使用 SceneManager.AddOwnerToDefaultScene 方法，则必须通过 SceneManager 显式加载客户端场景。只有通过 SceneManager 加载的场景，其中的对象才会被认定为网络同步场景。客户端可通过全局场景加载或针对特定连接（客户端）的场景加载成为场景成员。关于网络同步场景管理的详细说明（包括全局场景与连接场景的区别），请参阅 SceneManager 章节。

## Modifying Conditions

运行时可以修改多个条件。每个条件可修改的内容可能有所不同。我建议您查看API以了解每个条件公开了哪些属性。

要修改某个条件的属性，您必须通过NetworkObserver组件来访问该条件。

```C#
//Below is an example of modifying the distance requirement
//on a DistanceCondition. This line of code can be called from
//any NetworkBehaviour. You may also use nbReference.NetworkObserver...
base.NetworkObserver.GetObserverCondition<DistanceCondition>().MaximumDistance = 10f;
```

所有条件都可以启用或禁用。当某个条件被禁用时，其要求将被忽略，就像该条件不存在一样。这对于临时禁用对象上的条件要求非常有用。

```C#
//The OwnerOnlyCondition is returned and disabled.
//This allows all players to see the object, rather than just the owner.
ObserverCondition c = base.NetworkObject.NetworkObserver.GetObserverCondition<OwnerOnlyCondition>();
c.SetIsEnabled(false);
//Even though we are returning ObserverCondition type, it could be casted to
//OwnerOnlyCondition.
```

## Custom Conditions

有时您可能需要对观察器条件有特殊的需求。在这种情况下，您可以轻松地创建自己的 ObserverCondition。下面的代码中包含有关如何创建自定义条件的注释说明。

```C#
//The example below does not have many practical uses
//but it shows the bare minimum needed to create a custom condition.
//This condition makes an object only visible if the connections
//ClientId mathes the serialized value, _id.

//Make a new class which inherits from ObserverCondition.
//ObserverCondition is a scriptable object, so also create an asset
//menu to create a new scriptable object of your condition.
[CreateAssetMenu(menuName = "FishNet/Observers/ClientId Condition", fileName = "New ClientId Condition")]
public class ClientIdCondition : ObserverCondition
{
    /// <summary>
    /// ClientId a connection must be to pass the condition.
    /// </summary>
    [Tooltip("ClientId a connection must be to pass the condition.")]
    [SerializeField]
    private int _id = 0;

    private void Awake()
    {
        //Awake can be optionally used to initialize values based on serialized
        //data. The source file of DistanceCondition is a good example
        //of where Awake may be used.
    }
    
    /// <summary>
    /// Returns if the object which this condition resides should be visible to connection.
    /// </summary>
    /// <param name="connection">Connection which the condition is being checked for.</param>
    /// <param name="currentlyAdded">True if the connection currently has visibility of this object.</param>
    /// <param name="notProcessed">True if the condition was not processed. This can be used to skip processing for performance. While output as true this condition result assumes the previous ConditionMet value.</param>
    public override bool ConditionMet(NetworkConnection connection, bool currentlyAdded, out bool notProcessed)
    {
        notProcessed = false;

        //When true is returned it means the connection meets
        //the condition requirements. When false, the
        //connection does not and will not see the object.

        //Will return true if connection Id matches _id.
        return (connection.ClientId == _id);
    }

    /// <summary>
    /// Type of condition this is. Certain types are handled different, such as Timed which are checked for changes at timed intervals.
    /// </summary>
    /// <returns></returns>
    /* Since clientId does not change a normal condition type will work.
    * See API on ObserverConditionType for more information on what each
    * type does. */
    public override ObserverConditionType GetConditionType() => ObserverConditionType.Normal;
}
```

通过查看其他预置条件的源码，您可以大致了解一个条件所具备的灵活性。