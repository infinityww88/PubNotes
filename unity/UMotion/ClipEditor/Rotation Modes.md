3D 引擎中有两种方式处理旋转

- Euler Angles
- Quaternion

## Euler Interpolation

所有旋转存储为 Euler angles。对每个轴的 angle 分别进行插值

## Quaternion Interpolation

所有选择存储为 Quaternion。对 Quaternion 进行插值。Quaternion 表示为一个轴和一个角度。

## Progressive Quaternion Interpolation

这个也使用 Quaternion，但是引入了 Progression Curve。Progression Curve 表示两个 Keyframes 之间最小的旋转（最优劣弧）。它可以被用来编辑两个 keyframes 之间旋转插值的方式。

这联合了 quaternion 的健壮性和修改插值曲线的灵活性，这使得它成为 UMotion 的默认 rotation mode。
