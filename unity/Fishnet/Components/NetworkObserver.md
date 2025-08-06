# NetworkObserver

这个组件让你覆盖指定 network object 的默认 observer 条件。

​​网络观察器（NetworkObserver）​​通过条件判断机制来确定客户端是否符合成为某网络对象观察者的资格——只要通过所有生效条件的检验，该客户端即被视为该对象的观察者（观察者数量不限）。

该组件既可​​覆盖 ObserverManager 的默认观察规则​​，也能​​为所挂载的网络对象额外添加观察条件​​。

手动添加此组件时，请注意避免因使用 ​​"忽略管理器"（Ignore Manager）​​覆盖类型设置，而导致意外覆盖该对象的默认场景观察者条件。

在运行时，如果这个组件不存在，它会自动添加到 network object。

FishNet 提供了多个内置观察条件，这些条件可以组合使用。您也可以继承 ObserverCondition 类来自定义专属条件。当所有条件全部成立时，该对象将对客户端可见。

每个条件都必须创建为 ScriptableObject 脚本化对象，并拖拽到 NetworkObserver 组件中进行配置。

## 设置

### Override Type

该设置用于调整 NetworkObserver 组件如何使用 ObserverManager 的配置规则：

- ​​添加缺失项（Add Missing）​​

  将 ObserverManager 中存在但 NetworkObserver 未配置的条件自动补全（推荐默认选项）

- ​​使用管理器配置（UseManager）​​

  完全采用 ObserverManager 中的条件设置，替换 NetworkObserver 原有条件

- ​​忽略管理器（Ignore Manager）​​

  仅保留 NetworkObserver 自身的条件配置，完全忽略 ObserverManager 的所有设置

通常建议选择「添加缺失项」作为标准配置方案。

### Update Host Visibility

当服务器对象对客户端不可见时，此设置会改变主机客户端渲染器的可见性。若需在可见性变化时启用或禁用其他功能，建议使用 NetworkObject.OnHostVisibilityUpdated 事件。

### Observer Conditions

要使用的条件列表，可以在此添加观察者判断条件。