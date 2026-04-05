Unity 粒子系统里的 Trails 模块（拖尾） 用来让粒子在运动过程中留下轨迹，常用于子弹尾迹、火焰尾巴、能量轨迹、魔法效果等。

Trails 的作用是给每个粒子生成一条随时间延伸的“线带（Ribbon）”

它和普通 Trail Renderer 不同：

- Trail Renderer：绑定在 GameObject 上（一个物体一条轨迹）
- Trails 模块：每个粒子都有自己的轨迹

Trails 模块 = 让粒子“画出自己的运动轨迹”

## 参数

### Mode

- Particle：每个粒子一条单独的拖尾
- Ribbon：所有粒子连接成一条连续带，常用于：激光、能量流、风轨迹

### Lifetime（拖尾长度）

控制拖尾“持续时间”

- 数值越大 → 尾巴越长
- 数值越小 → 尾巴越短

本质是：轨迹点保留多久。

### Min Vertex Distance（顶点距离）

控制轨迹采样密度：

- 小 → 更平滑（性能更差）
- 大 → 更粗糙（性能更好）

常用值：0.1-0.5

### Width over Trails（宽度变化）

控制尾巴从头到尾的宽度变化

比如：

- 前粗后细（常见尾焰）
- 中间粗两头细（能量波）

### Color over Trails（颜色变化）

控制尾巴渐变颜色：

例子：

- 白 → 黄 → 红 → 透明（火焰）
- 蓝 → 透明（能量）

### Inhert Particle Color

是否继承粒子颜色

- 开启：尾巴跟粒子颜色一致
- 关闭：用独立的渐变

### Die With Particles

- 开启：粒子消失时尾巴立刻消失
- 关闭：尾巴继续存在直到消失（更自然）

推荐关闭（更真实）

### Size affects Width

粒子大小影响拖尾宽度

- 大粒子 = 粗尾巴
- 小粒子 = 细尾巴

### Texture Mode

- Stretch：纹理被拉伸（常用）
- Tile：重复铺贴（适合能量条）
- Distribute Per Segment：每段分布

### World Space/Local Space

- World Space：拖尾留在世界中
- Local Space：拖尾跟随粒子移动（不常用）

