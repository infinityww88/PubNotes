# Unwrapping

## Introduction

在感觉mesh完成之后进行unwrap mesh

如果在一个模型已经unwrapped之后添加faces或subdivide已有的faces，blender将会自动根据已有的faces unwrapped新的faces（插值），但是可能需要进一步手工调整。

使用UV texture图像来指导进一步的geometry修改

### About UVs

UV map中，每个vertex/edge/face对应mesh中的一个vertex/edge/face，但反过来不一定。mesh中的一个vertex/edge可能对应UV map中的多个，只有face是一一映射的。UV map中只有face才是要维护的一一映射，vertex/edge的一对多映射只是副作用

### Getting Started

默认mesh是没有UV的（即vertex没有uv坐标）。先map faces，然后编辑它们。

进入UV Editing workspace

所有unwrapping都在Edit Mode下完成

- Workfyuayua

  - 如果需要，标记seam edges
  - 选择所有的mesh元素
  - 在UV Unwrap菜单中选择一个UV mapping方法
  - 调整unwrap设置
  - 添加一个test image，查看是否有变形distortion
  - 在UV Editor中调整UVs

## Mapping Types

简单的投影方法使用公式，通过将vertex的position从surface上向一个target point/axis/plane进行插值，将3D space映射到2D space

复杂的方法有特定的使用场景

### Unwrap

通过沿着seam切开并使mesh surface变得平坦进行unwrap，对于有机mesh很有用

标记seam；选择全部元素；unwrap

- Options

  - Correct Aspect：考虑Image的aspect，按照aspect缩放uv
  - Use Subdivision Surface Modifer：Map UVs时采用Subdivision Surface Modifier应用之后的vertex的position
  - Margin：UV islands之间的space

### Smart UV Project

基于一个angle阈值切开mesh。对于简单和合成的geometries非常有效，例如机械、建筑等

- Angle Limit：控制faces如何分组。更大的值将产生许多小的groups，但是更少distortion
- Island Margin：控制UV island packed在一起时离得多近
- Area Weight：基于face大小进行uv投影，更大的face具有更大的uv area

### Lightmap Pack

用于游戏，产生第二个uv map。face之间没有重叠

### Follow Active Quads

将选择faces按照连续的face loops展开

展开的方向依据active quad在UV上的方向，而不是Mesh上的方向

### Cube Projection

将Mesh投影在包围盒的6个plane上，产生6个uv islands

- Cube Size

Common选项通用于Cube、Cylinder和Sphere

- Correct Aspect：按照Image的aspect进行修正

- Clip to Bounds：任何位于（0，1）之外的UVs移动到最近的border

- Scale to Bounds：缩放整个map以纳入（0，1）之间

### Cylinder and Sphere Projection

Cylindrical和Spherical具有相同的选项

用于球型shapes，例如眼睛、行星等

- Direction
  - View On Poles：将视线方向作为极轴，自上向下unwrap
  - View On Equator：将视线方向作为赤道，指定一个极轴
  - Align To Object：使用一个object的transform指定极轴和方向
- Align
  - Polar ZX：polar位于X轴
  - Polar ZY：polar位于Y轴
- Radius

### Project from View

将mesh投影到相机平面

- Orthographic：使用平行投影，而不是透视投影

### Project from View (Bounds)

Scale To Bound & Correct Aspect

### Reset

使每个face填满UV grid（0，1），使得每个face居于相同的mapping

tileable image

## Seams

对具有很多缩进indentations（不同的缩进往往意味着不同的部分），标记seam可以限制和指导unwrapping过程

就像缝合的过程，seam就是衣服/image的两个不同部分末端连接在一起的边界。unwrapping时，就像剥橘子或给动物剥皮一样

尽可能使用少的seam；seam尽可能放在不起眼的地方

Workflow

- 创建Seam
- 选择全部faces进行unwrap
- 调整seam重复unwrap
- 手动调整UVs

### Marking Seams

Face Mode中Linked Faces检测连接在一起的faces，直到seam。如果有你期望的seam之外的face被选中，就知道seam不是连续的。seam不必时连续的（闭合的），只要它们解决了那些可能拉伸的区域就可以

seams的另一个用处是，限制unwrapped的face。例如一些区域将被其他mesh覆盖，它们不需要texture，因此也不需要unwrap

当unwrap任何双边对此的模型时，沿着mirror axis标记seam。这样当unwrap时，可以将两边对称的部分重叠地放置在一起，使它们可以使用相同的纹理映射

Note：**你不必最终使用一个完美的unwrapping方法应对任何事情任何地方。你可以进行多次UV unwrapping，对不同的区域faces使用不同的方法进行unwrap**

- Mark Seams from island

  将使用任何方法创建的UV islands的边界标记为seam，使得之后调整时，它们始终作为一个island
  