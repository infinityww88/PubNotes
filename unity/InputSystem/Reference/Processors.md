# Processors

Input Processor 使用一个 value，返回一个 processed 结果，二者必须是相同类型的。例如可以使用一个 clamp Processor clamp 一个 control value 到一个特定 range。

Composite Bindings 将 input values 转换成不同的类型。

## Using Processors

可以在 Bindings，Actions，或者 Controls 上安装 Processors。

### Processors on Bindings

为 actions 创建 Bindings 时可以为其添加 Processors。在 Input value 应用到 Action 之前处理它。

在 Input Action Assets 中，可以在 Input Action editor 中添加/移除 Processor 到 Binding。

在 code 中添加 Processors：

```C#
var action = new InputAction();
action.AddBinding("<Gamepad>/leftStick")
    .WithProcessor("invertVector2(invertX=false)");
```

### Processors on Actions

影响 Action 上的所有绑定的 Controls，而不是指定 Binding。

```C#
var action = new InputAction(processors: "invertVector2(invertX=false)");
```

### Processors on Controls

处理 InputControl 上的 value。

ReadValue，ReadUnprocessedValue

## Predefined Processors

Input System 提供了一组有用的 Processors。

- Axis deadzone

  指定一个 float min，max。

  缩放一个 Control 的 value 使得任何绝对值小于 min 的 value 为 0，任何绝对值大于 max 的 value 为 -1 或 1.

  很多 Controls 没有一个精确的 resting point（静止点）（即当 Control 位于中心复位时，不总是报告 0）。使用 deadzone Processor 的 min value 避免非期望的 value。同样，一些 Control 在沿着 axis 移动到最大时，不总是返回最大值，使用 max 来避免这个问题。

- Clamp

  将 Input value 限制到 min...max 范围。

- Invert

multiple value by -1

- Invert Vector2/Vector3

  * -1

  bool invertX, invertY, invertZ

- Normalize

  如果 min >= 0, 将 [min, max] 映射到 [0, 1]

  如果 min < 0, 将 [min, max] 映射到 [-1, 1]

- Normalize Vector2

  Vector2.normalized

- Normalize Vector3

  Vector3.normalized

- Scale

  Scale input value

- Scale Vector2/Vector3

  scaleX, scaleY, scaleZ

- Stick deadzone

  Vector2 的 deadzone。如果 magnitude < min，magnitude = 0；如果 magnitude > max，magnitude = 1

## Write custom Processors

编写自定义 Processors

```C#
public class MyValueShiftProcessor : InputProcessor<float>
{
    [Tooltip("Number to add to incoming values.")]
    public float valueShift = 0;

    public override float Process(float value, InputControl control)
    {
        return value + valueShift;
    }
}
```

注册 Processors

```C#
#if UNITY_EDITOR
[InitializeOnLoad]
#endif
public class MyValueShiftProcessor : InputProcessor<float>
{
    #if UNITY_EDITOR
    static MyValueShiftProcessor()
    {
        Initialize();
    }
    #endif

    [RuntimeInitializeOnLoadMethod]
    static void Initialize()
    {
        InputSystem.RegisterProcessor<MyValueShiftProcessor>();
    }

    //...
}
```

现在 Processor 可以在 Input Action Asset Editor 中以及 code 中使用：

```C#
var action = new InputAction(processors: "myvalueshift(valueShift=2.3)");
```

自定义 Processor 的 UI

```C#
// No registration is necessary for an InputParameterEditor.
// The system will automatically find subclasses based on the
// <..> type parameter.
#if UNITY_EDITOR
public class MyValueShiftProcessorEditor : InputParameterEditor<MyValueShiftProcessor>
{
    private GUIContent m_SliderLabel = new GUIContent("Shift By");

    public override void OnEnable()
    {
        // Put initialization code here. Use 'target' to refer
        // to the instance of MyValueShiftProcessor that is being
        // edited.
    }

    public override void OnGUI()
    {
        // Define your custom UI here using EditorGUILayout.
        target.valueShift = EditorGUILayout.Slider(m_SliderLabel,
            target.valueShift, 0, 10);
    }
}
#endif
```