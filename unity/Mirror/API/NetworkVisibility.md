# NetworkVisibility

public abstract class NetworkVisibility : NetworkBehaviour

## Methods

- OnCheckObserver(NetworkConneciton conn)

  被 visibility system 调用来决定一个 observer（player）是否可以看见这个 object。

  如果这个 function 返回 true，network connection 将被添加为一个 observer

- OnRebuildObservers(HashSet<NetworkConnection> observers, bool initialize)

  被 visibility system 调用来重建可以看见这个 object 的 observers 集合

- OnSetHostVisibility(bool visible)

  被 visibility system 对 host 上的 objects 调用。

  Host 上的 Objects（具有一个 local client）在对 local client 不可见的时候，不能 disabled 或 destroyed，因为 server 还在使用。因此这个函数被调用允许特定代码隐藏这些 objects。典型的实现是，disable object 上的 renderer 组件。这个函数只在 host 上的 local clients 上调用。
  