This scene is an extension of the "Aim Swing" demo (take a look at it for a simpler example of redirecting animation).

Here I have added some basic raycasting to find the height of the ground at the position in front ot the character and redirect the swing animation based on the vertical offset of the raycast hit and the character's position.

Take a look at TerrainOffset.cs on the "Dummy" Game Object to see how it was done.

Right-click on any FinalIK component and select "User Manual" or "Script Reference" for more info.

这个 scene 是 Aim Swing 的扩展。添加了一些基础 raycasting 来找到 character 前面一个位置的 ground height，并且基于 raycast hit 的 vertical offset 和 character position 重定向 swing animation。

这个 scene 中 Aim Transform 就是一个很随意的位置，就像 Aim Boxing 中所说的一样，它只是用来定位动画中木棒的 hit position 的。
