# Overview

Final IK，Unity IK 解决方案终极集合。

## Final IK 包含

- Biped 角色 Full Body IK 系统
- VRIK：高速 full body solver，专注于 VR avatars
- Baker：烘焙 IK procedures，animation adjustments，Timeline 和 Mecanim layers 到 Humanoid，Generic 或 Legacy animation clips
- Biped IK：Unity 内置 Avatar IK 系统的代替品，提供更多的灵活性，并具有相同的 API
- CCD（Cyclic Coordinate Descent）IK
- Multi-effector FABRIK（Forward 和 Backward Reaching IK）
- LookAt IK：bipeds 的 look-at solver
- Aim IK：用于武器瞄准，looking at objects
- Limb IK：用于 arms 和 legs 的 3 joint solver（关节解析器）
- Arm IK：用于 arms 的 4 joint solver
- Leg IK：用于 legs 的 4 joint solver
- Rotation constraints：可以工作于 CCD，FABRIK 和 Aim solvers 的 Angular，Polygonal（Reach Cone），Spline 和 Hinge rotation limits
- Interaction System：用于创建过程化 IK interactions 交互的简单工具
- Grounder：自动化垂直 foot 放置和 alignment 修正系统
- CCDIKJ，AimIKJ：基于 AnimationJobs 的多线程 solvers

## 技术概览

- 不需要但是可以用于 Mecanim
- 优化得到很好的性能
- 模块化，易于扩展。组合你自己定制的 character rigs
