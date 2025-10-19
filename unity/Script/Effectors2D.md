# Effectors2D

Effectors2D是一种力场效果，它使用Collider2D定义力场范围，当GameObject进入力场时对其施加作用力

不同的施加作用力的规则定义了不同类型的Effectors2D

使用Effectors2D可以创建一些效果

1. 创建诸如单向碰撞的platform行为，物体只能在一侧于collider发生碰撞
2. 传送带，当物体于collider接触时，施加平行于collider表面的作用力
3. 源自一点的引力、斥力效果
4. 物体浮动效果
5. 指定方向随机变换大小的force

## Area Effector2D

使用Collider2D定义一个区域，当另一个Collider2D进入区域时，对齐施加作用力

可以配置力的方向，力的大小和随机变换量

还可以同时应用linear和angular阻力来减慢Rigidbody2D

定义Area的Collider2D通常是trigger，因为这样其他Collider2D可以于它重叠，使得它可以对其持续施加作用力。非trigger的Collider2D也可以工作，但是作用力只会在两个Collider2D接触时应用

## Buoyancy Effector2D

定义简单的液体浮力、阻尼、流动。你可以定义液体的表面，液体的行为在其下面发生
