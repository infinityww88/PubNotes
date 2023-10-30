# RenderTexture

RenderTexture 是用于渲染的 textures，而不只是一个 texture，包括 color buffer，depth buffer，如果 depth buffer 的 depth 是 24 或 32，可以支持 stencil。

RenderTexture 可以用于实现 image based 的 rendering effects，动态阴影，projectors，反射，监视器等效果。

RenderTexture 在 CPU 侧只有描述，真正的缓冲区（color & buffer）都在 GPU 侧创建。因此它是一个 native object。

屏幕现存本身就是一个 RenderTexture，RenderTexture 允许在 GPU 中创建相同结构的更多缓冲区，每个都可以视为一个虚拟显示器。

一个典型应用是将 render texture 设置为 Camera 的 target texture（Camera.targetTexture），这使 camera 渲染到一个 texture 上，而不是屏幕。

Render texture 的内容在特定事件时可能丢失，例如加载一个新的 level，系统进入 screensaver 模式，进入和退出 fullscreen 等等。此时，现有 render textures 将再次变成 'not yet created'，这可以通过 IsCreated 函数检查。因为 Render Texture 的 buffer 都在 GPU 中创建，而显存是被很多程序共享的。当从当前程序切换到另一个程序时，显存就被那个程序使用了，这个程序的所有 render texture 都变的无效了，只有等到这个程序恢复到前台工作时，才会每个 RenderTexture 重新创建 GPU buffer。

Asset 或构造函数只是创建了 RenderTexture 的描述（参数），缓冲区在需要的时刻在 GPU 中创建。

就像其他 native engine object 类型，留意任何 render texture 的生命周期非常重要，在完成任务时使用 Release 函数释放它们，因为它们不会像通常的 managed 类型被垃圾回收。

一个 RenderTexture 只在 GPU 上有一个数据表示，你需要调用 Texture2D.ReadPixels 将它读取到 CPU 内存中。

新创建的 render texture 的初始内容是未定义的。

## 创建 RenderTexture

可以以资源的方式创建 RenderTexture asset，也可以在内存中通过构造函数创建 RenderTexture。构造 RenderTexture 需要指定 width，height，format，depth 等一组参数。

RenderTexture 对象只是一组描述，真正的缓冲区数据在 GPU 中创建。

## RenderTexture.active

当前 active render texture。所有的渲染（Camera 没有指定 Target Texture 的渲染）都到 active RenderTexture。如果 active RenderTexture 是 null，则渲染到 main window。

设置 RenderTexture.active 和调用 Graphics.SetRenderTarget 是一样的。通常你实现自定义 graphics effect 时查询或修改 active render texutre。如果你需要使 Camera 渲染到一个 texture 上，则使用 Camera.targetTexture。

When a RenderTexture becomes active its hardware rendering context is automatically created if it hasn't been created already.

## camera.targetTexture

通常 camera 直接渲染到屏幕上，但是对一些效果来说，将 camera 渲染到 texture 上非常有用。这通过创建一个 RenderTexture 对象，并将它设置为 camera 的 targetTexture 实现。Camera 将渲染到那个 texture 中。

如果 targetTexture 为 null，camera 渲染到屏幕上。

当渲染到一个 texture 时，camera 总是渲染全部 texture。rect 和 pixelRect 都将被忽略，它们只被应用到 screen 渲染中。

还可以通过 SetTargetBuffers 函数使 camera 同时渲染到多个单独的 RenderBuffers，或 textures 中。

## camera.activeTexture

Camera 的临时 RenderTexture target。当前被渲染的相机将它的 image 应用到临时 render target 上，它只在 OnPostRender 方法中可用，在这里进行 post processing。在这里不必关心渲染目标是 RenderTexture.active 还是 Camera.targetTexture，它总是 camera 当前渲染到的 render texture。

RenderTexture.active 和 camera.activeTexture 都是动态属性，在不同时刻被所渲染的 camera 动态设置。例如在一个脚本的 Start 中设置 RenderTexture.active 为一个 RenderTexture，在后续查询中仍然可能得到 null 的结果。 

另外 tex.ReadPixels 总是从 RenderTexture.active 读取内容，因此要将某个 RenderTexture 的内容从 GPU 中读取到内存中，需要先设置 RenderTexture.active 为要读取的 RenderTexture。这是一种全局传参的形式。

## RenderBuffer

RenderTexture 的 color 或 depth buffer 部分。

一个 RenderTexture 对象总是表示 color 和 depth buffers，但是很多复杂的算法需要使用相同的 depth buffer 和多个不同的 color buffer，或者相反。

这个类表示一个 RenderTexture 的 color buffer 或 depth buffer。

RenderTexture.colorBuffer, RenderTexture.depthBuffer, Graphics.activeColorBuffer, Graphics.activeDepthBuffer, Graphics.SetRenderTarget.

## Camera.SetTargetBuffers

- public void SetTargetBuffers(RenderBuffer colorBuffer, RenderBuffer depthBuffer);
- public void SetTargetBuffers(RenderBuffer[] colorBuffer, RenderBuffer depthBuffer);

设置 Camera 渲染到一个或多个 RenderTexture 的 buffers 中。

RenderTexture.active 是一个全局动态参数，一些 API 默认使用这个参数，而不再函数声明中指定。

使 Camera 渲染到一个 RenderTexture 中，只能也只需要设置 camera 的 targetTexture。在读取 RenderTexture 的内容时，先使 RenderTexture.active 指向目标 RenderTexture。

```C#
using UnityEngine;
using System.Collections;

// Get the contents of a RenderTexture into a Texture2D
public class ExampleClass : MonoBehaviour
{
    static public Texture2D GetRTPixels(RenderTexture rt)
    {
        // Remember currently active render texture
        RenderTexture currentActiveRT = RenderTexture.active;

        // Set the supplied RenderTexture as the active one
        RenderTexture.active = rt;

        // Create a new Texture2D and read the RenderTexture image into it
        Texture2D tex = new Texture2D(rt.width, rt.height);
        tex.ReadPixels(new Rect(0, 0, tex.width, tex.height), 0, 0);
        tex.Apply();

        // Restore previously active render texture
        RenderTexture.active = currentActiveRT;
        return tex;
    }
}
```

将 RenderTexture 想象为一个虚拟屏幕设备。当将一个 RenderTexture 指定为 Camera.targetTexture 时，可以等价想象为这个 camera 渲染到这个 RenderTexture 的屏幕上。因此 RenderTexture 的分辨率就变成了 "Screen" 的分辨率。例如假设 RenderTexture 的分辨率为 512x512，则渲染的图像等价于在一个 512x512 窗口的程序中渲染这个相机的内容。相机在 RenderTexture 宽高比的矩形中计算视椎体。

