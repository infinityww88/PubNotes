# Variable Mix Shapes

和Mix Shapes相似，这个模块在两个Shapes之间线性插值。这是被用来作为ShapeExtrusion模块的输入Shape的，使得推挤横截面在两个shape沿着path进行插值渐变，而不是每处横截面都是一样的。MixShape只是产生一个固定不变的shape

## Slots

### Input

- Shape A
- Shape B

### Output

- Shape：混合结果，沿着path在两个shape之间渐变

## Mix Curve

定义结果shape如何被插值。Y值在[-1, 1]之间，-1完全等于A，1完全等于B。X值（time）在[0, 1]之间，0为extrusion起始，1为extrusion结束
