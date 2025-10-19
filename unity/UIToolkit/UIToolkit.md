# UI Toolkit

开发Editor 扩展，运行时调试工具，游戏和应用程序的运行时 UI。

UI Toolkit 是基于标准 web 技术。如果你有开发 web 的经验，你的很多知识都是可以应用的，很多核心概念都是相同的。

UI Toolkit 包含3部分：UI system，UI Assets，UI Tools and resources

## UI system

UI Toolkit 是一个 retained-mode UI 系统，基于标准 web 技术。它支持 stylesheets，dynamic 和 contextual 事件处理

UI system 包括以下功能：

- Visual tree：定义使用 UI Toolkit 构建的每个用户接口。一个 visual tree 是一个 object graph，由轻量 nodes 构成，它们保存一个 window 或 panel 中的所有元素
- Controls：一个标准 UI 控件库，包含 buttons，popups，list views，和 color pickers。你可以原样使用它们，定制它们，或者创建自己的控件
- Data binding system：连接属性到修改它们的控件
- Layout Engine：一个基于 CSS Flexbox 模型的布局系统。它基于 layout 和 styling 属性放置元素
- Event System：用户交互和元素之间的通信，例如 input，touch 和 pointer 交互，drag 和 drop 操作，以及其他事件类型。这个 system 包括一个 dispatcher，一个 handler，一个 synthesizer（合成器），一个事件类型的库
- UI Renderer：一个直接构建在 Unity Graphics device layer 上的渲染系统
- UI Toolkit Runtime Support（via the UI Toolkit package）：包含创建 runtime UI 必须的组件。UI Toolkit package 当前是 preview 状态

## UI Assets

- UXML documents：定义用户接口和可重用 UI 模板的 XML 语言。尽管可以通过 C# 脚本直接构建 UI，Unity 建议使用 UXML document
- Unity Style Sheets（USS）：Style sheets 允许你为 user interfaces 应用 visual styles 和 behaviors。它们类似 CSS，并支持标准 CSS 属性的一个子集。尽管你可以在 C# 中直接应用样式，Unity 建议使用 USS 文件

## UI Tools and resources

UI toolkit 还包含以下工具和资源帮助你来创建 UI。

- UI Debuger：类似 web 浏览器的 debugging view。使用它来浏览一个 elements 的层次结构，以及获得关于它下层 UXML 结构和 USS 样式的信息。
- UI Builder（package）：可视化创建 UXML 和 USS 文件的工具。
