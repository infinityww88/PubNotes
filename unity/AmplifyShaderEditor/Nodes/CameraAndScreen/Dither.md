# Dither

使用节点的Pattern属性创建一个屏幕空间抖动模式

如果没有Input port连接，它会直接输出这个pattern。如果存在一个Input port，抖动模式将基于一个step操作Step（Dither Pattern，Input）被应用到输入值上

## 参数

- Pattern

  - 4x4 Bayer：使用4x4矩阵创建16个唯一的dither layers
  - 8x8 Bayer：使用8x8矩阵创建64个唯一的dither layers
  - Noise Texture：使用Pattern输入端口根据预计算的噪声模式创建一个dither pattern

- Screen Position

    开启一个Input Port允许指定一个屏幕位置来确定ditter pattern。如果Input port没有输入，使用当前fragment的屏幕位置

## Input Port

- Input（float）：用来作为step的值，用来确定哪个dither pattern将被应用
- Pattern（optional）（Sampler2D）：接收一个Texture Object。当Pattern设置为Noise Texture时可见，表示用来创建dither的pattern texture
- Screen Position（float4）
