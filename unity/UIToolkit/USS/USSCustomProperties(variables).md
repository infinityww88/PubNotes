# USS custom properties(variables)

USS 变量，又称为 custom properties（自定义属性），定义你可以在 USS rules 中重用的 values（类似 C 语言中的宏定义）。你可以为任何类型的 USS 属性创建变量。

创建一个 USS 变量，以 -- 为前缀：

--color-1: red;

要在另一个 USS rule 中使用 USS variable，使用 var() 函数。

var(--color-1);

var() 还可以接受一个可选的默认值。

当定义个 variable 之后，可以在任意多个 USS 属性中使用它。当更新变量时，所有使用它的 USS 属性也会更新。

```CSS
:root {
  --color-1: blue;
  --color-2: yellow;
}

.paragraph-regular {
  color: var(--color-1);
  background: var(--color-2);
  padding: 2px;
  }

.paragraph-reverse {
  color: var(--color-2);
  background: var(--color-1);
  padding: 2px;
  }
```

要更新 color scheme，你只需要改变2个 variable values，而不是4个颜色值。

Variables 使得为复杂 UI 改变 styles 更容易，在其中多个 rules，有时时不同的 stylesheets（文件），使用同一个 variable。

## Specifying default values

var() function 接受一个默认值。当 UI system 不能解析 variable 时，使用默认值。例如你从一个 stylesheet 移除了一个变量，但是忘了移除对它的引用。

var(--color-1, #FFF0000);

## Built-in Unity variables

Unity 内置 style sheets 定义 USS 变量，它们为 Editor interface 设置默认值。你可以在自己的 style sheets 中使用这些变量来确保你的自定义 Editor extensions 匹配 Unity style。Unity style sheets 在内置的 uss 文件中定义，说明 variable 是跨文件可访问的。

## Differences from CSS

USS 中 Variables 和 CSS 几乎一样工作，只有一些很小的区别需要理解

### Calling USS variables from other functions

一些 web browsers 支持在其他 functions 中使用 var()，例如：

background-color: rgb(var(--red), 0, 0);

Unity 不支持这种 var() 用法。

### Declaring variables in root selector

一个常见的 CSS 实践是在 :root 伪类选择器中声明 global 变量。因为每个元素都继承 :root，一个 CSS style sheet 中的每个 selector 都可以使用那里声明的变量。

在 Unity，在 :root 中声明的变量作用于 Editor windows 和 runtime panels，使得你可以附加 stylesheet 到 panel 或者 Editor window 的 root VisualElement。但是不作用于 Inspector UI。

在 Inspector 中，:root 伪类只在 Inspector window 的 root VisualElement 有效，而附加 stylesheets 的 subtrees 在 Inspector hierarchy 非常低，因此 :root selector 从不匹配一个 subtree 的任何部分。

#### 为 自定义 Inspector UI 模拟 :root 

可以使用一个 USS class selector 作为 custom Inspector 的 :root selector 中代替者。创建一个 USS class 在其中声明你的变量，并应用它到你可以访问的 hierarchy 的最高元素。

```css
.root {
    --color1: rgb(25, 255, 75);
}

.label1 {
    color: var(--color1);
}
```

```XML
<UXML xmlns="UnityEngine.UIElements">
    <VisualElement class="root">
        <!-- Including, for example... -->
        <Label class="label1" text="Label text"/>
    </VisualElement>
</UXML>
```