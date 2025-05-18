## 设置基本的 Cinemachine 环境

最少必要设置：

- 创建一个 passive Cinemachine Camera，不指定 behavior
- 确保 Unity Camera 包含 Cinemachine Brain 组件
- 调整 Cinemachine Camera 属性，观察它如何影响 Unity Camera

场景中必须仅包含一个 Unity Camera。

要添加一个 Cinemachine Camera：

- 在 Scene View 中，调整 View 得到你想要 Cinemachine Camera frame 的 point of view
- GameObject > Cinemachine > Cinemachine Camera

  Unity 会添加一个新的 GameObject，它包含：

  - Cinemachine Camera 组件
  - 一个 Transform，它匹配 Scene view camera 的 position 和 orientation

当在 Scene 中创建了第一个 Cinemachine Camera，Unity 自动添加一个 Cinemachine Brain 到 Unity Camera，除非 Unity Camera 已经包含了一个。

一旦有了 Cinemachine Brain，Unity Camera 的 transform 和 lens 设置被锁定，并且不能在 Camera Inspector 中修改。只能通过修改 Cinemachine Camera 中的对应属性来修改相应 Unity Camera 的属性，包括 Position 和 Rotation。

## 设置多个 Cinemachine Cameras，管理 control 和 transitions

- 使用不同的属性创建多个 Cinemachine Cameras
- 在 Cinemachine Brain 管理 Cinemachine Camera 的 transitions
- 在 Play Mode 中测试 Live Camera 激活机制和 transitions

### 管理 Cinemachine Cameras 之间的 transitions

- 在 Hierarch 中选择 Unity Camera
- 在 Cinamachine Brain 组件的Inspector 中
  - 在所有 Cinemachine Cameras 中选择 Default Blend，或者
  - 创建并定向一个 asset，其在特定 Cinemachine Cameras 之间定义了要使用的 Custom Blends

### 在 Play Mode 中测试 transitions

- 进入 play mode
- 按顺序改变每个 Cinemachine Camera 的 active status，以查看它们之间如何按照 Cinemachine Brain 中的设置彼此 blend
- 退出 play mode

## 添加 procedural behavior 到 Cinemachine Camera

- 添加 behavior 来控制 camera position 和 rotation
- 指定一个 GameObject 来跟踪，让 Camera 自动跟随和瞄准
- 添加默认 noise 来模拟真实世界的物理相机震动 shaking
- 添加 extension 来得到更高级的 camera behavior

注意：

- 你必须至少创建一个 passive Cinemachine Camera（没有特定 behavior）的 Cinemachine Camera
- Scene 必须已经包含一个可以使用 Cinemachine Camera 跟随的 GameObject

### 添加 Position Control 和 Rotation Control behavior

- 在 Hierarchy 中选择 Cinemachine Camera GameObject
- 在 Cinemachine Camera 组件的 Inspector 中，设置 Position Control 属性为 Follow
  Unity 会添加 Cinemachine Follow 组件到 GameObject 上
- 设置 Rotation Control 属性为 Rotation Composer
  Unity 添加 Cinemachine Rotation Composer 组件到 GameObject 上

可以在 Editor 菜单中直接创建要给 Follow Camera 可以得到相同的结果：GameObject > Cinemachine > Targeted Cameras > Follow Cameras > Follow Camera。

Cinemachine 包含一组可用的 Position Control 和 Rotation Control behavior。

一个 Cinemachine Camera GameObject 只可以同时只可以拥有一个 Position Control behavior 和一个 Rotation Control behavior。如果编辑一个 behavior 组件的属性，然后选择另一个 behavior，之前的编辑将丢失。

### 指定一个要跟踪的 GameObject

上一步选择 behavior 需要要给跟踪目标。

- 在 Cinemachine Camera 组件的 Inspector 中，设置 Tracking Target 属性为要跟踪的 GameObject。
- 在场景中移动 Targeted GameObject 来测试 Cinemachine Camera behaviors。
  Cinemachine Camera 总是自动相对于 GameObject 放置 Cinemachine Camera，按照 Follow behavior 的逻辑；同时旋转 Camera 来瞄准 GameObject，根据 Rotation Composer behavior。

### 为 camera shaking 添加 noise

可选地添加 noise 来模拟真实世界物理相机 shaking：

- 在 Cinemachine Camera 组件的 Inspector 中，设置 Noise 属性为 Basic Multi Channel Perlin。
  Unity添加Cinemachine Basic Multi Channel Perlin 组件到 GameObject
- 在 Cinemachine Basic Multi Channel Perlin 组件中，点击 Noise Profile 右边的 configuration button。
- 在 Presets 下面，选择一个现有的 Noise Settings asset。
- 进入 Play mode 来查看 camera 上面选择的 noise profile 的效果，然后退出 Play mode。

### 添加一个 Cinemachine Camera Extension

当你需要一个特定或高级 behavior，可选帝添加一个 Extension 到 Cinemachine Camera 上。

- 在 Cinemachine Camera 组件 Inspector 上点击 Add Extension
- 在列表中选择一个 Extension。Unity会添加相应的 Extension 组件到 GameObject

可以添加多个 Extensions 到同一个 Cinemachine Camera GameObject 上。

## 设置 Timeline 和 Cinemachine Cameras

在 Cinemachine 环境中设置 Timeline，来编排 Cinemachine Cameras 来产生一个可预期的 shot sequence：

- 准备多个 Cinemachine Cameras 来支持不同的 shots
- 准备一个 Timeline，创建一个 Cinemachine Track，添加 Cinemachine Shot Clips
- 管理 camera cuts 和 blends

### 准备 Cinemachine Cameras

- 在 Hierarchy 中，根据你要得到的 shot，使用不同属性创建一些 Static 或 Procedural Cinemachine Cameras。一个 shot clip 就是一个 Cinemachine Camera 的一段 active 时间（在这段时间内这个 Cinemachine Camera 控制 Unity Camera）
- 命名 Cinemachine Cameras 以便于标识和管理它们

### 准备 Timeline

- 创建一个空 GameObject
- 打开 Timeline window，为这个 GameObject 创建要给 Timeline Asset

### 使用 Cinemachine Shot Clips 创建一个 Cinemachine Track

- 在 Hierarchy 中，拖拽一个带有 Cinemachine Brain 的 Unity Camera GameObject 到 Timeline Editor 中，然后选择 Create Cinemachine Track
  Unity 在 Timeline 中添加一个目标为 Unity Camera 的 Cinemachine Track。
- 在 Hierarchy 中，拖拽第一个 Cinemachine Camera GameObject 到 Track 上创建 shot clip。
  Unity 添加一个目标为 这个 Cinemachine Camera 的 Cinemachine Shot Clip 到 Cinemachine Track 上。
- 重复上面的过程添加其他的 Cinemachine Cameras 来得到更多的 Cinemachine Shot Clips，在 Cinemachine Track 上。
  可以重用同一个 Cinemachine Camera 多次到不同的 Cinemachine Shot Clips。
- 调整 Cinemachine Shot Clips 的 order 和 duration，来得到想要的 shot sequence。

### 创建 camera cuts

放置两个 Cinemachine Shot Clips 或者编辑它们的 boundaries，使得 clips 彼此 stick 在一起，没有 overlap。

### 创建 camera blends

要使 Cinemachine Cameras 在两个 shots 直接 blend 它们的属性：

- 移动两个 Cinemachine Shot Clips 或编辑它们的边界，使得 clips 重叠
  结果重叠的区域定义了 blend duration。
