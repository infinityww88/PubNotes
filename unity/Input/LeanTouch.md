# Lean Touch

## Get Started

添加 LeanTouch 到 scene，添加 EventSystem 到 scene 中。

当进入游戏时，这个组件会自动将所有 mouse 和 touch input 转换成易于使用的 format。

每个 scene 一个，或者所有 scene 共享一个，使用 DontDestroyOnLoad。

Lean Touch 主要用于 Game Scene 的交互，而不是 GUI。对于 GUI 使用 Unity 内置 EventSystem 即可。Lean Touch 通过标记是否忽略从 GUI 开始的 touch 或者位于 GUI 的touch 来于 GUI 事件处理隔离。为 GUI 使用 EventTrigger 即可。EventTrigger 和 Unity 内置的 EventSystem 机制都是要有 touch 目标的（GUI，或者 GameObject），而 Lean Touch 不需要目标，只处理 touch finger，当然，它提供了很多组件来为 touch 添加目标。

LeanTouch 为绝大部分常见 Touch 应用提供了支持，LeanFinger 也提供了非常多的已计算的 touch 数据，因此在遇到一个特定场景或者需要特定 touch 数据时，先查看 LeanTouch 是否已经提供了。

## Use Lean Touch without code

Lean Touch 为绝大多数场景 touch input 场景提供了 component，可以直接使用，而不需要自己再编写。

例如 LeanSpawn 组件可以在场景中通过 touch 生成一个 prefab。联合 LeanFingerTap 组件一起使用。在组件中的 OnFinger 事件字段中选择 LeanSpawn 组件的 LeanSpawn > Dynamic LeanFinger > Spawn 函数。

还有很多其他组件使用相似的方式使用：先添加一个用于 Input 的 Lean 组件，其中包含很多 event；再添加用于具体任务的 lean 组件；最后在 Lean Input 组件的事件中选择任务组件的函数。

## Use Lean Touch with code

你可以从 Lean.Touch.LeanTouch 类中访问全部的 finger data。

最简单的开始方式是访问它暴露的 static events。

例如，如果你想在 finger touch screen 时执行一个动作，可以 hook Lean.Touch.LeanTouch.OnFingerDown 事件。这个事件在每次一个 finger 开始 touch screen 时被调用，并被传递一个 Lean.Touch.LeanFinger 实例作为参数。建议在 OnEnable 中 hook 这些事件，在 OnDisable unhook 它们。

```C#
public class MyCoolScript : MonoBehaviour
{
	void OnEnable()
	{
		Lean.Touch.LeanTouch.OnFingerTap += HandleFingerTap;
	}

	void OnDisable()
	{
		Lean.Touch.LeanTouch.OnFingerTap -= HandleFingerTap;
	}

	void HandleFingerTap(Lean.Touch.LeanFinger finger)
	{
		Debug.Log("You just tapped the screen with finger " + finger.Index + " at " + finger.ScreenPosition);
	}
}
```

另一种访问 finger data 的方法是从 Lean.Touch.LeanTouch.Fingers static list 中直接轮询。这个列表存储当前 touch screen 的所有 fingers，你可以在任何时间使用这些 data（例如在 Update 中），来快速处理输入。

```C#
public class MyCoolScript : MonoBehaviour
{
	void Update()
	{
		var fingers = Lean.Touch.LeanTouch.Fingers;

		Debug.Log("There are currently " + fingers.Count + " fingers touching the screen.");
	}
}
```

如果你需要修改或排除特定 fingers，强烈建议使用 Lean.Touch.LeanTouch.GetFingers(...) 方法，它包含常见的 filter 选项，并返回一个临时列表，你可以进一步过滤而不需要 breaking LeanTouch。

## 如何处理 multi-finger gestures（例如 Pinch，Twist）

Lean.Touch.LeanGesture 类使得这个任务非常容易。

例如，如果你想找出在最近一帧 fingers twisted 多少角度，可以调用：

```C#
Lean.Touch.LeanGesture.GetTwistDegrees()
```

这个方法自动从所有 fingers 中计算。这个方法还有一个重载方法，可以传递一个特定 fingers 列表，如果你不想使用所有 fingers。

## 为什么 Input 延迟了一帧

LeanTouch 组件和其他 Lean Components 在 Update 方法中运行。如果你使用同样使用 Update 的组件，则可能出现一个场景，你的组件在使用旧的 input data（Lean Touch 组件稍后 Update），而所有事情都延迟了一个 frame。要修复这个问题，必须手动调整这些组件的 Script Execution Order，使得 Lean 组件在你的组件之前执行，或使你组件稍后执行。

- Step 1 Go to Edit > Project Settings > Script Execution Order.
- Step 2 Below the Default Time box, click the + button, and select a component like Lean.Touch.LeanTouch.
- Step 3 Change the execution order value. To make it execute before most components then set it below the Default Time (e.g. -100), or above (e.g. 100) to make it execute after.
- Step 4 Click Apply, and enjoy!

## 如何在 C# 中防止 touch 控制穿透 UI

如果你监听任何 Lean.Touch.LeanTouch.OnFingerXXX 事件，你将得到一个 Lean.Touch.LeanFinger 实例作为参数。这个 class 有 IsOverGui 和 StartedOverGui 选项可以选中。

```C#
public class MyCoolScript : MonoBehaviour
{
	void OnEnable()
	{
		Lean.Touch.LeanTouch.OnFingerTap += HandleFingerTap;
	}

	void OnDisable()
	{
		Lean.Touch.LeanTouch.OnFingerTap -= HandleFingerTap;
	}

	void HandleFingerTap(Lean.Touch.LeanFinger finger)
	{
		if (finger.IsOverGui)
		{
			Debug.Log("You just tapped the screen on top of the GUI!");
		}
	}
}
```

如果你从 Lean.Touch.LeanTouch.Fingers polling，并且想快速移除一些 touching GUI 的 fingers，你可以使用 Lean.Touch.LeanTouch.GetFingers 方法，它具有一个设置可以快速排除一些 fingers，以及限制它到一个特定数量的 fingers。

## 命名空间

所有 Lean Touch 类都放在 Lean.Touch 命名空间。

## 什么是 Lean Touch+

Lean Touch+ 提供了大量组件，可以解决绝大多数常见 touch 场景，几乎都是由 users 请求的，可以节约你的大量时间。

## Screen Depth inspector setting 如何工作

Fingers touch 只有一个 screen 2D XY 坐标，但很多交互需要计算一个 3D XYZ 点（例如 LeanCameraDrag）。Inspector setting 处理这种转换，并且足够灵活以支持 2D games，3D games，透视 2D games，以及更多。

Screen Depth 在 LeanFingerXXX 组件的 events section。Lean Touch 组件提供了一组基于 2D 屏幕空间坐标的事件，还提供一组基于 3D 世界空间坐标的事件。Screen Depth 只用于 3D 坐标事件。它用于这个组件的所有 3D 坐标事件。它指定一个计算方法，一个 camera，一个 Z 值。

计算方法：

- Fixed Distance

  这个设置在 finger 位置上，当前 camera 的前面计算一个 position，Distance setting 是 world space 中这个 point 从 camera 离开的距离。这个设置适合的场景是，你的前景 object 应该总是出现在到 camera 的相同距离，即使你的 camera 可以移动或者旋转。

- Depth Intercept

  这个 setting 在 finger 位置上，当前 camera 前面计算一个 ray，并且发现这个 ray 和指定 Z position 的 XY 平面的交点。这个设置适合于正常的 2D games。如果你使用 标准2D 设置，则 Z 值应该为 0，但这个可以为指定场景进行调整，因为在 Unity 中 2D sprites 可以被放置在任何 Z 位置并仍然可以工作。

- Physics Raycast

  类似 Depth Intercept，但是发现这个 ray hit 到 physics scene 的点。这个设置适合 3D 游戏，你需要在一个 object 上生成一些东西等等

- Plane Intercept

  类似 Depth Intercept，但是允许你指定一个自定义的 plane，通过 LeanPlane 组件，它可以朝向任何方向，并且可选地允许你约束或者 snap 最终的 values。

- Path Closest

  类似 Depth Intercept，但是它发现沿着指定 LeanPath 到 screen point 的最近的点。

- Auto Distance

  似于 Fixed Distance，但是 Distance 会基于当前 GameObject 的 depth 自动计算。这个设置适用的场景是，你场景中的 object 可以出现在到 camera 的任意距离上。

- Height Intercept

  类似 Depth Intercept，但是射线将和 XZ 平面相交。这个设置适合于 3D top-down 场景，playing field 是平的。

LeanTouch finger 总是得到一个 2D screen 坐标，但是会自动计算 3D world 中的一个位置，免去手动计算的工作，Depth inspector 设置就是用于指定如何从 finger screen position 计算 world 位置。

## 为什么必须 link 这么多组件

LeanTouch 中有两个主要的组件类型：self-contained components，和 separated components。

Self-contained component 的一个例子是 LeanTranslate。这个组件包含代码检测你想使用哪些 fingers 用于 translation，并且拥有代码来处理 finger data，并将它们转换为一个 translation movement。

Separated component 的一个例子是 LeanFingerTap 和 LeanSpawn。这些组件必须连接到一起工作。LeanFingerTap 检测何时一个 finger taps 到 screen 上，并且在 Editor 中，你必须连接 OnWorldTo event 到 LeanSpawn.Spawn method。两个组件各自负责独立的事情，前者检测 touch 事件，LeanSpawn 提供 spawn gameobject 的方法，可以被任何 Unity Event 连接，而 LeanFingerTap 提供了 Unity Event。

在早期 LeanTouch 版本，绝大多数组件都是 self-contained 组件，就像 LeanTranslate。这允许开发者快速添加 touch controls 到游戏中，但是这使得它非常难以自定义 controls。为了使 LeanTouch 更灵活，几乎所有新功能都使用 separated component system。

## 为什么所有的 objects 同时移动

绝大多数 LeanTouch components 被设计为在自身上工作，或者在 selection 上工作。如果你有很多 objects 设置为在自身上工作，则当 touching screen 时，将导致它们同时移动。

要修复这个问题，你需要使你的 objects 工作在 selection 上。为此，只需要添加 LeanSelectable 组件到每一个 objects 上。你会注意到每个 LeanTouch 组件带有一个 RequiredSelectable 设置，这个设置可以被用于关闭当前组件，如果指定的 specified selectable 没有被选中的话。你可以拖放之前添加的 LeanSelectable 组件到这些 fields 中。

一旦完成，你需要告诉 LeanTouch 你想如何选择你的 objects。最简单的方式是添加 LeanFingerTap 和 LeanSelect 组件到你的 scene 中。然后你可以连接 LeanFingerTap.OnFinger 事件到 LeanSelect.SelectScreenPosition 函数。默认地，LeanSelect 组件被设计为选择 2D objects，如果你想选择 3D objects 则改变 Select Using 设置为 Raycast 3D。

## Link

http://carloswilkes.com/Documentation/LeanTouch

http://carloswilkes.com/Documentation/LeanTouchPlus