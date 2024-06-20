# Textual CSS

Textual 使用 CSS 应用样式到 widgets 上，用 DOM tree 组织管理 widgets。

## CSS files

要添加样式表，设置 App 类变量 CSS_PATH 为 css 文件路径。

Widget 构造函数可以接收额外参数：id 和 classes。id 用于在 DOM tree 中 query 组件，classes 用于为 widget 指定样式类列表。

CSS_PATH 还可以包含 paths 列表，来应用多个 css 文件。

## Selectors

### Type selector

type selector 匹配组件类（Python class）。还可以匹配 widget 的基类。

如果同一个属性有两个类（基类）匹配并指定样式，最具体的那个类的样式优先。

### ID selector

每个 Widget 有一个 id 属性，通过构造函数设置。ID 应该对它的容器来说唯一。

```py
yield BUtton(id="next")
```

在 CSS 中可以用 \#id 匹配组件。

```css
#next {
    outline: red;
}
```

Id 在 widget 构建之后不可再改变。

### Class-name selector

每个组件可以有多个 css 样式类。可以将 CSS 样式类想象为 tag。具有相同 tag 的 widget 共享相同的样式类。

```py
yield Button(classes="success")
yield Button(classes="error disabled")
```

在 CSS selector 中，用 .className 指定一个样式类。

```css
.success {
  background: green;
  color: white;
}
```

Class name 选择器可以串联起来，匹配同时具有这些样式类的 widgets：

```css
.error.disabled {
    background: darked;
}
```

与 id 属性不同，widget 的样式类可以在 widget 创建之后改变。甚至，添加和移除样式类是运行时动态改变 widget 外观的建议方法。

- add_class() 添加一个或多个 class 到 widget
- remove_class() 从 widget 移除 class
- toggle_class() toggle 添加或移除 class
- has_class()
- classes：frozen set，包含 widget 上的 classes

### Universal selector

通配选择器用星号，匹配所有 widgets。

```css
* {
    outline: solid red;
}
```

### Pseudo classes

伪类可以用来匹配出于特定状态的组件。组件会自动被 Textual 设置伪类。

- :blur 匹配没有 input focus 的组件
- :dark 当 App 处于 dark mode 时，匹配组件（App.dark == True）
- :disabled 匹配处于 disabled state 的组件
- :enabled 匹配处于 enabled state 的组件
- :focus-within 匹配具有 input focus 的 child widget 的组件
- :focus 匹配具有 input focus 的组件
- :inline 当 App 出于 inline mode 时，匹配组件
- :light 当 App 出于 light mode 时，匹配组件（App.dark == False）

## Combinators

简单选择器可以组合构成更复杂的选择器。

### Descendant combinator

如果将两个 selector 用空白分开，它会匹配自身匹配第二个 selector 并且祖先组件匹配第一个 selector 的组件。

所有的 selector 都可以以这种方式组合任意多个：

```css
#dialog Horizontal Button {
  text-style: bold;
}
```

### Child combinator

Child combinator 类似 Descendant combinator，但是只匹配直接子组件。它使用 > 分离两个 selector。

```css
#sidebar > Button {
  text-style: underline;
}
```

## Specificity

如果一个 widget 匹配多个选择器，Textual 需要一种方法决定哪个 selector 胜出，简而言之，最具体的那个 selector 胜出：

- 拥有最多 IDs 的 selector 胜出。如果两个 selectors 有相同的 IDs 的数量，则转移到下一条规则
- 拥有最多 class names 的 selector 胜出，伪类在这里也被视为一个 class name，因此 .button:hover 胜过 .button。如果两个 selectors 具有相同的 class names 的数量
- 拥有最多 types 的 selector 胜出。Container Button 胜过 Button

### Important rules

Specificity 规则通常足够解决任何选择器冲突。但是还有最后一个方法来解析冲突。如果将 !important 放在一个 rule 的后面，它将无视 specificity 直接胜出。

## CSS Variables

可以在 CSS 中定义变量，来减少重复，并促进样式的一致性。

CSS 中变量以 $ 为前缀，它就像一条 css 样式一样，只不过 selector 的部分变成变量名，后面的样式就是变量的值。

```css
$border: wide green;
```

为 css 变量赋值之后，就可以在其他地方引用了，变量的值将被替换为它的值：

```css
#foo {
    border: $border;
}
```

变量允许定义可重用样式。变量只能用在一个 CSS 样式声明的 value 部分，不能用在 selector 中。

变量可以引用其他变量。

变量类似 C 语言的宏。

## Initial Value

所有的 CSS 规则都支持一个特殊的 initial 值，它将 css 样式重置为默认值（任何 default css 定义的值）。如果在 default css 中使用 initial，这个规则就好像没有添加任何样式一样。default css 就是 Widget 类变量 DEFAULT_CSS 定义的样式。

## Nesting CSS

CSS 样式可以嵌套，它们可以保护其他 rule sets。如果一个 rule set 出现在一个现有的 rule set 内部，它继承外面 rule set 的选择器（就像 if 中的 if 一样）。

这可以简化 css rule 的设计，尤其是对一个 selector 下面的多个 selectors 进行样式化的时候。

```css
/* Style the container */
#questions {
    border: heavy $primary;
    align: center middle;
}

/* Style all buttons */
#questions .button {
    width: 1fr;
    padding: 1 2;
    margin: 1 2;
    text-align: center;
    border: heavy $panel;
}

/* Style the Yes button */
#questions .button.affirmative {
    border: heavy $success;
}

/* Style the No button */
#questions .button.negative {
    border: heavy $error;
}
```

可以简写为：

```css
/* Style the container */
#questions {
    border: heavy $primary;
    align: center middle;

    /* Style all buttons */
    .button {
        width: 1fr;
        padding: 1 2;
        margin: 1 2;
        text-align: center;
        border: heavy $panel;    

        /* Style the Yes button */
        &.affirmative {
            border: heavy $success;        
        }

        /* Style the No button */
        &.negative {
            border: heavy $error;
        }
    }
}

Tip
```

### Nesting selector

默认嵌套的 selector 和外围的 selector 使用空白分开，但是如果前面加上 & 符号，就好将这个 selector 和外围的 selector 紧密连接起来。例如，

```css
#questions {
    .button {
        .affirmative {
            //....
        }
    }
}
```

等价于 #questions .button .affirmative，而

```css
#questions {
    .button {
        ^.affirmative {
            //....
        }
    }
}
```

等价于 #questions .button.affirmative。

### Why use nesting?

嵌套选择器不是必须的，但是它可以帮助将相关 rule sets 组织在一起，而将相关内容组织在一起，不相干内容各自分开是软件设计的根本原则。

嵌套选择器还可以帮助避免一些 selector 重复。
