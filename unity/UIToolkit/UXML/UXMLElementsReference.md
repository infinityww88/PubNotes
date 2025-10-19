# UXML elements reference

UnityEngine.UIElements 和 UnityEditor.UIElements namespace 中的 UXML 元素。

## Base elements

- VisualElement

  所有 visual elements 的基类。

  可以包含任意数量的 VisualElement。

  属性：
  - class：space 分割的 style class 名字
  - style：inline style
  - name：标识这个元素的唯一名字
  - picking-mode：是否响应鼠标事件，Position 或 Ignore，默认 Position
  - tooltip
  - focusable
  - tabindex
  - view-data-key：用于元素序列化的 key

  这个元素还接受任何其他属性，但默认忽略，只是传递给元素 init 构造器，由自定义控件解释

- BindableElement

  可以绑定到一个 SerializedProperty 的元素，处理编辑器的 dirty flags 和Undo history 支持。

  可以包含任意数量的 VisualElement。

  属性：

  - binding-path：元素绑定到的 property 路径

## Utilities

- Box

  类似 VisualElement，但是在 content 周围绘制一个 box

- TextElement
- Label
- Image
- IMGUIContainer

  绘制 IMGUI 内容

- Foldout

  具有一个 toggle button 来显示或隐藏它的内容

  包含所有 BindableElement 的属性

## Templates

- Template

  引用另一个 UXML template，可以使用 Instance 来实例化

- Instance

  Tempalte 的 Instance

- TempateContainer

  Template container

## Controls

- BaseField\<T>

  所有 fields（字段）的抽象基类

  - BindableElement 的属性
  - focusable = true
  - label：关联到 field 的 text label

- Button

  标准的 push button

- Repeat Button

  当按下时重复执行 action 的 button。

  - delay：button 开始执行 action 之前的初始 delay，milliseconds
  - interval：开始执行 action 之后重复 action 的间隔，默认 0

- Toggle

  显示为 checkbox 的 toggle button

- Scroller

  scroll bar

  - low-value
  - high-value
  - direciton：Horizontal or Vertical，默认 Vertical
  - value：scroller cursor 的 position

- Slider

  slider for float

  - low-value
  - high-value
  - direction
  - page-size

- SliderInt

  slider for int

- MinMaxSlider

  user 指定 min 和 max value 的 slider

  - low-limit
  - high-limit
  - min-value
  - max-value

- EnumField

  获得下层 Enum 的 string

  - type：使用的底层 Enum 的 C# 类型，string。如果 type 在一个 user assembly，在 assembly name 必须添加到 type name，例如 MyNamespace.MyEnum
  - value

- MaskField

  popup menu，user 可以选择一个 32-bit mask

  - choices：一个逗号分隔的列表，最多 32 个选择
  - value：一个 int，表示 32-bit mask

- LayerField

  popup menu，选择一个 layer

  - value：int，layer mask

- LayerMaskField

  选择一组 layer，通过 layer mask

- TagField

  popup menu，选择一个 tag

  - value

- ProgressBar

  显式一个操作的进度条

  - low-value：float，default = 0
  - high-value：default = 100
  - title：progress bar 的 title

## Text input

- TextInputBaseField\<TValueType>

  所有 text fields 的基类

  - text：field 的 text value
  - max-length：最大字符长度，默认=-1，无限制
  - password：bool，是否显示 maskCharacter
  - mask-character
  - readonly：bool = false

- TextField

  可编辑 text field

  - multipline：bool

- IntegerField
- LongField
- FloatField
- DoubleField
- Vector2Field
- Vector2IntField
- Vector3Field
- Vector3IntField
- Vector4Field
- RectField
- RectIntField
- BoundsField

  bounding box，6个分量

- BoundsIntField

## Complex widgets（UnityEditor）

- PropertyField

  一个 label 和一个 field 来编辑一个 value

  - binding-path：元素绑定到的 property path
  - label：field 的 label

- PropertyControl\<int/long/float/double/string>

  编辑一个 int/long/float/double/string type value

  - value-type：type string
  - value

- ColorField

  颜色 picker 字段

  - show-eye-droper：bool，是否显示一个 eye dropper
  - show-alpha：bool，是否显示 alpha control
  - hdr：bool，是否使用 high dynamic range color picker

- CurveField
- GradientField
- ObjectField
- InspectorElement

  在 Inspector window 显式属性的元素

## Toolbar

- Toobar

  保持 toolbar items 的容器

- ToobarButton

  toolbar 的 button

- ToolbarToggle

  toolbar 的 toggle

- ToolbarMenu

  dropdown menu for toolbar

- ToolbarSearchField

  search field for toolbar

- ToolbarPopupSearchField

  带有搜索框的 popup menu

- ToobarSpacer

  在 toolbar buttons 之间插入固定数量的空白

## Views and windows

- ListView

  elements 列表

  - item-height：每个 item 的像素高度

- ScrollView

  带有水平和垂直 scrollers 的 scrollable view

  - mode：scroll view 的模式，默认 ScrollViewMode.Vertical
  - show-horizontal-scroller：bool = false
  - show-vertical-scroller：bool = false
  - horizontal-page-size：horizontal scroller 的 page size value
  - vertical-page-size：vertical scroller 的 page size value

- TreeView

  elments 的 tree view
  
  - item-height：underlying list 的 item height

- PopupWindow

  一个 UIElements window，显示在其他 content 之上

