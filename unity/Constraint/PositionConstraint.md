Position Constraint 组件移动 GameObject 来跟随 src GameObjects。

属性：

- Activate（按钮）：在定位好 constrained GameObject(带这个组件的 GameObject)和 src GameObjects 之后，点击 Activate 可以保持相对位置信息。这是个编辑器功能，类似 Joint 的 Anchor Position，使开发者免于手动计算和输入当前偏移信息。Activate 保存到 src GameObjects 的当前偏移到 Position At Rest 和 Postion Offset 中，作为 Constraint 的归零位置（默认位置），然后开启 Is Active 和 Lock 两个选项。
- Zero（按钮）：和 Activate 类似，但是直接将 constrained GameObject 的 Position 设置到 src GameObjects 的位置（多个则取中），即重置 Position At Rest 和 Position Offset 两个属性为零，然后开启 Is Active 和 Lock。
- Is Active：开启 constraint 求值，要同时应用 Constraint，确保 Lock 开启。不开启 Lock，组件只会不断更新 Position At Rest 和 Position Offset 选项，但不会移动物体。开启 Lock 后 Position At Rest 和 Position Offset 被 Freeze，物体会跟随 src GameObjects 移动。
- Weight：Constraint 的强度。weight=1 让 Constraint 严格按照 src GameObjects 的 rate 移动 GameObject。weight = 0 则完全不移动物体。weight 影响所有 GameObjects。此外，Src GameObjects 每个都有自己的 weight。

Position At Rest 是 Base 值。Constrained GameObject 的最终位置等于：

```
FianlPosition = PositionAtRest + DeltaPositionOffset * weight + PostionOffset.
```

可见，当 weight=1 时，src GameObjects 移动多少，GameObject 就移动多少。

Constraint Settings：

- Lock：开启 Constraint 移动 GameObject。关闭这个属性可以编辑 GameObject 的位置，而不会受 constraint 影响。除了改变 GameObject 的位置，还可以直接编辑 Position At Rest 和 Postion Offset 属性。如果 Is Active 开启，当你移动 GameObject 或 src GameObjects 时，Constraint 会自动更新 Position At Rest 和 Offset 属性。当你满意了改变之后，选中 Lock 来让 Constraint 来控制 GameObject。这个属性在 Play Mode 没有效果。运行时，要停止 Constraint 要么 disable 组件，要么将权重设置为 0。
- Position At Rest：当 Weight = 0 或者 Freeze Position Axes 时 使用的 x y z 值。要编辑这个字段，关闭 Lock。
- Position Offset：最后额外强制的 offset，无视 weight。
- Freeze Position：开启 X Y Z 控制 constraint 可以约束哪个轴，然后就可以手动编辑或脚本操作或者动画哪些 unfrozen 的 axis。
