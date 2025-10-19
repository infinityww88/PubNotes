# Math Operators

Abs, Add, Ceil, Clamp, Divide, Exp, Exp2, Floor, Lerp, Log, Log10, Log2, Max, Min,  Negate, OneMinus, Power, Remainder, Round, Sign, Sqrt, Subtract

FMod：与被除数符号相同的浮点余数

DDX/DDY：输出指定向量在屏幕空间X/Y方向上的偏导数

Fract：保留输入值（或者向量的每个部分）的小数部分

FWidth：输出指定Input值的偏导数的绝对值，对于Vector输入，输出每个组件的对应值的和，即abs(ddx(input)) + abs(ddy(input))

Multiply：多通道数据逐通道进行

Remap：将一个在[Min Old, Max Old]范围内的值映射到[Min New, Max New]范围内的值

Rsqrt：1/Sqrt(Input)

Saturate：输入值小于0则为0，大于1则为1，否则等于自身

Scale：用一个float factor缩放输入值

ScaleAndOffset：(Value * Scale) + Offset

Simplified FMod：FMod简化版，不保证余数与被除数符号相同

SmoothStep：如果Input alpha值在[Min, Max]范围内，在[0, 1]之间计算一个平滑的插值Hermite插值。小于Min返回0，大于Max返回1

Step：给定两个值A和B，如果A>B，返回0，否则返回1

Trunc：与Fract相反，去除小数部分，保留整数
