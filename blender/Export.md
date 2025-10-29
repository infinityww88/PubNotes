**Blender 的导出面板（Export Panel）** 右上角有一个下拉菜单叫 **“Operator Presets”**，它的作用是——

> 💡 **保存、加载和管理导出参数的预设（Preset）。**

---

### 🔍 详细解释：

当你导出文件（比如 `.fbx`、`.obj`、`.glb`、`.dae` 等）时，
Blender 的导出面板会列出许多参数选项，比如：

* 选中对象（Selected Objects Only）
* 应用变换（Apply Transform）
* 动画设置（Bake Animation）
* 轴向设置（Forward/Up）
* 缩放比例
* 包含内容（Mesh、Armature、Cameras、Lights 等）

这些设置有时会根据项目或引擎不同而变化，比如：

* 导出到 **Unity** 要用一种参数组合（例如 scale 要设为 0.01，使用预设就不必每次都重新设置 scale 了）
* 导出到 **Unreal Engine** 要用另一种组合
* 导出到 **WebGL** 或 **Three.js** 又不同

这时就可以使用 **Operator Presets**。

---

### ⚙️ 使用方法：

1. 在导出面板中调整好所有导出参数。
2. 点击右上角的 **“Operator Presets”** → **“Add Preset…”**
3. 输入一个名称，例如：

   * `Unity Export`
   * `Unreal Export`
   * `GLTF Minimal`
4. 下次再打开导出对话框时，从下拉菜单里选中该 Preset，
   Blender 会自动恢复你当时保存的全部导出参数。

---

### 🧠 注意事项：

* 这些 Presets 是 **全局保存** 的（存在用户配置文件中），不是只针对当前 `.blend` 文件。
* 如果你更新 Blender 版本或重置用户配置，旧的 Preset 可能需要重新导入。
* 某些导出器（比如 glTF）可能还会额外提供独立的 **内置预设**（如 “gltf embedded” / “gltf separate”）。

---

### ✅ 总结一句话：

> **Operator Presets** 就是让你可以“一键切换不同导出配置”的功能，
> 方便在不同项目或平台间快速复用导出设置。

---

非常好的问题 👍
这两个选项——**Path Mode** 和 **Batch Mode**——确实经常让人困惑，
它们是 Blender 导出面板中比较底层但非常实用的功能。
我们来分别详细讲讲它们的作用和区别 👇

---

## 🧭 一、Path Mode —— 控制**外部文件路径的处理方式**

**用途：决定导出文件中，外部资源（比如贴图）的路径该怎么写。**

当你导出模型（FBX、OBJ、DAE、GLTF 等）时，
模型文件中可能会**引用贴图文件**（texture images）。
这些贴图可能是：

* 相对路径（如 `"textures/wood.png"`）
* 绝对路径（如 `"C:\Projects\textures\wood.png"`）
* 或直接嵌入到文件里。

---

### 🔧 Path Mode 常见选项解释：

| 模式                           | 含义                                                    | 典型用途                           |
| ---------------------------- | ----------------------------------------------------- | ------------------------------ |
| **Auto**                     | Blender 尝试自动判断：如果可能，就使用相对路径，否则用绝对路径。                  | 默认选项，一般能满足大部分情况。               |
| **Absolute**                 | 导出的文件会记录完整的绝对路径（例如 `C:\MyProject\Textures\wood.png`）。 | 仅用于本地调试，不适合跨设备共享。              |
| **Relative**                 | 导出的文件引用路径相对于导出文件的位置（例如 `./textures/wood.png`）。        | ✅ 推荐，用于游戏引擎（Unity/Unreal）等项目中。 |
| **Copy**                     | Blender 会**复制贴图文件**到导出目录，并在文件中使用相对路径引用。               | 当你想打包导出模型+贴图一起交付时非常有用。         |
| **Strip Path**               | 仅写入文件名（去掉路径，如 `wood.png`）。                            | 一些引擎中需要贴图和模型放在同一文件夹时用。         |
| **Embed**（部分格式支持，如 FBX、glTF） | 直接将贴图数据嵌入文件内部。                                        | 单文件交付最方便（但文件体积会变大）。            |

---

### ✅ 举例：

假设你导出一个 `model.fbx` 到路径：

```
D:\Project\Models\
```

贴图在：

```
D:\Project\Textures\wood.png
```

| Path Mode  | FBX 文件内记录的贴图路径                    |
| ---------- | --------------------------------- |
| Auto       | `../Textures/wood.png`            |
| Absolute   | `D:\Project\Textures\wood.png`    |
| Relative   | `../Textures/wood.png`            |
| Copy       | （导出目录会复制 wood.png） → `./wood.png` |
| Strip Path | `wood.png`                        |
| Embed      | 贴图数据直接嵌入 `.fbx` 内部                |

---

## 📦 二、Batch Mode —— 控制**一次导出多个对象/集合的方式**

**用途：决定 Blender 在导出时，是否为多个对象或集合分别导出多个文件。**

---

### 🔧 Batch Mode 选项：

| 模式             | 含义                                    | 示例输出                                            |
| -------------- | ------------------------------------- | ----------------------------------------------- |
| **Off**        | 默认。所有选中的对象导出为一个文件。                    | `all_objects.fbx`                               |
| **Group**      | 每个 **Group（旧版本 Blender 使用）** 导出为一个文件。 | `groupA.fbx`, `groupB.fbx`                      |
| **Scene**      | 每个 **Scene** 导出为单独的文件。                | `scene1.fbx`, `scene2.fbx`                      |
| **Collection** | 每个 **Collection** 导出为单独的文件。           | `environment.fbx`, `character.fbx`, `props.fbx` |
| **Object**     | 每个对象导出为单独的文件。                         | `Cube.fbx`, `Sphere.fbx`, `Chair.fbx`           |

---

### ✅ 举例：

如果你选中三个对象：
`Cube`, `Sphere`, `Chair`

* **Batch Mode: Off** → 导出一个 `all.fbx`，包含三个对象
* **Batch Mode: Object** → 导出三个文件：

  ```
  Cube.fbx
  Sphere.fbx
  Chair.fbx
  ```
* **Batch Mode: Collection** → 如果这些对象在不同 Collection 里，
  就按 Collection 名分成多个 FBX 文件导出。

---

## 🧩 小结对比：

| 功能       | Path Mode           | Batch Mode           |
| -------- | ------------------- | -------------------- |
| **作用对象** | 贴图路径处理              | 导出对象的组织方式            |
| **控制内容** | 文件中贴图路径写法或嵌入方式      | 是否为每个对象/集合导出独立文件     |
| **常用设置** | `Relative` 或 `Copy` | `Off` 或 `Collection` |
| **应用场景** | 控制资源路径              | 批量导出模型               |
