# USS Properties types

## Built-in vs Custom Properties

使用 USS 时，你可以在 UI code 中为内置 VisualElement 属性或自定义属性指定 value。

除了从 USS 文件中读取它们的 values，built-in property values 还可以在 C# 中被赋值，通过 VisualElement 的 C# 属性。

在 C# 中赋值的 Value 覆盖来自 USS 中的 value。

你可以使用 custom properties 扩展 USS。Custom USS Properties 需要 -- prefix。

## Property values

- Length

  pixels(px), percentages(%)

  px 是绝对像素长度，percentages 是相对于 parent 的相对长度

  默认 px（即不指定单位）

- Numeric

  浮点数，或整数字面量，例如 flex:1.0

- Keywords

  一些内置 properties 支持特殊的 keywords。Keywords 提供一个描述性名字而不是数值

  position: absolute

  所有属性支持一个 initial global 关键字，它重置一个属性到它的默认值

- Color

  - 十六进制：#FFFF00, #0F0
  - RGB 函数：rgb(255, 255, 0)
  - RGBA 函数：rgba（255, 255, 0, 1.0)
  - 关键字：blue，transparent

- Assets

  你可以使用 resource() 或 url() 函数应用 Assets。

  background-image: resource("Image/img.png") 来指定 img.png 作为一个 background 图像

  resource() 函数接受一个位于 Resources 或 Editor Default Resources 目录下的文件：

  - 如果文件位于 Resources 目录，不要包含文件扩展名
  - 如果文件位于 Editor Default Resources 目录，必须包含文件扩展名

  此外，当加载纹理时，resources() 提供了一个便捷的方法来处理 High DPI/Retina Screen。如果一个 Texture 在同一个目录下具有相同的文件名以及一个 @2x suffix 版本，Unity 依据 screen DPI 自动加载。

  url() 函数预期 file 路径相对于 project root 或者包含 USS 文件的 folder。

- Strings
  
  --my-property: "foo"