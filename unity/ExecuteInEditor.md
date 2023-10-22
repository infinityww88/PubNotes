# Execute In Editor

## ExecuteAlways

使一个脚本的实例无论是作为 Play Mode 的一部分还是 Editor Mode 时总会执行。

默认地，MonoBehaviour 只在 Play Mode 中执行，而不再 Edit Mode 中执行，也不会再 Prefab Mode 中执行，即使进入 Play Mode。通过添加这个属性，MonoBehaviour 在所有地方都执行它的回调函数。

当你想要脚本执行作为 Editor tooling 而不是 Play Logic 的 一部分逻辑时，可以使用 ExecuteAlways。有时这样的逻辑和 Play Logic 一致，有时却有极大不同。

使用这个属性的 MonoBehaviour 必须确保在 Editor Mode 运行时不会运行错误修改 object 的 Play Logic。这可以通过 Application.IsPlaying 来判断脚本自己的 GameObject 是否是 playing world 的一部分。

如果 MonoBehaviour 在 Play Mode 下运行 Play Logic，并且没有检查 GameObject 是否是 Playing world 的一部分，则 Prefab Mode 中编辑的一个 Prefab 可能被原本只应运行在 game world 的 logic 错误地修改和保存。

如果脚本使用了静态变量或单例模式，应该确保脚本的实例属于 playing world，并且不属于 playing world 的实例不会被那些变量或单例意外的影响。

在一个不属于 playing world 的 object 上，一些事件函数不像运行时那样频繁地调用：

- Update：只在 Scene 的 something 改变时执行
- OnGUI
- OnRenderObject

## Application.IsPlaying(Object obj)

如果 object 是 playing world 的一部分返回 true。

在 built Player，总是返回 true。在 Editor 中，如果 Editor 在 Play Mode 中，并且提供的 object 是 playing world 的一部分，并且不是 Prefab Mode 中的 object 的一部分。

```C#
using UnityEngine;

[ExecuteAlways]
public class ExampleClass : MonoBehaviour
{
    void Start()
    {
        if (Application.IsPlaying(gameObject))
        {
            // Play logic
        }
        else
        {
            // Editor logic
        }
    }
}
```

## ExecuteInEditMode

ExecuteAlways 的前身，但是已过时，因为它没有考虑 Prefab Mode。如果一个 Prefab 带有标记 ExecuteInEditMode 的 MonoBehaviour，并且在 Prefab Mode 下编辑，然后进入 Play Mode，Editor 将会退出 Prefab Mode 来防止本应运行在 Play Mode 的逻辑意外地修改 Prefab。

ExecuteInEditMode 和 ExecuteAlways 修饰 MonoBehaviour 类，而不是事件方法。

## bool MonoBehaviour.runInEditMode

允许一个 MonoBehaviour 的特定实例在 edit mode 中运行（只在 editor 中可用），而 ExecuteAlways 使 MonoBehaviour 的任何实例都在 edit mode 中运行。

## EditorApplication.QueuePlayLoopUpdate

强制更新 Editor 事件循环，执行更新。
