# Creating custom Surforge assets

Surforge 带有一个丰富的 asset 集合，并且它计划在将来的版本中扩展它到更多。

还可以为所有类型创建自己的 assets 在 Surforge 中使用。现阶段，没有特殊的工具用于资源创建，但是 Surforge 是基于 Unity prefabs 的，因此添加它们并不难。

通用方式，也是最简单的方式，是复制合适的 Surforge asset（即 Unity prefab），并调整它的属性。然后你必须为它创建一个 icon，并添加你自己的 asset 引用到适当的 list。

## Creating material sets.

Material Sets 是最容易添加的 asset type。不需要复制它或者手动添加的特定的 list。按下 Save material set 按钮，来创建当前激活 material set 的一个副本，保存到 Assets/CustomPresets/MaterialSets 中。当你开始操作一个新的 texture 时，它将会自动加载，并且和内置的 material sets 一起被添加到 dropdown 菜单中。这非常便于创建相同风格的 textures 集合。Material sets 自己存储 materials，没有只连接到它们（即创建了 material 的副本。material 只是包含 shader 参数的数据资源）。

## Creating materials.

点击 Save current material button 保存当前选择 material 的副本。它将被保存到 Assets/CustomPresets/Materials 目录。现阶段，你必须手动添加它的引用到 Surforge/Editor/surforgeSettings prefab 的 Materials list。当 Surforge 重启后，它将会被添加到 Materials tool panel，然后用于 material 拖放。不需要创建 material icon，因为它被自动渲染。添加自定义 materials 的方法在将来的版本将会被改进。

## Creating Add Detail tool assets.

创建你自己的 3D 模型，保存它为 .fbx 或 .obj 文件。Fbx 更好，因为它可以同时存储多个 models。确保你的 model 的 local positions 被设置到 scene origion，并且突出高于 grid，使得它们正确地实例化到 scene 中。

复制你的 model 文件到 Unity Assets 目录，设置合适的 import scale。创建一个 prefab 并添加一个 PlaceMesh 脚本，脚本位于 Assets/Surforge。为 light 和 dark skin 创建和添加 icons。

如果你的 asset 有 UVs 和 normal/ambient occlustion maps，添加它们到相应的字段中。你可能设置选项来随机化你的 asset UVs 的位置，这样每次实例化它们都会有一个随机的 UV 位移。如果你的 asset 有多个 variants，添加它们的 prefabs 到相应的 list，当使用 Add Detail tool 时点击右键可以随机化它们。

添加你的 prefab 的引用到 Assets/Surforge/AddDetailTool/placeMeshes prefab，placeMeshes 列表。当 Surforge 重启后，它将会被添加到 Add Detail tool assets 列表中。在将来版本中，将会实现一个自动加载模型的工具。

## Creating Poly Lasso profiles.

Poly Lasso profiles 不是基于 based 的，因此不需要在 3d editor 中创建任何模型。它们是完全通过 Unity Editor 设置的，通过大量的参数。它们的结构并不简单，但是如果你有胆量，在 Assets/Surforge/PolyLassoProfile.cs 下面有一个 parameters specification（参数说明）。

你还可以复制一个现有的 Poly Lasso profiles，并将它用作 base。它们位于 Assets/Surforge/PolyLassoProfiles/Profiles。当调整了 profile prefab 之后，为它创建 icons 并添加引用到 Assets/Surforge/PolyLassoProfiles/polyLassoProfiles prefab。在未来的版本中，计划实现一个 Poly Lasso profile editor。

## Adding custom skyboxes.

创建两个 .exr 文件，一个用于 lightning 的 skybox，一个用于 texture preview background 的 blurred skybox version。它不需要很高的分辨率。Surforge skyboxes 是 1024 x 512 的。

在 unity 导入 skyboxes 为 cubemaps，创建空的 prefab 并添加 SurforgeSkybox 脚本，位于 Assets/Surforge。添加 cubemap 和 blurred cubemap 材质到相应字段，创建并添加 icons。

将自己的 skybox prefab 的引用添加到  Assets/Surforge/Editor/surforgeSettings 的 Skyboxes list，并重启 Surforge。

## Adding custom decals, deform and shatter presets.

所有这些和上面一样。为 decals assets 导入模型。制作现有 asset 的副本，调整参数，添加 icon 和对你的 prefab 的引用：

- Assets/Surforge/Decals/decalSets - decals.

- Assets/Surforge/NoisePresets/noisePresets - deforms.

- Assets/Surforge/ShatterPresets/shatterPresets - shatter presets.
