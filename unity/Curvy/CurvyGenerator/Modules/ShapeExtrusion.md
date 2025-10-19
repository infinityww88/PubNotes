# ShapeExtrusion

沿着一个path推挤一个shape，创建一个volume

## Slots

### Input

- Path：推挤路径
- Shape：推挤横截面

## 选项

### Path相关

参见RasterizePath模块

### Cross相关

- Range/Resolution/Optimize/Angle Threshold

    参见RasterizePath，只不过前者是对Path栅格化参数，后者是对Shape（也是Spline）的栅格化参数

- Include CP：保证为所有shape的Control Points生成vertices

- Hard Edges：在Control Points处创建额外的vertices使得Shape在CP处具有硬边缘（TODO）

- Materials：额外的修补顶点（additional patches of vertices）被创建以Generator Options中定义的不同的Material ID（TODO）

- Extended UV：Meta CG Option中的扩展UV数据是否应该被包含

- Shift：定义一个偏移应用在输出volume的cross。这个shift在沿着volume表面插值数据（position，normal，...）时被使用（TODO）

  - None：使用Shape的start
  - By Orientation：starting point移动到path的orientation与cross shape的交点
  - Custom：starting point偏移用户自定的数值

- ReverseNormal：反转生成的Volume的normal。如果有Volume Hollow亦不影响

## Scale相关

缩放extrusion

- Mode

  - Simple：以任意值缩放
  - Advanced：使用曲线缩放

- Reference：确定如何应用scale

  - Self：缩放应用到整个path range上
  - Source：scale应用到path整个长度上

- Offset：Advanced scale mode only

    Scale从一个offset开始应用

- Uniform Scaling

    相同到scale同时应用到cross shape到X和Y方向

- Scale

    乘到cross Shape vertices的基础值（系数）

- Multiplier

    Advanced scale mode only

    乘以到curve的系数

## Hollow

一个缩小的结果volume的克隆与outer volume同时创建。选项的值定义inner volume缩小的百分比。绝大多数情况用于创建tubes

- ReverseNormal

    反转hollow volume（inner版本）的normals。不影响volume（outer版本）
