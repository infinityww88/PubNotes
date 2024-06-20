# Reactivity

Reactive 属性提供另一种添加属性到 widget 或 App 实例的方法，就像在 __init__ 为 self 添加属性一样。

Reactive 添加为类属性，但实际将称为实例属性，有点类似 C# 的 Property。

```C#
from textual.reactive import reactive
from textual.widget import Widget

class Reactive(Widget):
    name = reactive("Paul")
    count = reactive(0)
    is_cool = reactive(True)
```

reactive 构造函数接收一个默认值。它代表的属性类型默认从默认值类型推断，也可以用 type hints 显式指定：

```C#
name: reactive[str | None] = reactive("Paul")
```

Reactive 属性的四个超能力：

- Smart Refresh
- Validation
- Watch
- Compute

## Smart Refresh

当 Widget 的任何 Reactive 属性发生改变，自动触发 Widget 的刷新（render 方法）。

要关闭自动刷新，使用 textual.reactive 的 var 代替 reactive。

默认刷新只改变内容，不会改变大小。要同时改变 widget 大小，设置 layout = True。

reactive("name", layout=True)。

## Validation

当属性改变时，执行 validate 方法对新值进行校验修改，使之满足指定条件，修改后的值作为属性的最终值。

## Watch

属性改变时，执行相应的 watch 方法。Textual 只会在 reactive 的 value 改变时调用 watch。如果新值和旧值没有改变，不会调用 watch。可以传递 always_update = True 使得总是调用 watch。

不仅可以在 class 中声明 watch 方法，还可以在任何 Widget 中动态创建对任何 widget reactivity 属性的 watch 方法：

widget0.watch(widget1, "property", property_watch_method)

## Recompose

刷新的另一种方法是 recompose。如果在 reactive 上设置 recompose=True，当这个属性改变时，Textual 会移除这个组件的所有 child widgets，然后重新调用 compose()。移除挂载新组件在一个 update 中完成，因此它看起来就像简单的内容更新一样。

但是因为组件都被重新创建，之前缓存的组件引用就变得失效了，因此最后使用 query 直接查找组件。

## Compute methods

Compute methods 是 reactive descriptor 最后一个超能力。Textual 可以运行 compute 方法来计算 reactive 属性的值。Validate 方法也可以改变属性的最终值，但是这两者的区别是：

- validate 是属性值自己发生变化后，再次进行调整
- compute 是任意 reactive 属性变化时，都会触发这个方法，来计算这个属性的值，可以实现这个属性值对其他属性值的依赖

Textual 对 reactive 属性首先调用 compute 方法，然后是 validate 方法，最后是 watch 方法。

在 compute 中最好避免做任何 CPU 密集的操作，因为 Textual 会在任何 reactive 属性改变时调用每个属性的 compute 方法。

## 设置 reactives 不使用超能力

有时想直接设置 reactive 属性的值，但是不触发各种超能力方法，就像 Unity UIToolkit 组件的 SetValueWithoutNotify 一样，例如在组件构造函数初始化属性值的时候，超能力方法中引用的其他组件可能还没有初始化，此时只想设置初始值。

可以调用组件方法 widget.set_reactive(WidgetClass.property, value)

注意这个方法是组件的方法，而且 reactive 属性是 class 成员。

## 数据绑定

一个 widget 可以绑定另一个 widget 的 reactive 属性，使得改变一个 active 可以自动改变另一个 widget（甚至多个）。

与 set_reactive 方法一样，widget0.data_bind(WidgetClass1.property)。改变被绑定的属性时，会自动触发绑定组件的 watch_property 方法。

App 类也可以有 reactive 属性。App 可以看出是最大的 Widget 组件，它管理的区域是整个 screen。


