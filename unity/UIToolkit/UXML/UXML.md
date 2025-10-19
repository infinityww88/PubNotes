# UXML 格式

## Defining new elements

UI Toolkit 是可扩展的，可以定义自己的 UI 组件和元素。

在 UXML 中使用新的元素之前，必须继承 VisualElement 或它的子类来定义新的元素，然后实现适当的功能。新的 class 必须实现一个默认构造器。

```C#
class StatusBar : VisualElement
{
    public StatusBar()
    {
        m_Status = String.Empty;
    }

    string m_Status;
    public string status { get; set; }
}
```

为使 UI Toolkit 可以从 UXML 文件中实例化新 class，必须为新的 class 定义一个 factory。除非你的 factory 需要做一些特殊的事，你可以从 UxmlFactory<T> 派生 factory。建议将 factory class 放在自己的 component（新定义的 VisualElement） class 中。UI Toolkit 通过反射机制查找所有 Factory，并将它们注册到 UI Toolkit 系统中，这样就可以解释 UXML 中的新的元素了。

```C#
class StatusBar : VisualElement
{
    public new class UxmlFactory : UxmlFactory<StatusBar> {}

    // ...
}
```

这样就可以在 UXML 中定义 StatusBar 了。

## Defining attributes on elements

可以为新的 class 定义 UXML traits（特性），并设置 factory 使用这些 traits。

Traits 就是 XML 的属性

下面的 code 展示如何定义一个 UXML traits class 来初始化 StatusBar 的 status 属性。status 属性从 XML 数据初始化。

```C#
class StatusBar : VisualElement
{
    public new class UxmlFactory : UxmlFactory<StatusBar, UxmlTraits> {}

    public new class UxmlTraits : VisualElement.UxmlTraits
    {
        UxmlStringAttributeDescription m_Status = new UxmlStringAttributeDescription { name = "status" };
        
        public override IEnumerable<UxmlChildElementDescription> uxmlChildElementsDescription
        {
            get { yield break; }
        }

        public override void Init(VisualElement ve, IUxmlAttributes bag, CreationContext cc)
        {
            base.Init(ve, bag, cc);
            ((StatusBar)ve).status = m_Status.GetValueFromBag(bag, cc);
        }
    }

    // ...
}
```

这段 code 完成以下工作：

- m_Status 定义一个名字为 status 的 XML 属性
- uxmlChildElementsDescription 返回一个空的 IEnumerable，它指示 StatusBar 元素没有 child 元素
- Init() 从 XML parser 的 property bag（属性包）读取 status 的 value，并设置 StatusBar.status 属性为这个 value
- 将 UxmlTraits class 放在 StatusBar 中，允许 Init() 方法访问 StatusBar 的私有属性
- 新的 UxmlTraits class 继承自 UxmlTraits，因此它共享 base class 的属性
- Init() 调用 base.Init() 初始化 base class 的属性

UI Toolkit 支持以下类型的 attributes，每个链接一个 C# 类型到一个 XML 类型：

- UxmlStringAttributeDescription
- UxmlFloatAttributeDescription
- UxmlDoubleAttributeDescription
- UxmlIntAttributeDescription
- UxmlLongAttributeDescription
- UxmlBoolAttributeDescription
- UxmlColorAttributeDescription
- UxmlEnumAttributeDescription

UxmlChildElementDescription 返回一个空的 IEnumerable，指示 StatusBar 元素不接受任何 children。

要使元素接受任何类型的 children，你必须覆盖 uxmlChildElementsDescription 属性，返回可以接受的元素的集合（IEnumerable）。例如，要使 StatusBar 元素接受任何类型的 children：

```C#
public override IEnumerable<UxmlChildElementDescription> uxmlChildElementsDescription
{
    get
    {
        yield return new UxmlChildElementDescription(typeof(VisualElement));
    }
}
```

UxmlTraints 用于两个目的：

- 被 schema 生成过程分析，以获得关于元素的信息。即校验 UXML 定义的有效性，元素只包含指定的属性和 child 元素。
- 被 parser 用来生成并初始化元素实例

## Defining a namespace prefix

一旦你在 C# 中定义一个新的元素，就可以在 UXML 中使用元素。

如果新的元素定义在一个新的 namespace，你应该为 namespace 定义一个 prefix。Namespace prefixes 被声明为 root <UXML> 元素的属性，replace the full namespace when scoping elements。

对于每个你想定义的 namespace prefix，为 assembly 添加一个 UxmlNamespacePrefix 属性，来定义一个 namespace prefix。

```C#
[assembly: UxmlNamespacePrefix("My.First.Namespace", "first")]
[assembly: UxmlNamespacePrefix("My.Second.Namespace", "second")]
```

这可以在 assembly 的任何 C# 文件的 root level（任何 namespace 外部）完成。

Schema generation system 做以下事情：

- 检查这些属性，并使用它们生成 schema（XML schema）
- 在新创建的 UXML 文件，添加 namespace prefix 定义作为一个 UXML 元素的属性
- 在 UXML 的 xsi:schemraLocation 属性中包含 namespace 的 schema file 位置

你应该更新 UXML schemra。Assets > Update UXML Schema 确保你的 text editor 识别新的元素。

定义的 prefix 在新创建的 UXML 中可用，通过选择 Create > UI Toolkit > Editor Window。

## Advanced usage

### Customizing a UXML name

你可以通过覆盖 IUxmlFactory.uxmlName 和 IUXmlFactory.uxmlQualifiedName 属性定制一个 UXML name。确保 uxmlName 在 namespace 中时唯一的，UXMLQualifiedName 在 project 中是唯一的。

```C#
public class FactoryWithCustomName : UxmlFactory<..., ...>
{
    public override string uxmlName
    {
        get { return "UniqueName"; }
    }

    public override string uxmlQualifiedName
    {
        get { return uxmlNamespace + "." + uxmlName; }
    }
}
```

### Selecting a factory for an element

默认地，IUxmlFactory 使用 element 的 name 实例化和选择 element。

通过覆盖 IUXmlFactory.AcceptsAttributeBag，可以使 selection 过程考虑元素上的属性值。Factory 将会检查元素属性来决定它是否可以为 UXML element 实例化一个 object。

如果 VisualElement class 是 generic（泛型），这非常有用。这种情况下，class 的一个具化（generic specialization）的 class factory 可以检查 XML 的 type 属性的 value。根据这个 value，实例化可以被接受或拒绝。如果有多个 factory 可以实例化一个 element，选择第一个 registered factory。

### Overriding the default value of a base class attribute

你可以通过在派生的 UxmlTraits 类中设置 defaultValue 改变一个声明在 base class 中的属性的默认值。

```C#
class MyElementTraits : VisualElement.UxmlTraits
{
    public MyElementTraits()
    {
        m_TabIndex.defaultValue = 0;
    }
}
```

### Accepting any attribute

默认地，生成的 XML schema 声明一个 element 可以拥有任何属性。

那些没有声明在 UxmlTraits class 中的属性值，没有任何限制。

额外的 attributes 被包含在 IUxmlAttributes bag 中，它被传递到 IUxmlFactory.AcceptsAttributeBag() 和 IUxmlFactory.Init() 函数。由 factory 实现决定是否使用这些附加属性。默认 behavior 是丢弃额外属性，它们没有附加到 VisualElement 上，并且不能通过 UQuery 查询。

当定义一个新的元素时，可以限制只接受那些显式声明的属性，通过在 UxmlTraits 构造函数中 设置 UxmlTraits.canHaveAnyAttribute 属性为 false。

## Using Schema definitions

Schema definition files 指定每个 UXML element 可以包含哪些 attributes 和 child elements。使用 schemra definition file 作为 guide 来编写正确 docuemnts，并校验你的 documents。

UxmlTraits 的一个作用就是生成 schemra definition files，另一个作用就是在解析过程中初始化元素。

在 UXML 模板文件中，root 元素 <UXML> 的 xsi:noNamespaceSchemraLocation 和 xsi:schemaLocation 属性指示 schema definition files 在哪里。

选择 Assets > Create > UI Toolkit > Editor Window 以 project 中使用的 VisualElement 子类的最新信息 自动更新你的 schemra definition。

选择 Asset > Update UXML Schema 强制更新一个 UXML schema files。

如果 text editor 不识别 xsi:noNamespaceSchemaLocation 属性，还可以指定 xsi:schemaLocation。
