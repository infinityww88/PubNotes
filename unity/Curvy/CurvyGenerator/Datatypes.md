# Datatypes

一个Curvy Generator模块通常从一个或多个input slots获取输入数据，进行处理后，将数据写到一个或多个output slots

## Rich datatype classes

绝大多数datatype提供了大量构造函数和帮助函数来操作或使用它到数据。例如Volume提供来方法计算它表面上到点

## Datatype层次结构

CGDATA是所有数据类型到基类

- Shape -> Path -> Volume
- Bounds -> GameObject
- Bounds -> VMesh
- VSubMesh
- Spot

### CGData

- Name
- Timestamp

### Shape

表示一个多边形，例如一个栅格化到spline形状。在这个上下文中，Shapes需要严格限制在XY的2D平面

- Position
- Normal
- Material Setting for groups of line segments

### Path（extends Shape）

表示一个full polygon line，继承Shape，但是为每个曲线上每个点增加了方向向量（切向量）

- Direction/Tangents

### Volume（extends Path）

表示一个推挤出的体积，增加了表示体积的顶点、顶点法向量、和顶点uv坐标

- Vertex
- VertexNormal
- UV

### Bounds

包围盒。Bounds通常从Mesh或GameObject输入模块中获得，并且可以被用来正确放置源物体或其他计算

- Bounds

### GameObject

表示一个GameObject/Prefab

- Object

### VMesh

表示一个mesh data，只有顶点（就像顶点云一样，没有三角形面片）

- Vertex
- UV，UV2
- Normals
- Tangents
- List of VSubmeshes

### VSubMesh

表示一个submesh，主要记录三角形面片数据和材质

- Triangles
- Material

### Spots

表示一个spots数组，可以被用来放置物体或进行其他计算。一个spot，类似一个transform
，定义为

- Position
- Rotation
- Scale
