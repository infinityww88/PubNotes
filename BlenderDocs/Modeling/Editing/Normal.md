# Normal

Normal Edit Modifier可以用于编辑normals

Weight Normal Modifier可以使用各种方法影响normal，包括Face Strength

可以使用Data Transfer（Operator或Modifier）从其他mesh拷贝normal

## Shading

- Flat
- Smooth Object
- Smoothing Parts of a Mesh

## Tools

- Flip Direction
- Recalculate Normals
  重新计算选择的faces的normals，使得它们朝向volume的外部。Volume不必是闭合的。Inside和Outside通过相邻的faces的角度判断。这意味着要重新计算的faces必须至少有一个不共面的face，否则想Grid primitive（所有faces共面）是没有办法定义哪个方向是外部的
- Set From Faces
  位于corner的vertex在每个face上有各自和face相同的split normals，例如一个被3个face使用的vertex有3个normal。Set From Faces使得vertex在每个face上具有同一个normal，如果vertex被一个selected face使用，则等于这个face的normal，否则是多个face normal的平均值。对于那些使用vertex的unselected faces，vertex normal也将成为这个value
- Rotate
  通过移动鼠标选择selected normals，R+N key
- Point To Target

  所有selected的normals设置为从它们的vertex指向target

  - mouse cursor
  - pivot
  - object origin
  - 3D cursor
  - mesh item

  Mode

  - Align：所有normal指向相同方向，从selected vertices指向target
  - Spherize：每个normal在它的初始值和到target直接进行插值
  - Invert：反转上面的各种方向

  Reset

    将custom normal重置回操作开始的值

- Merge

  合并每个selected vertex的所有normal合并为平均值

- Split

  将选择的vertices的normals分离为每个face一个，指向face的normal（Flat shading）

- Average

  类似Merge（TODO）

- Copy Vectors/Paste Vectors

  如果选择一个normal，将它复制到一个内部的vector buffer，Paste Vectors将normal粘贴到当前vertex

- Smoothen Vectors

  类似Merge/Average，但不是一下将normals合并，而是调整normals使它们更接近相邻的vertex normals

- Reset Vectors

  重置normals到默认计算的normals

- Select by Face Strength

  选择指定Face Strength强度的faces

- Set Face Strength

  改变当前选择的faces的Face Strength为Weak、Medium、Strong。Face Strength被Weighted Normal Modifier使用，当合并一个vertex处的normals时，只有strongest Face Strength才会用来计算最终的normal。例如一个vertex处有4个face，一个week，一个medium，两个strong，则只有两个strong的faces才用来计算最终的normal
