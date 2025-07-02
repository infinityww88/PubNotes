Feel框架内置了多种类型的反馈效果组件，这些组件可大致分为以下几类：

- 作用于游戏对象(GameObject)的反馈
- 与摄像机(或其局部)交互的反馈
- 调用第三方系统的反馈
- 无法归入特定类别的通用反馈

特别说明：

- 部分反馈效果可独立运行
- 部分反馈需要依赖场景中的特定对象（通常是名为"Shaker"的组件，该组件负责实现震动效果）

附带的分类列表已详细说明各类反馈的特性。如需深入了解某个反馈的具体实现，可以直接查阅其源代码——所有类文件都包含完整的注释说明。

本页面仅提供反馈效果的目录清单。若需要获取每个反馈效果的详细技术文档，请参考API参考手册。

## Animation

- Animation Parameter：在 animator 上播放任意动画。绑定一个 animator 到 feedbacks 的 inspector，它会让你更新 trigger and/or bool 动画参数
- Animation Play State：通过名字播放一个 state，在 fixed 或 normalized time
- Animator Speed：在运行时调整 target animator 的 speed
- Animator Cross Fade：cross fade Animator 到一个指定 state，在 normal 或 normalized time 上
- Animation Sprite Sheet：使用一组 sprites 动画 target Sprite Renderers and/or UI Images，而无需 Animator 组件 

## Audio

- AudioSource : 按需播放、暂停、恢复、停止现有的 audiosource。还可以以随机 pitch 和 volume play/pause/stop/resume audiosource 和可选的 audio mixer group。
- Sound : 触发一个 sound 的另一种方式。你可以指定一个音频剪辑，然后决定是按需实例化播放、缓存、创建一个可随时使用的声音对象池，还是触发声音事件。此反馈还允许你在编辑器中预览声音。请注意，默认设置为事件模式，这需要在场景中存在MMSoundManager（或你希望用来捕获此类事件的任何其他类）来捕获声音事件。如果你不打算使用声音管理器，缓存模式可能是你想要选择的模式
- AudioSource Pitch : 随时间调整一个 AudioSource 的 pitch。你需要在 target audioSources 上具有要给 MMAudioSourcePitchShaker
- AudioSource Stereo Pan : 随时间修改 AudioSource 的立体声盘旋值。需要在 target audiosources 上挂载一个 MMAudioSourceStereoPanShaker
- AudioSource Volume : 随时间调整 audiosource 的音量。需要在 target audiosources 上挂着一个 MMAudioSourceVolumeShaker
- Distortion Filter : 随时间调整一个 distorttion filter 的 distortion level。需要在 MMAudioSourceDistortShaker
- Echo Filter : 随时间调整 echo。需要在 target audiosource 挂载 MMAudioSourceEchoShaker
- High Pass Filter : 随时间调整 high pass 的 cutoff。需要在 target audiosource 上挂载 MMAudioSourceHighPassShaker
- Low Pass Filter
- Reverb Filter : tween reverb levels over time. You will need a MMAudioSourceReverbShaker on your target audiosource(s)
- AudioMixer Snapshot Transition : lets you transition to a target snapshot over a specified duration
- MMPlaylist : lets you remote control (play/pause/stop/previous/next/etc) a MMPlaylist from a feedback.
- MMSoundManager All Sounds Control : control all sounds playing on a MMSoundManager
- MMSoundManager Save and Load : save and load MMSoundManager settings (track volume, etc)
- MMSoundManager Sound : lets you play a sound on the MMSoundManager
- MMSoundManager Sound Control : lets you play/pause/resume/setVolume/more on a sound playing on the MMSoundManager
- MMSoundManager Sound Fade : lets you fade sounds in/out on the MMSoundManager
- MMSoundManager Track Control : lets you control entire tracks (music, UI, sfx, master) on a MMSoundManager
- MMSoundManager Track Fade : lets you fade the tracks of the MMSoundManager

## Camera

- Camera Shake : 该反馈效果会随时间推移抖动摄像机，你可设置持续时间（秒）、振幅和频率参数。如需更高级的抖动效果，建议查看Cinemachine Impulse反馈。此功能要求摄像机上必须挂载MMCameraShaker组件。若你使用Cinemachine并希望优先采用本反馈而非Cinemachine Impulse，则需在虚拟摄像机上配置MMCinemachineCameraShaker组件，并设置噪声参数。添加噪声的方法：选中虚拟摄像机，在其噪声面板中选择"Basic Multichannel Perlin"噪声类型，然后指定噪声配置文件。当在常规摄像机或自定义摄像机控制器上使用MMCameraShaker时，建议采用"摄像机装配体"结构——这是一种能确保稳定运行的摄像机层级架构。你可以在MMF_PlayerDemo的"Camera & Lights"节点下找到示例：顶层是摄像机控制器对象，其下嵌套包含MMCameraShaker的中间层对象，最底层才是摄像机对象。当然，根据需要可以增加更多嵌套层级。
- Camera Zoom : 该反馈在播放时让你能够放大或缩小（视野），可以指定持续时间，也可以持续生效直至另行通知。如果你使用的是常规摄像机，需要在上面添加一个MMCameraZoom组件。如果你使用的是Cinemachine虚拟摄像机，则需要在上面添加一个MMCinemachineZoom组件。此反馈还允许你使用相对值，即在反馈播放时在当前缩放值的基础上进行增加。
- Flash : 在屏幕上闪烁显示一张图片，或者短暂显示一种颜色。要让此反馈生效，你需要在场景中放置一个或多个带有MMFlash组件的元素。此外，你还可以指定颜色、透明度和闪烁ID，从而完全控制闪烁效果。
- Fade : 该反馈效果可使图像淡入或淡出，适用于过渡效果。此反馈要求场景中有一个带有MMFader组件的对象。通过反馈检查器，你可以选择过渡曲线、目标透明度和位置。还可用于控制MMFaderRounds。
- Field of View : 随时间控制相机的视场角。需要在你的相机上使用MMCameraFieldOfViewShaker组件，或者在使用Cinemachine时，在虚拟相机上使用MMCinemachineFieldOfViewShaker组件。
- Clipping Planes : 让你能够在一段时间内对相机的近裁剪平面和远裁剪平面距离进行插值处理。如果你使用的是普通相机，需要在相机上添加MMCameraClippingPlanesShaker组件；如果你使用的是Cinemachine虚拟相机，则需要在虚拟相机上添加MMCinemachineClippingPlanesShaker组件。
- Orthographic Size : 仅适用于正交/2D相机，可让你在一定时间内对相机的大小（视野范围）进行插值处理，实现放大或缩小效果。如果使用普通相机，需要在相机上添加MMCameraOrthographicSizeShaker组件；如果使用Cinemachine虚拟相机，则需要在虚拟相机上添加MMCinemachineOrthographicSizeShaker组件。
- Cinemachine Transition : 让你能够过渡到另一个虚拟相机，使用你选择的混合方式，并自动管理其他相机的优先级。要让此功能正常工作，你需要在每个虚拟相机上添加一个MMCinemachinePriorityListener组件。如果你想获得更多控制权，还可以在Cinemachine大脑（Cinemachine brain）上添加一个MMCinemachinePriorityBrainListener组件。这样你就可以直接从反馈中指定要使用的过渡方式，从而覆盖默认的过渡方式。
- Cinemachine Impulse : 该反馈可触发Cinemachine震动脉冲来晃动虚拟相机。要使其正常工作，你的虚拟相机需要添加脉冲监听器组件。添加方法：选中虚拟相机，在检视面板底部找到"添加扩展"下拉菜单，从中选择"Cinemachine Impulse Listener"。在反馈的检视面板中，你可以调节各种参数——入门设置建议：先选择一个基础信号（点击"原始信号"字段旁的小齿轮图标，从预设中选择"6D震动"），然后将检视面板底部的速度值设为1,1,1作为起点，之后再按需调整。这个工具功能非常强大，可控制冲击强度、持续效果、衰减过程、缩放比例、影响半径等多项参数。更多关于震动脉冲的详情请参阅Cinemachine官方文档。需要注意的是，震动脉冲是基于距离的，务必确保虚拟相机处于发射器（此处指MMF_Player的Transform）的有效范围内，否则不会产生任何效果。
- Cinemachine Impulse Source : 让你能够在目标Cinemachine震动脉冲源上生成震动脉冲。其设置方式与Cinemachine震动脉冲反馈类似，不同之处在于，你需要一个Cinemachine震动脉冲源组件，并且你的虚拟相机上仍然需要一个Cinemachine震动脉冲监听器组件。
- Cinemachine Impulse Clear : 取消正在播放的任何 Cinemachine Impulse

## Events

- Unity Events：关联任何类型的 Unity event 到 feedback，这样可以在 play，stop，初始化，或 reset 时触发它们
- MMGameEvent：当播放时，触发一个指定名字的 MMGameEvent

## GameObject

- Destroy : lets you destroy, destroy immediate or disable a specific game object
- Enable Behaviour : enables or disables a monobehaviour when the feedback plays, inits, stops or resets
- Float Controller : 可能是所有 feedbacks 中最强大的，它可以让你控制任何 monobehaviour 的一个 float。需要在 target gameobject 挂载一个 FloatController
- Instantiate Object : 播放 feedback 会在指定位置生成 objects
- Rigidbody : 添加 force 或 torque 到 rigidbody
- Rigidbody2D : 添加 force 或 torque 到 rigidbody2d
- Collider : enable/disable/toggle a target collider, or change its trigger status
- Collider2D : enable/disable/toggle a target collider 2D, or change its trigger status
- Property : 让你 target 和 control 任何 property 或 field（floats，vectors，ints，strings，colors 等等），可以在任何 object（包括 ScriptableObjects），并且随时间控制它。拖拽一个 GameObject 或 ScriptableObject 到它的 TargetObject slot，然后选择一个组件，最后选择要控制的 property。在那里可以定义 remap 选项，调整 curve
- Set Active : sets an object active or inactive
- MMRadioSignal : 该反馈机制可让你控制一个MMRadio信号，进而将该信号广播至接收端，从而实现对任意对象上任意组件的目标值进行操控。若想深入了解MMRadio系统，不妨查阅更多相关资料——它可能会非常实用！
- MMRadio Broadcast : 类似 MMRadioSignal，但是直接广播信号到任何接收端，而不是通过一个 emmiter

## Feedbacks

- Feedbacks Player : 让你触发指定 range 内的 MMF_Players，或者可以指定一个 target MMF_Player，这种情况下这个 feedback 会匹配它 target 的 total duration
- MMF Player Chain : 让你将多个 MMF Players sequence 到一起，然后一个接一个播放它们，并可选指定开始或之后的延迟
- Player Control : 在一个或多个 target MMF Players 上触发方法

## HDRP Volume

- Bloom HDRP : control bloom intensity over time
- Chromatic Aberration HDRP : control the force of a chromatic aberration over time
- Channel Mixer HDRP : control red, green and blue channels independently over time
- Color Adjustments HDRP : lets you play with many color adjustments options : post exposure, saturation, hue shift, contrast…
- Depth of Field HDRP : control HDRP Depth of Field focus distance or near/far ranges over time
- Film Grain HDRP : lets you control the grain intensity over time
- Lens Distortion HDRP : lens distortion on demand
- Motion Blur HDRP : motion blur level over time
- Panini Projection HDRP : tweak a panini projection’s distance and crop to fit over time
- Vignette HDRP : control vignette parameters over time
- White Balance HDRP : control white balance parameters over time

## Loop

- Looper : 将一个 MMF_Player 的 sequence 的 head 移动回到 list 中上面另一个 feedback。然后你可以让这个 sequence repeat 任意次数，或无限循环
- Looper Start : 可以用作一个 pause，也可以用作 loops 的 start

## Nice Vibrations

- Nice Vibrations Preset : 播放一个 preset 震动反馈，受限但是超级简单的预定义震动模式
- Nice Vibrations Emphasis : play an Emphasis haptics, short haptic bursts whose amplitude and frequency can be controlled in real time, also called Transients in CoreHaptics/iOS.
- Nice Vibrations Clip : use this feedback to play a .haptic clip, optionally randomizing its level and frequency.
- Nice Vibrations Continuous : lets you play a continuous haptic of the specified amplitude and frequency over a certain duration. This feedback will also let you randomize these, and modulate them over time.
- Nice Vibrations Control : interact with haptics at a global level, stopping them all, enabling or disabling them, adjusting their global level or initializing/release the haptic engine

## Particles

- Particles Instantiation : 实例化 particles 并播放它们。可以按需实例化它们，或者缓存它们，还可以指定一个生成它们的位置
- Particles Play : 控制（play, pause, stop, resume）一个现有的 particle system。这个 feedback 还让你移动粒子系统的位置到 feedback 的位置
- Visual Effect : gives you control over a target visual effect and lets you play/pause/stop/etc.
- Visual Effect Set Property : lets you set the value of a Property ID of any type on a target Visual Effect.

## Pause

- Pause : 在 feedbacks sequence 中遇到这个 feedback 时，会导致暂停，阻止 sequence 下面任何 feedback 运行，直到 pause 完成
- Holding Pause : holds 直到 sequence 中所有之前的 feedbacks，以及这个 feedback 的暂停已经被执行

## Post Processing

所有这些需要在一个 PostProcessing Volume 上有它们各自的 shaker 来工作。Shaker（震动器、调和器）用于连接 feedback 和 target object/component，feedback 用来产生数值，shaker 接收信号并用这个 value 操作 target。

- Bloom : control bloom intensity and threshold over time. You’ll need a MMBloomShaker on your post processing volume.
- Chromatic Aberration : control the force of a chromatic aberration over time. You’ll need a MMChromaticAberrationShaker on your post processing volume.
- Color Grading : lets you play with many color grading options : post exposure, saturation, hue shift, contrast… You’ll need a MMColorGradingShaker on your post processing volume.
- Depth of Field : lets you control depth of field focus distance, aperture and focal length over time. You’ll need a MMDepthOfFieldShaker on your post processing volume.
- Global PP Volume Auto Blend : tween a PostProcessing volume’s weight.
- Lens Distortion : lens distortion on demand. You’ll need a MMLensDistortionShaker on your post processing volume.
- PP Moving Filter : move a post processing filter in or out of the camera.
- Vignette : control vignette parameters over time. You’ll need a MMVignetteShaker on your post processing volume

## Renderer

- Flicker : 让你快速改变 material 的颜色。默认会控制 target renderer 的 shader Color value，但是 feedback 还让你可以指定自己的颜色。还带有一个 flicker duration，octave，和 color 控制。你还可以提供一个额外 target renderers 的列表，此时所有 target renderers 都会立即 flicker

- Fog : 让你动画 scene fog 的 density，color，end 和 start 距离

- Material : 每次播放时改变 target renderer 的 material 为一个 materials 数组中的一个。你可以按顺序交互它们，或者随机地

- Line Renderer : 让你随时间更新要给 line renderer 的 width 和 color

- Material Set Property : 设置 target renderer material 上指定的 property 的 value

- MMBlink : controls an MMBlink, letting you do advanced blinking behaviours, either by enabling/disabling a gameobject, changing its alpha, emission intensity, or a value of your choice on a shader, with or without interpolation, and will let you define repeat patterns and phases.

- Shader Controller : 类似 Float Controller，让你控制任何 shader 绝大多数 settings。这需要在 target 上有 ShaderController 组件（或者 targets，可以同时控制多个 target renderers）

- Shader Global : 运行时控制 global shader 属性

- Sprite : 改变 target sprite renderer 上的 sprite
- SpriteRenderer : 控制 SpriteRenderer 的颜色和 X、Y flip
- Skybox : 指定一个新 material（随机或不随机）来改变 scene 的 skybox
- TextureOffset : 随时间控制 target renderer 的 material 的 texture 的 offset
- TextureScale : 随时间控制 target renderer 的 material 的 texture 的 scale
- Trail Renderer : 随时间控制 trail renderer 的 length，width，color

## Scene

- LoadScene : lets you load a destination scene using various methods, either native or using MMTools’ loading screens
- UnloadScene : lets you unload a scene, specified either via its build index or name

## Springs

- Float Spring : control any float spring (vignette intensity, light, timescale, and so many more), either directly or via event.
- Vector2 Spring : control any Vector2 spring (texture offset, etc)
- Vector3 Spring : control any Vector3 spring (position, scale, etc)
- Vector4 Spring : control any Vector4 spring
- Color Spring : control any Color spring (light color, sprite color, image, etc)

## TextMesh Pro

- TextMeshPro Font Size : lets you modify the size of a TMP’s font over time
- TextMeshPro Text : lets you modify the text of a target TMP text component
- TextMeshPro Character Spacing : change horizontal spacing between characters in your TMP text over time
- TextMeshPro Count To : lets you update a target TMP text with a float or rounded value going from A to B over time
- TextMeshPro Count To Long : same as CountTo, but using long instead of floats (useful to count up to really big numbers)
- TextMeshPro Word Spacing : change horizontal spacing between words in your TMP text over time
- TextMeshPro Line Spacing : change vertical spacing between lines in your TMP text over time
- TextMeshPro Paragraph Spacing : change vertical spacing between paragraphs in your TMP text over time
- TextMeshPro Color : change text color over time
- TextMeshPro Alpha : change text alpha over time
- TextMeshPro Outline Width : change a text’s outline width over time
- TextMeshPro Outline Color : change a text’s outline color over time
- TextMeshPro Dilate : will tweak the position of the text contour in the distance field
- TextMeshPro Softness : will let you animate the softness of the text contour
- TextMeshPro TextReveal : lets you reveal a target text character by character, word by word, or line by line, over time

## Time

所有与时间相关的反馈功能均通过 ​MMTimeManager​ API 实现。若你决定使用其中任意功能，并计划在脚本的其他部分修改时间缩放比例（timescale），​强烈建议通过该 API 统一管理所有时间缩放操作。

​时间管理器（Time Manager）​能够协调多个时间缩放层级——例如，它可以在已有减速效果的基础上，短暂地进一步降低时间流速，之后再恢复原有效果。但如果你绕过该系统，直接调用底层的时间缩放 API，​时间管理器将无法感知你的修改，最终可能导致逻辑冲突或异常行为。

若你因特殊需求不愿使用 ​MMTimeManager，则需自行设计专属反馈逻辑，直接对接你自定义的时间缩放 API。

- Freeze Frame：短暂 duration 冻结 timescale。需要场景中存在要给 TimeManager
- Time Modifier：完整控制 time，减慢、加速，以及可选定制插值。还可以触发 Change 或 Reset time modifications，让你改变 timescale 到新值，或者重置它到之前的值。需要场景中存在 TimeManager

## Transform

- Position ：该功能允许你通过不同模式随时间调整变换（transform）的位置：
  - **A到B模式（A to B）**：能将对象从初始位置移动到目标位置，且可指定移动速度、持续时间和加速度
  - **沿曲线模式（Along Curve）**：可使对象沿定义好的曲线移动，曲线上的值会被重新映射，且可在任意或全部3个轴向上进行移动
  - **到达目的地模式（To Destination）**：会将对象移动到指定的目标位置
- Rotation：随时间改变 transform 的 rotation，伴随各种选项。类似 position feedback，你可以在 absolute mode 旋转一个 object，additive mode（添加到 play 开始的 rotation），或者到定义的目的
- Scale：随时间动画 transform 的 scale。具有和 Position 和 Rotation feedbacks 相似的选项
- Position Spring : 使用弹簧 spring move 或 bump 一个 target 的 position
- Rotation Spring : 使用弹簧 spring move 或 bump 一个 target 的 rotation
- Scale Spring : 使用弹簧 spring move 或 bump 一个 target 的 rotation
- Squash & Stretch Spring : move or bump a target’s scale by squashing & stretching it using a spring.
- Wiggle : lets you play with rotation, scale and position over time. You’ll need an MMWiggle component on your target object for this to work. Wiggle(扭动、摆动、波浪形线)
- Rotate Position Around : lets you rotate a target object around another center object, with full axis control.
- DestinationTransform : 动画一个 transform 的属性（position，rotation，scale）来匹配 dest transform 的属性
- SquashAndStretch : modify the scale of an object on an axis while the other two axis (or only one) get automatically modified to conserve mass. This requires a normalized scale (see note below).
- Position Shake : activate 一个 target position shaker。Shaker 会在指定 duration 和特定 range 内沿着特定方向移动 target object 的 position。你可以随时间控制 shake 的随机性和衰减。这需要一个或多个 MMPositionShaker 在 target objects
- Rotation Shake
- Scale Shake
- Look At : 旋转 transform 使它面向另一个 target transform（或一个 direction，或特定世界坐标），可选可以锁定 axis，支持 event/shaker。需要在 targets 上有 MMLookAtShaker

关于缩放的重要说明：在处理缩放（挤压与拉伸、缩放抖动、缩放弹簧等）时，要确保目标变换（Transform）的归一化缩放值为1,1,1 。这并不意味着不能在其他缩放值的变换上使用这些反馈，只是需要将它们置于容器对象之下。以下是一个层级示例：MyCharacter（你的预制体主对象，可能包含一些逻辑、CharacterController等，缩放值为1,1,1）

- MyModelContainer（模型的容器节点，scale 为 1, 1, 1）
  - MySquashAndStretchContainer（一个 empty object，scale [1, 1, 1]，用来挂载 feedback）
    - MyActualModel（实际的 Mesh Renderer，scale 可以是任意值）

这样的解耦，可以应用与很多其他类似的情形。

## UI

- ImageRaycastTarget : this feedback will let you control the RaycastTarget parameter of a target image, turning it on or off on play
- CanvasGroup : lets you control a CanvasGroup’s alpha over time
- CanvasGroupBlocksRaycasts : lets you turn the BlocksRaycast parameter of a target CanvasGroup on or off on play
- Graphic : lets you change the color of a target Graphic over time
- Graphic CrossFade : lets you trigger cross fades on a target Graphic
- Image : lets you play with the color of an Image over time
- Image Alpha : lets you play with the alpha of an Image over time
- Image Fill : lets you play with the fill of an Image over time
- Image Material : lets you change the material of the target Image
- Image Sprite : lets you change the sprite of the target Image
- Image Texture Offset : animate an Image’s texture offset over time
- Image Texture Scale : animate an Image’s texture scale over time
- Raycast Target : lets you control the RaycastTarget parameter of a target image, turning it on or off on play
- RectTransformAnchor : lets you control a RectTransform’s min and max anchor positions over time
- RectTransformPivot : lets you control the position of a RectTransform’s pivot point over time
- RectTransformOffset : lets you control the offset of the lower left corner of the rectangle relative to the lower left anchor, and the offset of the upper right corner of the rectangle relative to the upper right anchor
- RectTransformSizeDelta : lets you animate the size of this RectTransform relative to the distances between the anchors, over time
- Floating Text : lets you easily spawn floaty text (usually damage text, but not limited to that)
- Text : lets you control the contents of a target Text
- TextColor : lets you change the color of a target Text over time
- TextFontSize : lets you alter the font size of a target text over time
- VideoPlayer Feedback which will let you control video players in all sorts of ways (Play, Pause, Toggle, Stop, Prepare, StepForward, StepBackward, SetPlaybackSpeed, SetDirectAudioVolume, SetDirectAudioMute, GoToFrame, ToggleLoop)

## UI Toolkit

对 UI Toolkit 的支持有一些需要注意的地方：

- 因为所有 Unity editor 版本对 UI Toolkit 的支持并不相同，所有 feedbacks，和它们的相关的 demo，是在 asset 中的一个 Unity Package，你需要先 extract 它。在 project 面板内，搜索 FeelUIToolkitPackage unity package，双击它导入其内容
- 对所有 UI Toolkit feedbacks，需要在 TargetDocument 字段中指定 UIDocument，选择一个 QueryMode（Name 或 Class），然后定义一个 Query（在 UIDocument 中查找想要影响的元素的 query 表达式）。这会返回一个或多个 elements。如果返回多个元素，feedback 会影响全部
- 确保查看 FeelUIToolkitFeedbacksDemo scene，它展示了所有这些 feedbacks
- Background Color : interpolate background color over time
- Border Color : control border color over time
- Border Radius : change the radius of UI elements’ borders over time
- Border Width : change the width of elements’ borders over time
- Class : lets you modify the classes on target UI elements
- Font Size : change the font size of a target UI element
- Image Tint : change the tint of a target image
- Opacity : change the opacity of a visual element over time
- Rotate : rotate one or more target visual elements
- Scale : change the scale of one or more target visual elements
- Size : change the size of one or more target visual elements
- Stylesheet : attach a new stylesheet to your UI Document
- Text : replace a text with a new one
- TextColor : change a text’s color over time
- Transform Origin : lets you move the point of origin where rotation, scaling, and translation occur
- Translate : translate a UI element
- Visible : lets you toggle a visual element’s visibility on and off

## URP Volume

所有这些效果都需要在Volume上各自对应的URP Shaker（通用渲染管线震动器）才能正常运行。在使用URP时，请务必选择着色器和反馈效果的URP版本，否则将无法生效。

这些跟上面的 feedback，本质还是在操作 target 对象的属性（通常就是 float），具体的效果则依赖与 target 的类型。如果是 transform，就是 position/rotation/scale，如果是 Image，就是 color/alpha，如果是 PostProcessingVolume，就是各种全屏效果。Volume feedback 只是操作各种 Volume 的属性。这需要相应的 shaker 在 Volume 上辅助工作。

- Bloom URP : control bloom intensity over time
- Chromatic Aberration URP : control the force of a chromatic aberration over time
- Color Adjustments URP : lets you play with many color adjustments options : post exposure, saturation, hue shift, contrast…
- Depth of Field URP : lets you control depth of field parameters over time
- Global PP Volume Auto Blend URP : tween a PostProcessing volume’s weight
- Lens Distortion URP : lens distortion on demand
- Motion Blur URP : motion blur level over time
- Panini Projection URP : tweak a panini projection’s distance and crop to fit over time
- Vignette URP : control vignette parameters over time
- White Balance URP : control white balance parameters over time

## Various

- Light：随时间控制 light 的强度和颜色
- Light 2D：随时间控制 URP 2D light 的强度和颜色

## Debug

- DebugBreak：feedback 播放时会导致一个 Debug.Break()
- DebugComment：让你在 inspector 中存储一个 text，用于在以特定方式设置 feedback 时留下一条信息。可选地可以输出在 console
- DebugLog：feedback 播放时会在 console 中输出 debug messages，通过各种方法（MMDebug, Warning， Error，Log 等等）

## Want more?

支持的对象属性还在增长。