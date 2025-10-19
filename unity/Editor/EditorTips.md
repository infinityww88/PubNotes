# Tips

可以绘制的地方

- Inspector
- Scene
- EditorWindow

可以绘制的东西

- Hierarchy 中的 GameObject
- Project 中的 asset

---

脚本或者是 MonoBehavior 或者是 ScriptableObject，前者挂载到 GameObject 上，后者挂载到 Asset 上。无论是 GameObject 还是 Asset，它们被选中时，Inspector 都会显示它们的 Inspector Editor（内置或自定义的 editor）。

EditorWindow 不关联任何 GameObject 和 ScriptableObject，它没有 target object。它不绘制 Inspector，只在自己的 window 中绘制。

对 SceneView 的绘制，任何 Editor 脚本都可以绘制，方法是订阅 SceneView.duringSceneGui。通常在 OnEnable 订阅，在 OnDisable 解除订阅。

InspectorGUI 中的 OnSceneView 应该是过时的，但是为了向后兼容遗留的消息函数，在 EditorWindow 或 Editor 中都应该使用 SceneView.duringSceneGui，它才是绘制 Scene View 的标准方法。

Inspector 的 OnSceneView 只对 MonoBehavior 有效，对 ScriptableObject 无效。
ScriptableObject 应该在 OnEnable 和 OnDisable 中注册和反注册 SceneView.duringSceneGui

---

自定义绘制3个 class：

- EditorWindow：绘制单独的窗口，可以绘制任何东西，和任何 GameObject/Component 无关
- Editor：自定义一个组件 MonoBehavior 在 Inspector 中的显式
- Property Drawers：自定义某个属性修饰的类型的字段在 Inspector 和 EditorWindow 中的显示
- TreeView：TreeView 是一个 IMGUI 控件，用于显示层次化数据，你可以展开或收拢它。使用 TreeView 为 Editor Windows 创建高度可定制的 list views，和多列 tables，你可以和其他 IMGUI 控件和组件一起使用

通常很少需要 TreeView 和 Property Drawer。只需要为 MonoBehavior 定制 Inspector Editor 和 绘制通用的 EditorWindow。Odin 属性可以同时应用于二者。

---

Handles.PositionHandle 绘制 3 轴 Position handle

Handles.BeginGUI、Handles.EdnGUI 在 Scene 中绘制 IMGUI

OdinEditor : Editor

使用 Odin 属性，可以直接在 MonoBehavior 或 ScriptObject 中标记字段，定制 Editor。但是如果需要在 Scene 中绘制，应该自定义 Editor 脚本，注册 SceneView.duringSceneGui。但是为了使自定义 Editor 和 Odin 属性一起使用，应该继承 OdinEditor。Odin 为 Editor 和 EditorWindow 提供了可以和属性一起使用的 Odin 子类，OdinEditor 和 OdinEditorWindow。

Handles 主要用于绘制 Scene 中常用的 handle，而不是通用的图形。为此应该使用 GL 或 Graphics。

Handles.CircleHandleCap(0, info.point, Quaternion.identity, 1f, EventType.Repaint);


controlId 通常用于 IMGUI 的交互式控件，controlId = 0 是为非交互绘制保留的 control id

EventType.Repaint 事件中绘制组件

---

IMGUI 通过全局变量 GUI.changed 传递 GUI 状态是否发生变化的通知。EditorGUI.BeginChangeCheck() 和 EndChangeCheck() 用于 stack GUI.changed，使得它可以用于局部通知 GUI 状态变化。

```C#
EditorGUILayout.LabelField("New value", labelText);

// Start a code block to check for GUI changes
// 将 GUI.changed 压到 stack 中，并重置为 false
EditorGUI.BeginChangeCheck();

sliderValue = EditorGUILayout.Slider(sliderValue, 0, 1);

// End the code block and update the label if a change occurred
// 将 GUI.changed 弹出到 GUI.changed，并返回之前的 GUI.changed
// 可以用于任何使用 GUI.changed 的地方
if (EditorGUI.EndChangeCheck())
{
    labelText = sliderValue.ToString();
}

```

---

自定义编辑器处理状态变化有3个需要考虑的地方：

- Undo system

  Undo.RecordObject(SceneManagement.Scene scene)

- Scene 中 GameObjects 有变化时，标记 Scene Dirty mask

  是指 GameObjects 上的组件由数据被更新，但是还只停留在内存中，没有保存到 Scene 的 disk 文件中。如果此时关闭或切换 Scene，Unity 会提示是否保存当前 scene，即将 GameObjects 的 change 保存到 disk scene 文件中。Scene 可以视为一个特殊的 Prefab（下面保存一组预置的 GameObjects）。因此对 Scene dirty 的处理，可以视为是下面 Prefab overrides 的一种特殊情况。

  EditorUtility.SetDirty(Object target)

  EditorSceneManager.MarkSceneDirty

- 正确地处理绘制到 Inspector 上的 Prefab overrides style

  类似 Scene dirty

  PrefabUtility

标记 Scene dirty（有所变化），Undo/Redo 系统，Prefab Overrides style 是3个独立的机制，但是对于自定义编辑器通常都需要处理它们，因此，就像任何其他地方一样，Unity 为这些常用的功能提供了一个便捷类 SerializedObject/SerializedProperty。它本质上时提供一组复用的 code，它们自身没有数据，需要手动为它指定一个要保证的 object 和 操作的属性的路径。然后只需要 SerializedObject 上的方法，就可以处理状态发生变化时所有 Editor 需要的事情。因此如果没有特殊需求，不应该手动依次处理 Undo，Scene Dirty，Prefab overrides，而是只使用高级的 SerializedObject。

Scene Dirty 只应用于场景中的 GameObjects，而不能应用于 Project 中的 asset，对 asset 的修改是立即更新大 disk 的文件中的，即使是在运行时，因此不需要这个功能。

SerializedObject.Update = set serialized object stream now based on what is in the actual class，保证 SerializedObject 当前是最新的状态。

SerializedObject.ApplyModifiedProperties = take what is in the object stream and put it in the class，只是将修改应用到 target object 的内存中（SerializedObject 内部是将对象序列化为字节数组的），如果是 Scene 中的 GameObject，这将导致 Scene 为 dirty 的，因为内存中的 scene 有更新，和 disk 文件不一致，需要保存。

**简而言之，自定义 Editor 需要考虑两个地方：Undo 和 保存（Scene 或 Prefab，是否将内存中的修改保存到磁盘文件中）**

---

```C#
public static GUIContent BeginProperty(Rect totalPosition, GUIContent label, SerializedProperty property);

public static void EndProperty();
```

创建一个 Propertry wrapper，使正常 GUI 控件可以和 SerializedProperty 一起工作。

绝大多数 EditorGUI 和 EditorGUILayout GUI 控件已经重载，可以和 SerializedProperty 一起工作。然而，对于不能处理 SerializedProperty 的 GUI 控件（例如自定义控件），你可以将它们包装在 BeginProperty 和 EndProperty 之中。

BeginProperty 和 EndProperty 主要自动处理 default labels，bold font for Prefab overrides，revert to Prefab right click menu，并且在 multi-object 编辑时如果 property 的 values 不同，设置 showMixedValue。

```C#
EditorGUI.BeginChangeCheck();
var newValue = EditorGUI.Slider(position, label, property.floatValue, leftValue, rightValue);
// Only assign the value back if it was actually changed by the user.
// Otherwise a single value will be assigned to all objects when multi-object editing,
// even when the user didn't touch the control.
if (EditorGUI.EndChangeCheck())
{
    property.floatValue = newValue;
}
```

IMGUI 中所有的 Begin/End 代码块，都是在向 stack 入栈和出栈什么东西，以创建一个运行时局部的作用域。

---

Editor

- OnInspectorGUI：绘制 InspectorGUI
- OnPreviewGUI：绘制 preview 窗口
- OnSceneGUI：绘制 SceneView

EditorWindow

- OnGUI
- OnSelectionChange

Selection

- activeGameObject
- activeInstanceId
- activeObject
- activeTransform
- gameObjects
- instanceIds
- objects
- selectionChanged：delegate callback

## 