方法

- T Acquire<T>()

  如果存在，返回一个备用的 item。否则创建一个新的。

  当用完时，记得调用 Release。

- void Acquire<T>(out T item)

  当用完时，记得调用 Release。

- AcquireList<T>()

- AcquireSet<T>()

- StringBuilder AcquireStringBuilder()

- T GetCachedResult<T>(Func<T>)

  使用提供的 delegate 创建一个 object 并缓存它，当这个方法使用相同的 delegate 再次调用时，返回相同的 object。

- Release<T>(HashSet<T>)

- Release<T>(List<T>)

- Release<T>(T)

- Release(StringBuilder)

- string ReleaseToString(StringBuilder)
