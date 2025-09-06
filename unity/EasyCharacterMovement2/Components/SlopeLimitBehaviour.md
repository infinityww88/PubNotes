# Description

SlopeLimitBehaviour 组件允许我们整体定义一个 object 的 walk-able 行为，而不是 per-face 定义。开启时，它允许我们覆盖 CharacterMovement slopeLimit 属性，提供了极大的灵活性。

当想要限制（或允许）特定 objects 或 zones 到一个特定行为，无视它们的 slope limit 值，这尤其有用。例如，标记其他 character 为 non-walk-able，阻止一个 player character 落在它们上面。

CharacterMovement 的 slopeLimit 属性，以 Character 为基础，定义它在所有 surface 的 slope 行为。SlopeLimitBehaviour 挂载到 Ground Surface（Collider）上面，当 Character 移动到这个 Collider 上面时，用这个组件的属性覆盖 CharacterMovement 的 slopeLimit 属性。

要使用这个功能，添加 SlopeLimitBehaviour 组件到 Collider 的 GameObject 上。然后在 CharacterMovement 组件中，确保设置 slopeLimitOverride 属性为 true。

# Enums

挂载的 Collider 的 slope 行为。

enum SlopeBehaviour

- Default

- Walkable

  设置 collider 为 walkable。

- NotWalkable,

  设置 collider 为 non-walkable。

- Override

  让你为 collider 指定一个自定义的 slope limit。

# Properties

- SlopeBehaviour walkableSlopeBehaviour：当前 behaviour

- float slopeLimit：slope limit 角度（度）。只用于 SlopeBehaviour.Override。

- float slopeLimitCos

  slope angle 的 cosine（余弦值，弧度）

  用于快速角度测试（例如 dotProduct > slopeLimitCos。