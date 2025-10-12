Cinemachine 相机模拟了真人摄影师操作真实相机的行为方式。因此，它们对上下轴向具有敏感性，并始终尽量避免在取景中引入旋转（Roll）。正是由于这种敏感性，Cinemachine 相机会避免长时间直视正上方或正下方。虽然偶尔可能会短暂出现这种情况，但如果"注视目标"（Look At target）长时间保持在正上方或正下方，相机可能无法始终达到预期的构图效果。

如果正在开发一款俯视角游戏，其中相机需要垂直向下观察，最佳实践是为相机重新定义“上方向”。你可以通过在 Cinemachine Brain 组件中设置 “World Up Override” 来实现这一点——将其指定为一个游戏对象（GameObject），该对象的本地“上方向”即为希望的 Cinemachine 相机默认采用的“上方向”。此设置将应用于该 Cinemachine Brain 所控制的所有 Cinemachine 相机。


