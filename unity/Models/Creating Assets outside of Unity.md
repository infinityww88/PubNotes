# Creating Assets outside of Unity

你可以在 Unity 之外为游戏角色，地形，以及其他环境物体创建复制模型。

Unity 支持 FBX 文件，你可以从绝大多数 3D 建模程序中导出 FBX 文件。

总是从 3D 建模程序中导出模型为 FBX，而不是保存应用程序文件到 Unity Project 中。不要直接使用 native 文件格式，即使使用 Unity 在 importing 它们之前也会将它转换为 FBX 格式。

## Scaling factors

Unity 物理和光照系统期望模型文件中游戏世界中一个单位是 1 米。

不同的 3D packages 的默认度量是：

- .fbx .max .jas = 0.01
- .3ds = 0.1
- .mb .ma .lxo .dxf .blend .dae = 1

当使用一个不同的 scaling factor 从 3D 建模程序中导入模型文件到 Unity 时，你可以通过开启 Convert Units 选项转换 file units 来使用 Unity scale。
