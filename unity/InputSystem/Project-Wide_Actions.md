Input System 存储 Input Actions 的配置和它们关联的 Bindings Action Maps 和 Control Schemes 在一个 Action Asset 文件。

尽管可以在 project 中有超过一个 Action Asset，绝大多数项目只需要一个 Action Asset。这是因为 Action Asset 可以包含多个 Action Maps，每个 Map 包含一组相关的 actions（例如 UI，Gameplay 等）。

Action Asset 提供了 Shemes、Maps、Bindings 等，已经足够灵活了，几乎不需要多个 Action Asset，这也是为什么提供 project-wide actions。

Input System project-wide actions 允许你选择一个单独的 Action Asset 作为 project-wide 的配置，这意味着那个 asset 中的 actions 可以直接通过 Input System API 访问，而不需要设置对 asset 的引用（全局 Action Asset）。

Project-wide Action Asset 也是 preloaded asset，当 app 启动时有 unity 加载，并且在运行过程中保持有效，直到程序终止。

除非有特殊的项目需求需要一个以上的 Action Asset，建议的 workflow 是使用一个 Action Asset 作为 project-wide actions。

# Create and Asign a Project-Wide Actions Asset

Edit > Project Settings > Input System Package

# Default Actions

当创建并分配了 default project-wide actiosn 之后，Action Asset 带有一组内置的 default actions，例如 Move，Jump 等等，它们适合绝大多数的游戏场景。它们被配置从绝大多数常见的 Input Controller 类型读取输入，例如 Keyboard，Mouse，Gamepad，Touchscreen 和 XR。这意味着大多数情况下，可以通过引用 default actions 的名字直接使用 Input System scripting，而不需要任何配置。你可以重命名和重新配置 default actions，或者删除 default actions 来满足你的需求。

如果想删除所有 default actions，以便从一个空的配置开始，你无需手动挨个删除 actions。你可以删除整个 Action Map，这会删除它包含的所有 actions。

还可以删除所有 action maps，或者重置所有 action 回 default value（通过 Input Actions Editor 面板右上角的 more menu）。注意这个菜单在 Action Editor 中不会出现，因为这个 Editor 是编辑通用 Action Asset 的，没有重置的意义。这个菜单只会出现在 Project Settings 窗口。

# 在 code 中使用 project-wide actions

为 project-wide actions 指定一个 Action Asset 的好处，是可以通过 InputSystem.actions 直接访问 actions，而不需要设置对 actions 的引用：

```C#
InputSystem.actions.FindAction("Move")
```

Project-wide actions 默认开启。
