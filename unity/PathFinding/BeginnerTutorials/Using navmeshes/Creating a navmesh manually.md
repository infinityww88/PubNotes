# Create a navmesh manually

使用Blender建模navmesh，就像可以为一个高精度mesh创建一个低精度的mesh作为碰撞体一样，这里作为navmesh

创建一个A* GameObject，添加Pathfinder组件

Graphs/Add Graph/Navmesh Graph添加一个navmesh graph。Mesh必须在Resources目录下。可以使用script设置mesh而不需要一定在Resources目录中

点击Scan生成Graph
