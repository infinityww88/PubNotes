# Control Points

## Extrude Curve and Move

E key

中间cp复制并分离，末端cp复制并延长曲线

## Make Segment

F key Fill

将两个分离的cp连接起来，就像连接两个vertices为一个edge

## Tilt

控制每个CP的normal扭转。在CP之间插值

## Clear Tilt

重置Tilt为默认的值

## Set Handle Type

Free/Align

## Recalc Normals

重新计算法向量，使得handle与曲线相切。使曲线更加平滑，看起来更一致

## Smooth

减小selected cp与它们邻接unselected cp之间的距离，移动cp，保持邻接cp不动。只移动cp位置，不改变handle方向

## Smooth Curve Tilt

平滑法向量扭转，减少法向量突变

## Smooth Curve Radius

平滑radius突变

## Smooth Curve Weight

平滑cp weight

## Hooks

类似Vertex Hooks，使得一个或多个CP可以跟随其他物体移动

## Make Vertex Parent

类似Vertex Parent，Hooks反效果，使得一个其他物体可以跟随一个或多个cp移动
