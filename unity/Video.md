# Video Overview

Unity video 系统可以集成 video 到游戏中。Video 片段可以增加真实性，免去复杂的渲染，也可以帮助集成外部内容。

要使用 Unity video，导入 Video Clips，使用 Video Player 组件配置它们。

系统可以让你直接将 video 片段 feed 给任何具有 Texture 参数的组件。Unity 在运行时在那个 Texture 上播放 video。

Unity video 功能包括硬件加速，软件解码视频文件，透明背景支持，多音频轨道（立体声），以及网络视频流。

## Video Player 组件

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

  
## Video Clips

Video Clip 是一个导入的 video 文件，典型扩展名包括 .mp4 .mov .webm .wmv 。

如果 transcode 关闭，video 文件原样不变地使用，这意味着视频和目标平台的兼容性必须人工确认。但是关闭 transcode 可以节省时间已经质量下降。


## Video sources

Video Play 组件可以播放从各种 sources(video clips，URLs，AssetBundles，以及 Streaming Asset 目录）的视频内容。

可以从 AssetBundles 中读取 Video Clips。Video clips 被导入后，可以将它赋给 Video Player 组件的 Video Clip 字段。

放在 Unity StreamingAssets 目录的文件通过 Video Player 组件的 URL 选项使用，或者平台特定的 Application.streamingAssetPath 使用。

## Video transparency support

Unity 的 Video Clips 和 Video Player 组件支持 alpha，即透明度。

当 Video Player 组件在 Camera 近平面和远平面播放视频时，支持一个全局 alpha。但是，videos 可以有逐像素的 alpha 值。这意味着透明度在 video image 中可以是不同的。逐像素透明度控制是通过图像、视频编辑软件例如 After Effects 完成的，而不是在 Unity Editor 中。

Unity 支持两种具有 per-pixel alpha 的 sources 类型：Apple ProRes 4444 和 Webm with VP8。

## 理解 video files

视频文件本质是一个容器。这是因为它不仅包含 video 本身，还包含额外的 audio，subtitles，以及更多 video footage 的 tracks。容器中，每种类型可以有多个 track，例如：

- 多 POV（points of view）
- 立体声音频
- 不同语言的 subtitles
- 不同语言的 dialogue

为了节省带宽和 storage，每个 track 内容使用一个 codec 进行编码，并按要求进行压缩和解压缩。

一个常用的 video codec（视频编码器）是 H.264，常用的音频编码器是 AAC。

文件扩展名 .mp4 .mov .webm .avi 指示视频文件是如何组织容器中内容的。

## 硬件和软件解码

大多数现代设备都有专门硬件用于解码视频。硬件解码可以更节省能量。

硬件加速通过 native custom APIS 提供，根据平台不同而不同。Unity 视频架构通过提供一个通用的 UI 和 Scripting API 隐藏了这些不同以访问这些能力。

Unity 还支持软件解码。它使用 VP8 video codec 和 Vorbis audio codec。在硬件解码结果不理想时，可以使用软件解码。例如硬件解码具有不想要的分辨率、音频通道数量的限制，或者要支持 alpha channel 时。

