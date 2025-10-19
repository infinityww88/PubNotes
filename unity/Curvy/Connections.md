# Connections

经常会希望逻辑上连接两个或多个CP。为铁路游戏创建连接点，在两个曲线之间定义传送点等等

## How it works

一个connection保存一个或多个cp的引用。每次一个控制点被移动或旋转时，它将它的transform同步到connection的transform上，因而同步到conneciton保存的所有cp的transform上

对connection中的每一个控制点，你定义它是否应该复制position/rotation的变化。这样你可以完全同步CP，因此逻辑上所有连接的cp

技术上Connections是带有CurvyConneciton组件的GameObject对象。它们被存储为Curvy Global Manager对象的子节点，并且使用Toolbar或相应的API被自动管理

如果一个CP是一个conneciton的一部分，connection的inspector将在CP的inspector中被展示以方便操作

## 创建

在Hierarchy中选择两个或多个CP GameObject，然后在SceneView点击“创建连接”按钮即可

## Follow-Up

一些Spline类型（Catmull-Rom和TCB）使用超过两个直接相邻的CP来定义曲线。如果你连接一个spline的end到另一个spline，你或许希望这个曲线看起来是无缝的seamless。要做到这一点，你可以定义曲线上应该在哪个连接的CP上继续进行计算。这被成为Follow-Up。将它想象成ending spline的自然扩展

例如：有两个Catmull-Rom splines，连接第一个spline的最后一个CP到第二个spline的第一个CP，并且设置两个CP完全同步。如果你移动coneciton，就会发现曲线break了。对于每个CP，定一个另一个CP作为Follow-Up，你就会看到连接的曲线看起来就像一条曲线一样，没有断开处。因为另一条曲线的控制点现在成为了segment计算的一部分

Follow-up只对Catmull-Rom和TCB曲线并且只有两个曲线末端连接在一起有效，connection平滑地连接两个曲线。除此以外，对于Linear、Bezier，或者连接曲线非末端CP，都不能平滑连接处，基本上就是简单地同步两个CP的transform而已

## CP选项

### ControlPoint

显示引用的CP名字，可以通过按钮选中CP或者移除CP

### Sync Position/Rotation

定义connection的transform是否应用到所有CP上

### Synchronization Presets

一些预制的Sync选项：不同步，仅位置，仅旋转，位置与旋转

### Follow Up

列出connection引用的属于开放spline的末端的CP

- Spline

    Follow-Up所定义的开放spline

- Control Point

    Follow-Up关心的spline的末端CP

- Follow Up

    作为Follow-Up的连接CP

- Heading Direction

    只在Follow-Up被定义时有效

    Follow-Up应该在哪个方向上继续

    - To spline's start：Follow-Up segment朝着spline的开始处继续
    - Nowhere：head to spline start
    - To spline's end：Follow-Up segment朝着spline的结束继续
    - Automatic：自动选择最佳选项，基于Follow-Up在曲线中的位置

### Conneciton选项

- Delete connection：删除此connection
