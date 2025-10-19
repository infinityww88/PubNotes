# 2D Sprite Shape

## Overview

SpriteShape是一个灵活强大的世界构建工具，它将Sprite沿着一个Shape Outline堆叠，自动变形以及基于outline的角度切换Sprites。此外，你还可以为Shape赋予一个填充的纹理来创建纹理堆叠的填充的形状作为背景或者非常大的关卡构建物品

SpriteShape = Sprite & Shape

    Shape定义一个形状
    Sprite沿着这个形状堆叠

SpriteShape由两部分组成：SpriteShapeProfile Asset（Sprite） & SpriteShapeController Component（Shape）

## Workflow

1. 创建一个SpriteShapeProfile资源，可选两种类型
    1) Open Shape
    2) Closed Shape
2. 在SpriteShapeProfile中创建Angle Ranges和并设置Sprites
3. 将SpriteShapeProfile拖拽到Scene中，自动创建一个基于这个Profile的SpriteShape GameObject

    还可以手动创建一个GameObject，添加SpriteShapeController组件，然后将Profile设置给它

    Profile是一个资源，记录Angle Ranges使用的Sprites。它可以被用于创建多个SpriteShapes

    SpriteShapeController定义Shape Outline，Profile中的Sprite按照Outline的角度沿着Shape堆叠

4. 在SpriteShapeController中边界Shape的Outline
5. 添加一个Collider组件开启SpriteShapes的Physics2D交互

## SpriteShapeProfile

Profile定义指定的角度范围应用什么Sprite

Profile可以被用于多个SpriteShapes GameObject
