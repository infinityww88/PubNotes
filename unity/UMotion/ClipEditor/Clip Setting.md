- Name：clip 的名字
- Framerate：当前帧率（默认 60）。修改帧率不改变 keys/animation events。为了维持动画片段相同的 speed/duration，使用 box tool（例如 dopesheet 中 selected keys/events 旁边蓝色的 bars）来相应地缩放所有 keys/events（例如，将帧率从 30fps 改为 60fps，意味着 keys 需要以因子 2 来缩放）。缩放指的是缩放 key 的 time
- Clip Length：以 frames 和 seconds 显示全部 clip length
- Loop Clip：开启时，导出 clip 的 loop flag 将被设置。更进一步，auto/clamped auto tangent mode 被改变为第一个和最后一个 key 的 tangent 无缝 loop
- Generate Root Motion Curves：开启时，UMotion 将会在 Unity 中为 humanoid *.anim 文件直接生成 root motion curves（指定 “root” bone 的移动和旋转的世界空间曲线，通常是 hip bone）

- Root Transform Rotation - Bake Into Pose

  Bakes root motion rotation 到 animation 中。这意味着当动画 loops 时，character 的 rotation 将会重置到 starting rotation

- Root Transform Position (Y) - Bake Into Pose

  Bakes root motion 的 y position 到 animation 中。这意味着当动画 loops 时，character 的 y position 将会重置到 starting value

- Root Transform Position (XZ) - Bake Into Pose

  Bakes root motion 的 x/z position 到 animation 中。这意味着当动画 loops 时，character 的 x/z position 将会重置到 starting value

