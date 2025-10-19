## Project Settings

- Chain Neighbour Keys

  开启时，一个属性中每个 channel 的同一帧的 keys 被连接在一起（默认开启）。这确保例如 position 属性（x，y，z）的每个 channel 在同一帧都有一个 key。

## Export Settings

这些设置被 Clip Export 过程使用。

- File Format

  Anim，Fbx Binary，Fbx ASCII

- Write Mode

  - Export As New File：导出操作创建一个新的文件，并覆写现有的文件
  - Update Existing File：导出动画片段到现有文件。同名的现有动画片段被覆写（一个文件多个片段，只覆写同名的片段，不影响其他片段）。用于附加动画到现有 3D 模型

- Clip Treatment

  - One Clip Per File

    导出 UMotion project 的每个动画片段为一个单独的文件。文件名是 UMotion project 中动画片段名

  - All Clips In One File

    导出 UMotion project 的所有动画片段到一个文件中。帧率在 fbx 文件中全局定义。这意味着文件中所有的 animation clips 都具有相同的帧率。第一个导出的 clip 定义 fbx 文件全局的帧率。

- Keyframe Reduction

  - Lossless：只移除冗余 keys（相同的 keys）
  - Lossy（Fbx only）：尝试通过应用一个容忍一定数量 error 的 key reduction 策略减少 fbx 的文件大小。这可以大大减少 fbx 文件大小。通常 fbx 文件大小不直接影响构建的文件大小，因为 Unity 在 import 时重采样 animation clips

- Position Error

  用于 position curves 的容错阈值，以 generic units 为单位

- Rotation Error

  用于 rotation curves 的容错阈值，以 generic units 为单位

- Scale Error

  用于 scale curves 的容错阈值，以 generic units 为单位

- File Scale

  导出时应用到 fbx 的 scale。Unity 使用米为单位，fbx 使用厘米为单位。默认导出 scale 为 0.01，Unity 默认导入 scale 为 100。当导出用在 Unity Asset Store 的 animation，应该使用 scale = 1

- Rotation Offset

  选择一个 bone/transform，从它获得一个 rotation offset 应用到 exported file。这用于当导出的动画没有正确旋转时。

- Destination Folder/File

  - One Clip Per File：导出目录
  - All Clips In One File：导出的文件

