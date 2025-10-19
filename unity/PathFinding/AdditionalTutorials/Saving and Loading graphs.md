# Saving and Loading Graphs

如何预计算 graphs 和存储那些数据。

所有 graphs 可以被保存到文件以及从文件中加载。这实际上是 editor 一直做的事情，几乎不使用任何 Unity 序列化，相反地，所有 graph 设置被序列化和存储在一个 byte array。然而，不仅 setting 可以被保存，一旦计算完成，graph 能够保存所有 nodes 到一个紧凑的 byte array 表示，然后 byte array 可以被保存到文件，并从文件加载。

在 A* inspector 中，在 Save & Load tab 下面，有两个 buttons 名为 ”Save to file“ 和 ”Load from file“，它们可以被用来保存和加载 graph files。

## Caching Graph Calculation

通常在开始时计算 graphs 是你想要的，但是有时，尤其是如果你使用 RecastGraph 或为移动平台开发，开始时计算 graphs 的延迟非常令人烦恼。还有可能有其他原因使你不能在开始时计算 graph。

在那些情况下，graph caching 非常有用。它允许你在 editor 中 scan graph，并保持它到一个外部文件，这个文件将会在开始时被加载。绝大多数情况下，它比实时 scan graph 快得多，并且你明确知道 graph 是什么样的。

要创建一个 cache，在 A* inspector 中打开 ”Save & Load“ tab 并点击 Generate Cache。它还会询问你在保存之前 rescan graph。现在你保存的 graph 将会在 startup 时被加载所有完整的 node info，没有必需的计算时间。

![saveloadtab](../../Image/saveloadtab.png)

## Saving Graphs to File and Loading them

你可能还想保存 graphs 到文件，你可以稍后手动加载。例如，你甚至可以在运行时从 server 加载它。

如果你想要保存 graphs，打开 ”Save & Load“ tab，然后点击 ”Save to file“ 按钮。你可以只包含 settings，或者同时包含 settings 和 node data。如果你只包含 setting，则 graph 被加载之后，你需要在任何角色使用它进行导航之前 recalculate graph。你可以使用下面的方法重新计算所有 graphs：

```C#
AstarPath.active.Scan();
```
当你想要重新加载 graphs，简单地按下 ”Load from file“ 按钮，然后定位保存的文件。注意，这将会替换你的当前 graphs。

### Loading and Saving using Code

如果你想要在运行时 load 或 save graphs，明显地，你不能使用 editor 界面。

使用 API 来保存和加载 file。

这将会序列化 graph settings 到一个 byte 数组中。默认地，node info 是被包含的（假设 graphs 已经扫描了）。

```C#
byte[] bytes = AstarPath.active.data.SerializeGraphs();
```

如果你想要更多控制，你可以添加一些设置

```C#
var settings = new Pathfinding.Serialization.SerializeSettings();

// Only save settings
settings.nodes = false;
byte[] bytes = AstarPath.active.data.SerializeGraphs(settings);
```

要加载保存的数据，可以调用：

```C#
AstarPath.active.data.DeserializeGraphs(bytes);
```

如果你只加载 setting，你可能想在加载 settings 之后调用 Scan（来重新计算 graph）：

```C#
AstarPath.active.data.DeserializeGraphs(bytes);
AstarPath.active.Scan();
```

### Additive Loading

相比于替换当前加载的 graphs，你可以增量加载 graphs：

```C#
AstarPath.active.data.DeserializeGraphsAdditive(bytes);
```

你可以卸载 graph：

```C#
var data = AstarPath.active.data;
var myGraph = data.gridGraph;
data.RemoveGraph(myGraph);
```

### Including Data in a TextAsset

Graph 数据可以被包含到 textassets，以更容易地包含到 build 中。当你已经保存数据到文件中，重命名那个文件为诸如 myGraph.bytes 之类的，并把它放到你的 Unity Project。这回告诉 Unity 将它处理为二进制信息。使用诸如 .txt 扩展名将会损坏数据，因为 Unity 将会尝试将它读取为 text。然后你可以从一个 text asset 加载 graph，通过引用它到一个变量，并访问它的 .bytes 字段。

```C#
using UnityEngine;
using System.Collections;
using Pathfinding;

public class TestLoader : MonoBehaviour {
    public TextAsset graphData;

    // Load the graph when the game starts
    void Start () {
        AstarPath.active.data.DeserializeGraphs(graphData.bytes);
    }
}
```

## Internal Data Structure

所有 settings 被序列化为 JSON。这是一个保持向前向后兼容非常好的方式。它被压缩为 .zip 文件以减少文件大小。

![serializedInternal](../../Image/serializedInternal.png)

Note

    Many of the files mentioned below are not always included in the zip. If it is determined that a file would not contain any relevant information (such as saving user created connections, but no connections have been created), it is left out.

## Meta

一个 meta.json 文件在所有序列化中出现。这个文件包含不连接到特定 graph 或者加载其他 graph 需要的信息。

Meta 文件包含：

- 系统的版本号
- 保存的 graph 的数量
- 每个 graph 一个 GUID value，来标识它们
- 每个 graph 的类型

下面是一个 meta.json 文件的例子：

```json
{
    "version": "3.0.9.5",
    
    "graphs": 1,
    
    "guids": 
        [
            "0d83c93fc4928934-8362a8662ec4fb9d"
        ],
    
    "typeNames": 
        [
            "Pathfinding.GridGraph"
        ]
}
```

## Graph Settings

每个 graph 的 settings 被保存为 ”graph#.json”，# 表示 graph 号码。这是一个序列化 grid graph setting 的例子：

```json
{
   "aspectRatio":1,
   "rotation":{
      "x":0,
      "y":0,
      "z":0
   },
   "center":{
      "x":0,
      "y":-0.1,
      "z":0
   },
   "unclampedSize":{
      "x":100,
      "y":100
   },
   "nodeSize":1,
   "maxClimb":0.4,
   "maxClimbAxis":1,
   "maxSlope":90,
   "erodeIterations":0,
   "autoLinkGrids":false,
   "autoLinkDistLimit":10,
   "neighbours":"Eight",
   "cutCorners":true,
   "penaltyPositionOffset":0,
   "penaltyPosition":false,
   "penaltyPositionFactor":1,
   "penaltyAngle":false,
   "penaltyAngleFactor":100,
   "open":true,
   "infoScreenOpen":false
   //...
}
```

Node 信息（如果包含在序列化数据中）作为 JSON 保存将会占据非常大的空间，相反它被写为二进制数据。每个 graph 类型对序列化的 node 数据有自己的编码。这是被每个 graph 的 SerializeExtraInfo 以及 DeserializeExtraInfo 方法处理的。

### User Created Connections

NodeLink2 组件也被序列化，当其发生时，它为那个组件存储一个 ID，然后当这个 graph 被反序列化，它会尝试找到相应的组件。这对于静态 maps 工作得很好，但是对于运行时动态创建的 objects，并没有任何好的方法保持对不同 objects 的追踪，因此不把 link 包含到保存的数据中可能更好（确保它们是 disabled 的），然后在 graphs 被加载后，enable 它们。

