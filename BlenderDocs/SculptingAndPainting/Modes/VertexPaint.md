# Vertex Paint

## Introduction

直接修改Vertex Color，而不是纹理，是简单直接的修改object颜色的方式

## Vertex Paint Tools

- Draw
- Blur
- Average
- Smear

## Editing Vertex Colors

- Set Vertex Color(Shift-K)：将当前所有vertices的vertex color layer设置为当前绘制颜色（即将object全部着色为当前颜色）
- Smooth Vertex Colors：在所有vertics之间Smooth Colors（不是vertices之间的face上的颜色渐变，而是vertices之间的颜色进行平滑）
- Dirty Vertex Colors（TODO）
- Vertex Color from Weight：将active weight 转换成灰度vertex colors
- Invert：反转所有vertices的颜色
- Levels：调整所有颜色的色阶
- Hue Saturation Value：调整vertex color的HSV
- Bright/Contrast：调整vertex color的亮度和对比度
