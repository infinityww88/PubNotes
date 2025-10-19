# Custom Deformer

- 创建一个CustomDeformer C#脚本
- 创建CurstomDeformer : Deformer类，放在Deform命名空间中
- 实现抽象方法和成员

    public override DataFlags DataFlags;

    public override JobHandle Process(MeshData data, JobHandle dependency = default);
- DataFlags属性用来确定deformer将修改那些数据，这可以让deformables明确将哪些数据复制到mesh中

    public override DataFlags DataFlags => DataFlags.Vertices;

    public override DataFlags DataFlags => DataFlags.Vertices | DataFlags.Normals;

- 在Process方法中调度deformer的工作。Deformable调用每个deformers的Process方法，并将它的MeshData作为data参数发送。你可以访问包含mesh不同元素的native数组。一旦一个deformable的deformers完成processing，deformable将复制任何修改的native mesh数据到原来的mesh中。创建并调度一个修改native数组的job。deformable会知道应用数组中的哪些修改，因为我们已经覆盖来DataFlags变量

- Deformer的Process方法，创建并调度一个job

    public override JobHandle Process(MeshData data, JobHandle dependency = default) {
        return new OffsetJob {
            vertices = data.DynamicNative.VertexBuffer;
        }.Schedule(data.Length, 64, dependency);
    }

- 定义真正执行deform的job

    private struct OffsetJob : IJobParallelFor {
        public NativeArray\<float3> vertices;
        public void Execute(int index) {
            //do deform
        }
    }

- Deformer的可调整参数在Defromer和Job中平行定义，在Deformer.Process创建Job时传递给Job。Deformer.DynamicNative.VertexBuffer包含要处理的vertices数据，也是在Process创建Job时传递给Job

- 在Deformer类定义头部使用Deformer Attribute定义Deformer的名字

- 在Job类定义头部使用BurstCompile Attribute

- 完成代码片段

```C#
    using UnityEngine;
    using Unity.Jobs;
    using Unity.Burst;
    using Unity.Collections;
    using Unity.Mathematics;

    namespace Deform
    {
        [Deformer (Name = "Offset", Type = typeof (OffsetDeformer))]
        public class OffsetDeformer : Deformer  
        {
            public Vector3 offset;

            public override DataFlags DataFlags => DataFlags.Vertices;

            public override JobHandle Process (MeshData data, JobHandle dependency = default)
            {
                return new OffsetJob
                {
                    offset = offset,
                    vertices = data.DynamicNative.VertexBuffer
                }.Schedule (data.Length, 64, dependency);
            }

            [BurstCompile]
            private struct OffsetJob : IJobParallelFor
            {
                public float3 offset;
                public NativeArray<float3> vertices;

                public void Execute (int index)
                {
                    vertices[index] += offset;
                }
            }
        }
    }
```

