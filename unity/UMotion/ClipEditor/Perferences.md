Perferences 全局存储，影响所有 UMotion projects。

就像 code projects = codes + 项目信息，gimp project = image/layers + 项目信息，UMotion Project 就是一个动画片段加上这个项目的各种其他信息，以允许非破坏性编辑。

每个 action 可以配置一个快捷键。所有 actions 可以分为 3 类：

- Clip Editor
- Pose Editor
- General

每个快捷键只在所在窗口被选中时有效。如果一个 UI 元素有一个 shortcut，将在它的 tooltip 中显式。

项目设置

- Select frame: Suppress modifications dialog

  开启时，当选择的 frame 在 Clip Editor 中被改变时，Unapplied Modifications 对话框将不会显示，所有未应用的修改将会被自动丢弃

- Automatic Backups

  开启 UMotion projects 自动 backup

- Backup Interval

- Num Backups per Project

  每个项目存储的最大 backups 数量

- Delete Backups After

  超过指定 hours 之后的 backup 自动删除

