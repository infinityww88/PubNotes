# Keyframes

## Introduction

存储属性值的时间标记

目的是为了插值动画

Dope Sheet

### Visualization

3D View中，如果当前frame是当前物体的keyframe，物体名字显示为黄色，前面的数字表示当前的关键帧序号

### Interpolation

Keyframe插值通过animation curves表示和插值

Interpolation Mode是为每个keyframe指定曲线如何从一个key插值到下一个key的主要设置

- Constant：从当前key到下一个key是常量的（方波）
- Linear：从当前key到下一个key是线性的（三角波）
- Quadratic：从当前key到下一个key是二次曲线变换
- Bezier：从当前key到下一个key是贝塞尔曲线变换

Extrapolation Mode指示curve如何扩展到第一个keyframe之前和最后一个keyframe之后。主要可用选项是

- Constant：first keyframe之前使用first keyframe到值，last keyframe之后使用last keyframe之后到值
- Linear：first keyframe之前使用first keyframe处的曲线切线，last keyframe之后使用last keyframe处的曲线切线

可以将曲线配置成循环的seamless loop

Bezier插值通过handles控制。Handles具有handle type和位置。Free和Aligned Handles的位置必须在Graph Editor中手动设置，而Vector、Automatic和Auto Clamped Handles通过keyframe的值自动计算

Interpolation、Extrapolation和Handle Type还可以在Dope Sheet editor中改变

### Keyframe Types（TODO）

### Handles & Interpolation Mode Display（TODO）

## Editing

### Insert Keyframes

- 在3D View中，按下I key弹出菜单选项添加那些属性到keyframe
- 在Blender任何面板任何可动画的属性上（例如Transform panel的location属性，Constraint panel的influence属性）按下I key或右键菜单将这个属性插入当前keyframe

- Auto Keyframe：Timeline header的record按钮。如果transform类型的属性发生改变，Auto Keyframe自动添加keyframes到当前frame

### Delete Keyframes

- 在3D view中，按Alt-I从当前frame移除选择的objects的key
- 在属性面板上按Alt-I，或者右键菜单Delete Keyframe

### Clear Keyframes

Object>Animation>Clear Keyframes
移除选择的object的所有keyframes

### Editing Keyframes

Keyframes可以在两个Editor中编辑，Graph Editor或者Dope Sheet

### Workflow

- 在Timeline或者其他Animation Editor中，将frame设置到1
- 在Object Mode下选择Cube object
- 在3D view中按I key弹出菜单，选择Insert Keyframe Menu/LocRotScale，这将在frame 1记录Cube的location、rotation和scale
- 将frame设置到100
- 使用Move（G），Rotate（R），Scale（S）变换Cube
- 在3D View中按I key，在弹出的菜单中选择Insert Keyframe Menu/LocRotScale

要测试动画，按spacebar播放

## Keying Sets

Keying Sets是属性的集合。它们被用于同时记录多个属性

当在3D View中按I key时，Blender会将当前激活的keying set中的所有属性添加到keyframes

有一些内置Keying Sets，也可以自定义Keying Sets

选择和使用Keying Set：

- Timeline Header的Keying popover选择Active Keying Set
- 在Properties Panel中的Scene Tab的Keying Set Panel选择
- 在3D View中按Shift-Ctrl-Alt-I选择

### Keying Set Panel

添加、选择、管理自定义Keying Sets

Active Keying Set：添加、选择Keying Set

属性：Keying Set属性

- Description
- Export to File：导出Keying Set到一个Python脚本File.py。要从File.py重新添加keying set，在Text Editor中打开并运行File.py
- Keyframing Setting（General Override）：控制Keying Set中的所有属性Preferences中的相同设置覆盖这些设置
  - Only Needed：只在相关F-Curves需要的地方添加keyframes
  - Visual Keying：基于visual transformaiton添加keyframes
  - XYZ to RGB：对新的F-Curve，为property set设置颜色为RGB，例如Location XYZ

### Active Keying Set Panel

添加属性到active Keying Set

Active Keying Set Paths：paths的集合，每个path有一个到属性的Data Path（Python属性的路径）

Target：

- ID-Block：为属性设置ID 类型和Object IDs Data Path（即场景中哪个物体，data path就是Python从bty对象开始向下应用到object.property的路径）
- Data Path：设置属性相对于Object的路径（例如Location，Rotation，Scale）
- Array All Items：使用Data Path的All Items，或者选择指定属性的array索引

F-Curve Grouping：控制将channels添加到哪个group，Keying Set Name/None/Named Group

Keyframing Setting（Active Set Override）：控制Keying Set中的独立属性

- Only Needed：只在F-Curve需要的地方插入keyframes
- Visual Keying
- XYZ to RGB

### Adding Properties

一些添加属性到keying set的方法

- 在属性面板右键菜单选择 Add Single to Keying Set 或者 Add All to Keying Set
- 鼠标hover属性，按K键，All All to Keying Set

### Whole Character Keying Set（TODO）
