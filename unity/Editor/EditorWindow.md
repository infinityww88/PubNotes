# EditorWindow

EditorWindow 在 play mode 和 editor mode 之间切换时会隐式地序列化和反序列化，不触发 OpenWindow，OnBecameVisible 和 OnBecameInvisible，只是简单地序列化成员变量（包括私有的公有的，不需要标记 SerializeField），然后恢复。但是被序列化和恢复的类型不能引用 Scene 中的 GameObject 或 Component。因为 EditorWindow 是整个编辑器范围内有效的，很可能在 EditorWindow 打开时，Scene 被切换为其他的 Scene，那么它引用的 Scene 的 GameObject 或 Component 就没有意义了。因为 EditorWindow 的成员变量能持久化的只能是那些和 Scene 无关，只对整个编辑器 session 有效的变量，包括 ScriptableObject，基本类型变量（int，float，string），基本 Unity 类型（Quaternion，Vector2，Vector3）等等，引用的 Scene 中的 GameObject 或 Component 在隐式序列化、恢复时会被重置为 null。如果使用 OdinEditorWindow 也是一样，而且要注意，使用 OdinEditorWindow 时，尽管 EditorWindow 面板中的字段还仍然保持有效, 但是内存中 GameObject、Component 可能已被重置为 null。

EditorWindow 的 OnBecameVisible 和 OnBecameInVisible 事件在 EditorWindow 切换被切换到其他 Tab 而隐藏时就调用，而不是在 EditorWindow 打开和关闭时才调用。要接受打开、关闭窗口的消息，使用 Awake 和 OnDestroy。

## 静态属性

- focusedWindow 当前具有 keyboard 焦点的 EditorWindow，只读
- mouseOverWindow 当前在 mouse cursor 下面的 EditorWindow，只读

## 属性

- autoRepaintOnSceneChange，开启这个属性后，当 SceneView 被修改后，自动重绘 window
- docked，EditorWindow 是否 docked
- hasFocus，EditorWindow 是否具有焦点
- hasUnsavedChanges，在关闭 widnow 时，是否提示 user 保存或丢弃未保存的 chagnes
- maximized，EditorWindow 是否是最大化的
- maxSize/minSize：当 EditorWindow 时 floating 或 modal 时的最大化/最小化尺寸
- position，window 在 screen space 中的期望位置
- rootVisualElement，window 的 root VisualElement
- saveChangesMessage，提示 user 保存 change 的消息
- titleContent，EditorWindows 的 title
- wantsMouseEnterLeaveWindow/wantsMouseMove EditorWindow 是否想要接受 mouse，key 事件

## Public Methods

- BeginWindows() / EndWindows() IMGUI 绘制区域
- Close()
- Show()
- DiscardChanges()


## 消息

- Awake

  Called as the new window is opened.

- CreateGUI
  
  CreateGUI is called when the EditorWindow's rootVisualElement is ready to be populated.

- hasUnsavedChanges

  This property specifies whether the Editor prompts the user to save or discard unsaved changes before the window closes.

- OnBecameInvisible

  Called after the window is removed from a container view, or is no longer visible within a tabbed collection of EditorWindow.

- OnBecameVisible

  Called after the window is added to a container view.

- OnDestroy

  OnDestroy is called to close the EditorWindow window.

- OnFocus

  Called when the window gets keyboard focus.

- OnGUI

  Implement your own editor GUI here.

- OnHierarchyChange

  Handler for message that is sent when an object or group of objects in the hierarchy changes.

- OnInspectorUpdate

  OnInspectorUpdate is called at 10 frames per second to give the inspector a chance to update.

- OnLostFocus

  Called when the window loses keyboard focus.

- OnProjectChange

  Handler for message that is sent whenever the state of the project changes.

- OnSelectionChange

  Called whenever the selection has changed.

- saveChangesMessage

  The message that displays to the user if they are prompted to save.

- Update

  Called multiple times per second on all visible windows.

