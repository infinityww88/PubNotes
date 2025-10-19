# Armatures Editing

## Introduction

就像任何其他物体一样，可以在Edit Mode下编辑armature，类似mesh编辑

Armature编辑是编辑armature的reset position，默认姿势。一个armature在reset position下，所有bones在局部空间都没有旋转和缩放

所有之后创建的poses都是基于reset position的。因此如果修改了reset position，所有已存在的poses都会被修改。因此通常在开始skin和pose之前armature是定义好的

一些工具操作joints，另一些操作bones自身

- Add Menu
  
  Shift-A添加一个新bone

  - 一个单位长度
  - 朝向Global Z轴
  - root放置在3D Cursor
  - 和armature其他bones没有任何关系

- Locking Bones

防止一个bone被transform

对于连接bone，只lock其tip，如果它的root连接到一个unconnected bone，root仍然可以transform

对于unconnected，lock同时lock其root和tip

## Transform

tranform和mirror与mesh editing相同。Bone的root和tip就像mesh的vertices，bone自身就像mesh的edge，armature就像mesh。编辑root/tip就像编辑vertices，编辑bone自身就像编辑edge。

对于具有父子关系的bones，就像具有父子关系的mesh（object）

在Object Mode下，只能操作armature整体，所有bones都是mesh的内部元素。
在Pose Mode下，parent bone才能影响child bone
在Edit Mode下，没有父子关系的约束，只是简单的vertices/edges编辑，只是connected bones的tip和root就像vertices merge一样合并成了一个vertex

Bones有两种关系：Parented和Connected。Connected是Parented的更进一步。Connected bones的parent的tip与child的root焊接在一起，而Parented bones则没有，只是简单的父子关系

其他的transform工具的local axes意味着object的axes，而bones的transform工具是每个bone自己的axes

- Scale Radius：调整Envelope影响半径

- Scale Envelope Distance：调整基于Radius生成的胶囊体的offset来调整Envelop的volume大小

- Align Bones：将选择的bones调整到active bone相同的方向

## Bone Roll

调整bone沿着local Y轴（root和tail的连线）的旋转

- Recalculate Bone Roll

  对齐bone的roll角度，将bone的roll角度对齐到指定value
  
  - Axis Orientation：对齐对标的axis方向
    - Local Tangent：相对于bone和其parent对齐roll角度（X/Z）
    - Global Axis：在global axis上对齐roll角度（X/Y/Z）
    - Active Bone：对齐roll角度到active的roll角度
    - View Axis：在Viewport中对齐roll角度
    - Cursor：朝着3D cursor设置roll角度
  - Flip Axis：反转axis方向
  - Shortest Rotation：避免从当前值roll超过90度

- Set Bone Roll

## Extrude

从tail extrude一个child bone，从root extrude一个sibling bone。child bone的root和parent的tail是焊接在一起的，sibling bone的root只是初始位置在一起，但是并没有焊接在一起

Mirror Extruding(Shift-E)：默认与标准extrusion相同。但是如果开启X-Axis Mirror编辑选项，每个extruded tip将产生两个新的bone，具有相同的名字，只是左边的具有_L后缀，右边的具有_R后缀

通过delete而不是cancel删除新建的bones

### Mouse Clicks

就像mesh editing，当前选择一个bone，Ctrl-RMB extrude bone的tail到鼠标当前位置，深度位于View空间3D Cursor平面

## Duplicate

Shift-D

复制骨骼链也是连接的

复制的骨骼与原始骨骼具有相同的parent，但不是connected的

## Fill Between Joints

就像fill两个vertices为一个edge，在两个joint之间创建一个bone

新创建的bone被parented和connected

选择一个Joint，在Joint和3D Cursor之间创建一个Bone

## Split

断开selection bones chain的起始和结束处的连接，清除parent，成为armature下面一个独立的bones chain，内部的parent和connection仍然保持

## Separate Bones

就像mesh一样，将选择的bones分离为独立的armature object

## Subdivide

就像edge subdivide，subdivide bones将一个bone划分为多个bones。Subdivide所有选择的bones，保留既存的关系，subdivide bones总是构成一个connected的bones chain

## Switch Direction

反转选择的bones的方向，root变成tip，tip变成root

反转方向通常会打破bones所属的chains。但是如果反转一整个chain，反转之后的bones仍然是parented/connected的，但是是反序的

## Symmetrize

强制使选择的bones对称，或者使用已有的bones，或者创建新的bones（复制）。

沿着X轴进行镜像对称，但是对称的bone必须遵循命名约定（以.L .Left .R .Right等为后缀）

## Naming

Blender提供了一些工具可以利用左右对称风格的bones，以及另外一些自动为armature中的bones命名的工具

### Naming Convertions

命名约定不仅可以用来找到正确的bone，还可以告诉Blender哪两个是对应的部分

对于armatrure是镜像对称的情形，非常值得使骨骼遵循left/right命名约定。这允许你可以使用一些工具节约时间和精力

- handLeft/handRight
- hand_L/hand_R
- hand.l/hand.r
- hand-l/hand-r
- hand LEFT/hand RIGHT
- 所有例子如果将left/right放在名字前面也是有效的
- 短写L/R必须使用分隔符分割，handL/handR是无效的

### Flip Name

按照命名约定重新命名镜像骨骼名字，移除数字扩展

### Auto Name

自动添加后缀到所有bones，基于它们的root相对于armature原点和local 坐标系的位置，无关镜像，只判定position落在坐标系哪个区间

- AutoName Left/Right

  为所有root是+x坐标的bones添加.L后缀，-x添加.R

  如果root.x = 0，则基于tail.x添加后缀

  如果root.x和tail.x都为0，则只添加.，没有L/R

- AutoName Front/Back

  基于Y轴添加.Bk/.Fr

- AutoName Top/Bottom

  基于Z轴添加.Top/.Bot

## Change Layers(TODO)

- Change Armature Layers
- Change Bone Layers

## Parenting

可以在3D View或者Properties Panel中决定骨骼之间的关系，仅parented，还是parented and connected

Properties Panel就是左下角的Context面板

Make Parent菜单

- Connected：parented and connected
- Keep Offset：only parented

选择多个bones，前面的bones都parent到最后一个bone（active bone）上

可以在Properties Panel中选择bone的parent，以及是否connected

Alt-P（Clear Parent）或者Properties Panel可以清除bone关系

## Bone Properties

Display Wire

Multiply Vertex Group by Envelope：控制bone对geometry对影响，基于joints的radius

Deform：控制Envelope如何deform geometry

Lock：防止bone在Edit Mode下被编辑

## Delete

- Bones

删除bone的unselected children变成其parent的children，但是不connect

- Dissolve

Dissolve edge
