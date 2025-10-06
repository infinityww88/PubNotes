使用Cinemachine Volume Settings扩展，可将HDRP/URP的VolumeSettings配置文件附加到CinemachineCamera上。

该扩展持有一个VolumeSettings配置文件资源，当CinemachineCamera被激活时，该配置将生效。若摄像机正与其他CinemachineCamera进行混合过渡，则混合权重也会同步作用于Volume Settings的各项视觉效果。

# 属性

- Profile：当 CMC 变成 live 时，应用的 Volume Settings profile
- Focus Tracking：若配置文件中启用了相应 override 选项，系统将自动把 base focus distance 设置为从选定目标到摄像机的距离。随后可通过 Focus Offset 字段对该距离进行修正。
  - None：没有 focus tracking
  - Look At Target：Focus offset 是相对 LookAt target 的
  - Follow Target：Focus offset 是相对 Follow target 的
  - Custom Target：Focus offset 是相对 Custom Target 的
  - Camera：Focus 是相对 Camera 的
- Focus Target：当 Focus Tracking 设置为 Custom Target，使用的 target。
- Focus Offset：当 Focus Tracking 不是 None 时，使用的 Offset。此设置将对焦最清晰的点从焦点目标所在位置进行偏移。
- Weight：此数值代表摄像机完全融入场景时所创建动态 volume 的混合权重。该权重值将随 camera 的混合过程在0与此设定值之间进行平滑过渡。

