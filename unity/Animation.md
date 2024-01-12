# Animation

Unity 的 AnimationClip 没有绑定在某个 GameObject 上，而是可以用于任何 GameObject。

AnimationClip 通过 Hierarchy 和名字来记录一个动画属性属于哪个 GameObject。在运行时，AnimationClip 可以绑定在任何 GameObject 上，当它播放的时候，在它绑定的 Hierarchy 中按照记录的层级和名字取找相应的 GameObject，找到的话，就在其上面活动属性。否则就是 GameObject Missing，忽略这个属性的动画。

例如有一个 GameObject 名为 obj，下面有一个 child 名为 obj0。在 obj 上录制一个动画片段，修改 obj0 的属性（例如 Transform），则 clip 记录对它绑定的 GameObject 下面第一层级的名为 obj0 的 GameObject 进行属性修改。

如果有另一个 GameObject 名为 obj1，将 clip 应用到这个 GameObject：

- 如果 obj1 下面有且仅有一个名为 obj0 的 child，则按照 clip 记录的关键帧对它进行属性修改，动画可以正常播放
- 如果 obj1 下面没有名为 obj0 的 child，则警告 GameObject missing，然后忽略这个属性 track
- 如果 obj1 下面有多个名为 obj0 的 child，则警告 Duplicate GameObject anem，然后只对第一个名为 obj0 的 GameObject 应用属性 track

总之，Animation Clip 就是按照层级加对象名字来记录和应用属性 track 的。

