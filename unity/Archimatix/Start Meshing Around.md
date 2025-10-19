# Start Meshing Around

Archimatix 中一个重要的 node 类别是 Mesher。Mesher nodes 程序化生成标准的 Unity meshes，通常从一个或多个 shapes（或 spline） input 开始，然后将它们根据特定的规则组合。例如，在一个 Extrude 中，shape 被 copy 并 extrude 特定距离，然后生成 triangles bridge 两个 shapes。这样，一个 cube 就是一个 square shape 的 extrusion。

要体验 Mesher，实例化 3D Object Library 中的 BevelBox 并操作它的各种 handles 来变换它的 output。 

