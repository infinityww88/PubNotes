# 倾斜的视椎体

默认，view frustum 是沿着 camera 中心线对称的，但这不是必须的。你可以使 frustum oblique（倾斜），这意味着中心线的一侧比另一侧角度更小。

![ObliqueFrustum](../Image/ObliqueFrustum.png)

这使得 image 的一侧的透视 perspective 看起来更浓缩 condensed，给出观察者更靠近浓缩边缘可见物体的印象。一个用例是赛车游戏。如果 frustum 在 bottom edge 是平的，看起来 viewer 更靠近 road，更强调速度的感觉。

在内置的 Render Pipeline 中，一个使用倾斜视椎体的 camera 只能使用 Forward rendering path。如果 Camera 被设置为使用 Defered Shading rednering path，而你使视椎体倾斜，Unity 将强制 Camera 使用 Forward rendering path。

## Setting frustom obliqueness

尽管 Camera 组件没有设置倾斜视椎体的特殊功能，你可以通过开启 camera 的 Physical Camera 属性并应用一个 Lens Shift，或者通过添加脚本来调整 camera 的 projection matrix。

## Setting Frustum Obliqueness with a Lens Shift

开启 camera 的 Physical Camera 属性，以暴露 Lens Shift 选项。你可以使用这些属性以最小化 rendererd image 失真 distortion 的方式沿着 X 和 Y 轴偏移 camera 的 焦点 focal 中心。

偏移 镜头 lens 减少 shift 方向相对方向的 frustum 角度。例如，当你向下偏移镜头 lens，frustum 的 bottom 和 camera 中心线的角度变小。

![ObliqueFrustum_LensShift](../Image/ObliqueFrustum_LensShift.png)

## Setting frustum obliqueness using a script

下面的脚本显式如何通过修改 camera 的 projection matrix 快速达成一个倾斜视椎体。注意你只能在游戏运行在 Play mode 时才能看见脚本的效果。

```C#
using UnityEngine;
using System.Collections;

public class ExampleScript : MonoBehaviour {
    void SetObliqueness(float horizObl, float vertObl) {
        Matrix4x4 mat  = Camera.main.projectionMatrix;
        mat[0, 2] = horizObl;
        mat[1, 2] = vertObl;
        Camera.main.projectionMatrix = mat;
    }
}
```

不需要理解 projection matrix 是如何工作的以使用这个脚本。horizObl 和 vertObl 分别设置 horizontal 和 vertical obliqueness。0 表示没有 obliqueness。正数值向上向右偏移视椎体，因此使左侧和下侧变平，负值则相反。

当脚本被添加到 camera 上并且在游戏运行时将游戏切换到 scene view 时，可以直接看到效果：camera 视椎体的 wireframe 将会随着你在 inspector 中调整 horizObl 和 vertObl 属性而改变。1 或者 -1 表示一侧完全重合到 camera 中心线上。使用超出 [-1, 1] 范围的值尽管可能但是很少见。
