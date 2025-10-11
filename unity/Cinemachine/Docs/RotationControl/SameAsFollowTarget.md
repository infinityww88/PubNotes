CC 同步 Tracking Target 的方向，并提供 Damping。

当与 Position Control 中的"硬锁定目标(Hard Lock To Target)"行为配合使用时，最终效果是让 CinemachineCamera 与控制游戏对象的路径和旋转保持一致。即 CC 的完全锁定在 Tracking Target，就好像是它的 child object。
