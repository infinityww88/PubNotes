# TimeLine

Activation Track 可以控制 GameObject 的 Active 和 Inactive，在特定事件 SetActive 一个 GameObject，进而触发其上面携带的脚本。

TimeLine 还可以通过 Singal Track 发射信号来和外界通信。

Activation Track 的 Post-playback state 控制 Track 播放完毕后 GameObject 应该是什么状态：

- Active
- Inactive
- Leave as is
- Revert

需要点击 Timeline 窗口中左边的 Trace 查看它的 Inspector，而不是右边的轨道细节。

每个 Track 都绑定一个 GameObject。

AudioTrack 使用绑定的 GameObject 上的 AudioSource，但不需要上面有 Audio Clip，而是使用它来轨道详情中不同时间线上的 audio clip。可以将 Project 中的 audio clip asset 拖放到轨道上来定义什么时间播放哪个音频。

可以在 Timeline 中直接为 GameObject 录制 animation。注意这个 animation 直接定义在 TimeLine 中，而不是外部的 animation 文件。因此需要再 Timeline 查看，但是可以右键打开 Edit In Animation Window 在动画窗口中编辑它。

使用外部 animation clip 是，注意它是否是 loop 的，因为在 timeline 中触发的 loop 动画在 timeline 播放完毕时会继续播放。确保这是你想要的效果，否则将 clip 的 loop 关闭。

Timeline 在脚本中的组件是 Playable Director，它引用一个 Timeline asset。Wrap Mode 控制 Timeline 播放完毕之后的行为：

- Loop：Timeline 播放完毕后，循环播放
- Hold：Timeline 播放完毕后，保持在最后一帧的状态
- None：Timeline 播放完毕后，Revert 到之前的状态

注意如果 Activation Track 定义了额 post-playback state，需要将 PlayDirector 的 Wrap Mode 设置为 None，不能是 Hold。因为 Hold 定义的是 Timeline 仍然在播放，只是保持在最后一帧，而正在播放的 Timeline 不会执行 post-playback。

可以在 Animation 窗口中编辑属性的 Curve，这可以更细致精确的调整动画曲线，使其平滑。

