# Curve

## Transform

Bezier可以通过transform控制点和handle变换，Nurbs则只有控制点

- Move/Rotate/Scale
- ToSphere/Shear/Warp/Bend/Push&Pull/Randomzie
- Move/Scale Texture Space：控制uv坐标的scale和offset

### Radius

Radius允许直接控制沿着spinal curve的extrusion/bevel的width。在cp之间插值。在Transform Panel中设置

## Mirror

与mesh vertices的mirror一样，在局部或全局坐标系按照指定轴对称反转handle

## Snap

Mesh snapping也用于curve组件。CP和Handle都可以被Snapping影响。2D snapping限制在XY平面

## Spin（TODO）

## Add Duplicate

复制CP或CP之间的Segment，无论选择CP还是Handle都可以。创建新的分离的CP，因此创建了新的分离的Spline

## Split

分离CP之间的Segment。将一个spline分割成3个spline

## Separate

类似Mesh的Separate，将一段Spline分离到独立的object

## Toggle Cyclic

将Spline在Open和Closed之间切换，首尾相连

## Set Spline Type

在Bezier、Nurbs和Poly Curves之间切换曲线类型

## Show/Hide

H：隐藏CP

Alt+H：取消隐藏的CP

Shift+H：隐藏unselected的cp

segment总是显示，只能隐藏CP

## Cleanup

尽量保持形状并移除不必要的cp

## Delete

Vertices/Segment/Dissolve Vertices
