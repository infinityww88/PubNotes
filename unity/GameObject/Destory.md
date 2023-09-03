# Destroy GameObject

销毁 GameObject 而不是 Component。

Destroy(component.gameObject) 而不是 Destroy(component)。

Destroy(component) 只是将这个组件从 GameObject 移除，GameObject 仍然在。

GetComponentsInChildren returns you the same array on every machine, thus you can safely use it for networking.

Destroy(gameObject) 只是将 GameObject 标记为销毁，并不立即销毁，就像 Unity 通常的技巧，同一帧销毁的 GameObject 缓存，到 end of frame 才销毁。因此 Destroy 后，立即查询 parent.children 还会查询到这个 GameObject。

要实现 Destroy(gameObject) 后立即查询不到它，应该先将它从 parent.transform 上移除，然后 Destroy，随后任由它何时被销毁。gameObject.transform.parent = null 后会立即从 parent 上移除，parent.children 立即体现。

因此清理一个 gameObject 的所有 children 应该先从 parent 摘除，然后销毁，可以这样：

```C#
while (parent.childCount > 0) {
    var child = parent.GetChild(0);
    child.parent = null;
    Destroy(child.gameObject);
}
```

或

```C#
int n = parent.childCount;
for (int i = 0; i < n; i++) {
    var child = parent.GetChild(0);
    child.parent = null;
    Destroy(child.gameObject);
}
```

DestroyImmediate 只设计用在 Editor 脚本中。

没有办法查询 GameObject 是否被销毁，没有 IsDestroyed 方法。一旦调用了 Destroy 之后，就立即不能再依赖它。

Destroy GameObject 先摘除再销毁。

Object 再当前 Update 循环后立即销毁，下一帧就不存在了。Destroy 可以指定一个延迟，再指定的时间后销毁。如果 Object 是 GameObject，销毁它所有的 Components，和所有的 Children。

销毁是递归的，销毁一个 GameObject，所有下游的 GameObject 都会被销毁。

Actual object destruction is always delayed until after the current Update loop, but is always done before rendering.

Note: When destroying MonoBehaviour scripts, Unity calls OnDisable and OnDestroy before the script is removed.
