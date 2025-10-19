# 导入模型

Model 文件包含各种类型数据。例如一个角色或者地形 mesh，动画骨骼和片段（片段包含骨骼沿时间线的数据），以及材质和纹理。几乎可以肯定，你的文件不会包含所有这些元素，但是你可以按照需要设置特定资源的导入选项。

导入的源就是建模软件导出的fbx等资源文件。

在 Project 面板选中导入的模型文件，Inspector 中将显示 Import Setting 窗口

所有外部资源都需要导入（模型、纹理、音频），都有各自可以调整的导入选项，它们也可以在 Editor 脚本中自动设置。

## 模型相关导入选项

角色和动画模型在 Model tab 提供了更多的选项

- 使用 Scale Factor 和 Convert Units 属性调整 Unity 如何解释 units。例如 3ds Max 使用1个单位表示10厘米，而 Unity 使用一个单位表示1米。
- 使用 Mesh Compression，Read/Write Enabled，Optimize Mesh，Keep Quads，Index Format，或 Weld Vertices 属性来减少资源和节省内存。
- 为 environment geometry（mesh）开启 Generate Colliders 选项
- 开启特定于 FBX 的设置，诸如 Import Visibility，Import Cameras，Import Lights
- 对于只包含 Animation 的模型文件，开启 Preserve Hierarchy 选项防止 hierarchy 和 skeleton 不匹配
- 如果 Mesh 使用 Lightmap，设置 Swap UVs 和 Generate Lightmap UVs
- 可以使用 Normals，Normals Mode，Tangents 或者 Smoothing Angle 选项精确控制 Unity 如何处理模型中的 Normals 和 Tangents

## Rigs和Animation相关选项

如果模型文件包含动画数据，在 Rig tab 设置 Rig，然后在 Animation tab 导出或定义动画片段。

人形动画和通用动画的 workflow 是不同的。因为 Unity 需要具体详细的人形骨骼结构，但是对于通用类型动画只需要知道 root node。

