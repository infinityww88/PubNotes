# Entity Component System

ECS 是 DOTS（Data-Oriented Tech Stack）的核心。

- Entities：entities，或者 things，即 GameObject，它们填充你的游戏或程序
- Components：entities 关联的数据，数据组织为 Components。这个数据组织的差别是面向对象和面向数据设计的核心不同
- Systems：将 component 数据从当前状态转换到下一个状态的逻辑。例如，一个系统可能通过速度乘以 deltaTime 来更新所有移动的 entities 的 positions

Scenes 包含许多 Entities；Entities 包含很多表示这个 GameObject 方方面面的数据 Components；Component 包含 GameObject 某个方面的所有数据。

