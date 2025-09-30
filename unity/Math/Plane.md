表示 3D 空间中的一个平面。

平面是无限大的，并将 3D 空间分为两半，成为 half-spaces。

# 属性

- float distance

  Plane 到原点的距离，或者说是原点沿着 plane 法向量到 plane 垂直线的长度。

  如果原点在 plane 法线一侧，distance 为正。如果原点在 plane 法线的另一侧，distance 为负。

- Plane flipped

  返回一个法向相反的 Plane 副本。

- Vector3 normal

  Plane 的法向量。

# 构造器

- Plane(Vector3 inNormal, Vector3 inPoint)

  Plane 由平面上的一点和法线定义。

- Plane(Vector3 inNormal, float d)

  Plane 由法线和到原点的距离定义。

- Plane(Vector3 a, Vector3 b, Vector3 c)

  平面由三个点定义。自上而下看这个平面，三个点按顺时针方向排列的一侧是平面的法线一侧。

# 方法

- Vector3 ClosestPointOnPlane(Vector3 point)

  Plane 上距离 point 最近的点，即 point 在 plane 上垂直投影的点。

- void Flip()

  反转 plane 的法线。

- float GetDistanceToPoint(Vector3 point)

  返回 plane 到 point 的有符合距离。point 在 plane 的法线一侧，距离为正，在 plane 法线另一侧，距离为负。

- bool GetSide(Vector3 point)

  point 在 plane 法线一侧（true）还是另一侧（false）。

- bool Raycast(Ray ray, out float enter)

  判断 plane 和 ray 的交点。如果射线与 plane 相交，enter 设置为沿射线的距离，从射线起点到 plane 交点。

  如果 ray 与 plane 平行，函数返回 false，enter 设置为 0. 如果 ray 指向平面的反方向，函数返回 false，enter 设置为沿着 ray 的距离（ray 起点到 plane 交点）但是为负。

- bool SameSide(Vector3 inPt0, Vector3 inPt1)

  判断两点是否在 plane 的同一侧。

- void Set3Points(Vector3 a, Vector3 b, Vector3 c)

  使用三个点重新设置 plane。plane 的法线为，从法线一侧看 plane，三个点按照顺时针排列。

- void SetNormalAndPosition(Vector3 inNormal, Vector3 inPoint)

  使用一个 point 和法线重新设置 plane。inNormal 必须是标准化向量。

- static Plane Translate(Plane plane, Vector3 translation)

  将 Plane 平移 translation，返回 Plane 副本。

