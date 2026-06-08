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

ExecuteModule 返回模块的 ScriptObject，通过 Get 可以访问它 export 的属性。但是 Get 不支持路径式访问 ```xxx.yyy.zzz```，只能访问一层，因此访问模块中类型的属性，需要两次 Get，第一次从模块 ScriptObject 获取类，第二次从类的 ScriptObject 获取属性。

```C#
ScriptObject so = ScriptEnvManager.Instance.scriptEnv.ExecuteModule($"js/main.mjs");
var classObj = so.Get<ScriptObject>($"MyClass");
var staticfunc = classObj.Get<System.Action<ScriptBehaviour>>("StaticMethod");
staticfunc.Invoke(this);
```

JS 的类支持静态方法：

```js
export class MyBehaviour {
    #scriptBehaviour : CS.ScriptBehaviour;

    constructor(scriptBehaviour: CS.ScriptBehaviour) {
        this.#scriptBehaviour = scriptBehaviour;
        this.#scriptBehaviour.onDestroy = this.onDestroy;
        main.registerTick(this.onUpdate);
    }

    onUpdate = () => {
        if (CS.UnityEngine.Input.GetKeyDown(CS.UnityEngine.KeyCode.Space))
        {
            var renderer : CS.UnityEngine.MeshRenderer = this.#scriptBehaviour.GetComponent(puer.$typeof(CS.UnityEngine.MeshRenderer)) as CS.UnityEngine.MeshRenderer;
            renderer.material.SetColor("_Color", CS.UnityEngine.Color.green);
        }
    }

    onDestroy = () => {
        main.unregisterTick(this.onUpdate);
    }

    static New(scriptBehaviour: CS.ScriptBehaviour)
    {
        new MyBehaviour(scriptBehaviour);
    }
}
```

js 中 GetComponent 总是返回 Component 类型，而不是具体的组件类型，从 index.d.ts 中可以看到，它的返回值就是 Component，因此需要使用 as 强制转换为具体的组件类型，才能获得具体的类型提示。这只是在 typescript 中类型提示出现的问题，如果是无类型的 js，可以直接访问具体组件的属性，但是没有类型提示。

js 类有一个巨坑，this 指针绑定。如上面的 MyBehaviour 类，onUpdate 和 onDestroy 都使用箭头函数定义，而不是普通的函数定义：

```js
onUpdate() {
    
}

onDestroy() {

}
```

这是因为 js 的行为中，函数中的 this 不是函数定义时的类的实例，而是运行时调用者。另外如果，将类的方法作为一级成员赋给其他变量，例如 C# 的 Action，当调用 Action.Invoke() 时，this 指针是丢失的，this === undefined，方法内无法访问对象的任何属性！

要想获得正常的行为，必须使用箭头函数：

```js
onUpdate = () => {
    
}

onDestroy = () => {

}
```

箭头函数内部，this 被绑定到定义时的对象，而不是运行时的调用者，此时将对象的方法赋值给 C# 的 Action 就没有问题了。

**因此，总是使用箭头函数定义类的方法**

要让自己编写类型出现在 ts 的类型提示中，只需要将类型添加到 PuertsConfig.cs 中，然后重新生成 index.d.ts 即可：

```C#
types.Add(typeof(ScriptEnvManager));
types.Add(typeof(ScriptBehaviour));
```

自己编写的类都位于 CS 命名空间下，跟 UnityEngine 在同一个命名空间。

js 类支持访问控制。js 和 ts 都提供了访问控制。其中 js 的访问控制是硬限制，在属性前加 # 就变成私有属性，在 js 运行时无法访问这种私有属性。

ts 提供了 public、protected、private 的访问控制，但是只在 ts 中有效，在 js 中如果不是带前缀 #，就是可访问属性。

PuerTS 中只能访问 C# 的 public 属性，不能访问 private，遵循 C# 的可访问性。

有时 GameObject Destroy 时，需要执行 js 端的一些清理工作。但是注意 ScriptEnv 可能也在 OnDestroy 中 Dispose，这样 ScriptEnv 的 OnDestroy 和 GameObject 的 Destroy 的顺序不是确定的，可能导致 GameObject 要执行 js 清理时，ScriptEnv 已经 Dispose 了，注意这一点。
