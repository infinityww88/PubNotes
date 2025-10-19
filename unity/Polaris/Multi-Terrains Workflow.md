# Multi-Terrains Workflow

Polaris 设计和架构一直将 multi-terrains 考虑在内。这意味着 terrain tools 应该从 terrain 自身分离，并且它应该无缝地在多个 terrain 中工作，而不需要手动在它们之间迭代。要得到最平滑的体验，资源密集操作例如 texture 修改应该在 GPU 端完成。

一些操作，例如 geometry painting 需要邻接的 terrain 被正确设置，使得它们的边缘可以 match up，消除 gap。

Scene 中的 terrains 可以出于各种目的被划分为一组，例如 play area group，或者 background group，或者 biomes，使用一个简单的 integer 作为 Group Id。这个 Id 告诉 terrain tools 哪些 terrains 应用这个操作，哪些不应该。
