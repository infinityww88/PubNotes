# Network Start Position

控制 player 在哪里生成。

附加一个 Network Start Position 组件到一个 scene 中的 gameobject，并且将这个 gameobject 放置到你想要一个 players 开始的位置上。你可以添加任意多个 start positions 到你的 scene。Network Manager 检测 scene 中所有的 start positions，并且当它生成一个 player instance 时，它使用其中一个的 position 和 orientation。

Network Manager 默认地将会在 （0，0，0）位置生成 players。添加这个组件到一个 gameobject 将会自动注册/反注册它的 gameobject 的 transform 到 Network Manager，作为一个可用的 spawning position。

依赖于 Network Manager Player Spawn Method 的设置，Spawning 或者是 Random（同一个 spawn position 可能被两个或多个 players 使用），或者 Round Robin（使用每个可用的 position，直到 clients 比 spawn points 更多）。

![NetworkStartPosition](../../Image/NetworkStartPosition.png)
