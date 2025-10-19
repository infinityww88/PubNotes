在建模工具中，人形动画模型和其他蒙皮骨骼动画模型没有区别。人形动画是 Unity Avater 中单独的概念。因此一个带人形动画的模型既可以作为 Humanoid 模型导入，也可以作为 Generic 模型导入。

Generic 模型就是一个模型的 animation clips 只能被自己使用。

- Humanoid 模型具有特殊的结构，包含最少 15 个骨骼，其组织方式大致匹配真实的人体骨骼。​
- Generic 模型是任何其他模型。它可以是茶壶，也可以是龙。

这里描述如何导入人形模型的导入。

当 Unity 导入包含 Humanoid Rigs 和 Animation 的 Model 文件时，它需要将模型的​​骨骼结构​​与其​​动画​​进行​​协调 reconcile​​。为此，系统会将文件中的每个​​骨骼​​映射到一个​​人形 Avatar​​，以便正确播放动画。因此，在将模型文件导入 ​​Unity​​ 之前，仔细准备该文件非常重要。

1. 定义 Rig type（Humanoid）并创建 avatar。
2. 修正并验证 Avatar 的映射。
3. 一旦你完成了骨骼映射，你可以（可选）点击 Muscles & Settings tab 来调整 Avatar 的 muscle 配置。
4. 你可以（可选）保存 Skeleton bones 到 Avater 的映射为 Human Template(.ht) 文件。
5. 你可以（可选）通过定义 Avatar Mask 限制导入的动画对特定骨骼的操纵。
6. 在 Animation tab 中，激活 Import Animation 选项，然后设置其他 Asset-specific 属性。
7. 如果文件包含多个 animations 或 actions，可以将特定 action ranges 定义为 Animation Clips。
8. 对文件中定义的每个 Animation Clip，你可以：

   - 选择 Pose 和 Root transform
   - 优化 Looping
   - 镜像 Humanoid skeleton 两侧的 animation
   - 添加 curves 到 clip 中，以动画其他 items 的 timings，就是为 animation 定义一条自定义曲线，用于程序中使用，类似 spline 为 knot 定义 data 一样
   - 添加 events 到 clip 中，在动画内的特定时间触发动作
   - 丢弃动画中的部分数据（某些骨骼的数据），类似在运行时使用 Avatar Mask，但是在 import 时使用
   - 选择一个不同的 Root Motion Node 来驱动 action
   - 读取任何 Unity 导入这个 clip 的相关消息
   - 观察一个 animation clip

9. 点击 Apply保存修改，或者 Revert 丢弃修改。

# 设置 Avatar

在 Rig tab 的 Inspector 窗口，选择 Animation Type 为 Humanoid。默认地，Avatar Definition 属性被设置为 Create From This Model。如果你保持这个选项，Unity 会尝试映射文件中定义的骨骼到一个 Humanoid Avatar 中。

有些情况下，你可以改变这个选项为 Copy From Other Avatar，以使用你已经为其他 Model 文件定义的 Avatar。例如，如果你在 3D 建模应用程序中创建了一个包含多个不同动画的 Mesh（皮肤），你可以将 Mesh 导出到一个 FBX 文件中，并将每个动画分别导出到各自的 FBX 文件中。当你将这些文件导入 Unity 时，您只需为第一个导入的文件（通常是网格）创建一个单独的 Avatar。只要所有文件使用相同的骨骼结构，你就可以将该 Avatar 重用于其余文件（例如，所有动画）。

如果你开启这个选项，你必须指定你想使用哪个 Avatar，在 Source 属性中指定。

你还可以使用 Skin Weights 属性改变影响一个 vertex 的骨骼的最大数量。默认，这个属性限制为 4 个，但是可以定义其他的值。

当点击 Apply 时，Unity 尝试匹配现有骨骼结构到 Avatar 骨骼结构中。很多情况下，它可以通过分析 rig 中的骨骼连接关系自动完成。

如果匹配成功，一个 check mark 就出现在 Configure 菜单旁边。Unity 还添加一个 Avatar sub-Asset 到 Model Asset 中，你可以在 Project View 中看到它。

一个成功的匹配简单意味着，Unity 能够匹配所有需要的 bones。但是，为了最佳效果，你还需要匹配可选的 bones 并在一个合适的 T-pose 中设置 model。

如果 Unity 没能创建 Avatar，Configure 按钮旁边会出现一个叉号，并且不会在 Model Asset 中创建 sub-Asset。

因为 Avatar 对 animation system 是如此重要的概念，正确配置你的 Model 非常重要。处于这个愿意，无论是否成功自动创建 Avatar，你都应该检查 Avater 是否有效已经正确设置。

# 配置 Avatar

如果你想检查 Unity 是否正确地将模型的骨骼映射到了 Avatar，或者如果 Unity 未能为模型创建 Avatar，你可以点击 Rig 选项卡上的 Configure 按钮以进入 Avatar 配置模式。

如果 Unity 成功创建了一个 Avatar，该 Avatar 将作为模型资源的 sub-Asset 出现。

你可以在 Project View 中选择该 Avatar asset，然后点击 Inspector 中的 “Configure Avatar” 按钮以进入 Avatar 配置模式。

此模式允许你检查或调整 Unity 是如何将模型的骨骼映射到 Avatar 布局上的。

一旦进入了 Avatar 配置模式，Inspector 中就会显示一个包含骨骼映射的 Avatar 窗口。

请确保骨骼映射是正确的，并且为 Unity 未分配的任何可选骨骼进行映射。

你的骨骼至少需要包含所需的必要骨骼，这样 Unity 才能生成有效的匹配。为了提高找到与 Avatar 匹配的机会，请以反映它们所代表身体部位的方式命名您的骨骼。

例如，“LeftArm” 和 “RightForearm” 可以清楚地表明这些骨骼控制的是哪些部位。

## Mapping strategies

如果 model 没能产生一个有效匹配，你可以使用一个类似 Unity 内部使用的过程：

1. 选择 Avatar window 底部的 Mapping 菜单中的 Clear 选项，重置 Unity 尝试的任何映射。
2. 选择 Avatar window 底部的 Pose 菜单中的 Sample Bind-pose，以近似 Model 的初始姿势建立 Model 的姿势。
3. 选择 Mapping > Automap 从初始 pose 创建一个 bone-mapping。
4. 选择 Pose > Enforce T-Pose 将 Model 设置回需要的 T-pose。

如果自动映射完全或部分失败，你可以通过从场景视图或层级视图中拖动骨骼来手动分配骨骼。如果 Unity 认为某个骨骼匹配，则该骨骼在 Avatar 映射选项卡中会显示为绿色；否则会显示为红色。

## Resetting the pose

T-pose 是 Unity 动画所需的默认姿势，也是在 3D 建模应用程序中建模时推荐的姿势。然而，如果你在制作角色时没有使用 T 姿势，并且动画没有按预期工作，你可以从姿势下拉菜单中选择“重置”（Reset）。

如果骨骼分配正确，但角色姿势不正确，你会看到消息“角色未处于 T 姿势”。你可以尝试通过从姿势菜单中选择“强制 T 姿势”（Enforce T-Pose）来解决这个问题。如果姿势仍然不正确，你可以手动将剩余的骨骼旋转至 T 姿势。

# 创建一个 Avatar Mask

Avatar Masking 允许你丢弃某个动画片段（clip）中的部分动画数据，使该片段只驱动对象或角色的**某些部位**，而不是整个对象。

例如，你可能有一个标准的行走动画，其中同时包含手臂和腿部的运动，但如果角色双手搬运一个大物体，你不会希望他们在行走时手臂向两侧摆动。

不过，你仍然可以在搬运该物体时使用标准行走动画，方法是通过使用一个 Mask，只播放搬运动画的上半身部分，并将其叠加在行走动画之上。

你可以在导入时或运行时对动画片段应用 Masking。导入时 Masking 更为推荐，因为这样可以避免丢弃的动画数据被包含在构建中，从而使文件更小，占用的内存也更少。此外，由于运行时需要混合的动画数据更少，处理速度也会更快。在某些情况下，导入时 Masking 可能不适合你的需求。在这种情况下，你可以通过创建一个Avatar 遮罩（Avatar Mask）资产，并在Animator 控制器（Animator Controller）的层级设置中使用它，从而在运行时应用 Masking。

要创建一个空的 Avatar Mask Asset，你可以：

- 从 Assets 菜单中选择 Create > Avatar Mask
- 在 Project view 中点击你要应用 mask 的 Model object，右键点击并选择 Create > Avatar Mask

现在你可以将身体的**某些部位**添加到 Mask 中，然后将该 Mask 添加到某个 Animation Layer（动画层），或者在 Animation（动画）选项卡的 Mask（遮罩）部分添加对它的引用。
