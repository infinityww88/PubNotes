# USS Selectors

Selectors 决定 USS rules 影响哪些元素。当 Unity 应用一个 style sheet 到一个 visual tree，它匹配元素到 selectors。如果一个元素匹配 selector，Unity 应用这个 selector 的 style rule 到这个元素。

USS 支持一些简单和复杂类型的 selectors

- C# class name
- name property
- USS classes list
- element 在 visual tree 的 position 和它与其他 elements 的关系

它还支持伪类，可以匹配特定状态的 target elements。

如果一个元素匹配多个 selector，Unity 应用最高优先级的 styles。

## Supported selector types

USS 支持简单，复合，和伪类 selector。

### Simple selectors

| Selector Type | Syntax | Matches |
| --- | --- | --- |
| C# Type | Type { ... } | 特定 C# 类型的元素 |
| USS class | .class { ... } | 带有指定 uss class 的元素 |
| Name | #name { ... } | 具有指定 name 属性的元素 |
| Wildcard | * { ... } | 任何元素 |

### Complex selectors

| Selector Type | Syntax | Matches |
| --- | --- | --- |
| Descendatn selector | selector1 selector2 { ... } | 匹配 selector1 的元素的任何 level 后继元素中匹配 selector2 的元素 |
| Child selector | selector1 > selector2 { ... } | selector2 是 selecto1 的直接子元素 |
| Selector list | selector1, selector2, selector3 { ... } | 匹配列表中任何一个 selector 的元素 |

### Pseudo-classes

| Pseudo-class | Matches an Element when |
| --- | --- | 
| :hover | cursor 位于 element 之上 |
| :active | user 和元素交互 |
| :inactive | user 停止和元素交互 |
| :focus | 元素具有焦点 |
| :selected | N/A。Unity 不使用这个 pseudo-state |
| :disable | 元素被设置为 enabled = false |
| :enabled | 元素被设置为 enabled = true |
| :checked | 元素时一个 toggle 元素，并被 toggled on |
| :root | 元素时 root 元素（visual tree 的最高层元素） |

## 确定 selector precedence

当一个元素匹配多个 selector 时，Unity 考虑很多因素来决定哪个 selector 优先

Unity 如何确定 selector 优先级依赖于冲突的 selectors 是在同一个 style sheet 还是在不同的 style sheet。

### 同一个 style sheet 中的 selector 优先级

具有最高 specificity 的 selector 优先。如果两个 selectors 具有相同的 specificity，最后一个出现的优先。

### 不同 style sheets 中的 selector 优先级

1. style sheet 的类型：用户定义的 selectors 被 Unity 默认的 style sheets 优先
2. Selector specificity：如果两个 selects 都是相同类型的 style sheet，具有最高 specificity 优先
3. element hierarchy 中的 style sheet 的 position：如果两个 selectors 具有相同的 specificity，应用到 hierarchy 最底层的 style sheet 优先（即最靠近应用的元素的 selector）
4. style sheets 中 selector 的 position：如果两个 style sheet 应用到 hierarchy 的同一个 level，最后出现的 selector 优先

### Selector Specificity（特征，专一性，具体程度）

Selector Specificity 是一个相关性度量。Specificity 越高，selector 和匹配的元素越相关

- Name selectors 比 Class selectors 更具体
- Class selectors 比 C# type selectors 更具体
- C# Type selectors 比 wildcard(*) selector 更具体

### Applied styles vs. inherited styles

直接应用到 元素的 styles 比元素继承的 style 更优先，即使继承的 styles 定义了更高的 specificity。

## Overriding USS selectors

直接应用在元素上的 styles 覆盖通过 USS 应用的 styles。

USS 不支持 !important 

### inline styles

在 UXML 文档中应用的 inline styles 比 USS styles 更优先

### C# styles

在 C# 中设置的 styles 覆盖任何其他 styles，包括 USS styles 和 inline styles。可以认为它们具有最高的 specificity（因为它们直接应用到元素实例）。
