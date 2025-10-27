# 为什么很多模型在 Hips 骨骼之上还有父骨骼，Hips 骨骼不应该是模型的根骨骼吗？

这其实涉及到**角色骨骼系统的设计层级和用途划分**。

在很多情况下，**Hips（臀部骨骼）**确实是动画上**人体运动的根骨骼（motion root）**，但并不总是整个**骨架层级的根节点（hierarchy root）**。

让我们分层来看为什么会这样👇

---

### 🦴 一、Hips 不是“绝对的”根骨骼

在大多数 3D 动画或游戏角色中：

* **Hips** 是控制身体运动（走、跑、跳）的“动画根”；
* 但在骨骼层级上，常常在它之上还有一个或多个“技术骨骼（technical bones）”作为真正的根节点。

例如：

```
Root
 └─ Hips
     ├─ Spine
     ├─ LeftLeg
     └─ RightLeg
```

这里的 **Root**（有时叫 Armature、Root、CharacterRoot、World、PelvisCtrl 等）并不直接参与身体变形，但用于整体控制。

---

### 🧩 二、为什么要在 Hips 上面再加父骨骼

| 原因                        | 说明                                                                             |
| ------------------------- | ------------------------------------------------------------------------------ |
| **1. 用于整体位移和缩放**          | 游戏或动画中，角色可能需要整体平移、旋转或缩放，而不改变动画数据。如果 Hips 是根，任何平移都会影响动画数据，添加一个 Root 可以独立控制整体变换。 |
| **2. 动画分层与导出**            | 在游戏引擎（如 Unity/Unreal）中，动画通常驱动 Hips，但“Root Motion”提取自它的上层 Root，这样可以区分角色动画和场景移动。 |
| **3. Retargeting（动画重定向）** | 不同模型间可能骨架结构略有不同，添加一个上层 Root 便于统一动画坐标和方向。Mixamo、Humanoid Rig、UE Mannequin 都这么做。 |
| **4. 避免 Hips 的坐标污染**      | 动画导入时，若 Hips 同时承担局部动作和整体位移，会导致 Root Motion 不干净（走路动作中 Hips 会上下移动，影响整体位置提取）。     |
| **5. 方便 Rigging 控制**      | Rig 里常有“master control”或“root control”用来移动整个角色，避免直接操控 deform 骨骼（如 Hips）影响权重。   |

---

### 🎮 三、常见标准骨架结构举例

#### ① Mixamo 骨架：

```
Root
 └─ Hips
     ├─ Spine
     ├─ LeftUpLeg
     └─ RightUpLeg
```

* `Root` 控制整体位置；
* `Hips` 控制人物身体运动；
* 动画文件中的 Root Motion 通常从 `Hips` 计算，但真正的层级根是 `Root`。

#### ② Unreal Engine Mannequin：

```
root
 └─ pelvis
     ├─ spine_01
     └─ thigh_l
```

同理，`root` 是技术骨骼，`pelvis` 对应 Hips。

#### ③ Unity Humanoid：

* Unity 要求定义 “Root Transform”；
* 常是 Hips 之上还有一个 “Root”；
* 以便 Root Motion 和身体动画分离。

---

### 🧠 四、总结一句话

> **Hips 是动画的“身体中心”，但不是整个骨架的“技术根节点”。**

在动画编辑层面，Hips 是运动的关键点；
在工程或导出层面，Root（Hips 的父骨骼）负责整体的移动、缩放、世界坐标、Root Motion 抽取等。

---

# Hips 本身可以作为 Root Transform 吗，还是必须在它上面加一个 Root Bone 作为 Root Transform?

简单回答是：

> ✅ **是的，Hips 可以作为 Root Transform**，
> 但在不同工作流（特别是游戏引擎里），**是否推荐这样做要看用途**。

我们来分三种常见情况详细说一下 👇

---

## 🧩 一、Blender / 动画编辑阶段

在 **Blender** 或任何 DCC（数字内容创建）工具中，
Hips 完全可以作为角色的**动画根骨骼（Root Transform）**。

### ✅ 合理用法

```
Hips
 ├─ Spine
 ├─ LeftLeg
 └─ RightLeg
```

此时：

* 你直接在 Hips 上做角色整体的移动和旋转；
* 所有身体动作都围绕 Hips 动；
* 动画系统也以 Hips 的位置来计算 Root Motion。

### ⚠️ 限制

当角色要**整体移动（例如角色行走穿越场景）**时，
Hips 同时承担了：

* 上下身体晃动的动画；
* 整个角色的世界位移。
  这两种运动会**叠加在一起**，导致导出后提取 Root Motion 不干净。

---

## 🎮 二、游戏引擎导入阶段（Unity / Unreal）

这是最常出问题的一环。

| 引擎                     | 是否可以用 Hips 作为 Root Transform | 推荐做法                                                                             |
| ---------------------- | ---------------------------- | -------------------------------------------------------------------------------- |
| **Unity (Humanoid)**   | ✅ 可以                         | Unity 允许你选择任何骨骼作为 Root Transform（包括 Hips）。但为了干净的 Root Motion，官方推荐额外添加一个 Root。    |
| **Unreal Engine (UE)** | ⚠️ 不推荐                       | UE 的 Root Motion 系统要求 Root Bone 在最上层，不参与变形。因此 UE 通常要求 `root → pelvis (hips)` 结构。 |
| **Mixamo / FBX 标准**    | ✅ 支持                         | Mixamo 的动画文件中经常以 Hips 为根（没有 Root 骨骼）。但导入 Unreal 时往往需要手动添加一个 Root。                |

---

## 🧱 三、推荐的通用结构

### ✅ 推荐结构（更灵活）

```
Root
 └─ Hips
     ├─ Spine
     └─ Legs...
```

优点：

* `Root` 专门用于整体位移和缩放；
* `Hips` 保留身体局部动画；
* 导出到任何引擎都兼容；
* Root Motion 更干净，易于控制；
* Retarget（动画重定向）时更稳定。

### ⚙️ 如果项目简单（仅 Blender / Unity 内使用）

可以直接：

```
Hips
 ├─ Spine
 └─ Legs...
```

没问题，但以后若要做：

* Root Motion 导出；
* 动画重定向；
* IK 控制器系统；
  那再加 Root Bone 会更安全、通用。

---

## 🧠 总结一句话

> ✔️ **Hips 可以是 Root Transform，但不是最优设计。**
> ⚙️ **推荐在 Hips 之上再加一个 Root Bone，用于整体变换与 Root Motion 提取。**

---

# 当存在作为 Root Transform 的 Bone 时，整体移动骨骼，是应该移动 Hips，还是应该移动 Root Bone？

这个问题是**动画师、技术美术和程序员最常讨论的“Root vs Hips”职责划分**。

一句话总结：

> 🎯 **有 Root Bone 时，整体移动角色应该移动 Root Bone，不是 Hips。**

下面是详细解释，为什么要这么做、两者职责如何区分、以及 Blender / Unity / Unreal 的具体操作区别👇

---

## 🦴 一、Root Bone 与 Hips 的职责分工

| 骨骼            | 主要作用                    | 是否影响变形          | 谁在动画中驱动                    |
| ------------- | ----------------------- | --------------- | -------------------------- |
| **Root Bone** | 控制角色整体的位置、旋转、缩放（世界坐标级别） | ❌ 不影响网格（通常没有权重） | 动画控制角色在世界中的位移（Root Motion） |
| **Hips Bone** | 控制身体的运动中心（骨盆、重心）        | ✅ 有权重，影响身体形变    | 驱动身体动画（走、跳、扭腰等）            |

### ✅ 正确关系（推荐）

```
Root
 └─ Hips
     ├─ Spine
     ├─ LeftLeg
     └─ RightLeg
```

* 角色在世界中移动、旋转、朝向变化：移动 **Root**
* 角色身体扭动、跳跃、重心上下晃动：动画驱动 **Hips**

---

## 🎮 二、为什么不应该直接移动 Hips

如果你移动 Hips 让角色整体移动：

* 那个动作会包含身体晃动 + 世界位移；
* 当导出动画时，Root Motion 会混杂身体动作（例如走路时 Hips 上下抖动导致位移轨迹不干净）；
* 在游戏中提取 Root Motion 时角色可能“抖动”或“漂移”。

### 举个例子

走路动画中：

* **Hips** 在原地前后上下运动；
* **Root** 决定整个人的前进路径。

如果你移动的是 Hips：

```
Hips: →→→（含身体晃动）
Root: 固定不动
```

结果：身体在动，但世界坐标没变。
而游戏引擎提取 Root Motion 时，会得到上下抖动的轨迹，无法平滑地驱动角色移动。

如果你移动的是 Root：

```
Root: →→→（平滑前进）
Hips: 局部上下晃动
```

结果：身体动画干净，Root Motion 提取正确。

---

## 🧰 三、在不同软件中的行为

| 环境                       | 应该移动谁                            | 原因                                              |
| ------------------------ | -------------------------------- | ----------------------------------------------- |
| **Blender**              | 通常移动 Root 控制器（如果存在）              | 用于控制角色整体移动或放置位置；Hips 保留局部动画。                    |
| **Unity (Humanoid Rig)** | Root Motion 从 Root 或 Hips 提取（可选） | 若有 Root Bone → 优先使用 Root；若没有 → Unity 允许使用 Hips。 |
| **Unreal Engine**        | 必须移动 Root Bone                   | Unreal 的 Root Motion 系统默认从层级根（Root Bone）读取位移。   |

---

## 🎬 四、动画工作流举例

### 走路循环动画（有 Root Bone）

1. **Hips** 在原地前后上下摆动；
2. **Root Bone** 随时间沿 X 轴平滑前进；
3. 游戏中提取 Root Motion，让角色跟随 Root Bone 移动；
4. 播放时角色不会“在原地跑步”，而是平滑地走动。

### 动画在原地制作（常见工作流）

有些动画师为了方便，会让 Root 固定不动，只让 Hips 动（例如“在原地走路”循环）。
导出时，再由引擎使用 Hips 位移计算 Root Motion。
这种方式虽然行得通，但不如“Root Bone 驱动”干净可控。

---

## ✅ 总结要点

| 场景                              | 应该移动谁                |
| ------------------------------- | -------------------- |
| 角色在世界中平移、旋转                     | **Root Bone**        |
| 身体重心上下摆动、旋转、扭腰等局部动作             | **Hips Bone**        |
| 导出动画时需要 Root Motion             | **Root Bone 提供位移轨迹** |
| 没有 Root Bone 的模型（如 Mixamo 原始骨架） | 临时用 **Hips** 代替 Root |

---
