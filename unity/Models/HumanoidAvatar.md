Unity Animation 系统有一个特殊功能，专门用于人形角色。因为人形角色在游戏中太常见了，Unity 为人形动画提供了一个专门的工作流和扩展工具。

Avatar System 是 Unity 如何识别一个特定的动画模型是人形模型，模型的哪部分对应 legs，对应 arms，对应 head 和 body 等等。

因为不同人形角色骨骼的相似性，可以将一个人形角色的骨骼映射到另一个角色。

Avatar 为人形骨骼结构定义了一个抽象通用的结构，在导入时，每个人形骨骼都映射到这个抽象结构中。播放人形动画时，动画的会操作这个抽象的骨骼，然后抽象的骨骼带动真实的骨骼。这样，一个人形动画就可以适用于所有的人形骨骼了。

# Retarget Humanoid animations

Unity Mecanim 动画系统最强大的一个功能就是 retarget humanoid animations。这意味着可以应用一组相同的动画到不同的角色模型上。

Retargeting 只能用于配置了 Avatar（定义了模型骨骼到抽象通用骨骼结构映射）的人形模型。一个配置了的 avater 提供了在模型骨骼之间对应的能力。

模型动画不再操作骨骼，而是操作抽象通用的骨骼，然后抽象骨骼带动真实骨骼。

## 建议的 Hierarchy 结构

当使用 Mecanim animations，你可以期待 scene 中包含以下元素：

- 导入的角色模型，上面有配置好的 Avatar（骨骼到 Avatar 的映射）
- Animation Component，引用一个 Animator Controller asset
- 一组 animation clips，被 Animator Controller 引用
- 角色的脚本
- Character 相关的组件，例如 Character Controller

你的 Project 中还应该包含其他带有有效 Avatar 的角色。

要在 character models 之间 retarget，按照以下步骤：

- 在场景中创建一个 GameObject，包含 Character 相关组件（例如 Character Controller）
- 将模型作为 child 放到 GameObject 下面，并挂载 Animator 组件
- 确保 Root 的脚本引用的 Animator 查找的是 child 中的 animator，而不是在 root 身上。使用 GetComponentInChildren\<Animator\>()，而不是 GetComponent\<Animator\>()

然后要重用同一个动画到另一个模型中，按照以下步骤：

- disable 原来的模型
- 将想要的模型作为另一个 child 挂载到 Root 下面
- 确保新模型的 Animator Controller 属性引用相同的 controller asset。

  Animator Controller 中引用着 animation clips。这些 clips 通常是作为一个模型的资源文件导入，并包含在其中。因此通常这些 clips 只应用于它所在的模型。而 Retargeting 功能，可以让一个模型中的 animation clip 驱动另一个模型。

- 调整 Character Controller，transform，和其他 Root 上的属性，确保 animations 和新的模型能正常工作
