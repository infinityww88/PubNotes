# Styles and Unity style sheets

每个 VisualElement 包含 style 属性，设置元素的 visual aspect。

Style 属性或者在 C# 中设置，或者在 style sheet 中设置。Style properties 在它们自己的数据结构（IStyle）中 regroup。

UI Toolkit 支持在 USS 中编写 style sheets，取自 CSS。

USS 格式和 CSS 相似，但是可以更好地在 Unity 中工作。

## Definition of a Unity style sheet

- 一个 USS 文本文件，被识别为 asset，必须具有 .uss 扩展
- 一个 USS 只支持 style rules
- 一个 style rule 由一个 selector 和一个 declaration block 组成
- selector 指示 style rule 影响的 visual elements
- declaration block，由花括号包围，包含一个或多个 style 声明。每个 style 声明有一个 property 和一个 value 组成，由一个分号结尾
- 每个 style 属性是一个字面量，匹配 target property name

```css
selector {
  property1: value;
  property2: value;
}
```

## Attaching USS to visual elements

Style rules 应用到 visual element 和它所有的 descendants。Style sheets 在必要的时候还可以自动重新应用。

使用标准 Unity APIs 例如 AssetDatabase.Load(), Resources.Load() 加载 StyleSheet objects。使用 VisualElement.styleSheets.Add() 方法附加 style sheets 到 visual elements。

如果在 EditorWindow 运行时修改 USS 文件，style 改变立即应用。

style 的应用过程对使用 UI Toolkit 的开发者时透明的。Style sheets 在必要的是哦户重新应用。

## Style matching with rules

一旦定义了一个 style sheet，它可以应用到 visual elements tree。

在这个过程中，selectors 和元素进行匹配以解析应用 USS 文件中的哪些属性。如果一个 selector 匹配一个元素，style 声明应用到这个元素。

## VisualElement matching

UI Toolkit 使用以下条件来匹配一个 visual element：

- 它的 C# class name（总是最末端的派生类）
- name 属性，string
- class list
- 祖先和 VisualElement 的 position

这些 traits 可以用在 style sheet 中的 selectors。
