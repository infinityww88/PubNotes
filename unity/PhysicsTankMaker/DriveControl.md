坦克控制输入 vector2(horizontal, vertical)，控制 5 个选项：

- L_Input_Rate
- R_Input_Rate
- Turn_Brake_Rate
- Stop_Flag
- Pivot_Turn_Flag

L_Input_Rate < 0 是左边履带向前滚动，R_Input_Rate 是右边履带向前滚动，因此要设置以一定档位 gear 前进时，应设置：

```C#
controlScript.L_Input_Rate = -gear;
controlScript.R_Input_Rate = gear;
```

当两个履带档位的值不相同时，坦克就会转弯。

Turn_Brake_Rate：当履带档位不相同时，坦克会发送转弯，这个值控制转弯的速度，这个值越大，坦克转弯越快，甚至接近原地转圈。当这个值为 0 时，tank 只会略微转弯一下，然后继续直线前进。

Stop_Flag：指示 tank 处于停止状态，停止一切动力学计算。尽管当 L_Input_Rate 和 R_Input_Rate 都设置为 0 时，tank 也会停下，但是内部的动力学计算仍在继续，可能会导致一些轻微的异常运动。例如，在平面上，tank 可能仍然以非常小的速度运动。在斜坡上，即使引擎不再输出，但是 tank 仍然会沿着斜坡缓慢下滑。当设置 Stop_Flag 时，会直接停止动力学计算，并让 tank 真正停下来。但是当设置 L_Input_Rate 或 R_Input_Rate 不为 0 时，必须将 Stop_Flag 设置为 False，否则，坦克仍然会静止不动。

通常，当两个履带存在差速时，坦克就可以转弯转向。但是这种转向时带运动的，坦克会走一个弧线。而 Pivot_Turn_Flag 可以让坦克原地转向，而无需运动一段距离。尤其时当只有水平输入，没有垂直输入时，例如只按下 A 键时，玩家可能期望的是坦克原地向左转。

```C#
if (controlScript.Allow_Pivot_Turn)
{ // Pivot-turn is allowed.
    if (vertical == 0.0f && controlScript.Speed_Rate <= controlScript.Pivot_Turn_Rate)
    { // The tank should be doing pivot-turn.
        horizontal *= controlScript.Pivot_Turn_Rate;
        controlScript.L_Input_Rate = -horizontal;
        controlScript.R_Input_Rate = -horizontal;
        controlScript.Turn_Brake_Rate = 0.0f;
        controlScript.Pivot_Turn_Flag = true;
        return;
    }
}
```

这些值都是每帧根据输入动态设置的。
