# misc

DOVirtual 有一些帮助函数可以对 ease 曲线进行求值

```C#
float DOVitual.EasedValue(float from, float to, float lifetimePercentage, Ease easeType);
float DOVitual.EasedValue(float from, float to, float lifetimePercentage, Ease easeType, float overshoot);  //Overshoot时间
float DOVitual.EasedValue(float from, float to, float lifetimePercentage, Ease easeType, float amplitude, float peroid); //振幅与震荡周期
float DOVitual.EasedValue(float from, float to, float lifetimePercentage, AnimationCurve easeCurve);
```

lifetimePercentage 在超出 from-to 范围之后，只是简单地按照曲线公式在相应的位置计算，而不是常量外插值，即小于 from 的范围求值为 from 的 value，大于 to 的范围求值为 to 的 value。但是常量外插值可以很容易地对 lifttimePercentage 进行 Mathf.Clamp 而得到。

from 可以大于 to，得到递减 ease 曲线。
