# 消息系统

消息系统是一种通知但不知道通知的对方是谁的机制。

新的 UI 系统使用一个 messaging system 机制替换 SendMessage，解决了 SendMessage 中的存在的一些问题。

这个系统使用一个自定义接口来工作，一个 MonoBehavior 实现这个自定义接口向 messaging system 指示它可以接收一个 callback。当发射消息时，需要制指定一个 GameObject，然后消息调用将在这个 GameObject 上的所有实现自定义接口的👣上发生。

Messaging System 允许传递自定义用户数据，以及 event 应该在 hierarchy 中传播多远，即它是应该只在 GameObject 上执行，还是还可以在 children 以及 parents 上执行。除此以外，这个 messaging framework 还提供了许多 helper 函数来搜索和查找实现给定消息接口的 GameObjects。

这个消息系统是通用的，不仅仅用于 UI System，而且可以用于任何通用的游戏代码。

添加自定义 messaging events 非常简单，而它们就像使用相同 framework 来处理所有事件的 UI system 那样工作。

## 定义一个自定义消息

任何扩展 UnityEngine.EventSystem.IEventSystemHandler 的类或接口，都可以被认为是从 messaging system 接受事件的 target。

```C#
public interface ICustomMessageTarget : IEventSystemHandler
{
    // functions that can be called via the messaging system
    void Message1();
    void Message2();
}
```

一旦这个接口被定义，就可以被一个 MonoBehavior 实现。当实现时，它定义如果给定的消息在 MonoBehavior GameObject 上发出时将被执行的 functions（消息）。

```C#
public class CustomMessageTarget : MonoBehaviour, ICustomMessageTarget
{
    public void Message1()
    {
        Debug.Log("Message 1 received");
    }

    public void Message2()
    {
        Debug.Log("Message 2 received");
    }
}
```

现在已经有了一个脚本可以接收消息，我们需要发射消息。通常这将是对一些发生的低耦合事件（事件发送者不关心谁接收这个事件）的响应。例如，在 UI 系统中我们发射诸如 PointerEnter 和 PointerExit 等事件。

一个 static helper class 用来发送一个事件。它的参数需要一个消息的 target object，一些 user data，一个 functor（函数对象）用来映射 message interface 中的指定函数。

```C#
ExecuteEvents.Execute<ICustomMessageTarget>(target, null, (x, y) => x.Message1());
```

ExecuteEvents.Execute 用来发送消息，消息是 ICustomMessageTarget，发送目标是 target，即查找 target 上所有实现 ICustomMessageTarget 的组件，对于每个这样的组件调用它的 Message1 方法。
