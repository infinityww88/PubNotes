# Editing

Unwrap之后整理UV maps使得它可以被合理地textured或painted

- 将一些pieces缝合在一起
- 最小化浪费的空间
- 放大需要更多细节的faces
- 重新调整被拉伸的faces
- 缩小那些颗粒度大太显示太多细节（而实际不需要）的faces

尽可能让像素有所贡献

UV face可以小到一个像素，大到整个图像

先做主要调整，然后调整细节layout

## Transform

Move/Rotate/Scale/Shear/Axis Locking

## UV Options(TODO)

- Live Unwrap（TODO）
- Snap To Pixels
  - Disabled：UVs不会snapped
  - Corner：如果加载了image，强制UVs snap到image最近像素的corner
  - Center：如果加载了image，强制UVs snap到image最近像素的center
- Constraing To Image Bounds
  放置UVs移动出 0～1 UV范围

## Pin And Unpin（TODO）

Pin UVs使得它们在多次unwrap操作中不被移动。当unwrap一个模型时，有时锁定一些特定UVs非常有用，因此一个UV layout的部分保持相同shape，甚至相同位置。

选择UVs，选择Pin菜单或者P key。Unpin = Alt+P

## Pack Islands

打包一组UV islands使得它们尽可能优化地占据texture space

## Average Island Scale

缩放每个UV island使得它们接近相同的scale

## Minimize Stretch

通过最小化angles，减少UV拉伸。Relax UVs

## Stitch

join被选择的共享vertices的UVs。即使得共享的vertices对每个UVs具有相同的UV坐标

Stitching by distance：Use Limit & Limit Distance

## Copy Mirrored UV Coordinates

将选择的vertices的UVs从一侧复制到镜像的另一侧vertices

Axis Direction：Positive/Negative

Precision：用于查找镜像vertices的容差

## Mirror

在X或Y轴上镜像UVs

## Snap

UV Editor的Snapping类似Snapping in 3D（磁铁）

- Selected To Pixels：移动选择到最近的像素

  有时image可能只有几个像素表示调色盘。通过将UVs（=Vertices，只不过一个是2D坐标，一个是3D坐标）放到不同的颜色的像素上，可以为vertices设置不同的颜色。此时每个像素在UV Editor窗口中将显示为硕大的像素块。这个工具可以方便地将像素移动到指定像素块。但是对于高分辨率的image，期望的是为一个face赋予图像，而不是为单个vertices设置颜色，就不是这个工具的目的了

- Selected To Cursor：移动选择到2D Cursor

- Selected To Cursor（Offset）：移动选择的中心到2D Cursor，保持相对位置

- Selected To Adjacent Unselected：移动选择到相邻的未选择的元素

- Cursor to Pixel：移动2D Cursor到最近的pixel

- Cursor to Selected：移动2D Cursor到选择的中心

## Weld

移动选择的UVs到它们的平均位置

## Merge UVs By Distance

合并指定距离内的UVs

## Straighten/Align

将选择的UVs沿着X/Y轴排列成直线

## Proportional Editing

类似3D的Proportional Editing

## Show/Hide Faces

- 取消Hidden：Alt-H
- Hide Select：H
- Hide Unselect：Shift-H

## ExportUVLayout

导出UV Layout为png

## 3D View

- Face Mirror && Rotate UVs

  按照90旋转每个UV face

  镜像反转每个UV face
