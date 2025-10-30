# Root Transform 是角色身上某个具体骨骼，还是一个虚拟的位置

**Root Transform** 到底是角色的某个骨骼，还是一个“虚拟”的位置？——**取决于 Rig 类型**。

在 Unity 中，Root Transform 的本质是“动画中表示角色整体移动和旋转的坐标系”，
但这个坐标系的来源因 Rig 类型而不同。

##  一、Humanoid Rig 下的 Root Transform

在 **Humanoid（人形 Avatar）** 模型中，

> Root Transform **不是任何一个骨骼**，而是一个 **虚拟的节点**。

### 详细解释：

* Unity 在导入 Humanoid 模型时，会根据 Avatar 的定义生成一个“抽象层”（Human骨架映射）。
* 在这个抽象层中，有一个名为 **“Root”** 的虚拟节点，它不对应于模型内的任何实际骨骼。
* 这个节点的作用，是统一表示角色整体的位移（translation）与旋转（rotation）。

比如：

```
Humanoid Avatar 层级（抽象）：
Root (虚拟)
 └── Hips (映射到模型的 Hips 骨骼)
     └── Spine
         └── Chest
            ...
```

这个虚拟 `Root` 的位置和旋转由动画数据中推算得出（通常是从 Hips 及其运动计算的结果）。
在动画重定向时，所有角色都会以这个虚拟 Root 作为统一参考点，保证跨模型动作一致。

所以在 Humanoid 中：

* Root Transform = 虚拟节点（不是骨骼）
* 它的运动曲线来自动画文件（通过 Avatar 自动解析）
* 它是用来计算 **Root Motion** 的位移来源


## 二、Generic Rig 下的 Root Transform

在 **Generic（通用骨骼）** 模型中，

> Root Transform 是由用户手动指定的——通常是某个骨骼。

### 详细解释：

* 导入 FBX 时，Unity 在 Import Settings 的 “Root Transform” 面板里允许你指定：

  * 哪个骨骼的平移（Position）和旋转（Rotation）将被视为 Root Transform；
  * 通常选择的是 `Hips`，或者 `Root`（有时模型最上层专门有个 Root 骨骼）。

举例：

```
模型骨骼结构：
Root (实际骨骼)
 └── Hips
     └── Spine
        ...
```

如果你指定 “Root Transform” = `Root`，
那么动画中的整体移动、旋转曲线就取自 `Root` 骨骼的运动。

所以在 Generic 中：

* Root Transform = 真实存在的骨骼（你选定的那个）
* 它的运动就是动画文件中该骨骼的运动
* Root Motion 会根据这个骨骼的位移更新角色 Transform

## 三、对比总结表

| Rig 类型       | Root Transform 来源 | 是否为实际骨骼 | 如何确定                  |
| ------------ | ----------------- | ------- | --------------------- |
| **Humanoid** | 虚拟节点（Avatar Root） | ❌ 否     | Unity 自动创建，根据 Hips 推算 |
| **Generic**  | 用户指定的骨骼           | ✅ 是     | 导入设置中手动选择             |

## 四、为什么 Humanoid 要用虚拟 Root？

因为 Humanoid 动画要能**跨不同骨架重定向（Retargeting）**。

不同模型的骨骼结构（例如 Hips 的高度、根骨层级）可能不同，Unity 必须抽象出一个统一的“Root”坐标系来表示角色整体运动，否则动画无法精确匹配不同角色。

主要是因为不同来源的角色模型，骨骼结构、不同骨骼的作用往往都不一样，没办法用统一的方法提取采样 Root Motion。因此直接用所有骨骼计算一个虚拟质心，对它进行采样，作为 Root Motion 的动画曲线保存，运行时应用到 Animator GameObject 上（如果开启 Apply Root Motion）。

因此这个虚拟 Root：

* 是动画系统中的抽象存在；
* 不直接绑定到 Mesh 或 Skeleton；
* 是所有 Humanoid 角色都具备的统一运动基准。

## 举个例子直观理解：

| 类型           | Root Transform 表现                                    |
| ------------ | ---------------------------------------------------- |
| **Generic**  | “我动画里的 Root Bone 真的动了几米，这几米就是 Root Motion”           |
| **Humanoid** | “我的 Hips 动了几米，但系统计算出我虚拟的 Root 节点动了几米，这是 Root Motion” |
