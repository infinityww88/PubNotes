# HybridCLR

## 更换引擎版本或打包目标平台后必须重新 install（菜单：HybridCLR > Installer）

这是因为点击 install 之后，会将 Unity Editor 的本地文件夹中的 il2cpp 代码拷贝到项目中名为 HybridCLRData/LocalIl2CppData-{current platform} Editor 文件夹下。不同的 Unity 版本中的 il2cpp 源码也不一样，可能会导致生成出来的 cpp 文件中的编译有错误。同理不同平台 Unity 中的 il2cpp 代码也不一样，更换目标平台后也要重新 install。

## 快速找到 Assembly-CSharp 中引用热更程序集的地方

由于 HybridCLR 在执行的时候会将热更程序集剔除掉，如果 Assembly-CSharp 是作为 AOT 程序集，那可能会出现 Assembly-CSharp 的代码中引用了热更程序集的情况，此时打包会报错。此时，可以找到热更程序集的 .asmdef 文件，然后在 inspector 中关闭 auto referenced 选项。

这样 Assembly-CSharp 就不会再引用此热更程序集，会出现编译错误帮助定位。HybridCLR 教程上是建议所有热更程序集都一直禁用此选项的，但如果禁用掉会导致 Assembly-CSharp-Editor 程序集也无法引用此热更程序集了，很多自己写的编辑器就没法用了。

```
如果项目把 Assembly-CSharp 作为 AOT 程序集，强烈建议关闭热更新程序集的 auto reference 选项。因为 Assembly-CSharp 是最顶层 assembly，开启此选项后会自动引用剩余所有 assembly，包括热更新程序集，很容易就出现失误引用热更新程序集导致打包失败的情况。
```

既然是作为热更新程序集，是不应该放在预置程序集中的，而是运行时动态下载的。


热更新程序集 dll 仍然是普通的 dll，与其他 dll 没有区别。HybridCLR 的作用是对 il2cpp 进行了修改，添加了解释器模块，对运行时加载的 dll 可以解释执行，而不是以普通的 dll 加载的方式融入到原本的程序集中。一些平台（主要是 iOS）禁止在运行时修改已发布程序的预置程序集，因此就无法动态加载 dll。一般热更新的方式是不修改预置程序集，而是在其中安插一个 vm，在 vm 中运行动态代码，例如 XLua，HybridCLR 也是类似，只是它的动态代码不是 lua 脚本，而是普通的 dll。

HybridCLR 修改的 ilcpp 使得它变成全功能的 mono，既可以运行 AOT，也可以通过 System.Reflection.Assembly.Load 动态加载 dll（解释执行）。

每个 Assembly Definition 定义一个程序集，它下面的所有脚本被编译为一个 dll。dll 默认只能引用自己模块内部的代码和类型，要引用其他模块的代码类型，dll 的 Assembly Definition 必须为程序集指定要引用的相应程序集。默认 Unity 会使所有程序集都引用 UnityEngine、UnityEditor dll，因此无需显式指定对 UnityEngine 和 UnityEditor 的引用（尤其是 Assembly-CSharp 程序集）。但是其他的程序集之间的相互引用必须要显式指定。

Assembly-CSharp 也是被 Unity 特殊处理的程序集，所有没有指定程序集的代码都编译到这个程序集，并且它自动引用所有导入的 dll 或程序集。但是它不应该引用热更新程序集的代码，因为这违反热更新的意义，热更新程序集应该运行时动态下载。而其他程序集以及导入的 dll 也不能引用 Assembly-CSharp，因为通常前者都是自包含的第三方插件，不应该依赖它自身模块之外的东西。所以 Unity 没有提供引用 Assembly-CSharp 程序集的方法。

总而言之：

- 所有的程序集都自动引用 UnityEngine 和 UnityEditor 程序集，无需显式指定
- Assembly-CSharp 自动引用所有其他第三方和自定义的程序集
- 第三方和自定义的程序集之间必须显式指定引用才能使用对方的代码和类型

热更新代码不仅要编译为单独的程序集，它编译后的 dll 还要从 Assembly-CSharp 引用的程序集中排除，以免于被其引用，否则会打包失败。

热更新 dll 和普通的 dll 一样，只是它是通过 Load 动态加载而被解释执行的，而它引用的其他 dll 如果是 AOT（预置 dll）的，那些 dll 中的代码仍然是 AOT 执行的（因为使用和执行这些 dll 的代码不仅只有热更新 dll，还会被其他 dll 尤其是 Assembly-CSharp 调用）。

因此自定义的程序集不能引用 Assembly-CSharp，因此要将一部分代码和类型随 app 分发，然后在热更新集中引用这些预分发的代码类型，它们也必须编译到自定义程序集中，然后自定义程序集的 dll 随 app 分发，并在热更新程序集中指定对它的引用。

可以将 app 的主体逻辑（即原本放在 Assembly-CSharp 中的代码）放在单独的自定义程序集，并将生成的 dll 随 app 分发，因为这样的 dll 仍然是 AOT 执行的，只是所在的程序集变了而已。这样的有好处也有坏处：

- 好处是 热更新程序集可以引用它，使用它里面（预置）的代码和类型
- 坏处是 它使用的所有第三方插件和 dll 都必须要显式在 Assembly Definition 中指定，而 Assembly-CSharp 程序集则不需要，因为它自动引用所有导入的 dll

## 错误地将Editor文件夹放到了asmdef文件管理的文件夹下

接入 HybridCLR 后，肯定会自行创 建asmdef 文件来新建热更程序集，但是 asmdef 文件的管辖范围是其所在文件夹下的所有代码，如果之前在其管辖范围内创建过 Editor 文件夹并写了 Editor 代码，这些 Editor 代码的程序集会从 Assembly-CSharp-Editor 变为你新建的程序集，打包时就会报错。

建议是所有 Editor 代码都放在一个位于根部的 Editor 文件夹中。

## 插件没有自定义程序集

某些集成到 Assets 中的插件没有使用自定义的程序集，这些插件的代码就会被归于 Assembly-CSharp 中，而 Assembly-CSharp 是只被 Assembly-CSharp-Editor 引用的，热更程序集就不能引用插件代码了。这会导致热更程序集中所有依赖了该插件的代码报错，解决办法是自行为其创建一个asmdef文件。

## 代码剥离

Unity 会对所有程序集（无论是 Unity 标准库，C# 标准库，还是自定义或第三方插件的程序集）进行代码剥离。如果要进行热更新，即使是自定义的程序集，也要在 link.xml 标记为 preserve，否则会在 Build 中被剥离。

