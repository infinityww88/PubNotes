# UQuery

UQuery 提供一组扩展方法来获取一个 visual tree 中的元素。UQuery 是基于 JQuery 或 Linq，但是 UQuery 被设计为尽可能显式动态内存分配。这允许在 mobile platform 上优化性能。

使用 UQueryExtensions.Q，或者使用 UQueryExtensions.Query 初始化一个 QueryBuilder。

下面的例子从 root 开始查找第一个名为 foo 的 Button

```C#
root.Query<Button>("foo").First();
```

下面 UQuery 在同一个 group 中迭代每个名为 foo 的 Button

```C#
root.Query("foo").Children<Button>().ForEach(//do stuff);
```
