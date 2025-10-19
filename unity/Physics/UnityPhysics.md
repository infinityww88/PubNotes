# Physics

- 触发trigger事件的两个gameobject必须至少有一个是Rigidbody
- ConfigurableJoint -> cloth
- PhysicsScene && size && rigidbody fixjoint mass 0.1kg
- Selection.active Selection.gameobject, for multiple selection(use control/shift)
  - In Hierarchy, active object is always the first one
  - In Scene, active object is always the last one
- Undo.RegisterCompleteObjectUndo until next frame?
  - record object, not gameobject, only record first level field change
  - if record transform change, must record transform, not gameobject
- MenuItem call
- Physics不适用模拟极限情形，只用于模拟简单低速正常尺寸的物理现象。相对论/量子力学vs牛顿力学。尺寸。连接在一起的约束数量限制。fake，看起来正确就是正确，用简单的物理伪装成复杂的物理现象，抛石机不用真的网兜，只用rope连接stone，但是在stone上覆盖cloth，使得看起来像网兜，让后在stone抛掷到45度速度方向，断开隐形的rope，让stone飞出去，这样使用简单的stringjoint就伪装出真实网袋抛石机。不仅物理，渲染、声音、AI等等都是使用简单机制伪装复杂机制，这也是游戏开发的精髓和有意思的地方。纵观游戏开发历史，就是如何使用简单机制伪装真实复杂机制的历史，这才是游戏开发本质，而不是用游戏模拟真实场景。即使游戏引起提供了越来越复杂的功能，但它们不是用来模拟对应的真实场景的，而是为了更方便的伪装更真实更高级的场景的。最终的游戏效果应该是远远超出游戏引擎提供的功能本身能实现的效果的。
- 交互，输入-系统变化-输出（影响新的输入）
- 诸多独立系统平行运行，一个系统变化会引起另一个系统变化，系统之间发送消息来相互产生变化
- 自造轮子，尽管不会使用，甚至不能成功，但是你会在其中学会很多知识经验，很多知识经验甚至十分重要，你不亲自造一次轮子很难或者很晚才能知道（模仿而不是模拟）

