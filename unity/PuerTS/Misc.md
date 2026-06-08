ScriptEnv 只有两个执行代码的方法：Eval 和 ExecuteModule。

Eval 用于在全局环境中执行普通脚本，ExecuteModule 用于加载模块。ExecuteModule 相当于 C# 侧的 import，模块只会加载一次，它返回 ScriptObject，这是一个模块对象，通过它的 Get 方法可以访问模块 export 的属性：

```C#
ScriptObject obj = scriptEnv.ExecuteModule("js/main.mjs");
System.Action myFunc = obj.Get<System.Action>("myFunc");
myFunc.Invoke();
```

这可以访问 main.mjs 模块的 export 属性 myFunc。

ScriptEnv 的 Tick 方法必须在 C# 侧端显式调用，它驱动 JS 中的所有异步方法和 Timer/Timeout，否则 promise、await、SetInterval/SetTimeout 都不会工作。

Eval 在全局上下文中执行脚本，相当于 node main.js。所有的 Eval 都在同一个全局上下文执行脚本，因此在共享同一个全局环境。一个 Eval 声明的全局变量，在下一个 Eval 中可见。要在 Eval 中封闭作用域，使用立即执行函数。

要访问全局作用域的全局变量，使用 ```Type var = scriptEnv.Eval<\Type>("...")```。

在 js 环境中，new 一个对象，但并不赋给任何变量，它就是不可达对象，就会在下一次 GC 中被回收。只有它或者它的一个属性被其他地方引用这，它就是可达的，就不会被回收。在 C# 侧引用一个 js 对象或者它的属性，就像在 js 中引用一样，也会增加计数，导致 js 对象不会被回收，直到 C# 侧放弃引用。

PuerTS 中 Eval 只用于执行表达式、调试、临时逻辑，基本是 play around 的角色， ExecuteModule 才是正式开发的核心。
