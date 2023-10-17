# Input

混合使用 UIToolkit 和 UGUI 时，通过 UIDocument 和 Canvas 的 Sort Order 控制谁在上，谁在下。上面的 UI 会遮蔽下面的 UI 的事件。

使用 UGUI 需要在场景中添加 EventSystem 才能工作。如果还使用 InputSystem，EventSystem 组件上会提示需要将 Standard Input Module 转换为 InputSystem 兼容模式，否则会出现非预期的行为。

