Constraint 组件连接一个 GameObject 的 position，rotation，scale 到另一个 GameObject。

被约束的 GameObject 就像它连接的 GameObject move，rotate，scale。

Unity 支持以下 Constraint 组件：

- Aim：旋转 constrained GameObject 朝向连接的 GameObject
- Look At：简化的 Aim Constraint
- Parent：跟随 linked GameObject 一起 Move 和 Rotate constrained GameObject
- Position：跟随 linked GameObject 移动 constrained GameObject
- Rotation：跟随 linked GameObject 旋转 constrained GameObject
- Rotation：跟随 linked GameObject 缩放 constrained GameObject

# Linking to GameObjects

使用 Constraint 组件的 Sources list 指示要连接的 GameObjects。

一个 Constraint 可以连接多个 GameObjects。此时，Constraint 使用它 source GameObjects 的平均 position，rotation，scale。

例如要将一个 Light 指向一组 GameObjects，添加 Aim Constraint 组件到 Light GameObject。然后将要照亮的 GameObjects 添加到 Sources list 中。Aim Constraint 旋转 light 朝向 sources 的平均位置。

Unity 按照 GameObjects 出现爱 Sources list 中的顺序求值。这个顺序对 Position 和 Scale Constraints 没有影响。但是会影响 Parent，Rotation，Aim Constraints。要得到想要的效果，在 Sources list 中拖放 item 改变其顺序。

你可以串联约束一系列 GameObjects。例如你想要让一组小鸭子排成一列跟随它的妈妈。你可以为每个小鸭子添加一个 Position Constraint 组件，第一个小鸭子的 Source 指向鸭妈妈，后面的每个小鸭子的 Position Constraint 组件的 source 指向前一个小鸭子。

要避免创建 Constraints 的循环，这会导致非预期的结果。

# 设置 Constraint 属性

Weight 属性控制 Constraint 的影响程度。

Source list 中每个 GameObject 也可以单独设置一个 weight。

Constraint 有两个重要的属性值：At Rest 和 Offset。

- At Rest：当 constrained GameObject 完全不受约束时，GameObject 相应属性的数值（位置、旋转、缩放）

  注意这是全局数值，因为约束组件之间没有 parent-child 关系，它们是完全独立的。因此当 Constraint 有效关闭时，将相应属性设置为 At Rest 的数值。

  At Rest 还有一个作用，它是 Constraint 更新 GameObject 属性时 Lerp 的 start 数值，Lerp 的 end 数值，Lerp 的时间因子就是 weight。

  当 Source GameObjects 更新时，Constraint 在 At Rest 数值和 Source 当前数值之间通过 weight 进行 Lerp 插值，插值结果作为 GameObject 的更新值。

  当 Constraint 的 weight 或 Freeze Axes 相应属性取消时，数值被设置为 At Rest 的数值。

- Offset

  Lerp 的 End 数值是 Source GameObjects 平均值加上 Offset。即 Constraint Anchor 点到 Source GameObjects 平均值的偏移。

如果 Lock = false，无论是在 Editor Mode 还是 Play Mode，无论 Constraint 是 active 还是 inactive 的，都可以实时更新 At Rest 或 Offset。如果 Lock = true，禁止更新这两个数值（注意是这两个数值，而不是 GameObject 本身）。

**即 Lock 控制是否可以更新 At Rest 和 Offset（不管是在 Editor Mode 还是 Player Mode，Constraint 是 Active 还是 Inactive），不是锁定 GameObject**

Is Active 控制 Constraint 是否生效。

Constraint 生效时，最终控制 GameObject 的 transform 属性，抹去其他系统对 Transform 的更新。

Freeze Axes 控制哪些轴不被 Constraint 修改。选中的轴被 Constraint 更新，反之不被 Constraint 更新。

当添加一个 Constraint 组件，它默认是 inactive 和 unlocked 的。这可以让你在 active 和 lock Constraint 之前，精细调整 constrained 和 source GameObjects 的 position，rotation，scale。

Activate 和 Zero 按钮提供了一些便捷设置：

- Activate：基于当前 Source GameObjects 和 Constrained GameObject 的姿态，设置 At Rest 和 Offset，然后 Lock（At Rest 和 Offset）并 Active Constraint 组件

  - At Rest：设置为 Constrained GameObject 的当前姿态
  - Offset：Contrainted GameObject 的当前姿态到当前 Source GameObjects 平均姿态的偏移，设置为 Offset

- Zero：类似 Activate，将 GameObject 移动到 Source GameObjects 的平均姿态，将其设置为 At Rest 的值，Offset 设置为 zero，然后 Lock 并 Active Constraint 组件

注意 Editor Mode 时，Lock = false 可以编辑 At Rest 和 Offset，而不进行约束，即使 Is Active = true，它根据 Source GameObjects 和 Constrained GameObject 的当前状态实时更新 At Rest 和 Offset，并不会有 constraint 效果。也可以认为 constraint 在 At Rest 和 Offset 编辑后起作用，因此看起来就好像 constraint 没有生效一样。Lock = true 则禁止对 At Rest 和 Offset 的编辑，如果 Constraint Is Active = true，则在 Editor Mode 中，也可以看见 Constraint 生效。

但在 Play Mode 时，Lock = false 可以运行时编辑 At Rest 和 Offset，这也会实时修改 Constrained GameObject 的当前姿态（前提是 weight 不为 0）。

在 Play Mode 时，如果 Constraint 组件生效，无论如何，不可能直接编辑 Constrained GameObject 的 Transform。Constraint 完全控制 Transform，无论 Lock 为 True 还是 False，Lock 只控制是否编辑 At Rest 还是 Offset。

