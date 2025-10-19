## Exporting

UMotion 可以导出动画片段为 Unity 的 *.anim 文件或者 *.fbx 文件。在导出动画片段之前，需要配置 exporter。

绝大多数情况，*.fbx 是首选的选择。 *.fbx 文件内部使用欧拉角而不是四元数表示旋转。因此，即使 UMotion 使用四元数曲线，也可能导致 Gimbal Lock 问题。

## Importing

导入现有动画到当前 UMotion project 中。

要添加多个文件到 Import Clips Dialog 中，在 Project Window 中选择多个文件，并拖拽到 list view 中。

| UI Element | Description |
| --- | --- |
| Add Clips | 添加动画片段到 import list 中。可以选择 *.anim 文件，UMotion 项目文件，或者任何 Unity 支持的 3D 模型文件。对于后面二者，文件中所有的 animation clips 将被添加到 import list 中 |
| Select All | 选择 import list 中所有的 clips |
| Deselect All | ... |
| Try Convert To Progressive | 当开启时，如果可能的话，不损失任何质量地将所有 rotation 属性转换为 Progressive Quaternion Rotation |
| Disable Animation Compression | 对从 3D 文件中导入的 clip 设置 Import setting "Animation Compression" 为 None。这确保 clips 以最高质量导入。原始 setting 在导入过程完成之后恢复 |
| FK to IK Conversion | 自动转换导入的 clip 到 IK。只有在 project 中配置了 IK chains 时可用 |
| Delete FK Keys | 当开启时，被转换为 IK 的 FK 被删除 |
| Animator Foot IK | 只有当前 project 是 Humanoid 类型时可用。开启时，在导入时，应用 Animator（Unity Mecanim）的 Humanoid Feet IK。这确保 feet 到达它们的原始位置（当 retargeting 一个动画到一个不同比例 legs 的模型时就会如此） |
| Animator Hand IK | 类似 Foot IK |
| Abort | ... |
| Import | 导入选择的所有 animation clips 到 list 中 | 
| | |

可以将一个 humanoid animation clip 导入到一个 generic project 或者反之。

为了使 UMotion project import 正确工作，rig 配置需要完全一样。这意味着 characters 的 rigs 需要匹配，而且自定义创建的 joints/transforms 和所有约束 constraints 需要以相同方式配置（几乎就是这个模型或它的副本）。

## 在 humanoid/generic 中转换

可以在 humanoid 和 generic 之间转换，就像将一个 humanoid project 导入到一个 generic project 或反之一样。

Example Workflow

这个例子，一个包含 generic 类型的 character animations 被转换为 humanoid：

- 在 Unity Project Explorer 中复制 character 的模型（非破坏性）
- 选择复制的模型，在 Inspector 中设置它为 humanoid 类型
- 拖放复制的模型到 Scene View 中
- 创建一个 humanoid 类型的 UMotion project，并在 Pose Editor 中指定复制的模型
- 在 Clip Editor 中点击 "File -> Import Clips"
- 点击 Add Clips 并选择应该转换的 UMotion 项目文件
- 点击 Import
- 就这样。一旦新导入的片段被导出，它们就可以被用于你所有的 characters（retargeting），因为这些动画片段现在是 humanoid 类型的
