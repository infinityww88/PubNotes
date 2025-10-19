# Optimizing graphics performance

良好的性能是很多游戏成功的关键

## Locate High graphics impact

CPU vs GPU

### 常见瓶颈

GPU经常受限于fillrate或内存带宽，如果更低的display resolution使游戏运行地更快，则可能受限于GPU的fillrate

CPU经常受限于需要渲染的batches（drawcall数量）

### 不常见瓶颈

GPU有太多vertices要处理。mobile上不要超过10w个vertices

CPU有太多vertices要处理。可能是skinned meshes，cloth模拟，粒子系统，或者其他gameobjects和meshes

使用Unity Profiler定位瓶颈

## CPU优化

CPU对gameobject的渲染是逐物体的，对每个物体都要决定应用哪些光照，设置shader和shader参数（material），发送绘制命令到graphics driver。因此1000个三角形在一个mesh中比每个三角形在一个mesh中要快1000倍

所有系统（无论是linux应用程序还是Unity应用程序或渲染管线）最快的运行方式都是不切换上下文，每个组件都工作在最高效率下

合并object，手动或者draw call batching
使用尽可能少的material，将单独的texture放在更大的texture atlas上
尽可能少地使用导致一个object绘制多次的功能（反射，阴影，逐像素光照）

只用共享material的meshes才能合并减少drawcall。通常导致不能共享material的情况是texture不同。因此要优化CPU性能，要保证合并的objects共享相同的textures

### 使用OnDemandRendering优化CPU

OnDemandRendering类控制和查询独立于其他所有子系统（物理、输入、动画）渲染速度的信息

下面是一些可能希望更少帧率的场景：

- 菜单场景（例如应用程序入口或者暂停菜单）：菜单通常是非常简单的场景，不需要full speed的渲染。因此可以以很低的帧率渲染菜单，减少电量消耗，放置设备温度上升到需要限制CPU频率的阈值
- 回合制游戏（turn based games）
- 绝大多数时间是静态场景的应用程序：例如Automotive UI

Adaptive Performance Package(TODO)

即使渲染可能不需要那么频繁，但是应用程序仍然按照正常频率向脚本发送events。要放置input延迟，可以设置OnDemandRendering.renderFrameInterval=1，来使input能被迅速响应

- effectiveRenderFrameRate（TODO）
- renderFrameInterval
- willCurrentFrameRender

## GPU：优化模型

图形硬件需要处理的顶点数通常不和3D application报告的相同。3D application只报告构成model的不同corner的顶点数。但是图形硬件通常需要将一些几何顶点分离成两个或更多逻辑顶点以便渲染。如果一个vertex具有多个normals，UV坐标或者vertex color就必须分离

因此不使用不必要的三角形
尽量少的使用UV mapping seams和hard edges，前者使vertex具有不同的uv，后者使vertex具有不同的normal

## 光照性能

使用bake static lighting烘焙光照贴图

使用一些欺骗技巧，例如在shader中直接计算光圈效果而不是使用真实光源产生光圈

Lights in forward rendering（TODO）

## GPU：Texture压缩和mipmaps

使用压缩纹理可以加速load times，占用更少的内存使用，大大提升渲染性能（在GPU中解压）

### Texture mipmaps

在3D scene中，对texture总是使用Generate mipmaps。mipmaps使GPU对更小的三角形产生一个更低分辨率的texture

mipmap使一组progressively smaller版本的图像。当texture使用mipmap时，Unity在mesh远离camera时自动使用更小的texture版本。这减少了渲染纹理的性能消耗，而不产生明显的细节丢失。mipmap需要更多的内存使用，因此只对那些距离camera会变化的texture使用mipmap

在Import texture使勾选Generate Mipmap，Unity就自动产生mipmap

## LOD和per-layer cull distances

Culling objects使物体不可见。使过小的物体在很远的距离上不可见（例如小石头，小装饰）

达成此效果的方法：

- LOD
- 手动设置per-layer剔除距离
- 将很小的objects放到一个单独的layer，使用Camera.layerCullDistances脚本函数设置per-layer剔除距离

## 实时阴影（TODO）

## GPU：编写高性能shader的tips（TODO）

## Simple checklist to make your game faster

- 保持vertex数量尽可能低而不损失质量
- 尽可能使用Mobile或Unlit类别的shader
- 使每个场景使用material尽可能少，尽可能共享material
- 对静止物体使用static标记，使得可以内部优化，例如static batching
- 只是用一个pixel light影响geometry（特别是方向光），其他光源使用vertex light
- 烘焙光照而不是使用动态光照
- 如果可能使用压缩纹理，使用16-bit纹理而不是32-bit纹理
- 如果可能，避免使用fog
- 对复杂静态场景，使用Occlusion Culling减少可见geometry和drawcall。Occlusion culling bake
- 使用天空盒表现很远的geometry
- 使用pixel shaders或者纹理混合来混合多个纹理而不是通过多个pass
- 如果可能使用half精度
- 尽量在pixel shader中少用复制的数学运算
- 每个fragment使用更少的纹理

## Draw call batching

要绘制一个gameobject到屏幕上，engine必须发起一个drawcall到图像api（OpenGL或者D3D）。DrawCall经常是资源密集型的，图像API对每个drawcall做了大量工作，引起CPU方面的性能消耗。这几乎总是由于两个draw call的状态切换引起的（切换material），它将导致图形驱动的资源密集的校验和传输步骤

Unity使用Dynamic batching和Static batching来减缓这种问题。

Dynamic batching：将一组小的mesh合并到一起发送给图形驱动，需要消耗cpu
Static batching：合并静态mesh到一起发送给图形驱动，需要消耗内存

只有使用相同material的gameobjects才能batch到一起

尽可能多的共享material

如果又两个不同的material，但是只有texture不同，则可以将textures合并到一个单一的大纹理中。这个过程成为Texture atlasing。一旦纹理都在一个图集中，则可以使用一个material

Renderer.material写时复制，Renderer.sharedMaterial共享修改

## Occlusion culling

阻塞剔除是一个过程，阻止Unity对被其他GameObject完全遮挡对GameObjects执行renderer计算

同时节省CPU和GPU的时间，但是需要在CPU上执行剔除计算，因此几乎只节省了GPU的时间

在运行时加载阻塞剔除数据到内存中，因此确保又足够的内存

静态物体可以剔除动态物体，但是动态物体不能剔除静态物体

当烘焙oclusion culling data时，Unity将scene分割为小的cell，生成以cell描述的geometry数据（体素化），以及相邻cell的可见性。在运行时Unity加载backed data到内存中，对每个开启Occlusion Culling property的相机，它查询这些data来确定相机能看到哪些cell，然后只有占用了这些可见cell的gameobject才被渲染

设置Occlusion Static标记，执行烘焙
