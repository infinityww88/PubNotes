# USS Transition

类似 CSS transition 动画。

重要：

- 如果提供的属性包含 value 和 unit，确保 start value 和 end value 的 unit 相同。尤其注意 to or from defalut values 的 transition，因为默认 values 也是有单位的
- 一帧中的 transition animation 在属性的当前状态与 previous 状态不同时触发。场景中的第一帧没有 previous 状态，因此必须在第一帧之后开始一个 transition
- 对于一个 hierarchy 中的 visual element，USS transition 表现的与 CSS transition 一样，如果为一个继承属性设置 transition，例如 color，应用到 parent elements 上的 transitons 级联（cascade）到 children elements。可继承的 USS 属性：

  - color
  - font-size
  - letter-spacing
  - text-shadow
  - -unity-font
  - -unity-font-definition
  - -unity-font-style
  - -unity-paragraph-spacing
  - -unity-text-align
  - -unity-text-outline-color
  - -unity-text-outline-width
  - visibility
  - white-space
  - word-spacing

  其他属性都是不可继承的，child 元素不会去 parent 上获得属性值。

- 当一个没有完成的 transition 被中断（开始了一个新的 transition），USS transition 与 CSS transition 一样，reverse transition 可能更快
  
  很多常用 transitions 效果包含两个 states 之间的 transitions，例如当鼠标移动到一个 ui element 上，然后再离开时发生的 transition。对于这些效果，通常会在 transition 完成之前打断它，然后 property reset 到 transition 开始时的状态。如果正在进行和即将开始的 transition 使用它们指定的 durations 和 timing functions 执行，最终效果可能非常不均匀，因为第二个 transition 用指定的全部时间移动更短的距离。相反，这个规范使得第二个 transition 更短（时间）。

一个 Transition 包含以下属性：

- Property (transition-property)：指定要 transition 的 USS 属性名，默认 All
- Duration (transition-duration)：指定 transition 发生的时长，默认 0s
- Easing function (transition-timing-function)：指定 ease type
- Delay (transition-delay)：指定 transition effect 开始的延迟，默认 0s
- Transition (transition)：上面 4 个属性的简写

你可以在 UI Builder，USS 文件，或 C# 中为 visual element 设置这些属性。

和 DOTween 或其他 tween 动画不同，USS transition 不会显式 Start，End 一个动画，而是每当你设置了和当前 USS 属性不同的值时，动画自动开始。每个 Transition 只指定的 Property，Duration，Easing，Delay 这 4 个属性，每个 visual element 可以创建多个 transition。只有指定了 transition 的 USS 属性可以动画。要开始动画，只需指定一个和当前 USS 属性不同的值。

## Property

Property 控制一个 transition 应用到哪个 USS 属性上。可以使用样式规则为一个 visual element 设置 transition 属性。你可以在 USS 文件或 UXML 文件内设置样式。

transition-property 可以提供一个 USS 属性，一个关键字，或一个逗号分隔的列表。关键字包括

- all：transition 应用到所有属性，并且覆盖任何之前的 transitions
- initial：应用到所有属性，不覆盖之前的 transitions 定义，不可用在逗号分隔的列表中
- none：为所有的属性忽略 transitions。不可以用在逗号分隔的列表中

Unity 建议对 Transform 属性使用 transitions。尽管可以对其他 USS 属性使用 transitions，这可能导致 poor frame rates 的动画，因为这些属性上的 value changes 可能导致 layout recalculations。每帧执行 Layout recalculations 可能减低 transition animation 的帧率。

## Duration

单位可以是 s 或 ms。

transition-duration，可以提供一个带单位的数字，关键字，或者逗号分隔的 numbers and units 列表。

## Easing

## Delay

## C# properties

设置了 transition 后，只要修改了 transition 的指定的属性值就会触发动画。修改属性值既可以通过 style rule，也可以通过 C# code。

```c#
List<StylePropertyName> properties = new List<StylePropertyName>();
properties.Add(new StylePropertyName("rotate"));
element.style.transitionProperty = new StyleList<StylePropertyName>(properties);
```

也可以隐式转换：

```c#
element.style.transitionProperty = new List<StylePropertyName> {"rotate"}
```
