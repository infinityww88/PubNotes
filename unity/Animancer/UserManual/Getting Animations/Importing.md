# Importing

你可以通过复制文件到 Project 的 Assets folder 的任何地方来导入资源。然后在 Project Window 中选择 imported asset，并使用 Inspector 来查看和编辑它的 import setting。

## Rig

当导入一个 model 时首先要做的是进入 Rig tab，并设置 Animation Type 到 Humanoid 或 Generic：

- Humanoid

  Character 必须有一个特定骨骼集合，然后 Unity 将能够使用它的 Retargeting system 在那个 character 上播放任何 Humanoid animation。

- Generic

  Character 可以有任何 骨骼层次结构，但是 Generic animation 只能播放在它被构建的特定骨骼 hierarchy 之上。这还使得 Generic animations 被 Humanoids 性能更佳。

Mixamo 还可以在你下载它们之前 retarget 它的 animations 到任何 character，允许你将 Humanoid 设置为 Generic Rig 来节省性能。

Generic Rig 的剩余选项通常应该按如下配置：

| Option | Selected | Reason |
| --- | --- | --- |
| Avatar Definition	| 从 Model 中创建 | 你通常想要 character model 定义所有动画将会使用的 bone hierarchy，但是如果你在多个 characters 中使用相同的 Rig，或者如果你从 model 单独地导入 animation 文件，你可以相反地使用 Copy From Other Avatar |
| Root Node	| Hips | 仅在 Generic Rigs。你通常想要使用 model 的 hierarchy 的 topmost bone 作为它的 root。如果你不想使用 Root Motion 来移动 character，设置 Root Node 为 None 将会提升性能 |
| Skin Weights | Standard (4 Bones)	| See the Unity Manual for details |
| Optimize Game Objects	| Enabled | 通过不为 character 的每个 bone 创建一个 Hierarchy 的 Transform 来改善性能 |
| Extra Transforms to Expose | Right Hand | 如果你想要在运行时能够访问 character bones 例如将一个 weapon 放到它们手上，你需要选择要 expose 的 bones。使得它可以从 Optimize Game Objects setting 排除它们 |
| | | |

![character-rig](../../../Image/character-rig.png)

## Animation

一个从 Mixamo 将会包含一些我们不想要的 empty animation data，因此你可以简单地在 Animation tab
 deselect Import Animation。

![character-animation](../../../Image/character-animation.png)

Unity Manual 解释当文件实际包含你想要导入的 animations 时如何使用 Animation tab。

如果你从一个 model 中单独地导入一个 animation 

- 你必须为这个 model 在 Rig tab 设置 Animation Type 来匹配你选择的 type
- 如果你使用 Generic Rig 而没有 Root Motion，你可以将 Avatar Definition 设置为 No Avatar
- 否则你可能应该使用 Copy From Other Avatar，并且选择模型的 avatar。或者如果你想要配置它区别于这个 animation，可以使用 Create From This Model

![animation-rig](../../../Image/animation-rig.png)

## Materials

Mixamo 嵌入 character 的 textures 到 FBX 文件中，但是为了使 Unity 使用它们，你需要进入 Materials tab，并使用 Extract Textues... 来保存它们到 project 的某些地方（包含 FBX 的 folder 通常是一个很好的地方，或者你可能想要创建一个 Textures folder）。

如果弹出一个 NormalMap settings 窗口，解释说一个 texture 被用作一个 normal map，简单地点击 Fix now 按钮，来正确地设置它的 import settings。

![character-materials](../../../Image/character-materials.png)
