Hot Reload 是一个 C# 编译器扩展，它只编译发生改变的方法（这非常快，只需要几毫秒）。编译后，只会用这个新版本的代码替换那个函数。这意味着，不需要 domain reload，因此你的静态变量保持不变。

Hot Reload 窗口会时不时显示 No changes applied。这意味着 Hot Reload 处理了一个文件，但是绝对不应用其修改。这通常是因为修改时无关紧要的，例如在函数中添加了一个空白行。但是在少数情况下，它还意味着发生的修改不支持 Hot Reload。

如果 Hot Reload 显示了 No Changes applied，而你真正进行了有意义的修改，建议使用 Recompile 按钮进行重新编译。

可以手动触发 recompile，Ctrl-R。编辑器会自动确定哪些需要被编译。当发生不支持的 code 修改时，应该进行手动 recompile，例如添加一个新 class。当进行了不支持的 code change，会显示一个 warning。

即使发生了不支持的 code changes，仍然可以继续修改其他的 files 和 functions，仍然可进行 hot reload。不支持的 code edit 简单地在 editor 中不可见，直到进行手动编译。

## 支持的功能

- 编辑 MonoBehaviour，普通 class，static class 中的函数

  可以以任意方式编辑 function body，只有是合法的 C# 代码。Hot Reload recompile 整个函数。

- 添加、编辑、移除 fields

- 编辑 lambda methods

  如果修改一个 lambda，我们 hot-reload 现有的 lambda。例如，在 startup 时在一个 static field 存储一个 lambda，然后编辑 lambda，而没有允许 startup code，对 lambda 的改变仍然会立即生效。

- 编辑带闭包 closures 的 lambda

  修改 lambda 时，如果在 lambda 内部使用一个外部变量，lambda 仍然可以正常工作。如果使用了一个新的外部变量，则 lambda 只在你重新创建它时被 hot-reload。

  例如，Array.Sort(() => ...) 中的 lambda 每次允许代码时都重新创建，因此它总是如期望那样工作。

- 编辑 async/await 方法

- 编辑 properties(get/set)

- 编辑 events(add/remove)

- 编辑 indexers（方括号访问，例如 dict）

- 编辑 operators 方法（显式、隐式 operators）

- 编辑 conversion operators 方法，例如 == 和 +=

- 编辑非泛型类中的非静态构造函数

- 添加、编辑、移除 local function

- 编辑泛型类的方法

- 将方法从 async 改变为 sync，或从 sync 改变为 async

- 删除任何方法、properties，fields，class

- 添加、编辑、移除 using 指示符，using UnityEngine

- 添加、编辑变量初始化器，例如 class 中的 private int x = 1

  注意，变量只会在创建新的实例时才会应用新的初始化。已经创建的 class 不会重新运行变量初始化，否则会破坏现有代码。

- 使用最新的 C# 语法。Switch 表达式、using 语句、pattern matching、null coalescing statements 等等。

  默认，我们支持 C# 编辑器支持的所有 syntax。

- 使用 nullable

- 添加新的方法

- 添加、编辑、删除方法参数

- 改变任何方法的返回类型。包括 instance，static，properties，events，indexers，generics 等

- 改变可访问性，例如 private -> public

- static keyword 改变，例如将要给方法变为 static 的

- 重命名方法

- 编辑泛型方法，就像正常方法一样

- 添加、编辑、删除泛型参数

- 添加、编辑、删除泛型方法的 constraint 子句（ where T : class, new() ）

- 添加、替换、删除参数的 ref，out，in

- 编辑标记为 [BurstCompile] 的 code

- 部分支持 coroutine。修改值应用到新创建的 coroutines，但是已经开始的 coroutine 不会更新

## 响应 Hot Reload patches

Hot Reload 可以在应用新 patch 时调用你的函数。有两个属性可以允许你的函数在 Hot Reload patches 时调用。

- [InvokeOnHotReload]

  带有这个属性的方法在应用 patch 时调用。

  ```C#
  [InvokeOnHotReload]
  static void HandleMethodPatches(List<MethodPatch> patches) { // patches parameter is optional
      foreach (MethodPatch methodPatch in patches) {
          Debug.Log($"Received patch for method: {methodPatch.newMethod.Name}");
      }
  }
  ```

  实例方法也是支持的。

  方法参数中的 MethodPatch 包含：

  - 原始方法：被 Unity Editor 编译的。如果是新加的方法，则为 Null
  - 之前的方法：Hot Reload 应用 patch 之前的方法。如果是新加的方法，则为 Null
  - 新加的方法：Hot Reload 生成的方法

  函数移除不会调用 [InvokeOnHotReload] 方法。改变函数名字表现为之前函数的移除，和新加一个函数。

  domain reload 之后，例如从 editmode 到 playmode，Hot Reload 重新应用所有 changes 到新的 domain。结果就是，InvokeOnHotReload 在 domain reload 之前会应用所有 patches。

- [InvokeOnHotReloadLocal]

  带这个属性的方法在其自身修改时会被调用。类似 InvokeOnHotReload，这个属性可以添加到任何类（不仅仅是 MonoBehaviour）的 instance 方法和 statick 方法上。

  ```C#
  [InvokeOnHotReloadLocal]
  static void MyMethod() {
      // change the string below to receive the log
      Debug.Log("MyMethod got invoked");
  }
  ```

这两个属性位于 SingularityGroup.HotReload 命名空间之下。

