## Overview

AllIn1VFX 的目标是为 VFX artists 提供最佳 workflow，无论你是新手还是专家。

这个 Asset 移除了创建 VFX 和 shader 需要的绝大多数技术知识，同时提供强大的工具，自定义编辑器，学习资源，尤其灵活的 shaders。

所有东西都设计为对于有经验的 VFX artists 拥有它们需要的所有事情，并且希望加快他们的 workflow。而新手 artists 将会被提供以学习资料，例如庞大的 asset library 以及更多。

这个 Asset 拥有大量的功能，资源，和示例，但是使用 main features 是非常容易和直观的。

## All In 1 Vfx 组件

- Deactivate All Effects

  关闭所有 effects，但是不修改任何属性。如果再次激活 effects，就会得到之前的 visual results。

- New Clean Material

  创建一个新的 AllInVfxShader 材质，并赋给 Renderer。

- Create New Material With Same Properties

  使用之前的 AllInVfxShader 材质的相同属性创建一个新的实例。当你想创建当前 material 的变体时，这很有用。

- Save Material to Folder

  使用当前 GameObject 的名字创建一个 Material asset，并默认保存在 Assets/AllIn1VfxToolkit/MaterialSaves，保存路径可以在 Asset Window 中修改。这可以用于将同一个 Material 赋给很多不同的 Renderers。

- Apply Material To All Children

  将当前选择的 object 的 material 应用到它 Hierarchy 的所有 objcts。

- Render Material To Image

  渲染当前 Texture + Material 到一个 image texture。

- Add Particle System Helper

  添加 Particle System Helper 组件。这个选项只在 Particle System 出现在当前 GameObject 上时可用。

- Remove Component

  移除这个组件，而不改变任何东西。

- Remove Component add Material

  从 GameObject 移除组件，并设置 Sprite Material 为 Sprite/Default。

## Shader Structure and Usage

shader 组织为 3 个 blocks。

- Configuration

  这个 section 可以决定 material 的所有 render settings。

  改变这些设置对得到你想要的精确效果非常重要。这是 shader 的最重要部分，并且需要一点技术知识来对每种情况选择正确的配置。

  理想情况是不需要改变任何 Advanced Configuration settings，而只需使用顶部的 Presets，Presets 包括：

  - Transparent

    默认 preset。使用常规 Alpha Blending。这对使用带 alpha channel 的 texture 的 transparent materials 非常有用。

  - Additive

    Additive Alpha Blending，它累加 Material 的最终颜色到 frame。这意味着 block 将会不可见。这个 blending mode 用于没有 alpha channel 以及 black 背景的 textures，以及用于 bright effects。当背景不够 dark 时，Additive blendings 看起来会非常亮。

    注意：当 Additive Configuration 被勾选时，Alpha effects 将会影响全局效果的 greyscale 而不是 alpha。Shader 会读取 black color 为 alpha 0。这允许 shader effects 以和所有 presets 相同的方式工作。

    Additive 效果不使用 alpha channel，而是直接累加 RGB channel 得到最终颜色。Transparent 则是将 RGB 乘以 RGB 后再累加。

  - Soft Add（use with caution）

    类似 Additive preset，但是更加柔和一点，不会太亮。这里 Black 仍然是完全透明不可见。这个 blending mode 对于没有 alpha channel，具有 black background 但不是很亮的 textures 很有用。当一些 bright 或 glowing 的材质重叠时可能会遇到问题，对于这种情况可以使用 Additive preset 以及更小的 alpha 来得到类似的效果。    

  - Blend Add / Premultiply

    这个 preset 是 Transparent 和 Additive 的组合。这种 blending 在很多游戏（例如暗黑破坏神3）中被使用。这个 blending mode 的优势是它具有 additive 属性，例如 black background 被忽略，但是结果不会太亮，而且 Material 可以被 tint 为 black 而不 fading。

  - Opaque

    用于不透明的 Material。这种模式最高效，但是通常不会被用于 VFX。

- Shaders

  这是 shader 的核心。shader 在应用 effects 之前会计算一个 shape result（这是每个粒子的形状，不是最终所有粒子形成的形状）。shape result 将会通过组合最多 3 个不同的形状来形成。每个形状可以有不同的 texture，texture 可以滚动，旋转，扭曲，以及更多。Shapes 可以根据意愿开启或关闭，你总有一个开启的 Shape，然后可以使用 shape block 底部的 button 添加两个额外的 shapes。

  这个 workflow 将包括单独设置你需要使用的每个形状的所有属性和效果，然后组合它们来满足你的需要。要选择如何组合它们，你需要有至少一个 shape 开启，然后选择 Shape 的组合选项（每种 shape 的权重）。

  默认 shapes 都是乘到一起（颜色 multiply）的，但是如果想要它们加到一起（颜色 add）你可以设置 Add Shape Results toggle。通过 weight sliders，可以调整每个 shape 的影响度。

- Effects

  当 shapes 组合到一起时，effects 就会被应用。shape 结果将会被 effects 修改。有 3 中 effects：

  - Color effects：影响全局 shape result 的 color(rgb)
  - Alpha effects：影响 global shape result 的 alhpa
  - UV and Vertex effects：影响所有 textures（包括 shapes）的 texture 坐标，以及随时间替换目标 mesh vertices。


## Advanced Configuration and Key Rendering Concepts

如果 Configuration Preset 不能满足需求，可以调整高级配置。

- Alpha Blending Modes

  设置 shader output 的 blending，决定 shader result 如何混合到 final frame（颜色缓冲区）。因为 Material 通常都是透明的，你需要决定透明部分如何和 final frame 混合。

- Additive Configuration

  告诉 shader，这是一个 additive configuration。这会使 shader global result 的灰度被认为是 alpha。即直接使用 rgb 实现透明度，不考虑 alpha。这只在当 Blending Mode 设置为 Additive configuration 时有意义。

- Premultiply Alpha

  这会将 shader result alpha 乘到 color 中，当 alpha 小于 1 时可以有效地 darken color。

- Premultiply Color

  这会将 shape result greyscale（RGB 的平均值）乘到 alpha 中。当 color 是 black 时，这可以使结果不可见。result 颜色越暗，越不可见。

- Enable Z Write

  开启时，material 渲染的 mesh 将会写入 Z Buffer。

- ZTest Mode

  设置写入 Z Buffer 的条件，当前要写入的 depth 的值，和 Z Buffer 的 depth 的比较关系。

- Culling Mode

  - Off：双面渲染
  - Front：只渲染正面
  - Back：只渲染背面

- Color Write Mask

  选择 Material 写入哪些 channels。这决定了 shader output 的 channels。

- Random Seed

  为 texture 创建 scrolling，rotation，distortion variations 的数字。这用来为重用的 material instances 创建 variations。你可以使用它打断重复的 pattern。你可以通过 script 或 particle system 的 custom data 改变它。

- Use Unity Fog

  使材质被 Unity 的 Render Pipeline 的 fog 影响。注意，HDRP fog 是一个 post processing effect，因此这个 toggle 没有影响。

- Enable GPU Instancing

  使 Material 可以被 GPU 实例化（GPU instanced），来节省 draw calls。要使这个选项工作，所有 instances 中的 meshes 必须是相同的。

- Render Queue

  这会设置 material 的渲染顺序。越高的数字，越晚渲染。这对确保 material 正确的渲染顺序非常重要。你可以在 Project Settings，Graphics，Transparency Sort Mode 和 Axis 中选择 transparent objects 如何排序，但是有时我们还需要调整 Render Queue 的值以确保得到我们需要的渲染顺序。

## Particle System Helper Component

Particle System Helper Component 可以仅通过点击和输入，极大地加速 Particle System workflow。

通过使所有东西在相同的地方，以及当属性改变时自动刷新 particle system，你可以在几秒中之内得到你想要的 particle system。在此基础上，你可以创建和加载 particle system presets 来进一步加速你的 workflow，并为你经常用到的 setup 创建模板并重用它们。

Hierarchy Helpers 允许你创建当前 particle system 的副本作为 Child 或 Sibling GameObject，并使用 new copy number 来命名新的副本。

这可以在一个更复杂的 effect 中快速地添加更多的 sub particle systems。

Palette Color Change 使用一个 New Color 作为输入，然后 recolor Particle System 的所有 Colors 和 Gradients，来满足新的 color scheme。这可以为 particle system 快速创建 color variations。

按下 Custom Data Auto Setup 将会开启 Particle System 的 Custom Data section，并配置它来为每个 particle 设置一个随机 timing seed，还可以添加你需要的 vertex stream，根据你是否有 effects 使用它。Vertex streams 的 effects 包含两种 Custom Stream effect：Fade effects 和 Texture Offset。然后你可以使用生成的 curves 来调整 effect 到你想要的效果。

- General Options

  快速访问粒子系统的所有 main 属性。这个 section 可以免去你的很多 clicks，并加速 workflow。

  各个属性值在添加组件时，可以从 particle system 中获取。也可以在需要的时候点击 Fetch 按钮重新获取。

- Emission Options

  允许你快速设置 particles 如何发射。你可以选择 1 burst 或 constant 发射速率，并快速地调整其值。

- Shape Options

  快速设置粒子系统的发射 shape。None 意味着从 Transform origin 发射。

- Over Lifetime Options

  创建一个简单地 递增或递减的 Color 或 Size Over Lifetime gradient。你可以用这个选项快速的 prototype effect，然后再精确调整 curve 来获得更准确的效果。

- Particle Helper Preset

  引用这个组件保存的数据的副本。这个选项允许你保存和加载这个组件的 presets，使得你可以重用它来满足你的需要，并加速你的 workflow。

- Particle System Presets

  保存和重用 Particle System 的配置。

- Apply All Options Settings

  开启这个选项时，属性的改变将更新 Particle System。如果要避免自动更新，而是手动应用 changes，关闭这个选项，然后使用 Apply button。这样既可以调整 particle system，也可以使用 Helper 来快捷设置 particle system。

## Asset Window

通过 Window > AllIn1VfxToolkitWindow 打开 Asset Window，它提供了一组设置选项和工具，并划分为 3 个 sections。

- Save Paths：设置 asset 生成的 Materials，Presets，Textures 的不同的保存路径。

- Texture Editor：用来编辑现有 Textures。它可以用于快速调整纹理外观，旋转、翻转它们。

- Texture Creators：可以创建 Normal Map textures 用于 Screen Distortion effect（或任何其他可能的场景），创建 Gradient Textures 用于 Color Ramp effect 或 regular greyscale gradients（经常用于其他 effects 的 masks 或 shape textures，创建 atlas textures 来随机你的 Particle Systems，创建 Tileable noise textures 用于你的 effects。

  - Normal/Distortion Map Creator

    从一个 Target Image 生成一个 Normal Map。调整 Strength property 使 normal map 更明显，调整 Smoothing 来 blur 结果。

  - Color Gradient Editor

    编辑 Color Gradient，选择一个 texture size（如果 filtering 设置为 Bilinear 它通常会很小），选择 texture filtering 点击 Save button。这可以用于创建 textures 用于 Color Ramp 效果，或者 black and white masks，用于 effects。

  - Texture Atlas / Spritesheet packer

    用于将多个 images 打包到一个 atlas 中。这对创建 particle system 的 variation 非常有用。例如可以使用一个 4x4 texture 然后使 System 每次播放时在 Texture Sheet Animation tab 中随机选择一个。

    要使用这个工具，添加 desired textures 到 Atlas array。选择 Columns 和 Rows 的数量，然后选择 Atlas size 和 filtering，然后 Save。

  - Tileable Noise Creator

    允许你预览、编辑、保存 8 种 tileable noise textures，用于 effects。通过几次点击来创建和编辑 tileable noise 可以节约大量时间。

- Others

  - Auto Setup Pipeline shader variant。这个 asset 有一些 shader variants，两个用于 Built-in Render Pipeline，1 个用于 URP，1 一<F12>个用于 HDRP，一个包含 3 个 pipeline 中开箱即用的 effects。这些 shader variants 会被 asset 自动切换和维护。

  - Disable Depth and Scene Color Effects：如果使用 URP 2D Renderer，有 3 个 effects 是你想要避免的，因为开启这些 effects 的 graphics features（Soft Particles，Depth Glow，Screen Distortion）在这个 pipeline 中不支持。使用这个 feature，可以确保这 3 个 effects 在所有的 desired folder 的所有 materials 中关闭。

  无论哪种情形，先选择你想要处理的 Materials 所在的目录，然后点击下面的按钮开始处理。

## Textures Setup

绝大多数情况下，这是 texture 的 import setting 的 Wrap Mode 为 Repeat 是最好的。这确保当使用滚动纹理时得到正确的结果。

## Saving Prefabs

默认情况下，这个 asset 不保存你使用的 Material，而是将它作为 Scene 的一部分保存以避免太多 objects 充满 project。这意味着，默认情况下，当你把一个设置 AllIn1VfxShader material 的 GameObject 转换为 Prefab 时，prefab 不会正确渲染，因为它在 Project Asset files 中没有对 Materials 的引用。

为了保存为 Prefab，必须先将 Material 保存为 asset。点击 Save Material To Folder 保存 Material。


## Screen Distortion and Creating Distortion Maps

Screen Distortion 是一个 effect，它基于一个 Distortion Map Texture 扭曲最终的 frame。注意这个 effect 非常消耗性能，尤其是在 Built-in Render Pipeline 中。

Normal map 可以在 Unity 之外创建，也可以在 Unity 中使用 All In 1 Vfx Window Texture Creator 创建。

## Custom Vertex Streams and Custom Data Auto Setup

一些 effects 可以使用 Particle System Custom Data 控制它们。这些 effects 是 Fades/TextureOffset Custom Stream 和 Shape Weights Custom Stream，它们随时间 fade 或 scroll particles。

要在 Fade From Noise Texture 或 Fade From Final Shape effects 上使用这个 feature，需要首先选中 Fade Amount Driven By Vertex Stream Toggle，之后 Particle System 的 Custom Data 将会负责随时间改变 Fade Amount。如果 toggle 设置为 false，effect 的 alpha 将会负责 Fade Amount。

Procedural Dissolve 也是一样。

Texture Offset effect 只在 Particle System 上的 Materials 可用，并只显示 enabled 的 shapes。然后通过改变每个 shape 的 multiplier property 选择相应的 shape 被影响多少。

Shape Weights Custom Steam 和 Texture Offset 类似。它只在 Particle System 的 Material 上可用，并只显示 enabled 的 Shapes。

负值将使相应的 Shape 更不可见，正值相反。这可以被用来 fade in/out particle 的一部分。


要设置 Custom Data，使用 Particle System 组件的，并点击 Custom Data Auto Setup 按钮来自动添加 vertex stream channels。可以添加多个 Channel。

## How to Animate Materials

Custom Material Inspector 属性可以向其他 Unity 组件一样通过 Animation window 记录动画。

注意：UI Material 属性不能使用 Animator 制作动画，因为 Unity 不允许 animate shared material 属性。Unity UI Images materials 总是 shared 的，这意味着所有 images 使用一个特定 image 的完全相同的 material 实例，因此如果一个属性为一个 Image material 改变，那个 share material 的所有其他 images 也会改变。因此 Unity 不允许这种行为，也不支持在 UI Material 属性上使用 Animator。

建议使用 DoTween 通过 code 来动画 UI material 属性，也可以用脚本自己实现动画逻辑。

还要考虑到 UI material 实例是共享的，你可能想要为每个 material 通过脚本创建一个副本：

```C#
private void Awake()
{
	Graphic graphic = GetComponent<Graphic>();
	graphic.material = new Material(graphic.material);
}
```

## Scripting

可以通过脚本修改 Material 属性。这通常用于 Mesh Renderers，对于 Particle System Material 没有太大意义。

可以通过悬浮光标到 Material Inspector 上的任何属性来看到这个属性的在脚本中的名字，例如 "\_ALPHA"。然后使用 Material.SetFloat/SetColor/SetTexture 等函数修改材质属性。

还可以查看 AllIn1VfxToolkit\Shaders\Resources\AllIn1Vfx.shader，接近 200 个属性都位于 Effects and Properties Breakdown section 下。

```C#
Material mat = GetComponent<Renderer>().material;
mat.SetFloat("_Alpha", 1f);
mat.SetColor("_Color", new Color(0.5f, 1f, 0f, 1f));
mat.SetTexture("_MainTex", texture)
```

## Visual Effect Graph(Vfx Graph)

## How to Enable/Disable Effects at Runtime

- 所有 effects 都有一个属性值组合来使它们看起来 deactivated（通常是将 amount 或 blend 属性降低为 0，但是这个依赖于具体 effect 而不同）。因此最干净的 deactivate 和 activate 的方式是通过 enabling 所有你使用的 effects，然后动态改变属性值。

- 另一个方式不够高效，容易混乱，并且如果你没有完整包含依赖，会导致 materials 在 final build 中变得不可见。通常避免使用这种方式，最好使用第一种方式。这个方法主要是在运行时开启和关闭 shader 编译开关，因此 Unity 会在运行时编译和替换 shader（在 final build 中，shaders 不能被编译，因此每个具有不同属性组合的 shader variant 必须在运行时可用以避免错误）。如果你确定对一个 resulting toggle 组合有一个 shader variant，就可以使用 Enable/Disable 方法：

```C#
Material mat = GetComponent<Renderer>().material;
mat.EnableKeyword("GLOW_ON");
mat.DisableKeyword("GLOW_ON");
```

如果你真的向使用这个功能，而且知道你在做什么，以及如何避免前面提到的错误，可以将光标悬浮到 material inspector 上，确定开关的名字，例如 "GLOW_ON"。

## Random Seed

Asset shader 有一个 random seed 属性（\_TimingSeed）。这个属性可以为 material 提供变化。不同的 seed values 会导致 shader 上不同的 scroling，rotations，和 distortions。在使用相同的 materials 之间使用不同的 seeds 可以产生视觉变化。这可以避免使用相同 Material 的 meshs 产生重复。

对于 Particle System，可以添加 Particle System Helper Component，然后点击 Custom Data Auto Setup 按钮。Custom Data section 的 0-100 X axis 属性就是 random timing seed。

对于 Meshes，可以简单点击 All1VfxRandomTimeSeed 脚本到 GameObject，然后 Random Seed 就可以在 Start 是被赋值到 Material 上。注意 shader 已经被设置为 GPU instance 这个属性，因此你可以在 Material Inspector Advanced Configuration 开启 GPU Instanceing，并且即使你在所有 mesh instances 上使用这个脚本，instancing 也不会 break。

## Render Material To Image

点击 Render Material To Image，当前 GameObject 的当前 Texture + Material 被渲染到一个 texture，并被保存。

在这个 asset window，可以改变默认保存路径，以及 Rendered Image Texture Scale。因为 output 看起来会比 in-engine version 略微模糊一点，因此可以为 result 使用更大的 scale，这样重新引用到 in-engine 时可以显得更清晰。

这个功能可以用了从 gpu offload 一些工作，或者创建 texture 的变体。通过 baking result 到一个 texture，意味着 GPU 不需要每一帧都计算全部 effects。始终记住，这个 asset 一开始设计为高效运行的，无论是在低端还是高端设备，因此这只是供你使用的一个工具，但是不要过早优化（将所有 Materials 渲染到一个 texture 上）。只在遇到运行时问题时才使用这个工具进行性能优化。

你可以使用这个 feature 为一些 VFX 来预渲染一个 image，或者预渲染一个 texture 然后用来在 asset shader 进行修改。这个 feature 允许你递归地 stack 和 re-apply asset effects，无论你想要执行多少次。

## Premade Textures, Meshes and Materials

Asset 包括很多你可以用于 project 的 textures，meshes，materials，并允许你 prototype effects，甚至创建完全 awesome 专业的 effects，而不需要创建自己的 assets，并节省大量时间。

## Helper Scripts and Other Utilities

Asset 包含一些额外的脚本和工具，在一些情况下很方便：

- Particle System Helper（AllIn1ParticleHelperComponent.cs）
- Look At（AllIn1LookAt.cs）

  用来是一个 GameObject 面对一个特定方向。你可以选择每一帧 Update 时都面对一个方向，或者仅在 Start 设置方向。可以选择一个 Transform 作为 target，或者 target 到 Main Camera。最后选择那个 axis 朝向 target，默认是 Forward 向量。

- Bouce Animation（AllIn1VfxBounceAnimation.cs）

  随时间 back and forth 动画 transform 的位置。开始位置是 origin point，然后可以选择一个 Target Offset 以及一个 speed 来调整动画。

- Auto Rotate（AllIn1AutoRotate.cs）

  随时间在选择的 axis 旋转 transform。

- Auto Destroy（AllIn1VfxAutoDestroy.cs）

  在实例化之后 N 秒销毁 GameObject。如果你想要清理 Particle Systems，设置 Stop Action 为 Destroy（这是最佳实践，因为它更干净更高效）。

- Scroll Shader Property（AllIn1VfxScrollShaderProperty.cs）

  使用一个 shader 的属性名字符串，随时间增加或减少它的值。如果需要可以应用一个取模操作，这对于想把一个值保持在一个特定范围的属性非常有用，例如将角度限制在 0-360 度之间。还可以在一个 min 和一个 max 值之间进行 pingpong 操作，已经选择 scroll 的速度。

- Screen Shaker and DoShake（AllIn1Shader.cs 和 AllIn1DoShake）：这个两个组件的组合可以 shake 任何 GameObject Transform，它是个简单实现但高效的 shaker。DoShake 组件可以添加到任何需要在实例化时 shake camera 的 effect 上。这个组件会在 start 时调用 AllIn1Shaker.i.DoCameraShake(shakeAmount)。因为 Shaker 组件遵循 singleton 模式，你可以使用上面的函数调用在任何需要的时候激活一个 shake。

- Scale Tween（AllIn1DemoScaleTween.cs）：这个组件创建一个 Scale Down，Scale Up 过程化 code 动画，通过调用 ScaleUpTween() 和 ScaleDownTween()。在 Demo 中用于 Button，以 polish UI 和 GamePlay 交互。有很多方式可以实现这个功能（例如 DOTween）。

## Effects and Properties Breakdown

## Custom Gradient Property Drawer

## Running out of Shader Keywords

