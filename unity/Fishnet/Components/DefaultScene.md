# DefaultScene

这个组件可以用于在 network start 时加载一个 online scene，在 network stop 时加载一个 offline scene。

这个组件根据 server 和 client 的连接状态自动在 online 和 offline scene 之间切换。

online scene 和 offline scene 必须在 inspector 中设置好，而且不能是同一个 scene。

## 设置

- Enable Global Scenes

  开启时，这会导致让 scenes 作为 global 加载，否则作为 connection 加载。

- Start In Offline

  这会导致 game start 时，server 和 clients 加载 offline scene。

- Offline Scene

  当 offline 加载的 scene。

- Online Scene

  当 online 加载的 scene。

- Replace Scenes

  - 使用 online or offline scene 替换所有已加载的 scenes
  - 使用 online or offline scene 只替换 online scenes