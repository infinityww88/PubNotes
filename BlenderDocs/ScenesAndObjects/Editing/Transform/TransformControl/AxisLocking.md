# Axis Locking

限制transform到特定axis上，当对于transform orientation

在Transform期间可以按下X Y Z键随时改变，但每次改变都从起始位置重新开始

开始一个Transform之后可以按MMB选择X Y Z轴，就像按下X Y Z键一样

## Plane Locking

将transform限制在两个axes上，因此创建来一个平面，object可以在上面自由move/scale，Plane只限制move/scale。对于rotate，Axis/Plane Locking效果是一样都，因为旋转总是绕着一个轴的

## Axis Locking Modes

按下一个键将transform约束到Global Axis上，再按一次相同的按键，将transform限制到当前transform orientation。第三次按下相同的键取消Locking约束
