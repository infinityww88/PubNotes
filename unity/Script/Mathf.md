# Mathf

## 静态属性

- Deg2Rad/Rad2Deg：角度与弧度的转化因子
- Epsilon：float和zero可以相差的最小值
  - anyValue + Epsilon = anyValue
  - anyValue - Epsilon = anyValue
  - 0 + Epsilon = Epsilon
  - 0 - Epsilon = Epsilon
- Infinity/NegativeInfinity
- PI

## 静态方法

- Abs/Sign
- Cos/Sin/Tan/Acos/Asin/Atan2
- Exp：e的指数
- Log/Log10/Power
- Sqrt
- Max/Min
- Approximately(float a, float b)：两个float是否近似相等，以Epsilon为容差
- Ceil/CeilToInt/Floor/FloorToInt/Round/RoundInt
- Clamp/Clamp01
- int ClosestPowerOfTwo(int value)：返回与value最接近的2的幂
- IsPowerOfTwo：int value是否是2的幂
- NextPowerOfTwo：大于等于int value大下一个2大幂
- float DeltaAngle(float current, float target)：计算两角度的最小差值，绝对值小于180，无符号
- Lerp/LerpUnclamped：在两个float之间插值
- InverseLerp：反向插值，给出a、b，返回value在a、b之间插值的系数，即(b - a) * t + a = value
- LerpAngle：在两个角度直接线性插值，正确处理在360度处的wrap，总是在两个角度小于180度的区间进行插值
- float PingPong(float t, float length)：随着t增加，返回值在[0, length]之间来回反复
- Repeat：类似PingPong，但是不返回，每次超过length，从0开始，相当于对浮点数对求余
- float PerlinNoise(float x, float y)
  - 返回值在[0, 1]之间
  - 通常x，y是连续变化对函数，无论如何变化，只要是连续变化对就可以
  - x，y是2D平面的采样点，柏林噪声沿着任何方向都是平滑的，因此只需要采样坐标是连续的就能产生平滑的噪声函数
  - 噪声可以以不同频率叠加，创建自相似的噪声图像
- MoveTowards：float版本的Vector3.MoveTowards
- MoveTowardsAngle：LerpAngle版本的MoveTowards，考虑了角度对360度的wrap
- SmoothDamp：float版本的Vector3.SmoothDamp
- SmoothDampAngle：LerpAngle版本的SmoothDamp，考虑了角度对360度的wrap
- float SmoothStep(float from, float to, float t)
  - ease in/out的Lerp，t在初始阶段加速，在末尾阶段减速
  - 常用于natural-looking动画，fading和其他transtions
  - Unity CrossFade

