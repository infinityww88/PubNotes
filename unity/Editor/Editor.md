# Undo

在对 Object 属性改变之前，调用 Undo.RecordObject(s) 将其记录到 Undo stack，然后对属性进行修改即可。没有 End Record 之类的结束 API，Unity 将 Editor 一帧中的所有 Undo 记录合并为一个，添加到 stack 中。

RecordObject 记录需要指定一个名字。但是记录的 Undo 操作不会出现在 Edit 菜单中，似乎 Edit 菜单只能显示 Editor 界面操作的记录。但是 RecordObject 仍然将 Undo 记录添加到了 stack 中，只需按 Ctrl-Z 就可以回退。

RecordObject 记录的是 Object，不是 GameObject。如果修改某个组件，必须记录对此组件的修改，而不是记录它的 GameObject。因为 GameObject 也是 Object，修改的组件只是它的引用，只要引用没变，GameObject 就没变。例如，若要修改 transform，并记录 Undo，必须记录 transform 组件本身，不能是 GameObject，否则就会发现没有记录添加到 Undo stack。

# MenuItem

MenuItem、Odin、Monkey、Quantum Console 这些为系统添加命令的系统都是直接标记要成为命令的方法（通常是 static 的），跟 class 无关，直接在方法上标记即可，不管在哪个类。

MenuItem 将需要显示为菜单的静态方法（不管在哪个类）用 ​​[MenuItem("路径/名称")]​​ 标记，方法必须是 ​​static​​，脚本需放在 ​​Assets/Editor​​ 文件夹下并使用 ​​UnityEditor​​ 命名空间。

菜单路径支持多级，例如：​​"Tools/MyTool/DoIt"​​。

最简单的使用就是如此而已，为任何一个类的静态方法标记 [MenuItem(path)]。

这个菜单项目还会出现在 Project Window 的右键菜单中。

## 高级用法

### 菜单校验函数

可以为菜单添加一个验证函数，验证函数是与菜单函数同名且 MenuItem 属性增加第二个参数 true（表示执行检验），在显示或执行同名菜单项目前调用。返回 false 时，菜单项会变灰或禁用。

```C#
[MenuItem("MyMenu/Log Selected Transform Name")]
private static void LogSelectedTransformName()
{
    Debug.Log("Selected: " + Selection.activeTransform?.name);
}

// 验证函数：只有选中了 Transform 才启用
[MenuItem("MyMenu/Log Selected Transform Name", true)]
private static bool ValidateLogSelectedTransformName()
{
    return Selection.activeTransform != null;
}
```

### 快捷键

在菜单路径后添加快捷键，需要与菜单名用空格分开。

快捷键的修饰键（前缀键）写法：
​
- ​%​​：Ctrl（Windows/Linux）或 Cmd（macOS）
- ​​#​​：Shift
- ​&​​：Alt
- _​：普通按键（如 ​​_g​​ 表示按 ​​G​​）

特殊键：​​LEFT/RIGHT/UP/DOWN、F1..F12、HOME、END、PGUP、PGDN、INS、DEL、TAB、SPACE​​。

示例：

- "%g"​​ → Ctrl/Cmd+G
- ​​"#&g"​​ → Shift+Alt+G
- ​​"_g"​​ → 单按 G
- ​​"#LEFT"​​ → Shift+左箭头

快捷键字符串必须与菜单名之间有空格，否则不生效。

### 优先级与分组

- 通过第三个参数 ​​priority​​ 控制菜单项的顺序，数值越小越靠上，默认值 ​​1000​​。
- 相邻菜单项的优先级差 ​​≥ 11​​ 会在中间插入分隔线，便于分组。

```C#
[MenuItem("MyMenu/A", false, 1)]
private static void ItemA() { }

[MenuItem("MyMenu/B", false, 12)] // 与 A 之间差 11，会分隔
private static void ItemB() { }
```

### 在 GameObject Hierarchy 创建对象与上下文菜单

- 在 ​​GameObject/​​ 菜单下创建对象时，若希望出现在 ​​Hierarchy 右键创建下拉​​与​​层级右键菜单​​，需将优先级设为 ​​10​​（与内置创建项同组）。
- 创建对象时请调用：
  - ​GameObjectUtility.SetParentAndAlign​​：确保在 Hierarchy 右键点击时正确设置父子关系与对齐。
  - ​Undo.RegisterCreatedObjectUndo​​：让创建可撤销（Ctrl+Z）。
  - 将 ​​Selection.activeObject​​ 设为新对象，便于立即选中。

```C#
using UnityEditor;
using UnityEngine;

public static class CreateTools
{
    [MenuItem("GameObject/MyCategory/Custom Cube", false, 10)]
    private static void CreateCustomCube(MenuCommand menuCommand)
    {
        var go = new GameObject("Custom Cube");
        GameObjectUtility.SetParentAndAlign(go, menuCommand.context as GameObject);
        Undo.RegisterCreatedObjectUndo(go, "Create " + go.name);
        Selection.activeObject = go;
    }
}
```
### 在 Inspector 中为组件添加右键菜单

- 使用 ​​"CONTEXT/组件名/菜单名"​​ 为组件添加上下文菜单（Inspector 右键）。
- 回调方法可接收 ​​MenuCommand command​​，通过 ​​command.context​​ 获取被右键的组件或对象。

```C#
using UnityEditor;
using UnityEngine;

public static class ComponentContextMenu
{
    [MenuItem("CONTEXT/Rigidbody/SetMass")]
    private static void SetMass(MenuCommand command)
    {
        var rb = command.context as Rigidbody;
        if (rb != null)
        {
            rb.mass = 5f;
            Debug.Log($"设置 Rigidbody 质量为 {rb.mass}");
        }
    }
}
```

该方式适合为组件暴露“就地修改”的便捷操作。