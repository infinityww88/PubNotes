# UNIVERSAL RENDER PIPELINE UPGRADE GUIDE

Polaris 还支持 Universal Render Pipeline。当使用它时，你必须知道一些东西。注意除了 built-in 和 URP 的 render pipelines 是不支持的。你必须编写自己的 shaders 并手动升级它。

## Install URP

要使用 URP，你需要使用 Package Manager 导入以下 package

- Universal RP (com.unity.render-pipelines.universal)

然后进入 ​Window > Polaris > Project > Update Dependencies​ 来重新配置 project。

## Install URP Support Extension

用于 URP 的 Materials 和 Shaders 被保存在 package 中以避免编译错误。

当你打开 Wizard window 时，这个 package 将会自动被导出并安装。

如果你正使用 URP（在 Project Settings 中 URP asset 已经被赋值），它会尝试为你 project 中所有 terrains 更新 material。你还可以打开 Extension window 稍后完成这个步骤。

## Creating new terrain

Wizard 自动检测当前使用的 render pipeline，并为你采用合适的 material。

## Upgrade previously created terrain

对于之前使用 built-in render pipeline 创建的 terrains，你可以使用 Wizard 来 重新配置它的材质。在 Inspector 中，点击​ Shading > CONTEXT >Set Shader​ 来完成。

## Upgrade Grass and Tree Billboard materials

Grass 材质根据你的 render pipeline 被自动采用，因此不需要关心任何东西。对于新的 billboard assets，相应的材质将会被自动配置来适配你的 render pipeline。对于之前创建的 billboard material，你必须切换到 Griffin > Universal RP > Foliage > TreeBillboard​ shader

## Upgrade art asset materials

对于其他类型的 art assets，例如 Asset Store 中购买的 trees，你必须切换到 Universal Render Pipeline>... s​hader group 下的一个合适的 shader，Polaris 不能处理这些 assets 的任何问题，需要自己解决这些问题。

