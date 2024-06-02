# QuantumConsole

## Getting Started

所有代码位于 QFSW.QC namespace 下面。

- 确保 TextMeshPro Package 安装
- 确保场景中存在 EventSystem
- 在 Assets/Plugins/QFSW/Quantum Console/Source/Prefabs 找到 Quantum Console Prefab，添加到 scene 中

如果 project 中使用任何 SRP（LWRP，URP，HDRP），使用 Quantum Console(SRP) prefab。

- help 命令提供使用 console 的简介。
- man 命令查看指定命令的用法
- all-commands 查看所有被 processor 加载的命令

### 添加命令

通过添加 \[Command\] 属性到 function，property，field 上面，就将它转化为一个 command。

命令调用参数通过空白分隔，而不是逗号。

### 自动补全

Quantum Console 可以在你输入命令的同时提供自动补全建议。这些建议可以使用 Tab 和 Shift+Tab 循环（这可以在 QuantumKeyConfig 中配置），也可以直接点击建议。

KeyConfiguration 在 Console 的 asset field 中配置，而不是在 Project Setting 中。

因为自动补全是上下文相关的，诸如 enums 和 macros 的参数也可以在输入命令的时候给出建议。

注意，UnityEditor 的 Simulator 模式下，按键事件 Input.GetKey/GetKeyDown/GetKeyUp 没有作用，总是返回 false。Simulator 模式下只支持 Mouse 事件，不支持 Key 事件。

### man Command

man 命令会产生给定命令的 user manual。它能够展示一个命令的所有可用签名，以及每个参数的类型。通过添加一个描述到 command，将它包含到 [Command] 或 [CommandDescription]。[CommandParameterDescription] 可以为参数给定一个描述。

### 参数解析

默认，参数通过空白分隔。通常这对绝大多数参数都没问题，但是有两种情况需要特殊关注：

- Strings

  如果字符串包含空白，必须使用双引号 "" 整个字符串包含。因此 spawn "player 10" 被解释为 spawn("player 10") 而不是 spawn("player", 10)。

  如果字符串本身包含引号 \"，必须使用反斜线 \\ 将它转义。

- Arrays and Collections

  Arrays，Lists，和其他支持的 Collections 可以通过将元素包含在 \[\] 中来输入。

  例如 sort\<int\> [3, 2, 1] 将会使用泛型方法 sort\<int\> 排序 int 数组，并返回 [1, 2, 3]。

  嵌套数组可以使用相似方式输入，因此 [[Quantum, Console], [Array, Test]] 是 string[][] 类型的一个有效输入。

所有参数直接输入，不需要指定类型，QuantumConsole 会根据命令方法的签名自动将输入转换为参数类型，因此字符串不需要用引号显式包含，除非它包含空白。

## Commands

\[Command\] 属性有以下成员可以定制和修改生成的命令：

- alias：QuantumConsole 中命令的名字，默认是它使用的函数名
- descripiton：man 命令生成的命令描述，默认为空
- supportedPlatforms：bitwise enum，只是这个命令应该在哪些平台上加载，默认是 Platform.All
- monoTarget：调用命令的 target。默认为 MonoTargetType.Single

### Multiple Commands

Quantum Console 允许在一个方法上使用多个 [Command] 来为一个 command 创建 aliases。要避免多次重复 description 和其他东西的麻烦，可以添加下面的属性到方法上，他们覆盖 Command 指定的 description 和 platform enum。

- \[CommandDescription\] 覆盖任何 Command 定义的 description
- \[CommandPlatform\] 覆盖任何 Command 定义的 platform num

```C#
[Command(alias="Alias0")]
[Command(alias="Alias1")]
[CommandDescription("general description")]
private void Func() {
    //...
}
```

这样 Func 有两个别名，两个别名 Command 都有相同的 description，但无需再每个 Command 都指定相同的 description。

### Static Usage

```C#
[Command]
private static void cmd(int a) { }
//In scenario 1, a command called cmd will be generated that has no return type and takes an argument of type int

[Command("int-prop")]
protected static int someInt { get; private set; }
//In scenario 2, two commands called int-prop will be generated:
//The first will take 0 arguments and will return an int; this uses the property.get
//The second will take 1 argument of type int and will not return; this uses the property.set

[Command("bool-field")]
public static bool someBool;
//In scenario 3, two commands will be generated called bool-field. Fields are treated as auto-properties, so this will behave like scenario 2

[Command("del")]
public static Func<bool> someDelegate;
//In scenario 4, a command will be generated called del. Delegate are treated as a normal method, so this will behave like scenario 1

//Delegate fields must be strongly typed, this means the following is not allowed:

[Command("del")]
public static Delegate someDelegate;
```

### Non-static Usage

非静态方法命令有更多需要注意的地方，但是仍然非常简单。Non-static 命令需要：

- declaring class 是 MonBehaviour 类型
- 或者使用了 Quantum Registry

即默认 Non-static 命令只能用在 Scene 中的 GameObject 的组件上，不是任何 object 都可以。

这是因为需要再 scene 中找到要调用命令的 object。Non-static commands 引入了另一个概念：MonoTargetType。它定义如何选择进行调用的 target。

下面命令在同一个方法上面创建了两个命令：

- kill-all，在所有 active 的 Enemy 上面调用 Die
- kill，在 Enemy 单个实例上调用 Die，实例通过 argument 提供

```C#
using QFSW.QC;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    [Command("kill-all", MonoTargetType.All)]
    [Command("kill", MonoTargetType.Argument)]
    private void Die()
    {
        // Death implementation here
    }
}
```

### 限制

为了防止命令调用的模糊性，command 的名字和参数数量必须唯一。这意味着两个具有相同 alias 的 commands 是合法的，当必须具有不同的参数数量。

Command 的签名和 code 中的签名不一样，code 中的签名包含参数的类型，但是 command 的签名类型只包含参数个数。

如果两个方法具有相同的名字和参数数量，必须覆盖 alias 使它们变得唯一。这应该为命令创建别名的主要用途，否则为一个具有唯一名字的 command 创建 alias 是没有意义的。

此外，所有参数类型必须是以下支持的类型（部分）之一：

- int float decimal double string bool
- byte sbyte uint short ushort long
- Vector2 Vector3 Vector4 Quaternion Color Type
- ulong char GameObject
- Component 或 MonoBehaviour
- Array List<T> Stack<T> Queue<T>
- 所有的 enum 类型

查看 Parsers 确定所有支持的类型，另外 Custom Parsers 可以添加新的类型。

任何违反上面限制的情形，Quantum Console Processor 会丢弃命令并抛出一个警告。

## Command Actions

所有 actions 位于 QFSW.QC.Actions 命名空间下。

Actions system 可以编写强大的交互式命令，它们可以挂起，类似 coroutines。

要使用 actions 创建一个 command，简单地让 command 返回 IEnumerator<ICommandAction> 或 IEnumerable<ICommandAction>。然后 yield return 想要使用的 action。

### Printing Values

```C#
using QFSW.QC;
using QFSW.QC.Actions;
using System.Collections.Generic;
...

[Command("countdown")]
public static IEnumerator<ICommandAction> Countdown()
{
    for (int i = 3; i > 0; i--)
    {
        yield return new Value(i);
        yield return new WaitRealtime(1);
    }

    yield return new Value("Countdown over!");
}
```

这就是在 Quantum Console 执行一个 Coroutine。yield return 将控制权返回给 Quantum Console。yield return Value，Value 的值在 Console 被打印。

### Reading Input

```C#
using QFSW.QC;
using QFSW.QC.Actions;
using System.Collections.Generic;
...

[Command("read-key")]
public static IEnumerator<ICommandAction> ReadKey()
{
    KeyCode key = default;
    yield return new GetKey(k => key = k);
    yield return new Value(key);
}
```

这会等待 user 输入一个 key，然后将它展示到 console。

### Presenting Choices

```C#
using QFSW.QC;
using QFSW.QC.Actions;
using System.Collections.Generic;
...

[Command("choice")]
public static IEnumerator<ICommandAction> Choice()
{
    string[] consoles = {"PS4", "Xbox", "Switch"};
    string selectedConsole = default;

    yield return new Value("Pick a console");
    yield return new Choice<string>(consoles, s => selectedConsole = s);

    yield return new Typewriter($"You picked {selectedConsole}.");
}
```

这在 Console 中运行一个 Coroutine，打印 Pick a console，然后等等 user 从 Console 选择一个值，最后将选择的值打印出来，Coroutine 结束。

### Included Actions

- ReadLine: Coroutine 将控制权返回给 Console，Console 等等用户输入，获得输入，然后将控制权返回给 Coroutine 并传递用户输入的文本。如此反复以此类推，直到 Coroutine 运行结束
- ReadValue<T>：获取 Console 下一行输入作为用户响应，并解析为 type T
- Wait：等待给定 seconds 的 scaled time（暂停 Coroutine 的运行）
- WaitRealtime：等等给定 seconds 的 real time
- WaitWhile：等待直到给定的 condition 不满足
- WaitUntil：等待给定的 condition 满足
- WaitFrame：等待到下一帧
- WaitKey：等待指定的按键按下
- Value：序列化并 log 到 console 中
- RemoveLog：移除 console 最近的 log
- GetKey：等待任何按键按下，然后通过 delegate 将 key 返回给 Coroutine
- GetContext：获得命令当前被调用的 ActionContext
- Composite：将一组 actions 合并为一个 action
- Choice<T>：为 user 提供一组输入，user 可以使用箭头键和回车键选择其一
- Typewriter；在 console 中逐渐输入一个 message（每此按键都交换执行权）
- Async, Async<T>：将一个 async Task 转换为一个 action。即直接运行一个 async task
- Custom：通过 delegates 实现的 Custom action

## Lambda Commands

通常情况下，应该将 \[Command\] 属性添加到 方法，属性，字段，和 delegates 上来创建命令，然而有时可能想要在运行时从 lambda 创建 commands。此时，可以使用 LambdaCommandData 类型从 lambda 在运行时创建 Command。

MonoTargetType 不需要指定，因为 command 会保持一个对 labmda target 的引用，它会支持捕获变量，就像普通的 lambdas 一样。

一旦创建了 LambdaCommandData，它可以通过 QuantumConsoleProcessor.TryAddCommand 添加到 Quantum Console.

下面的例子创建了 10 个 lambda commands，每个捕获不同的 value。

```C#
using QFSW.QC;
...

for (int i = 0; i < 10; i++)
{
    int value = i;

    Func<int, int> func = x => x + value;
    LambdaCommandData command = new LambdaCommandData(func, $"lambda-add-{i}");
    QuantumConsoleProcessor.TryAddCommand(command);
}
```

### Non-static Methods 绑定

Lambda 命令还可以用来将 non-static 方法绑定为 Command，并自动捕获调用的 instance 作为 target。像这样创建的 Lambda commands 就像使用 lambdas 一样。

由于 C# 类型系统的限制，函数必须首先被转换为强类型的 delegate，就像 Action 或 Func，即使 editor 中声明这是多余的。

由于 C# 类型系统的限制，不像标准 commands，lambda commands 不能直接从 generic methods 创建，必须为泛型方法添加一个非泛型的外壳。

```C#
using QFSW.QC;
using UnityEngine;

public class LambdaMethodCommandExample : MonoBehaviour
{
    private void Start()
    {
        LambdaCommandData command = new LambdaCommandData((Func<Vector2>)GetPosition, $"get-pos-{name}");
        QuantumConsoleProcessor.TryAddCommand(command);
    }

    private Vector2 GetPosition()
    {
        return transform.position;
    }
}
```

为了使用 suggestor tags 系统，lambda 命令应该从一个 non-static 方法或 local 方法创建，而不是匿名 lambda，这样可以像通常那样应用 suggestor tags 到 parameters。

## 自动补全

Quantum Console 包含一个上下文自动补全系统，这会在你输入命令的同时提供建议。默认 Quantum Console 可以建议命令和它们的参数，同时对一些参数类型，例如 enums 和 GameObjects，Quantum Console 还支持可能的 values。

Suggestions 可以通过点击建议条目，或者使用 keyboard 箭头或 tag/shift+tab 循环。

### Suggestor Tags

所有 suggestor tags 都位于 QFSW.QC.Suggestors.Tags 命名空间。

一些情况下，通用自动补全规则可能不足以从当前输入给出建议，尤其是对于 string 参数。Suggestor tags 允许更显式地指定一个给定 argument 想要哪种 suggestions。要使用一个 suggestor tag，只需要简单添加 tag 属性到 command 声明中的 parameter 上。

### Included Tags

- \[Suggestions\] 指示一个 values 列表，作为 parameter 的 suggestions
- \[CommandName\] 将所有 Command 的名字作为 parameter 的 suggestion
- \[SceneName\] 将所有 scene 的名字作为 parameter 的 suggestion

## Quantum Registry

通过使用 registry 和 MonoTargetType.Registry，可以完全控制哪些 objects 被用作 invocation 的目标。

Objects 可以通过以下方法添加到 registry 中：

- QuantumRegistry.RegisterObject<T>(T target) 编程方法
- register-object<T> Command

每种类型 T 可以注册多个 objects，并且不会从 registry 中移除，除非它们被销毁或者手动移除。

移除 registry：

- QuantumRegistry.DeregisterObject<T>(T target)
- deregister-object<T>

通过使用 Registry，还可以添加 non-static non-monobehaviour 命令。默认情况下，任何类型的 static 方法和 Component/MonoBehaviour 的方法才可以添加为 Command。

## Expressions

Quantum Console 灵活的 grammer construct 系统允许你构建复合表达式作为 commands 的输入。

- 任何二元操作符：set-speed 10*2

  为了在操作符周围添加一些空白，整个表达式必须包含在 () 中：set-speed (10 * 2)

- Expression Bodies

  Expression bodies，{expr}，可以用于将 commands 以强大的方式 chain 在一起。expr 将会递归地调用，它的结果作为外层 expr 的值。

  destry-obj {find-obj "robot"}

  player.hp ({player.hp} + 10)

  默认地，Expression bodies 不允许 null values 传递，并且会抛出警告。要允许 null values 传递，使用 nullable expression bodies，{expr}?

- Bool 取反

  vsync !off

  vsync !{vsync}

## Macros

Macros，就像 C Macros，允许你创建 shorthands，它会在 command 被解析之前展开。

Macros 使用 #define 在 Quantum Console 中定义，或者 QuantumMacros.DefineMacro 在 code 中定义。

```C
#define pi 3.14
#define reset-player "teleport player (0, 0, 0)"
```

在 console input 中通过前缀 \# 来使用 Macros。

```C
rotate object (0, 0, #pi)
#reset-player
```

\# 操作符的使用导致 macro 在解析之前被展开。Macros 本身不可以包含 \# 或空白。

Macros 在定义新 macro 时（#define 或 QuantumMacros.DefineMacro）不可以展开，这使得定义嵌套 macros 成为可能。

### 嵌套 Macros

Macro 展开后可能包含其他 macros，这允许创建嵌套 macros，更方便地创建复杂和动态的 macros。

```C
#define num 5
#define array [#num, #num, 20]
```
使用这些 macros 定义，#array 全面展开为 [5, 5, 20]. 如果 #num 重新定位为 10，#array 将扩展为 [10, 10, 20].

### API

可以在 code 中使用 macros。

## Async Commands

除了正常的同步的命令，QC 还支持 async 命令，基于 C# 的 async/await 系统。

### Async Command Support

要编写 async 命令，简单编写一个 async 函数，就像通常那样，然后添加 \[Command\] 属性即可。

```C#
using QFSW.QC;
using System.Threading.Tasks;
...

[Command]
private static async Task<int> Delay(int time)
{
    await Task.Delay(time);
    return time;
}
```

### Blocking vs Non-blocking mode

默认地，对 async 命令，QC 以 non-blocking mode 运行。这意味着在一个 async 命令正在运行的同时，仍然可以运行其他（sync 或 async）commands。一个计数器将会出现在 input field 旁边，显示当前正在运行多少个 async jobs。

Blocking mode 下 console 在当前 job 完成前不可以使用。要切换到 Blocking mode，在 Inspector 中的 Async Settings 开启 Block on Execute。此外，Show Current Jobs 可以开启和关闭 job counter。

## Extra Attributes

QC 带有一些额外的，非核心的属性，可以让使用 QC 更加容易。

### \[CommandPrefix\]

通过在一个 class 上使用 \[CommandPrefix\] 属性，可以很容易地添加一个 attribute 到它里面声明的所有 commands。

```C#
using QFSW.QC;

[CommandPrefix("test.")]
public static class MyClass
{
    [Command("foo1")]
    private static void Foo1() { }
    
    [Command("foo2")]
    private static void Foo2() { }
}
```

这个示例产生两个命令，test.foo1 和 test.foo2 。这可以很容易将命令分组。如果不提供名字，就像 \[Command\]，将使用 class 的名字。

这个属性还可以用于嵌套类，以及在同一个 class 上使用多个属性。

```C#
using QFSW.QC;

[CommandPrefix("test1.")]
[CommandPrefix("test2.")]
public static class MyClass
{
    [CommandPrefix("a.")]
    private static class MyClass1
    {
        [Command("foo")]
        private static void Foo() { }
    }
    
    [CommandPrefix("b.")]
    private static class MyClass2
    {
        [Command("foo")]
        private static void Foo() { }
    }
}
```

这会产生命令 test1.test2.a.foo 和 test1.test2.b.foo 。

Command 前缀还可以应用到整个 assemblies。

```C#
using QFSW.QC;

[assembly: CommandPrefix("assembly.")]

[CommandPrefix("class1.")]
public static class MyClass1
{
    [Command("foo1")]
    private static void Foo1() { }
    
    [Command("foo2")]
    private static void Foo2() { }
}

[CommandPrefix("class2.")]
public static class MyClass2
{
    [Command("foo1")]
    private static void Foo1() { }
    
    [Command("foo2")]
    private static void Foo2() { }
}
```

这个属性应用在顶级 namespace level。

### \[QcIgnore\]

这个属性可以用到任何 class 或 assemblies，只是 QC Processor 在扫描命令时忽略它。这可以用于加速生成 table。

## Events and Callbacks

QC 组件提供各种 event callbacks 用于订阅，这允许你添加自己的行为到 console，而不需要修改它。

- OnStateChange：Action，QC state 改变时执行
- OnInvoke：Action\<string\>，QC 调用一个命令时执行
- OnClear：Action，QC clear log 时执行
- OnLog：Action\<ILog\>，text 打印到 QC 时执行
- OnActivate：Action，QC activated 时执行
- OnDeactivate：Action，QC deactivated 时执行

## 内置命令

### Core Commands

- help
- man
- commands：生成当前加载的所有命令列表
- register-object\<T\>：添加 object 到 registry，用于 MonoTargetType=Registry 的命令
- deregister-object\<T\>：从 registry 移除用于 MonoTargetType=Registry 命令 target 的 object
- clear-registry\<T\>：清理指定 registry 的 contents
- display-registry\<T\>：显示指定 registry 的内容
- use-namespace
- remove-namespace
- all-namespace
- reset-namespace
- \#define：添加一个 macro 到 macro table
- remove-macro：从 macro table 移除指定 macro
- clear-macros：清理 macro table
- all-macros：显示当前 macro table 中的所有 macros
- dump-macros：将当前 macro table 中的 macros 导出到一个外部文件中，之后可以使用 load-macros 重新加载
- load-macros：从外部文件加载 macros 到 macro table
- verbose-errors
- logging-level
- max-logs：最大 logs 条数
- clear
- qc-script-extern：执行外部 QC 脚本文件，每一行都是一个单独的 QC 命令

### Extra Commands

#### Util 命令

- get-scene-hierarchy：显示当前 scene 的 GameObjet hierarchy
- get-object-info：查找并返回 scene 中指定名字的第一个 GameObject，并显示它的 transform 和 component data
- destroy：销毁一个 GameObject
- instantiate：实例化一个 GameObject
- teleport：telport 一个 GameObject
- telport-relative：相对当前位置 teleport 一个 GameObject
- set-active：Activate/deactivate 一个 GameObject
- send-message：在 target GameObject 的每个 MonoBehaviour 上调用指定名字的方法
- add-component\<T\>
- rotate

#### Screen 命令

- fullscreen：Application 的 Fullscreen 状态
- screen-dpi：当前 device screen 的 DPI
- screen-orientation：screen 的 orientation
- current-resolution
- supported-resolutions
- set-resolutions
- capture-screenshot

#### Scene 命令

- load-scene
- load-scene-index
- unlaod-scene
- unload-scene-index
- all-scenes
- active-scene
- loaded-scenes
- active-scene
- set-active-scene

#### Graphic 命令

- max-fps
- vsync
- msa

#### Type 命令

- enum-info：获取指定 enum 类型的所有 value 名字和 value 数值

#### Time 命令

- time-scale

#### Coroutine 命令

- start-coroutine：将指定命令作为 coroutine 运行

#### Exec 命令

不支持 AOT（IL2CPP）构建。

- exec
- exec-extern

#### KeyBinder 命令

- bind：将给定的命令绑定到一个 Key 上，每次按下这个 Key 就调用这个命令
- unbind
- unbind-all
- display-binding

#### MegaCommand

- call-static：使用提供的参数调用指定的方法或属性。如果存在歧义重载方法，提供 \[argTypes\]
- call-instance

#### 文件命令

- write-file
- read-file

#### Application 命令

- quit

#### Http 命令

- http.get
- http.delete
- http.post
- http.put

