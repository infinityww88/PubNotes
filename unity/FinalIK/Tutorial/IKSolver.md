IKSolver 是所有 IK Solver 的基类

- IKPosition
- IKPositionWeight
- Transform GetRoot()
- IKSolver.Point[] GetPoints()

  被 solver 使用的 points

- IKSolver.Point GetPoint(Transform transform)

  获得指定 transform 的 point

IKSolver.Point 是 IK chain 中最基本的元素类型，所有其他类型从它扩展

Point

- Transform transform
- float weight：solver 中这个 bone 的权重
- Vector3 solverPosition：IK solver 中虚拟 position
- Quaternion solverRotation：IK solver 中虚拟 rotation
- Vector3 defaultLocalPosition：Transform 的默认 local position
- Quaternion defaultLocalRotation：Transform 的默认 local rotation
  ```C#
  public void StoreDefaultLocalState() {
      defaultLocalPosition = transform.localPosition; defaultLocalRotation = transform.localRotation;
  }
  
  public void FixTransform() {
      if (transform.localPosition != defaultLocalPosition) {
        transform.localPosition = defaultLocalPosition; 
      }
      
      if (transform.localRotation != defaultLocalRotation) {
        transform.localRotation = defaultLocalRotation;
      }
  }
  ```

Bone : Point

- float length：bone 的长度
- float sqrMag：bone 的平方
- Vector3 axis：用于 target/child bone 的 local axis
- RotationLimit rotationLimit：获取来自 Transform 的 rotation limit 组件

Node : Point

- float length：到 child node 的 Distance
- float effectorPositionWeight：effector 的 position weight
- float effectorRotationWeight：effector 的 rotation weight
- Vector3 offset：Position offset
