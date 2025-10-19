# Importing non-humanoid animations

一个 Humanoid 模型是一个非常特定的结构，包含至少 15 个骨骼，以大致和人体骨骼一致的方式组织。所有其他使用 Unity Animation System 的东西都属于 non-Humanoid，或 Generic 类别。这意味着一个 Generic 模型可能是任何东西，从一个茶壶到一条龙，因此 non-Humanoid 骨骼可以有任何可能的结构。

处理这个复杂性的解决方案是 Unity 只需要知道那个 bone 是 Root node。对于 Generic 角色，这等价于 Humanoid 角色的 center of mass。它帮助 Unity 确定如何以尽可能准确可靠的方式渲染动画。因为只有这一个 Root node 是公共约定的（mapping），而不像 Humanoid 有至少 15 个约定的骨骼，因此 Generic 不使用 Humanoid Avatar window。因此，导入 non-Humanoid 模型到 Unity 比 Humanoid 模型更简单。

1. 设置 Rig 为 Generic。
2. 你可以可选地限制导入的动画到特定 bones，通过定义一个 Avatar Mask（对于 Generic 也具有 Avatar Mask）
3. 在 Animation tab，开启 Import Animation 选项，然后设置其他 Asset-specific 属性
4. 如果文件包含多个 animations 或者 actions，你可以定义特定 frame ranges 作为 Animation Clips
5. 对于文件中每个 Animation Clip，你可以：
  - 设置 Pose 和 Root Transform
  - 优化 Looping
  - 添加 curves 到 clip，以 animate 其他 items 的 timing
  - 添加 events 到 clip，以在动画中触发特定动作
  - 丢弃部分动画数据，类似使用一个运行时 Avatar Mask，但是在 import 时应用
  - 选择一个不同的 Root Motion Node 来驱动 action
  - 阅读任何 Unity 导入这个 clip 的消息
  - 观察 animation clip 的预览
6. 点击 Apply 保存修改，或者 Revert 放弃修改

## 设置 Rig

参照 Importing humanoid animations 中的 “设置 Rig”

如果选择 Create From This Model 选项，必须选择一个 bone 作为 Root Node 属性。

Generic Avatar 和 Humanoid Avatar 不同，但是它出现在 Project view，它保存 Root node mapping，即 Generic Avatar 只有一个 bone 映射，而不像 Humanoid Avatar 包含一组 bones 的 mapping，因此没有 Configure Avatar 按钮。

## 创建 Avatar Mask

参照 Importing humanoid animations 中的 “创建 Avatar Mask”
