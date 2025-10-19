# The OdinSerialize And The ShowInInspector

OdinSerialize 或 Serialize 与 ShowInInspector 之间有很大的区别，尽管第一次看到的时候不那么明显。

它们都导致一些东西被绘制到 inspector 上。但是使用 ShowInInspector，显示的任何东西不会被保存。如果你想一些东西即在 Inspector 上显示，又能够被保存，使用 OdinSerialize。

如果你将 OdinSerialize 放在一个成员上，而它还是没有显示在 inspector 上，这是因为这个属性实际上没有导致成员被序列化，例如一个 non-auto 属性，或者一个 virtual 或 abstract auto-property 从不会被 Odin 序列化。还有那些在 interface 中声明，但是在派生类中实现的属性也不会被序列化（因为这导致 property 方法成为 virtual 的）。其他正常的字段会显示在 inspector 上并序列化。

可以联合 HideInInspector 和 OdinSerialize，这样你可以保存一些东西，但是不把它显示在 Inspector上。

在 Inspector 上绘制数据的 editor 和序列化数据是两个分开独立的功能。尽管通常会将它们组合在一起使用，但是确实可以分开独立地使用每个功能，或者仅绘制，或者仅保存。
