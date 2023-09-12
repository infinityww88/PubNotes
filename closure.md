# 闭包

闭包类似于一个匿名类，它包含一组引用的外围变量，以及一个或多个共享它们的匿名函数。

通常闭包是用来包装一个函数和它引用的外围变量。但有时会包装多个函数。这类似于有多个方法的类，这些方法共享类的成员。

```js
function makeClosure(data0) {
    data1 = ...
    closure0 = () {
        // do something with data0 and data1
    }
    closure1 = () {
        // do something with data0 and data1
    }
    // makeClosure 自身还可以修改 data0 和 data1，因此 closure0 和 closure1 中引用的 data0 和 data1 在它们执行时，不一定是它们创建时的状态
    return (closure0, closure1)
}
```

与下面的类定义类似

```text
- class
  - data0
  - data1
  - method0
  - method1
```

当在一个函数中创建多个闭包函数时尤其注意这一点，经常会在这里面落入陷阱，即变量被多个函数共享，而且还可能被当前创建闭包的函数修改，例如使用 for 循环创建多个闭包函数，而闭包函数引用了循环计数 i。
