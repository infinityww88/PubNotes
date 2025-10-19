# Resources

在CG中，资源是保存资源数据的GameObjects的引用。有两种主要资源：

- Input Resources：被模块读取的资源（例如CurvySpline，Meshes，Prefabs等等）
- Output Resources：被模块创建的资源（例如Meshes或Prefab克隆等等）

CG区别被管理资源和非管理资源

## 被管理资源

这些资源是CG的子对象，需要被一个module创建。当创建一个模板时，它们将被存储在模板内部，对它的引用也被保存

## 非管理资源

这些是用户创建的资源，通常在CG层次之外。当创建一个模板时，它们不被复制，对他们的引用将重置为null。这些就是模板的参数，通过改变这些参数来复用模板
