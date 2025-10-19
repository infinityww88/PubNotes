# Collider2D

## 属性

- attachedRigidbody

    collider挂载的rigidbody，不一定在collider自身gameobject上

    在GameObject Hierarchy中，一个具有Rigidbody的GameObject挂载下面children的collider，直到children自己具有Rigidbody

    每个具有Rigidbody的GameObject都是物理世界空间中的独立个体

- bounciness/friction

    collider表面物理材质的弹性系数/摩擦系数

- bounds

    世界空间包围盒

- composite

    当usedByComposite=true时，返回它参与合并的CompositeCollider2D

- density

    当auto mass开启时，用来计算collider mass的密度

    Collider3D没有在Collider上设置密度的功能，只能在Rigidbody上SetDensity，而且只能写不能读。因此3D Rigidbody所有Collider都具有相同的密度。Collider2D可以在每个Collider上设置密度

- isTrigger

    collider是否被配置为触发器

- offset

    自身空间中Collider Geometry的偏移量

- shapeCount

    Collider Geometry中分离的形状区域个数

- usedByComposite/usedByEffector

- sharedMaterial

    应用到Collider2D上的PhysicsMaterial2D;如果Collider2D上没有PhysicsMaterial2D，则应用Rigidbody2D.sharedMaterial;如果没有挂载的Rigidbody2D或者sharedMaterial为null，则应用Physics2D.defaultSharedMaterial

### 方法

Physics2D.GeometryCast/Overlap是完全基于Collider Geometry计算的，不要求接触的任何一方是Rigidbody或Kinematic

Physics2D.GetContacts和Collider2D.GetContacts则要求至少有一方是Rigidbody（非kinematic，非static）

Collider2D.Cast则要求至少有一方具有rigidbody组件，可以是Rigidbody，Kinematicbody，StaticBody

- Cast

    检测初始位置即重叠的collider

    Collider2D.Cast双方至少有一个Rigidbody，否则Cast不到，但是Rigidbody可以是static的

    可指定ContactFilter2D查询

    输入RaycastHit2D既可以是数组[]，也可以是List。List在空间不够的情况下会自动重新分配

- ClosestPoint
  
    计算到Collider边界距离给定位置最近的点

    如果position在Collider内部，直接返回position

- CreateMesh

    创建一个与Collider2D Geometry一致的平面的Mesh。创建的mesh可以被用于任何目的而不仅限于2D导航网格。

    所有的Collider2D位于Rigidbody2D的空间中。可以通过参数useBodyPosition和useBodyRotation指定是否使用rigidbody2d的位置和旋转变换mesh的顶点。如果Collider2D不挂载到一个Rigidbody2D上，则geometry总是位于世界空间中的，并且useBodyPosition和useBodyRotation应设为false

- GetContacts/IsTouching/IsTouchingLayers/OverlapCollider/OverlapPoint

    针对本Collider2D的Physics2D代理方法

- Raycast

    到Physics2D的代理方法，但是不与本Collider2D碰撞

## CompositeCollider2D

不同于其他的Collider2D，CompositeCollider2D不定义固有的2D形状，而是将其他的BoxCollider2D或者PolygonCollider2D合并在一起，CompositeCollider2D使用这些小的polygon的vertices合并成一个大的polygon。

CompositeCollider2D必须挂载到Rigidbody2D上。但是Rigidbody2D可以是kinematic的。

CompositeCollider2D只能合并BoxCollider2D和PolygonCollider2D，这两种collider上具有usedByComposite属性，开启这个选项将标识它可以被CompositeCollider2D合并。CompositeCollider2D只能合并共享同一个rigidbody的Collider2D。

CompositeCollider2D将所有Collider2D.usedByComposite为true的Colliders合并在一起。当一个Collider2D被一个CompositeCollider2D使用时，它的Collider2D.sharedMaterial, Collider2D.isTrigger和Collider2D.usedByComposite属性将从Editor上消失，它们将采用CompositeCollider2D上的设置，因为这些colliders将成为一个整体的collider。

CompositeCollider2D是Collider2D的派生类，下面列出它独有的属性和方法

- GeometryType

    Composite Collider generates生成的geometry类型

    Outlines：生成只有闭合边沿的Collider，内部是中空的

    Polygons：生成封闭的多边形Collider，内部是实心的

- GenerationType

    当被Composite Collider使用的Collider发生改变时，指定何时生成新的Composite Geometry

    Synchronous：立即更新同步

    Manual：关闭自动更新，手动同步

- edgeRadius：

    当GeometryType时Outlines时，edgeRadius控制边沿两侧每侧的厚度。如果edgeRadius=0，则边沿将是无限薄的。但edgeRadius>0，每个edge表现的就像一个末端圆滑的胶囊体，edgeRadius就是控制胶囊体半径的。因此Composite Collider将是圆角的

    当使用useAutoMass时，修改edgeRadius并不改变计算的mass即使碰撞区域以及改变了。mass总是按照edgeRadius=0的情况下计算

- offsetDistance

    顶点焊接距离阈值。任何小于这个阈值的两个点被合并在一起

    不要将这个值设置超过Sprite的长度，因为这会在合并大量vertices时导致细节丢失

- pathCount

    一个path是一组闭环的线段序列，定义一个polygon的outline。因为polygon可以有洞以及不连续的多个部分，因此它的形状可能不止包括一个path定义

- pointCount

    所有paths上的顶点数量

- vertexDistance

    生成的vertices之间允许的最小距离

    任何小于或等于这个距离的vertices将会被移除。这个值设得太高会导致什么都不生成

- GenerateGeometry

    GenerationType为Manual时，手动生成Geometry的方法

- GetPath

    int (int pathIndex, Vector2 points)

    获得指定index的path上的顶点，返回在points中的顶点数量

- GetPathPointCount

    返回指定index的path上的顶点数量

## ColliderDistance2D

表示两个Collider2D的分离或重叠

主要定义每个collider2d边界上的一个点，pointA & pointB，和它们之间的距离。距离为正表示两个collider2d是分离的；距离为0表示两个collider2d是接触的；距离为负表示两个collider2d是重叠的

normal从B指向A，表示移动B物体。向量模长缩放到两点的距离，因此以这个向量移动B物体将使得它们不再分离或重叠，而是正好接触

一个常用的情形是，手动解析两个collider2d的碰撞，尤其是当把一个rigidbody2d设置为kinematic的时候

- distance
- isOverlapped <=> distance < 0
- isValid：如果任何一个collider2d是disable的或者没有有效shape，ColliderDistance2D将是无效的，但是它是一个structure，不能通过null判断是否有效，因此提供此字段表示结果是否有效
- normal
- pointA
- pointB

## ContactPoint2D

对应3D物理中的ContactPoint

描述2D物理碰撞的一个接触点，两个Collider2D交集区域中的一个点。ContactPoint2D只能存在于没有设为triggers，因为triggers不定义接触点，triggers不定义任何接触信息，只在发生接触时触发消息函数

- collider/otherCollider
- enabled：参加Collision2D

## Collision2D

- collider/otherCollider/gameObject/rigidbody/transform/otherRigidbody
- contactCount/contacts/GetContact/GetContacts

    返回碰撞点ContactPoint2D数组

- relativeVelocity

    两个Collider2D的相对线性速度，在self坐标系定义的另一个collider2d的相对线性速度

- enable

    一些2D物理引擎特性可以禁止collision响应，你仍然可以接受碰撞消息，但是物体不会对碰撞作出任何响应。这与trigger不同，trigger不定义接触点，无法得知碰撞接触点信息。Platform effector是这种特性的一个用例

## ContactFilter2D

一组用来过滤物理查询结果的参数，使用Filter来精确控制返回哪些contact结果。这移除了查询所有结果再执行过滤的需求，而是再执行查询的时候就过滤，因此更快更方便

如果你调用一个需要ContactFilter2D参数的查询方法，但是不想进行任何过滤，使用ContactFilter2D.NoFilter

### 属性

- isFiltering

    获取这个ContactFiler的状态，当前是否会过滤任何结果

    检测useTriggers，useLayerMask，useDepth，useNormalAngle是否任何一个被开启

- layerMask/useLayerMask

    只返回包含指定layerMask上的Collider2D的结果

- maxDepth/minDepth/useDepth/useOutsideDepth

    只返回Z坐标再指定范围的Collider2D的结果

    Outside反转过滤范围

- maxNormalAngle/minNormalAngle/useNormalAngle/useOutsideNormalAngle

    只返回contact normal再指定范围的结果

    Outside反转过滤范围

- useTriggers

    只返回Collider为trigger的结果

### 方法

#### Clear方法

关闭相应过滤选项，但不改变过滤参数

- ClearDepth
- ClearLayerMask
- ClearNormalAngle

#### 手动过滤测试

检测对应的选项是否开启，检测对应的参数是否满足测试条件/范围

- isFilteringDepth(GameObject)

    指定object的Z坐标是否被depth filter过滤

- isFilteringLayerMask(GameObject)

    指定object是否被layer mask filter过滤

- isFilteringNormalAngle(Vector3 normal)

    指定normal是否给normal angle filter过滤

- isFilteringTrigger(Collider2D collider)

    指定collider是否被trigger filter过滤

#### Set方法

设置指定Filter参数，并开启相应过滤选项

- SetDepth
- SetLayerMask
- SetNormalAngle

- NoFilter

    不过滤ContactFilter2D常量

## RaycastHit2D

- centroid

    执行cast的图形在计算的接触点与被cast到的collider恰好发生接触时，cast图形的中心位置。如果cast的图形是raycast，则cetroid=point

- collider/rigidbody/transform

    cast投射到的collider。2D cast直接返回RaycastHit2D，而RaycastHit2D是结构体，不能与null比较。因此通过判断collider是否为null判断是否投射到物体上

- distance

    投射原点到接触点的距离

- fraction

    distance / direction.length

    如果direction参数向量是单位向量，这个值等于distance

- point

    世界空间中hit到collider表面的接触点
