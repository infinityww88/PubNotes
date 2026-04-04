# 概述

Unity 粒子系统里的 Sub Emitters（子发射器），是做“一个粒子触发另一个粒子系统”的机制，常用于组合复杂特效（爆炸、火花、烟雾等）。

Sub Emitters = 粒子在某个时机（出生/死亡/碰撞）触发另一个粒子系统。

主粒子系统（Parent）里的每个粒子，在特定事件发生时：会“生成”一个新的粒子系统（Sub Emitter）。

Sub Emitter 支持 4 种触发方式：

- Birth：粒子刚出生时，触发 sub ps（particle system）。例如 火焰+火星，魔法粒子 + 小粒子尾巴
- Death：粒子死亡时，触发 sub ps（最常用）。例如 爆炸结束产生烟雾，子弹命中后产生火花
- Collision：粒子碰撞到物体时，触发 sub ps。需要开启 collision 模块。例如 雨滴落地产生水花
- Trigger：粒子进入触发区域时，触发 sub ps（较少使用）。需要开启 Trigger 模块

## 如何使用

在场景中创建 parent particle system 和 child particle system，在 parent ps 的 sub emitter 选择 child particle system。

子粒子系统通常要：

- Play On Awake = false
- Stop Action = None
- 调整为“短生命周期”

典型粒子（爆炸）

- 主粒子（Parent）：大火球（0.5秒）
- 子粒子（Child）：Death，烟雾（2~5秒）

重要参数：

- Emit Probability（发射概率）

  不是每个粒子都会触发。1 -> 每个都触发，0.5 -> 一半会触发。

- Inherit Lifetime

  子粒子是否继承父粒子的剩余时间

- Inherit Color/Size

  子粒子可以继承父粒子的颜色、大小、速度。

每个粒子都可能触发一个子粒子系统，数量可能非常多，开销可能非常大。因此适当降低主粒子数量，使用 Emit Probability 控制触发子粒子系统的数量，子粒子要轻量（发射粒子要少，生命周期要短），避免嵌套太深（parent -> sub -> sub）。

总结就是，Sub Emitters = 让“一个粒子”在特定时机生成“另一个粒子效果”，用于构建复杂特效链。

## 工作原理

子粒子系统必须是场景中的 Child Particle System，不能是 Prefab 资源。

上面说的父粒子“触发”子粒子系统，不是调用子粒子系统的 Emit() 发射粒子，而是以子粒子系统为模板实例化一个新的粒子系统并自动播放。因为 Sub Emitter 需要独立的位置，独立的生命周期，独立的模拟状态。如果仅使用 Emit，所有粒子的子粒子效果只会从一个系统发射，无法做到每个父粒子触发一个独立的效果。

但是 Unity 不会在场景中实例化一个 Sub Emitter 的副本，而是在内部进行的，并进行了池化优化，因此在 Scene 看不见实例化的粒子系统。

Unity 内部每次触发时：

- Unity 会创建一个子粒子系统实例（internal instance）
- 位置 = 父粒子的位置
- 状态 = 从模板复制
- 自动播放

因此 Child Particle System 本质是作为模板用的，它本身通常不应该工作，即 Play On Awake = false，否则你就会看见一个额外的粒子效果。

粒子系统默认靠 Emit 模块发射粒子（Rate Over Time/Rate Over Distance/Burst）。但是你也可以在脚本中手动调用 Emit 函数，手动发射粒子，创建独特的发射行为，例如响应某些时间，或以不同于 Emit 模块的行为发射粒子。

粒子系统的 Duration 只是发射粒子的时间，不是粒子的生存时间，即使 duration 结束，仍然会有很多粒子在运行，只有最后一个粒子死亡，粒子系统才算结束。

Stop 函数默认只是停止发射粒子，不会销毁正在运行的粒子，但是可以传递 bool 参数 指示同时销毁所有粒子。

普通的粒子系统的 Stop Action 可以是 Destroy 或 Disable。但是 Sub Emittes 不依赖这个设置。Unity 内部会自动处理生命周期，不需要配置 Stop Action。

普通的粒子系统调用 Play() 函数就可以重复播放，但是如果系统正在运行，需要先 Stop 并清理。仅调用 Play() 的话，如果系统正在播放，就没有效果，如果系统已结束，就会重新播放。注意，这里说的粒子系统结束指的是所有粒子都已死亡，而不是 Duration 结束，Duration 只表示发射多久，所有粒子的生存时间才是粒子系统的生命周期。

可以配置多个 Sub Emitters，Birth、Death、Collision、Trigger 都可以配置多个子粒子系统。

Sub-Emitters 是 Scene 中创建的普通 Particle System GameObjects。

可以使用 Inherit Options 从 Parent Particle 向新创建的 Particle 传递属性，包括 size，rotation，color，lifetime。要控制如何继承 parent particle 的速度，配置 sub emitter 的 Inherit Velocity 模块。 
