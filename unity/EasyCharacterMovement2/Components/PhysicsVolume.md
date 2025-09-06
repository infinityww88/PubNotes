# Description

PhysicsVolume 是一个辅助组件，用于定义诸如 water，air，oil 等区域的体积，或者修改 character behaviours。

当 Character 在 volume 的内部，它会根据定义的设置反应。

# Properties

- BoxCollider boxCollider：这个 collider 的 volume（trigger）。

- int priority：定义发生重叠时，哪个 PhyscisVolume 具有优先级（更高的值具有更高的优先级）。

- float friction：定义当 Character 使用 CharacterMovement 通过 volume 时，应用到 volume 的摩擦力 friction amount（阻尼）。

  更高的值，Character 会感到更难通过这个 volume。

- float maxFallSpeed

  当 Character 使用 CharacterMovement 在这个 Volume 中 falling 时，临时的最大下落速度。

- bool waterVolume

  确定 volume 是否包含流体，例如水。