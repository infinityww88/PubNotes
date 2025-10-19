# VolumeCaps

为Mesh创建一个flat cap（封口平面），即两端的Cross Section

## Slots

### Input

- Volume：用来构建caps的Volume
- Volume[]\(Holes)：用来增加holes的Volumes

### Output

- VMesh[]：结果VMesh

## 通用选项

- StartCap/EndCap

    定义cap如何创建

  - Yes：创建Cap
  - No：不创建
  - Auto：如果Volume不是封闭的，自动创建Cap

- ReverseNormals：反转normal

- Generate UV：生成UV坐标

## StartCap选项

- Swap UV：是否交换U、V坐标

- Keep Aspect：保持纹素texel长宽比例

  - Off：不应用Aspect修正
  - ScaleU：缩放U坐标以保持texel比例
  - ScaleV：缩放V坐标以保持texel比例

- UV Rotation：定义texture旋转

- UV Offset/Scale：Unity材质的ST

- Material：Unity使用的material

## EndCap选项

- Clone Start Cap

    如果开启，EndCap材质设置复制StartCap的材质。否则独立设置EndCap的材质
