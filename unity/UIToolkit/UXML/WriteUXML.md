# Writing UXML Templates

```XML
<?xml version="1.0" encoding="utf-8"?>
<UXML
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="UnityEngine.UIElements"
    xsi:noNamespaceSchemaLocation="../UIElementsSchema/UIElements.xsd"
    xsi:schemaLocation="UnityEngine.UIElements ../UIElementsSchema/UnityEngine.UIElements.xsd">

    <Label text="Select something to remove from your suitcase:"/>
    <Box>
        <Toggle name="boots" label="Boots" value="false" />
        <Toggle name="helmet" label="Helmet" value="false" />
        <Toggle name="cloak" label="Cloak of invisibility" value="false"/>
    </Box>
    <Box>
        <Button name="cancel" text="Cancel" />
        <Button name="ok" text="OK" />
    </Box>
</UXML>
```

第一行是 XML 声明；声明是可选的；如果包含声明，它必须在第一行，并且前面没有其他内容或任何空白；version 属性是必须的；encoding 属性是可选的；如果包含 encoding，它必须声明文件的编码。

<UXML> 元素包含 namespace prefix 定义 以及指定 schema 定义文件的位置。

UIToolkit 中，每个元素定义在 UnityEngine.UIElements 或 UnityEditor.UIElements namespace 中；

- UnityEngine.UIElements namespace 包含可以用于 Unity Runtime 中的元素
- UnityEditor.UIElements namespace 包含可以用于 Unity Editor 中的元素

要指定一个元素，必须包含它的 namespace 前缀。例如，如果想使用 Button 元素，必须指定 <UnityEngine.UIElements:Button />

为了使指定 namespace 更容易，可以定义一个 namespace prefix。例如 xmlns:engine = "UnityEngine.UIElements" 定义 engine prefix 为 UnityEngine.UIElements。一旦定义了一个 namespace prefix，你可以用它指定 namespace，<engine:Button /> 和 <UnityEngine.UIElements:Button /> 是等价的。

还可以定义一个默认的 namespace：xmlns="UnityEngine.UIElements" 定义 UnityEngine.UIElements 为默认 namespace，\<Button /> 等价于 \<UnityEngine.UIElements:Button />

如果定义自己的 elements，这些元素可能定义在自己的 namespace（程序集，例如 UnityEngine，UnityEditor）。如果要在 UXML 中使用这些元素，必须在 UXML tag 中包含 namespace 定义并指定 schema 文件位置，就像 Unity namespaces 一样。

通过 Asset > Create > UI Toolkit > Editor Window 创建的 UXML 模板，自动定义 namespace。

UI 定义是 <UXML> root 元素内部嵌套的一系列 XML 元素，每个代表一个 VisualElement。

每个元素名字对应一个要实例化的元素的 C# class name。绝大多数元素拥有属性，它们的 value 被映射到相应的 C# 对象属性。每个元素从 parent class 类型继承属性，还可以添加自己定义的属性。VisualElement 是所有元素的基类，提供以下属性：

- name：element 的 identifier，应该是唯一的，用于查询，等价于 HTML 中标签的 id 属性
- picking-mode：设置 position 来响应 mouse events，或者 ignore 来忽略 mouse events
- focus-index：过时 OBSOLETE，使用 tabIndex 和 focusable
- tabindex：int，定义当前元素的 tabbing position，可以通过 tab 切换焦点
- focusable：bool，指示元素是否可以拥有焦点
- class：空白分割的 style class 列表。使用 classes 为 elements 赋予 visual styles。还可以使用 class 在 UQuery 中选择元素集合
- tooltip：string，当鼠标移动到元素上时显示的 tooltip
- view-data-key：string，元素序列化使用的 key

使用 style 为元素添加 visual aspect，例如 dimensions，fonts，colors。

## Adding styles to UXML

在任何元素声明下面使用 \<Style> 元素引用一个 stylesheet 文件。

```XML
<engine:UXML ...>
    <engine:VisualElement class="root">
        <Style src="styles.uss" />
    </engine:VisualElement>
</engine:UXML>
```

```css
#root {
    width: 200px;
    height: 200px;
    background-color: red;
}
```

Unity 不支持在 root \<UXML> 元素下面的 \<Style>

还可以直接在 UXML 元素中声明内联 styles。

```XML
<engine:UXML ...>
    <engine:VisualElement style="width: 200px; height: 200px; background-color: red;" />
</engine:UXML>
```

## Reusing UXML 文件

在一个 UXML 文件中定义，在另一个 UXML 中使用 \<Template> 和 \<Instance> 元素 import 它，来创建一个组件。

当定义很大的 user interface 时，你可以创建 template UXML 文件，来定义 UI 的一部分。

可以在很多地方使用相同的 UI 定义。类似 UXML 的 prefab。

例如一个包含一个 image，name，lable 的 portrait UI 元素

```XML
<engine:UXML ...>
    <engine:VisualElement class="portrait">
        <engine:Image name="portaitImage" style="--unity-image: url(\"a.png\")"/>
        <engine:Label name="nameLabel" text="Name"/>
        <engine:Label name="levelLabel" text="42"/>
    </engine:VisualElement>
</engine:UXML>
```

你可以嵌套 Portrait 组件到另一个 UXML 模板中：

```XML
<engine:UXML ...>
    <engine:Template src="/Assets/Portrait.uxml" name="Portrait"/> <!--声明模板-->
    <engine:VisualElement name="players">
        <engine:Instance template="Portrait" name="player1"/> <!--生成模板实例-->
        <engine:Instance template="Portrait" name="player2"/>
    </engine:VisualElement>
</engine:UXML>
```

## Overriding UXML 属性

当穿件一个 UXML 模板的实例时，可以覆盖它的元素的默认属性值。属性覆盖允许你实例化同一个模板多次，每个实例具有不同的 values。

<AttributeOverrides element-name="player-name-label" text="Alice" />

属性覆盖影响整个 instance，因此如果 instance 有两个名为 player-name-label 的元素，都有 text 属性，会同时覆盖它们。

### Attribute override example

例如为每个 player 显式信息，创建一个可重用的模板，使用属性覆盖为每个 player 创建特定实例

```XML
<UXML xmlns="UnityEngine.UIElements">
    <Label name="player-name-label" text="default name" />
    <Label name="player-score-label" text="default score" />
</UXML>
```

```XML
<UXML xmlns="UnityEngine.UIElements" xmlns:uie="UnityEditor.UIElements">
    <Template src="MyTemplate.uxml" name="MyTemplate" />
    <Instance name="player1" template="MyTemplate">
        <AttributeOverrides element-name="player-name-label" text="Alice" />
        <AttributeOverrides element-name="player-score-label" text="2" />
    </Instance>
    <Instance name="player2" template="MyTemplate">
        <AttributeOverrides element-name="player-name-label" text="Bob" />
        <AttributeOverrides element-name="player-score-label" text="1" />
    </Instance>
</UXML>
```

### Overriding multiple attributes

你可以在每个 override 覆盖多个属性（每个覆盖针对一个元素）。

```XML
<AttributeOverrides element-name="player-name-label" text="Alice" tooltip="Tooltip 1" />
```

### Nesting attribute overrides

属性覆盖在 element hierarchy 的嵌套模板中传播。例如，如果 template A 实例化 template B，template B 实例化 template C，A 和 B 都可以覆盖 C 中的属性。

当覆盖嵌套模板中的属性，最深层次的覆盖优先，因此 B 对 C 的覆盖胜出。

### 限制：

- 属性覆盖根据指定的元素名查找匹配属性，不使用 USS Selectors 或 UQuery 匹配元素
- 属性覆盖不绑定到 data binding，尽管你可以覆盖一个元素的 binding-path 属性
- 你不可以覆盖一个元素的 name 和 style 属性

## Referencing other files from UXML

UXML 文件可以通过 element 引用其他 UXML 文件和 USS 文件

\<Template> 和 \<Style> 元素接受一个 src 属性或者 path 属性。

src 属性允许相对 paths，在 import time 提供 error messages，确保 Unity 在 player builds 中正确包含 UXML files 应用的 Assets（例如 image）。

path 属性允许使用 Unity Resources 机制，但是在 import time 时不提供错误报告，不允许相对 paths。

### src attribute

接受相对于 project root 或包含 UXML 文件的目录的路径。必须包含文件扩展。

- 相对于引用 UXML 文件的位置

  src="../USS/styles.uss" or src="template.uxml"

- 相对于 project 位置

  src="/Assets/Editor/USS/styles.uss" or src="project:/Assets/Editor/UXML/template.uxml"

### path attribute

接受位于 Resources 目录或 Editor Default Resources 目录的文件

- 如果文件在 Resources folder，不包含文件扩展名

  path="template" => Assets/Resources/template.uxml

- 如果文件位于 Editor Default Resources 目录，必须包含文件扩展名

  path="template.uxml" => Asset/Editor Default Resources/template.uxml
