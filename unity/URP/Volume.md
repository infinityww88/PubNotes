# URP Post Processing

URP 后期处理不需要原来的 Post Processing（包括 v2）package，URP 管线自带后期处理。

为 URP 添加后期处理，需要创建 VolumeProfile asset。在其上面为每种后期处理效果添加 override。添加了 override 的后期处理才会生效。

然后将 VolumeProfile 应用到 URP 管线中，有两种方式使用 VolumeProfile：

- 在 Universal Render Pipeline Asset 的 Volumes 中添加一个 VolumeProfile，这会成为默认的 Post Processing
- 在 Scene 中为 GameObject 添加 Volume 组件，为 Volume 组件添加 VolumeProfile

引用了 VolumeProfile 的地方，都 inline 显示 Post Processing override 模块，无论是在 URP Asset，Volume Component，还是在 VolumeProfile asset 自身上，在 Inspector 中查看的 VolumeProfile 都引用的是磁盘上的 asset，改变任何 override，都同步到 asset 上。

Volume 组件有两种使用方式：

- Local：使用 GameObject 上的 Collider 定义一个区域，当 Camera 进入到区域中会应用 VolumeProfile 定义的后期处理效果。
- Global：全局后期处理，不需要 Collider，直接生效。

无论是 URP asset 上的还是 Volume component 上的 VolumeProfile，效果是叠加在一起的。

Volume 有两个属性：

- Weight：定义后期效果应用的权重，0 完全没效果，1 完全效果
- Priority：当多个 Volume 有相同的影响程度时，定义哪个 Volume 被使用。更高优先级的 Volume 将被使用

Camera 需要启用 Post Processing 选项，才能启用后期处理。

可以为每个 Camera 定义后期处理效果。

在脚本中控制后期处理，包含这两个 namespace：

```C#
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal; // 各种效果 例如Bloom，在这里
```

获取指定后期效果的 override：


```C#
		
if (volume.profile.TryGet(out var bloom)) {
    bloom.threshold.Override(0.5f);
    // bloom.threshold.value = 0.5f;
}
```

每种效果是 VolumeComponent 的子类，例如 Bloom。通过 VolumeComponent 改变效果各个属性有两种方法：

- bloom.threshold.Override(0.5f);
- bloom.threshold.value = 0.5f;

注意不可以直接为属性（threshold）赋值，例如

```C#
bloom.threshold = new MinFloatPatameter(...);
```

控制后期效果应用强度有两种方式：

- 直接修改 VolumeProfile override
- 为每种效果定义一个 VolumeProfile asset，并在一个 Volume 中引用它，然后不修改 VolumeProfile，而是调整 Volume 的 weight。

  ```C#
  volume.weight = 0.5f
  ```

后期效果是叠加的，尤其要注意 renderpipeline 中的默认 profile。

