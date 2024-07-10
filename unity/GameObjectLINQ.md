# LINQ to GameObject

每个 traverse 方法返回 IEnumerable\<GameObject\>，并且延迟执行。

```C#
origin.Ancestors();
origin.Children();
origin.Descendants();
origin.BeforeSelf();
origin.AfterSelf();
```

可以将 query 连接，并使用一些特定方法（Destroy，OfComponent 等等）。

```C#
// 销毁所有 tag == foobar 的 objects
root.Descendants().Where(x => x.tag == "foobar").Destroy();

// 销毁所有 cloned objects
origin.transform.root.gameObject
    .Descendants()
    .Where(x => x.name.EndsWith("(Clone)")
    .Destroy();

// 获得自己和自己下游 objects 的 FooScript 组件
var fooScripts = root.ChildrenAndSelf().OfComponent<FooScript>();
```

注意：LINQ to GameObject 对迭代是优化的，返回结构体 struct 的 enumerable/enumerator，而不是 IEnumerable\<GameObject\>（class 对象）。

所有方法都是 GameObject 的扩展。使用 Unity.Linq，然后就可以使用这些扩展方法。

```C#
using Unity.Linq;

var origin = GameObject.Find("origin");
origin.Decendants().Destroy();
```

## 操作

LINQ to GameObject 有一些操作方法，append child（Add，AddFirst，AddBeforeSelf，AddAfterSelf），append multiple objects（AddRange，AddFirstRange，AddBeforeSelfRange，AddAfterSelfRange），以及 destroy object（Destroy）。

```C#
var root = GameObject.Find("root");
var cube = Resources.Load("Prefabs/PrefabCube") as GameObject;
var clone = root.Add(cube);
var clones = root.AddAfterSelfRange(new[] { cube, cube, cube });
root.Destroy();
```

Add 方法添加的 object 是 cloned，因此可以用于 instantiate prefab 的场景。如果想只移动 child，可以使用 MoveToLast，MoveToFirst，MoveToBeforeSelf，MoveToAfterSelf，和 MoveToLastRange，MoveToFirstRange，MoveToBeforeSelfRange，MoveToAfterSelfRange。

## 遍历方法

所有 traverse 方法都可以查找 inactive object。如果找不到，返回类型为 GameObject 的方法返回 null，返回类型为 IEnumerable\<GameObject\> 的方法返回空序列。

- Parent：返回这个 GameObject 的 parent GameObject
- Child：返回指定名字的第一个 child GameObject
- Children：返回所有 child GameObjects 的集合
- ChildrenAndSelf：返回 self 和 child GameObjects 的集合
- Ancestors：返回这个 GameObjects 的所有 ancestor GameObjects 的集合
- AncestorsAndSelf
- Descendants：返回 descendant GameObjects 的集合
- DescendantsAndSelf
- BeforeSelf：返回这个 GameObject 前面的 sibling GameObjects
- BeforeSelfAndSelf
- AfterSelf：返回这个 GameObject 后面的 sibling GameObjects
- AfterSelfAndSelf

Descendants 有一个 descendIntoChildren 重载方法，它在条件不匹配时停止遍历 children。

## 操作方法

操作方法有 4 个可选参数：

- cloneType：配置克隆 child GameObject 的 localPosition/Scale/Rotation，默认只克隆 original local transform
  - KeepOriginal：默认，设置 Transform 与 original object 一样
  - FollowParent：设置 transform 与 parent 一样
  - Origin：设置 position=zero，scale=one，rotation=identity
  - DoNothing：Position/Scale/Rotation as is
- setActive：配置 child GameObject 的 active 状态
- specifiedName：配置 child GameObject 的 name
- setLayer：配置 child GameObject 的 layer 与 parent 相同

方法：

- Add：将 GameObject/Component 添加为 GameObject 的 Children。Target 被克隆
- AddRange
- AddFirst
- AddFirstRange
- AddBeforeSelf
- AddBeforeSelfRange
- AddAfterSelf
- AddAfterSelfRange
- Destroy：安全销毁 GameObject（检查 null）

MoveTo 方法与 Add 类似，但是不 clone target：

- MoveToLast：将 GameObject/Component 移动为这个 GameObject 最后一个 children
- MoveToLastRange
- MoveToFirst
- MoveToFirstRange
- MoveToBeforeSelf
- MoveToBeforeSelfRange
- MoveToAfterSelf
- MoveToAfterSelfRange

If target is RectTransform always use SetParent(parent, false) and ignores TransformCloneType。

## 扩展方法

IEnumerable\<GameObject\> 扩展。如果 source collection 有多个 GameObjects 有相同 GameObjects 结果，它们将会被包含多次。要避免重复包含，使用 LINQ 的 Distinct 方法。

- Ancestors：返回 source collection 中每个 GameObject 的 ancestors GameObject 集合
- AncestorsAndSelf
- Descendants：
- DescendantsAndSelf
- Children
- ChildrenAndSelf
- Destroy：安全销毁 source collection 的 GameObject
- OfComponent：返回 source collection 中指定 component 的集合

LINQ 方法有两个变体，一个是 GameObject 扩展方法，一个是 IEnumerable\<GameObject\> 扩展方法。应用在 GameObject 的扩展方法返回 IEnumerable\<GameObject\>，然后再它上面可以再次应用 LINQ 方法，类似 jQuery 返回的对象总是 element 的集合，所有 chain 方法应用到集合中的每个元素上。

## 性能提示

LINQ to GameObject 是高度优化的。遍历方法返回优化的 struct enumerator，它可以在迭代时避免 garbage。很多方法还提供了 NonAlloc 版本。

如果进行简单迭代或使用 ForEach/ToArrayNonAlloc，LINQ to GameObject 保证没有 gc allocate，并且性能非常快。

