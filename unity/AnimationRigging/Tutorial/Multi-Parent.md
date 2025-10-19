这个模型播放一组动画，在 pickup 和 onback 动画中注册了两个事件：hand 和 back。

lfik 和 rfik 是之前的例子用来实现行走动画的设置，和这里要展示的约束没有关系。

MParent 上定义了 Multi-Parent Constraint 组件，上面包含了 3 个 GameObject：ground，hand，back。在动画事件中，通过切换不同 Source Objects 的 weight，将 sword 固定在不同的 Source Object 上。而且切换是瞬间完成的，即 weight 在 0 1 之间直接切换，没有混合过程。

Rigging 约束的 target object 只能是 Animator 下面的 bone。因此这个约束通常用于拔剑或将剑放回的动画中改变剑的 parent 的情景。这种情景中，模型中的一个 bone 改变 parent bone，而 parent bone 也是模型中的 bone（挂载点）。

mPosition 和 mRotation 和 mParent 类似，都是从多个 Source Objects 约束一个 target，但是只限制 position 或 rotation。

Source Objects 可以是骨骼 Hierarchy 上的 bones 和 Hierarchy 之外的 GameObject。Target Object 则只能是 Hierarchy 上的 bone。

