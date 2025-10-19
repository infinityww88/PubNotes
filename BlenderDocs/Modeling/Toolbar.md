# Mesh Edit Tools

## Select

- Box
- Circle
- Lasso

## Extrude Rgion

- Along Normals
- Individual
- To Cursor

## Inset Faces

## Bevel

## Loop Cut

## Knife

- Cut edge in mesh
- Bisect

## Poly Build

通过一个一个添加vertex创建geometry

## Spin

通过extruding和rotating创建geometry

- Spin Duplicate：通过duplicating和rotating创建新的geometry

Extruding的本质是复制被extrude的元素，并将副本和原来的元素bridge起来。这样，extrude只是简单地extrude并translate，而spin则是extrude并rotate

这也是UModeler中Push&Pull不仅可以extrude，还可以cut hole一样，它们的本质是一样的。Extrude时，在外部创建一个shape副本，删除原来的副本，然后将两个shape的边缘bridge起来。而Cut Hole时，在对面Polygon上cut出相同的shape（就像绘制工具一样），然后删除两个相同的shape，最后将两个shape的边缘bridge起来

Spin Duplicate与Spin的区别时，它只复制原来的元素，不会bridge它们的边缘以创建连续的mesh

## Smooth

平滑选择的vertices的angles，是它们看起来更平整

- Randomize：是Smooth相反的过程，将vertices随机化

## Edge Slide

默认移动工具是在空间中任意移动edges的，Edge Slide可以沿着平面移动edge，使平面仍然保持

- Vertex Slide：沿着edge移动vertex

## Shrink/Fatten（收缩或变肥）

沿着法向量scale vertices

- Push/Pull：缩放选择的元素（edges/faces）

## Shear

在指定的坐标系，沿着指定的坐标轴切变选择的元素，在Scene中可以使用Gizmos或者Properties面板调整切变程度

- To Sphere：向着object中心之外的包围球移动vertices

## Rip Region

选择vertices或者edges（不能是faces），将mesh剥开（vertices/edges被duplicate并split）并移动其中一个切口

- Rip Edge
