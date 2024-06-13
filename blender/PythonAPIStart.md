# Python API Start

Blender Python API features：

- 编辑任何 UI 可以编辑的数据（Scenes，Meshes，Particles 等等）
- 修改 user preferences，keymaps 和 themes
- 使用自己的设置运行工具
- 创建 UI 元素，例如 menus，headers，panels
- 创建新的工具
- 创建交互工具
- 订阅数据和属性的改变
- 使用 Python 在 3D Viewport 绘制

开始之前注意：

- Python Console 非常适合 one-liners（一行代码），它能够自动补全，可以快速查看 API。

- Blender 的 Preferences > Interface > Display > Tooltips 可以开启两个选项：

  - User Tooltips
  
    开启后，当鼠标滑过一个控件时，显示一个 tooltip。tip 将解释控件的功能，显示关联的 hotkey（如果有的话）。
  
  - Python Tooltips
  
    显示 tooltip 下的属性的 Python 信息。

- Button tooltips 显示 Python 的属性和 operator 名字。

- 在按钮上右键点击上下文菜单，可以直接连接到 API 文档（online menu）

- text editor 的模板菜单包含很多 python 实例


## 运行脚本

运行 Python 脚本最常用的两个方法是使用内置的 text editor，或在 Python console 输入命令。

从 text editor 可以打开 .py 文件，或者从剪贴板粘贴代码，然后使用 Run Script。

运行 Python 脚本 print 的输出打印到 System Console。如果没有打开，可以使用 Window > Toggle System Console 打开。但是这个选项只在 Windows 可用。对于其他 OS，从 System Console（命令行窗口）中打开 Blender，然后打开 Blender 的 System Console 就可以显式 Blender 脚本的输出，这个方法也可以 Windows 上使用。

Python Console 通常用于输入 snippets 和测试，来即时获得回馈，但是也可以粘贴整块脚本。脚本也可以在命令行中使用 Blender 运行，但是对于学习 Blender 脚本，这不是必须的。

## 数据访问

### 访问 Data-Blocks

可以使用 Python API 访问 Blender data，就像 animation system 或 user interface 一样。这意味着任何可以通过 button 改变的设置也可以使用 Python 改变。从当前加载的 blend-file 访问数据通过 bpy.data 完成，例如：

```py
bpy.data.objects
bpy.data.scenes
bpy.data.materials
```

### 访问 Collections

可以用 index 或 string 访问 collection 的成员。不想 Python 的字典，两个方法都是可以使用的。但是一个 memeber 的 index 在 Blender 运行时修改。

```py
list(bpy.data.objects)
bpy.data.objects["cube"]
bpy.data.objects[0]
```

### 访问 Attributes

一旦有了一个 data-block，例如 material，object，collection等等，它的属性就可以想通过 UI 改变 setting 一样被访问。事实上，每个 button 的 tooltip 可以展示 Python attribute，这可以提示子如何在脚本中改变这个属性。

```py
bpy.data.objects[0].name
bpy.data.scenes["Scene"]
bpy.data.materials.new("MyMaterial")
```

使用 Python Console 可以方便地用来测试要访问什么数据，它支持自动补全，提供了一个快速浏览 data 的方法。

```py
bpy.data.scenes[0].render.resolution_percentage
bpy.data.scenes[0].objects["Torus"].data.vertices[0].co.x
```

### 数据创建/移除

和一般的 Python API 不同，bpy 的 data blocks 不能通过调用 class（构造函数）来创建。

```py
>>> bpy.types.Mesh()
Traceback (most recent call last):
  File "<blender_console>", line 1, in <module>
TypeError: bpy_struct.__new__(type): expected a single argument
```

这是故意设计的 API 模式。Blender Python API 不能在 Blender database（通过 bpy.data 访问）之外创建 Bldner data，因为它们被 Blender 管理（save，load，undo，append 等等）。

Data 通过 bpy.data 的 collections 的方法来添加和移除。

```py
>>> mesh = bpy.data.meshes.new(name="MyMesh")
>>> print(mesh)
<bpy_struct, Mesh("MyMesh.001")>
```

移除数据

```py
bpy.data.meshes.remove(mesh)
```

### 自定义属性

Python 可以在任何具有 ID（可以被 linked 以及从 bpy.data 访问的 data）的 data-block 上访问属性。如果要为 data-block 赋予一个 property，可以采用你自己的名字，这会创建或覆写相应的属性。

这些数据保存在 blend-file，并且 copied with objects。

```py
bpy.context.object["MyOwnProperty"] = 42

if "SomeProp" in bpy.context.object:
    print("Property found")

# Use the get function like a Python dictionary
# which can have a fallback value.
value = bpy.data.scenes["Scene"].get("test_prop", "fallback value")

# dictionaries can be assigned as long as they only use basic types.
collection = bpy.data.collections.new("MyTestCollection")
collection["MySettings"] = {"foo": 10, "bar": "spam", "baz": {}}

del collection["MySettings"]
```

注意这些属性只能被赋予基本的 Python 类型：

- int, float, string
- array of ints/floats
- dictionary(key 只支持 string，value 必须是基本类型）

### Context

尽管能够通过 name 或作为一个 list 直接访问 data（所有 data block）非常有用，操作 user 的 selection 更常见。

总是可以使用 bpy.context 访问 context，并且可以得到 active object，scene，tool settings，以及很多其他属性。

```py
>>> bpy.context.object
>>> bpy.context.selected_objects
>>> bpy.context.visible_bones
```

context 是只读的，这意味着这些 values 不能直接修改。但是它们可以通过 running API 或 data API 修改。

因此 bpy.context.active_object = obj 将会抛出一个 error。但是 bpy.context.view_layer.objects.active = obj 将会正常工作（仅限 bpy.context 的属性只读）。

### Operators(Tools)

Operators 是 user 通过 button，menu items，或 key shortcuts 访问的 tools。从用户视角看，它们是 tool，但是 Python 可以通过 bpy.ops 模块使用它自己的设置来运行这些功能。

```py
>>> bpy.ops.mesh.flip_normals()
{'FINISHED'}
>>> bpy.ops.mesh.hide(unselected=False)
{'FINISHED'}
>>> bpy.ops.object.transform_apply()
{'FINISHED'}
```

### Operator Poll()

很多 operators 有一个 poll 函数，可以检查 cursor 是否在一个有效的 area，或者 objects 是否在正确的模式下（Editor Mode，Weight Paint Mode 等等）。如果一个 operator 的 poll 函数在 Python 中失败，将会抛出异常。

例如，在 console 调用 bpy.ops.view3d.render_border() 将会抛出异常：

```
RuntimeError: Operator bpy.ops.view3d.render_border.poll() failed, context is incorrect
```

在这种情况下，context 必须是 3D Viewport 并带有一个 active camera。

要避免 try-except，可以调用 operators 自己的 poll() 函数来检查 operator 是否位于它可以运行的 context：

```py
if bpy.ops.view3d.render_border.poll():
    bpy.ops.view3d.render_border()
```



