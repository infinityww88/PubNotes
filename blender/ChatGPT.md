# Blender Python API

## 请描述一下 Blender Python API 的 bpy.context 的具体作用和用法

Blender 无论是 UI 环境，还是 Script 环境，都是一个状态机。可以说 Script 环境就是 UI 环境的脚本模拟，因此也要想 UI 环境一样操作。就像操作 Blender UI 一样来编写脚本，只是需要找到每个操作对应的 API 而已。

bpy.context 保存 Blender 环境的当前状态，bpy.ops 都是在操作 bpy.context 中记录的当前状态。

Blender 的 Python API (bpy) 是一个强大的工具，用于自动化 Blender 的各种操作，创建插件，以及进行复杂的 3D 操作和动画。bpy.context 是这个 API 中一个非常重要的部分，它提供了对 Blender 当前状态的访问。下面是 bpy.context 的具体作用和用法：

### 作用

bpy.context 用于获取 Blender 当前运行环境中的上下文信息，包括但不限于：

当前活动的对象 (bpy.context.object)
当前选择的对象 (bpy.context.selected_objects)
当前活动的场景 (bpy.context.scene)
当前窗口、区域和空间 (bpy.context.window, bpy.context.area, bpy.context.space_data)
当前模式 (编辑模式、对象模式等) (bpy.context.mode)
这些信息允许脚本根据 Blender 的当前状态做出响应，比如在特定对象上执行操作、根据当前选择执行操作等。

### 用法

下面是一些常见的 bpy.context 用法示例：

获取当前活动的对象

```python
import bpy

obj = bpy.context.object
if obj:
    print("当前活动的对象是：", obj.name)
else:
    print("没有活动对象")
```

获取当前选择的对象

```python
import bpy

selected_objects = bpy.context.selected_objects
if selected_objects:
    print("当前选择的对象：")
    for obj in selected_objects:
        print(obj.name)
else:
    print("没有选择对象")
```

获取当前活动的场景

```python
import bpy

scene = bpy.context.scene
print("当前活动的场景是：", scene.name)
```

根据当前模式执行操作

```python
import bpy

mode = bpy.context.mode
if mode == 'EDIT_MESH':
    print("当前是编辑模式")
    # 在编辑模式下执行特定操作
elif mode == 'OBJECT':
    print("当前是对象模式")
    # 在对象模式下执行特定操作
```

修改当前场景的帧数

```python
import bpy

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250
print("帧范围设置为：1 到 250")
```

注意事项
上下文依赖性：许多 bpy 操作都依赖于上下文。例如，试图在对象模式下执行只能在编辑模式下运行的操作会导致错误。
实时更新：bpy.context 是动态的，反映了 Blender 当前的实时状态，因此在脚本执行过程中，某些上下文信息可能会发生变化。
通过使用 bpy.context，脚本可以对 Blender 的当前状态做出智能响应，从而实现更复杂和灵活的自动化操作。

## bpy.data

Blender 的 Python API (bpy) 中的 bpy.data 模块是一个强大的工具，用于访问和操作 Blender 内部的数据块。bpy.data 提供了对所有数据块的访问权限，包括场景、对象、材质、纹理、灯光、相机等。通过使用 bpy.data，可以创建、修改和删除这些数据块，从而实现对 3D 场景的全面控制。

### 作用

bpy.data 的主要作用包括：

- 访问 Blender 的所有数据块：包括对象、网格、材质、纹理、灯光、相机等。
- 创建新的数据块：例如，可以创建新的网格对象或材质。
- 删除现有的数据块：例如，删除不需要的对象或材质。
- 修改数据块的属性：例如，修改对象的位置、旋转、缩放，或材质的颜色等属性。

### 用法

下面是一些常见的 bpy.data 用法示例：

获取所有对象

```python
import bpy

objects = bpy.data.objects
for obj in objects:
    print(obj.name)
```

获取所有材质

```python
import bpy

materials = bpy.data.materials
for mat in materials:
    print(mat.name)
```

获取特定类型的数据块

```python
import bpy

# 获取所有网格对象
meshes = bpy.data.meshes
for mesh in meshes:
    print(mesh.name)
```


创建一个新的网格对象

```python
import bpy

# 创建一个新的网格
mesh = bpy.data.meshes.new(name="NewMesh")

# 创建一个新的对象并链接到网格
obj = bpy.data.objects.new(name="NewObject", object_data=mesh)

# 将对象添加到当前场景中
bpy.context.collection.objects.link(obj)
```

创建一个新的材质

```python
import bpy

# 创建一个新的材质
material = bpy.data.materials.new(name="NewMaterial")

# 将材质赋予当前活动对象
if bpy.context.object:
    bpy.context.object.data.materials.append(material)
```

删除一个对象

```python
import bpy

# 获取要删除的对象
obj = bpy.data.objects.get("ObjectName")

# 从场景中移除并删除对象
if obj:
    bpy.data.objects.remove(obj)
```

删除一个材质

```python
import bpy

# 获取要删除的材质
mat = bpy.data.materials.get("MaterialName")

# 删除材质
if mat:
    bpy.data.materials.remove(mat)
```

注意事项

- 引用计数：删除数据块时，需要确保没有其他数据块引用它，否则可能会导致问题。
- 上下文问题：操作数据块时，有些操作依赖于上下文，可能需要切换到正确的上下文才能执行。
- 数据块类型：bpy.data 提供了对多种类型数据块的访问，每种类型的数据块都有其特定的属性和方法，需要根据具体类型进行操作。

通过 bpy.data，可以全面控制 Blender 的所有数据块，从而实现各种复杂的 3D 场景构建和修改操作。

## bpy.ops

Blender 的 Python API (bpy) 中的 bpy.ops 模块用于调用 Blender 的各种操作（operators）。这些操作是 Blender 中的命令，执行各种任务，例如添加对象、转换对象、修改网格等。bpy.ops 是 Blender 中执行动作的核心接口，通过它可以模拟用户在图形界面中的操作。

### 作用

bpy.ops 的主要作用包括：

- 执行各种操作：包括对象的创建、删除、转换、修改、渲染等。
- 自动化复杂任务：通过脚本批量执行一系列操作。
- 模拟用户输入：通过代码模拟用户在 Blender 界面上的各种操作。

### 用法

bpy.ops 按照操作类型分类，例如 object 操作、mesh 操作、transform 操作等。每个操作通常由一个模块和一个操作名称组成，使用点号分隔。例如，bpy.ops.object.select_all(action='SELECT') 用于选择所有对象。

下面是一些常见的 bpy.ops 用法示例：

创建一个新立方体对象

```python
import bpy

bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
```

删除当前选择的对象

```python
import bpy

bpy.ops.object.delete()
```

选择所有对象

```python
import bpy

bpy.ops.object.select_all(action='SELECT')
```
进入编辑模式并细分网格

```python
import bpy

# 进入编辑模式
bpy.ops.object.mode_set(mode='EDIT')

# 细分网格
bpy.ops.mesh.subdivide(number_cuts=2)

# 返回对象模式
bpy.ops.object.mode_set(mode='OBJECT')
```

翻转选中的面

```python
import bpy

# 假设当前在编辑模式下并选择了一些面
bpy.ops.mesh.flip_normals()
```

移动对象

```python
import bpy

# 移动当前选择的对象
bpy.ops.transform.translate(value=(1, 0, 0))
```

旋转对象

```python
import bpy

# 旋转当前选择的对象
bpy.ops.transform.rotate(value=1.5708, orient_axis='Z')  # 90 degrees in radians
```

渲染当前帧

```python
import bpy

bpy.ops.render.render()
```

保存当前文件

```python
import bpy

bpy.ops.wm.save_as_mainfile(filepath='/path/to/your/file.blend')
```

注意事项

- 上下文依赖性：许多 bpy.ops 操作依赖于当前的上下文，例如当前模式（对象模式、编辑模式等）、当前选择的对象等。确保在正确的上下文中执行操作，否则会导致错误。
- 返回值和报告：许多操作返回一个字典，包含操作的结果和状态报告。例如，{'FINISHED'} 表示操作成功完成，{'CANCELLED'} 表示操作被取消。
- 操作参数：大多数操作接受参数，这些参数通常可以在 Blender 的操作面板中找到。例如，bpy.ops.mesh.primitive_cube_add(size=2) 会创建一个边长为 2 的立方体。

通过 bpy.ops，可以自动化和批量执行 Blender 中的各种操作，使得复杂的任务变得更加简单和高效。

## bpy.types

Blender 的 Python API (bpy) 中的 bpy.types 模块提供了对 Blender 内部各种数据类型的访问和操作。bpy.types 是定义和扩展 Blender 数据结构的核心模块，它允许开发者创建自定义属性、操作符、面板、UI 元素等。通过使用 bpy.types，可以扩展 Blender 的功能，创建复杂的插件和自定义工具。

### 作用

bpy.types 的主要作用包括：

- 定义和扩展数据类型：创建自定义的操作符、面板、属性组等。
- 访问内置数据类型：例如对象、网格、材质、灯光、场景等。
- 注册和注销自定义类型：将自定义类型注册到 Blender 中，使其可用。
- 创建和管理 UI 元素：定义自定义的界面布局和控件。

### 用法

创建自定义操作符

自定义操作符是可以通过 bpy.ops 调用的自定义命令。以下是一个创建自定义操作符的示例：

```python
import bpy

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        self.report({'INFO'}, "Hello World")
        return {'FINISHED'}

# 注册操作符
bpy.utils.register_class(SimpleOperator)

# 调用操作符
bpy.ops.object.simple_operator()

# 注销操作符
bpy.utils.unregister_class(SimpleOperator)
```

创建自定义面板

自定义面板可以添加到 Blender 的 UI 中，例如属性面板或工具面板。以下是一个创建自定义面板的示例：

```python
import bpy

class SimplePanel(bpy.types.Panel):
    bl_label = "Simple Panel"
    bl_idname = "OBJECT_PT_simple_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Hello World")
        layout.operator("object.simple_operator")

# 注册面板
bpy.utils.register_class(SimplePanel)

# 注销面板
bpy.utils.unregister_class(SimplePanel)
```

创建自定义属性组

自定义属性组可以用于存储和管理自定义属性。以下是一个创建自定义属性组的示例：

```python
import bpy

class SimplePropertyGroup(bpy.types.PropertyGroup):
    my_float: bpy.props.FloatProperty(name="My Float")
    my_int: bpy.props.IntProperty(name="My Int")
    my_string: bpy.props.StringProperty(name="My String")

# 注册属性组
bpy.utils.register_class(SimplePropertyGroup)

# 将属性组添加到对象属性中
bpy.types.Object.my_custom_properties = bpy.props.PointerProperty(type=SimplePropertyGroup)

# 使用自定义属性
obj = bpy.context.object
obj.my_custom_properties.my_float = 1.23
print(obj.my_custom_properties.my_float)

# 注销属性组
del bpy.types.Object.my_custom_properties
bpy.utils.unregister_class(SimplePropertyGroup)
```

注意事项

- 注册和注销：所有自定义类型在使用前必须注册，在不再需要时应注销，以避免内存泄漏和其他问题。
- 命名规则：自定义操作符的 bl_idname 必须遵循命名规则，通常是 category.name 的格式，例如 object.simple_operator。
- UI 更新：自定义面板和属性在更改后需要调用 context.area.tag_redraw() 来刷新 UI。

通过 bpy.types，可以创建复杂的自定义功能，扩展 Blender 的界面和工具，从而实现更高效的工作流程和更强大的插件。
