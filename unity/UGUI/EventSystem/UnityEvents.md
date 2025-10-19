# UnityEvents

UnityEvents 是一种在 Editor 配置和持久化 callback 而不需要编程和脚本配置的方法。

Unity Events 用于：

- 内容驱动回调
- 系统解耦合
- 回调持久化
- 预配置的调用事件

UnityEvents 是一种 Serializable 对象，可以在 MonoBehavior 中声明这种类型的对象，然后它可以在 Inspector 上显示并配置，在 code 可以想标准 .net delegate 一样调用，而真正调用到的方法就是在 Inspector 中配置的函数。

UnityEvents 有着和标准 delegates 类似的限制，即它们保存对 target 对象的引用，阻止其被垃圾回收。

## 使用 UnityEvents

- 确保 using UnityEngine.Events
- 点击 + 按钮添加一个回调
- 选择想要接受回调的 UnityEngine.Object（target）
- 选择想要调用的函数
- 可以为这个 event 添加多个回调

在 Inspector 上配置一个 UnityEvent 时，有两种类型的函数被支持：

- Static：Static call 是预配置的调用，在 UI 中配置调用时使用的参数
- Dynamic：Dynamic call 使用 code 中发送的参数进行调用，并且这绑定到被调用的 UnityEvent 的类型。UI 过滤回调函数，只显示参数和 UnityEvent 匹配的函数

## 泛型 UnityEvents

默认地，UnityEvent 动态绑定到一个 void function。但是可以定义最多 4个 参数的泛型 UnityEvents。你需要先自定义支持多个参数的 UnityEvent 类

```C#
[Seriazlizable]
public class StringEvent : UnityEvent <string> {}
```

通过 event.Invoke(arguments) 调用事件回调函数。

