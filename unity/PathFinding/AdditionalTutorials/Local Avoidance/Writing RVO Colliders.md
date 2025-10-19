# Writing RVO Colliders

编写 custom local avoidance obstacles。

RVOSimulator class 只是 Pathfinding.RVO.Simulator 类的一个包装类。你可以这样获得一个对它的引用：

```C#
Pathfinding.RVO.Simulator sim = (FindObjectOfType(typeof(RVOSimulator)) as RVOSimulator).GetSimulator (); 
```

这个 Simulator 有一些方法可以添加和移除 obstacles。

一个 obstacle 可以通过传递一个 object outline 的 Vector3 数组（XZ 平面 outline），和一个指示它的高度的参数来添加。

![rvo_outline](../../../Image/rvo_outline.png)

这个图显示了一个 box obstacle 的 outline。

比如说，我们想添加一个很小的 square obstacle 到 world origin 上：

```C#
using UnityEngine;
using System.Collections;

public class SimpleRVOObstacle : MonoBehaviour {

    void Start () {
        //Get the simulator for this scene
        Pathfinding.RVO.Simulator sim = (FindObjectOfType(typeof(RVOSimulator)) as RVOSimulator).GetSimulator ();
        
        //Define the vertices of our obstacle
        Vector3[] verts = new Vector3[] {new Vector3(1,0,-1), new Vector3(1,0,1), new Vector3 (-1,0,1), new Vector3 (-1,0,-1)};
        
        //Add our obstacle to the simulation, we set the height to 2 units
        sim.AddObstacle (verts, 2);
    }
}
```

Code 非常简单明了，如果将它添加到 scene 中的任何一个 GameObject 上，就会发现没有 agents 可以穿越 world origin，因为它们被这个添加的 obstacle 阻塞了。

注意：outline vertices 的顺序很重要，顺时针 polygons 将会导致 agents 可以自由地移动到其中，但是被锁定在里面了，而逆时针 polygons 则会保持 agents 在 polygons 外面，但是如果处于某些原因，一些 agents 一开始就在 obstacle 里面，它们可以很轻易地移动出来，但是无法在进入了。

可以通过 System.Array.Reverse(verts) 翻转 polygons 的顶点顺序。

还可以按照独立的 edges 来添加 obstacles：

```C#
sim.AddObstacle(firstPoint, secondPoint, height);
```

这将被视为一个 convex polygons，因此 agents 将不能从任何方向穿越它们。

为了使你更容易，以及有一些内置的 “colliders”。你可以在 Components > Local Avoidance 下面发现它们，它们和上面一样，简单地想 simulator 添加一些预制形状的 obstacles。要简化自定义 colliders 的创建，可以查看 RVOObstacle 类。
