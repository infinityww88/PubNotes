# UV Coordinates

## Flipbook UV Animation

UV帧动画，通过transform输入的UV（或UV参数，如果未连接），顺序访问通过Columns和Rows指定的网格cell，从Start Frame开始，按照每秒Speed速度播放

如果是2x2的spritesheet，uv坐标(0.5, 0.5)将被依次缩放为(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)

## Panner

平移一个UV坐标或者其他Vector2，通过指定Speed，按照Time值进行平移。如果Time Input没有连接，则使用Unity内部的Time.time提供连续的动画。此时Time属性作为一个timer缩放系数。否则如果Time Input有连接，则它作为最终的时间值，不会进行任何缩放。

如果平移一个纹理，它必须设置Wrap Mode为Repeat

## Parallax Mapping/Parallax Occlusion Mapping/Parallax Offset（TODO）

## Pixelate UV（像素化效果UV）

变换UV输入为一组grid上的每个cell的常量值，grid/cell通过Pixels X/Y参数指定

## Rotator

类似Panner，但是是选择UV或者Vector2，而且指定一个Anchor

## Texture Coordinates

使用Mesh UVs并根据纹理tilling和offset参数操作它来定义一个纹理如何映射到Mesh上。如果Tex Port连接到一个Texture Object或者在属性面板引用一个Texture Object，UV操作将使用材质面板上设定的tilling（scale）和offset（translate），此时Tilling和Offset Port都不可用。否则使用输出端口给定的Tilling和Offset

- Reference（Param）：指向一个存在的Texture Object或者Texture Sample
- Coord Size：允许从vertex坐标读出更多的packed数据，Float[2, 4]，输出端口相应可输出W、T

输出UV（WT），U，V（，W，T）
