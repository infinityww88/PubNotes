# EditorWindow

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

