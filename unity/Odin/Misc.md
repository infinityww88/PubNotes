# Misc

OnValueChange 只对从 Inspector 中的修改起作用，对于脚本中的修改无效。

C# 属性的生成直接调用属性名，如果有参数就像调用函数一样，没有 new，同时 [] 中可以放多个属性

[MinValue(1), MaxValue(30), OnValueChanged("GenerateTrajectoryPoints")]