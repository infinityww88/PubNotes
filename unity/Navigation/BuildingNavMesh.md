# Build a NavMesh

从 scene geometry 中构建 NavMesh 的过程称为 NavMesh Baking。

这个过程收集所有被标记为 Navigation Static 的 GameObjects 渲染的 Meshes 和 Terrains。然后处理它们来创建一个mesh，近似 scene 中的 walkable surfaces。

Navigation Window（Window > AI > Navigation）

1. 选择影响 navigation 的 scene geometry（walkable surfaces 和 obstacles）
2. 标记它们为 Navigation Static，来将它们包含到 NavMesh baking 过程
3. 调整 baking setting，来匹配你的 agent
   - Agent Radius 定义 agent 中心可以靠近 wall 或 ledge（边沿）多近
   - Agent Height 定义 agent 可以通过的高度
   - Max Slope 定义 agent 可以行走的斜坡角度
   - Step Height 定义 agent 可以 step on 的 obstructions 的高度
4. 点击 bake 构建 NavMesh

![NavigationSetupObject](../Image/NavigationSetupObject.png)

![NavigationSetupBake](../Image/NavigationSetupBake.png)

当 Navigation Window 打开时，NavMesh 的结果将会在 scene 中显式为 blue overlay，在 scene geometry 之上。

注意到 NavMesh 比 geometry 窄一些，因为 NavMesh 表示的是 agent 中心可以移动的区域。
