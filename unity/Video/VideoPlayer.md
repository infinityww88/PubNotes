# Video Player 组件

使用 Video Player 组件来挂载 video 文件到 GameObjects，运行时在 GameObject 的 Texture 上播放它们。

默认的，Video Player 组件的 Material Property 被设置为 GameObject 的 main texture，这意味着当 Video Player 组件挂载到一个具有 Renderer 的 GameObject 时，它自动将它自己赋给那个 Renderer 上的 Texture（因为这是 GameObject 的 main Texture）。

还可以为 video 指定特定的播放目标，包括：

- 一个 Camera plane
- 一个 Render Texture
- 一个 Material Texture 参数
- 一个组件的任何 Texture 字段

## Video Player 组件参考

- Source

  选择视频的 source 类型（视频片段或网络流，VideoClip/URL）

- Video Clip：要播放的 clip 文件
- URL：要播放的视频 URL 地址

- UpdateMode

  设置 Video Player 组件用来更新它的 timing 的 clock source。

  - DSP Time：使用和处理 audio 相同的 clock source
  - Game Time：使用和 game clock 相同的 clock source。这个 clock source 被 time scaling 和 capture frame rate 设置影响
  - Unscaled Game Time：类似 GameTime，但是不被 time scaling 或 capture frame rate 影响

- Play On Awake

  在 Scene 加载时自动播放。也可以关闭它，在运行时调用 Play() 来播放视频。

- WaitForFirstFrame

  在游戏开始前等待原视频第一帧可用。关闭它将使得 video time 和游戏同步，但是前几帧可能会被丢弃。

- Loop

- Skip On Drop

  开启这个选项时，Video Player 组件检测 playback 位置和 game clock 之间直接的漂移 drift，Vido Player 向前跳过 drift。关闭这个选项时，Video Player 不会修复漂移。

- Render Mode

  - Camera Far Plane 在 Camera 的 far plane 渲染 video。3D 世界将在 video 之前
  - Camera Near Plane 在 Camera 的 near plane 渲染 video，3D 世界被挡住 video 之后
  - RenderTexture 渲染视频到一个 Render Texture 中
  - Material Override 通过 Renderer Material 渲染视频到一个 GameObject 中的一个选择的 Texture 属性中
  - API Only 渲染 video 到 VideoPlayer.texture 脚本 API 属性中。你必须使用脚本手工将 Texture 赋值到想要目标中。

- Camera 定义接收 video 的 Camera
- Alpha 设置要添加到 source video 的全局透明度等级。这允许 plane 后面的 elements 可以被看见。

- 3D Layout 3D VR 相关设置
- Target Texture

  渲染视频内容到目标 Render Texture target。

- Aspect Ratio

  设置填充 Camera Near Plane, Camera Far Plane, 或 Render Texture 的 Image 的 aspect ratio。

  - No Scaling：不使用缩放，video 居中在目标 rectangle。
  - Fit Vertically：缩放 source 动态垂直 fit 目标 rectangle（在垂直方向填满 rectangle，水平方向，超出的部分切除，不足的部分留白），保持原视频的 aspect ratio。
  - Fit Horizontally
  - Fit Inside：使水平或垂直方向中最大的那个适配 rectangle，另个方向留白
  - Fit Outside：使水平或垂直方向中最小的那个适配 rectangle，另一个方向切除
  - Stretch：缩放视频在水平和垂直方向视频 rectangle，不保持 aspect ratio

- Renderer

  选择 Video Player 组件渲染的目标 Renderer。如果设置为 None，则渲染到 Video Player 组件所在的 GameObject 的 Renderer。

- Auto-Select

  开启这个选项，Video Player 组件自动选择 Renderer 的 main texture。关闭这个选项，可以手动选择 Material 选项。

- Audio Output Mode

  定义 source 的 audio tracks 如何输出：

  - None：不播放 audio
  - Audio Source：Audio samples 被发送到选择的 audio sources
  - Direct：Audio samples 被直接发送到 audio 硬件输出，跳过 Unity 的 audio 处理
  - API only（实验性）：Audio samples 被发生到关联的 AudioSampleProvider

- Controlled Tracks

  video 中的 audio tracks 数量。只在 Source 为 URL 时显示。当 Source 时 Video Clip 时，tracks 的 数量被 video file 决定

- Track [Number]

  支持多个 audio track 时，可以选择哪些 track 用于播放，例如 Track 0，Track 1。它们必须在 playback 之前被设置。如果 source 时 URL，这些信息只会在 playback 时可用。

  - Audio Source：播放这个 track 的 audio source。目标 audio source 还可以播放其他 AudioClip。Audio source 的 playback controls（Play On Awake 和 Play API）不应用到 video source 的 audio track。
  - Mute：静音这个 audio track。
  - Volume

  
