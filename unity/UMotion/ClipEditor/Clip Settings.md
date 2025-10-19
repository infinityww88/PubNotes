- Chain Neighbour Keys

  当这个选项开启时，同一个 frame 上的 keys 的属性中的每个 channel 被连接在一起（默认 enabled）。这确保每个 channel（例如 position 属性的 x y z 分量）在同一个 frame 都有 key

- Clip Treatment

  - One Clip Per File
  - All Clips In One File

- Keyframe Reduction

  - Lossless：只移除冗余的 keys
  - Lossy（Fbx only）：通过应用一个 key reduction 策略（容忍一定程度的 error）来减少 Fbx 文件大小。这可以大大减少 Fbx 文件的大小。Fbx 文件大小通常不直接影响 built game 的大小，因为 Unity 在 import 时会重新采样（例如对 humanoid animations 或者如果开启 Resample Curves）。有损压缩，类似 mp3

- Position Error：position curves 的容错阈值，以 generic units 为单位
- Rotation Error：rotation curves 的容错阈值，以 generic units 为单位
- Scale Error：scale curves 的容错阈值，以 generic units 为单位

- File Scale：导出时应用到 *.fbx 的缩放。默认文件缩放是 0.01，Unity 以米为单位，fbx 文件以厘米为单位。如果导出的动画用到 Asset Store 上，scale 应该为 1

- Rotation Offset：选择一个 bone/transform，从它获取 rotation offset 以应用到 exported files 中。这通常用于导出的动画没有正确旋转时
- Destination Folder/File
  - One Clip Per File：目录名
  - All Clips In One File：文件名
