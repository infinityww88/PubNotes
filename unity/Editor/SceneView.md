# SceneView

SceneView 是 EditorWindow 的子类。

其他 EditorWindow 想要在 SceneView 中嵌入 code：

- 通过 SceneView.sceneViews 访问当前打开的 SceneView 实例
- 注册 SceneView.beforeSceneGui/SceneView.duringSceneGui event，接受 SceneView 调用 OnGUI 的回调
- 通过 SceneView.rootVisualElement 添加 UIElements 到 SceneView 中

currentDrawingSceneView 只在 OnGUI 中可用，在其他的函数中不可用，只能通过 sceneViews 访问当前的 SceneView。

## 事件

SceneView 当前有两种方式操作，IMGUI 和 UIToolkit。

- IMGUI

  要访问事件，在 SceneView.OnGUI 中访问 Event.current.type

  ```C#
  if (Event.current.type == EventType.MouseDown && Event.current.button == 0) {
    Debug.Log("mouse down " + Event.current.mousePosition + ", " + Mouse.current.position.value);
  }
  ```

- UIToolkit

  通过 rootVisualElement 像普通的 UI Elements 一样 RegisterCallback 即可

### 鼠标位置

访问鼠标位置，既可以通过 Event.current.mousePosition，也可以通过 InputSystem.Mouse.position.value。但是同一个鼠标位置在不同的 UI panel 中有不同的坐标，必须要注意让鼠标位置是相对于当前要操作的 panel 的。使用 IMGUI 方式（直接访问 Event.current），只能在 MouseDown event 中才能得到正确的坐标，否则返回的是全局的坐标。使用 InputSystem.Mouse 也是一样，两者总会返回相同坐标，使用哪个都可以。

如果不是在 MouseEvent 中访问鼠标坐标，就需要自己将鼠标坐标转化为当前相对于 EditorWindow/SceneView 的坐标。IMGUI 当前还不清楚有和转换方式，UIToolkit 通过 WorldToLocal 直接转换 Mouse.current.position.value 即可：

```C#
void OnKeyDown(KeyDownEvent evt) {
//Debug.Log("Scene View KeyDown " + evt.keyCode + $" {evt.originalMousePosition} {Mouse.current.position.value}");
// evt.originalMousePosition == Mouse.current.position.value
VisualElement ve = evt.currentTarget as VisualElement;
Vector2 p = Mouse.current.position.value;
p = ve.WorldToLocal(p);

Ray ray = HandleUtility.GUIPointToWorldRay(p);
Debug.Log($"{ray.origin} {ray.direction}");

Vector2 pos = ray.origin;
var o = GameObject.CreatePrimitive(PrimitiveType.Cube);
o.transform.position = pos;
}
```

- public Vector2 originalMousePosition

  The original mouse position of the IMGUI event, before it is transformed to the current target local coordinates.

转换后，HandleUtility.GUIPointToWorldRay(p) 可以将 GUI 坐标转化为 world ray，就可以与 3D world 交互了。

Input.mousePosition 不能用于 Editor，只能用于 Runtime。


## 静态属性

- currentDrawingSceneView，当前绘制的 SceneView，只有在 SceneView OnGUI 中有效
- lastActiveSceneView
- lastActiveSceneViewChanged
- sceneViews
 
使用 UIToolkit 向 SceneView 中添加 UIElements，要使用 Absolute position。可能是 IMGUI container 本身就使用 Absolute overlay 到 SceneView 中，使用 Relative position 添加的 UIElements 不可见。

