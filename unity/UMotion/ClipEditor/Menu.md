Edit 菜单

| Menu Item | Description |
| -- | -- |
| Select All | 选择 Dopesheet 或 Curve View 中的所有 keys，关键帧 |
| Deselect All | Deselect Dopesheet 或 Curve View 中所有的 keys |
| Cut | 剪切所有选择的 keys 关键帧到粘贴板中 |
| Copy | ... |
| Paste | 添加之前复制的 keys 到 animation clip 的当前 frame 位置上，这会覆盖现有 keys |
| Insert | 插入之前赋值的 keys 到 animation clip 的当前 frame 位置上，这会向后移动后面的 keys |
| Reverse | 在时间轴上翻转所有选择的 keys，这样它们将反向播放 |
| Crop to Playback | 截断 animation clip 为当前选择的 playback 区域。这影响 clip 的所有 layers |
| FK to IK Conversion | 转换当前 opened clip 到 IK |
| Preferences | 打开偏好窗口 |
| | |

一切都是数据。一切 Editor 都是操作数据的可视化数据。Animation Editor 中的一个 key，比如 Dopesheet View 中的一个方块点，本质就是一个 time 加上一个属性的 value，即：

struct Key {
    float time;
    float value;
}

Animation Editor 就是编辑这种结构体数据的可视化工具。复制粘贴 Key 本质上就是在改变 time，而保持 value 而已。选择一个 key，使用 Handle 修改相应的属性（Position/Rotation）就是在编辑 value。添加一个 key，就是在当前 time 以当前属性值创建一个 key。

动画数据中的 IK channel 也是同理。IK 本身也是数据，即 Effector 在时间线上的 position/rotation 数据。既然是数据，就可以被 animation clip 活动。IK 数据本身就是在动画片段之后，IK 解析过程之前设置到 IKPosition 或 IKRotation 上。因此动画片段中的 IK channel 就是在普通动画属性数据输出之后，最后输出 IK 数据到 IKPosition/IKRotation 中，和 FinalIK 在 LateUpdate 中的通过脚本手动设置 IKPosition/IKRotation 没有区别。另外，FinalIK 在每一个 LateUpdate 中设置常量的 IK 数据，动画片段中的 IK channel 在每一帧中设置 IK 为动画数据，区别仅此而已。

Unity Timeline 就像是 Audio 或 Video 编辑器，一个 Timeline 由一组 track（轨道）组成，每个 track 可以添加很多多媒体以及 gameplay 资源，包括声音片段、动画片段、script 等等，Audio/Video 编辑器则只能添加声音片段或者视频片段，区别仅此而已。Timeline 最终创建影视类过场动画和 gameplay 无缝衔接过渡效果。
