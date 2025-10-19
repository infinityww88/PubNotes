# 透明效果

- Unity中通常使用两种方法实现半透明效果
  - alpha test：无法得到真正的半透明效果
  - alpha blending
- 渲染顺序
  - 对于不透明的物体（opaque），由于深度缓冲测试（depth-buffer/z-buffer），不考虑渲染顺序也能得到正确的排序结果
  - 对于半透明物体
    - alpha test: 只要一个fragment的透明度小于一个阈值，那么片元就会被舍弃，被舍弃的片元不会再进行任何处理。否则就按照普通的不透明物体的处理方式来处理它
      - 不能称为半透明，只能称为部分透明
      - 不需要关闭深度写入
      - 和其他不透明物体相比最大的不同就是它会根据透明度来舍弃一些片元，其他方面没有任何差别
      - 片元要么完全透明，要么完全不透明
    - alpha blending
      - 使用当前fragment的alpha作为混合因子，与已经存储在颜色缓冲中的颜色值进行混合，得到新的颜色
      - 需要关闭深度缓冲，但不关闭深度测试，即对于alpha blending，z-buffer是只读的
  - 即使都是半透明物体，渲染顺序依然重要
    - 两个半透明的物体渲染顺序不同会导致不同的混合结果
  - 因此，渲染引擎一般都会对物体进行排序再渲染
    1. 先渲染所有不透明的物体，并开启它们的深度测试和深度写入
    2. 把半透明物体按照它们距离摄像机的远近进行排序，然后按照由远及近的顺序渲染这些半透明物体，并开启深度测试，但关闭深度写入
    3. 就像只使用距离摄像机远近排序来解决不透明物体遮挡问题一样，无法正确得到半透明物体fragment级别上的遮挡关系。但是已经没有其他z-buffer来解决半透明物体每个fragment的遮挡关系了。大多数引擎都采用了这个方法，通过应用层手段尽可能减少错误的出现
- Render Queue
  - Unity使用Render Queue解决渲染顺序问题
  - SubShader的Queue标签决定使用这个shader的模型将归于哪个渲染队列
  - Unity内部使用一系列整数索引来表示每个渲染队列，而且索引号越小表示越早被渲染
  - Unity预定义了一些渲染队列，但是再其中间可以使用其他队列
    - Background（1000）：这个渲染队列会再任何其他队列之前渲染，用于渲染那些需要绘制在背景上的物体
    - Geometry（2000）：默认的渲染队列，大多数物体都是用这个队列，不透明物体使用这个队列
    - AlphaTest（2450）：alpha test的物体使用这个队列，其实它们可以放入Geometry队列，但是在所有不透明物体渲染之后再渲染它们会更高效
    - Transparent（3000）：这个队列中的物体会在所有Geometry和AlphaTest物体渲染后，按照由远及近的顺序渲染。任何使用了alpha blending的物体都应该使用这个队列
    - Overlay（4000）：该队列用于实现一些叠加效果。任何需要在最后渲染的物体都应该使用这个队列
- Replacement Shader
  - 使用指定的Replaced Shader替换场景中具有指定tag的所有shader，用于实现一些特殊效果
  - It works like this: the camera renders the scene as it normally would. the objects still use their materials, but the actual shader that ends up being used is changed:
  - Since the camera determines what objects end up shown on screen, the functionality for setting up replacement shaders are in the camera class as well
  - Shader replacement is done from scripting using Camera.RenderWithShader or Camera.SetReplacementShader
    - Take in a shader as parameter which will be the final applied shader for replacement
    - The replacementTag is sort of like a filter that applies the replacement only objects which have a sub-shader that has a similar tag
      - if replacementTag is not empty, only object with sub-shader included that tag is rendererd, others will not.
      - if replacementTag is "", the shader will be applied to all the objects in the scene
  - RenderType tag is just Unity predefined shader tag, which can be used in shader replacement, the effect of RenderType is determined by how any shader system use them, Unity predefine RenderType is consumed by various sub-systems and have special effect.
  - In conclusion, tag is just tag, how they affect the final result is determined by system that use them.
  - All builtin-in UnityShaders have a "RenderType" tag set, that can be used when rendering with replaced shaders
  - You can set RenderType to anything that suit you need
