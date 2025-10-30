：**Unity 在导入一个 Humanoid 动画时，会将动画片段的数据从“模型自身骨骼空间”转换为“Unity 的标准人形骨架空间”**。

这一步就是所谓的 **“Humanoid 归一化（retarget standardization）”**。

下面详细说明 Unity 在导入时到底做了什么（一步步讲清楚 👇）：

## 一、导入前：动画片段原始状态

当一个带动画的 FBX 文件进入 Unity 前：

* 它内部的动画数据是基于 **原始骨骼层级和名称** 的。
* 每条曲线对应模型中的骨骼（例如 `"Root/Hips/LeftLeg/LeftFoot"`）。
* 所有旋转、位置关键帧都是相对于这些骨骼的 **局部坐标系**。

## 二、导入时：Unity 的 Humanoid 转换过程

当你在 Import Settings 里把 **Rig Type** 设为 `Humanoid` 时，Unity 会执行以下步骤：

### Avatar Mapping（建立标准人形骨架映射）

Unity 根据模型骨骼命名、拓扑结构，创建一个 Avatar。
它描述了模型的每个骨骼对应 Unity 内部“标准人形骨架”的哪个部位，比如：

| 模型骨骼路径    | 标准人形骨骼       |
| --------- | ------------ |
| Hips      | Hips         |
| Spine1    | Spine        |
| LeftUpLeg | LeftUpperLeg |
| LeftFoot  | LeftFoot     |
| ...       | ...          |

这一步会生成一个 `.avatar` 文件（或在 FBX 中嵌入）。

### Animation Retargeting（转换动画曲线）

Unity 会用上一步的 Avatar 映射，把动画从“原骨骼”空间转换成标准人形骨架空间。

例如：

```text
原动画：  Hips.Rotation.x = ...
标准化后：Human.Hips.Rotation.x = ...
```

换句话说：

* Unity 不会再让动画片段直接依赖模型骨骼路径。
* 它会用一个中间的“Human Pose Representation”（人体姿态标准空间）来记录关键帧。
* 动画片段此时就和原模型骨架解耦了。

### 存储

导入完成后，`.anim` 文件中的曲线实际上是：

* 相对于 Unity 的 **标准人形骨架**；
* 不再依赖原始骨架层级；
* 因此可以被任何 Humanoid Avatar 重定向回对应骨骼。

## 三、播放时的反向过程

播放时：

1. Animator 读取动画片段（标准人形空间）。
2. 根据 **Animator 所绑定的 Avatar**，将这些标准化的人体姿态重新映射到目标模型的骨骼。
3. 结果：同一动画能驱动不同角色。

## 四、验证方式（可实验）

你可以在导入模型时：

1. 先设 Rig = **Generic** → 打开动画，看到每条曲线都绑定到具体骨骼路径。
2. 改 Rig = **Humanoid** → 再打开同一个动画，会发现：

   * 曲线变少了（不再是一堆骨骼路径）；
   * 名称中不再出现模型骨骼路径；
   * 这就是被“标准化”后的状态。

## 五、一个重要细节

Unity 在转换动画时：

* 会**重新计算骨骼姿态到人体关节空间**；
* 并且丢弃掉 Avatar 未使用的额外骨骼的动画（例如装饰性骨骼、裙子、翅膀等）；
* 所以 Humanoid 动画导入后可能丢失某些细微动作（比如非人形部分）。

## 总结：

> 在导入 Humanoid 模型时，Unity 会读取模型动画的骨骼姿态数据，通过 Avatar 映射转换成 Unity 内部的“标准人形骨架动画”，并将其存储在 `.anim` 文件中。因此动画片段再也不依赖原模型的骨骼路径，而是基于 Avatar 标准骨架空间。

因此配置为 Humanoid 模型的动画片段中骨骼已经变成了 Avatar 标准骨骼的名字，因此不需要依赖任何 Avatar 配置文件，就可以在任何也配置了 Avatar 的模型上播放。
