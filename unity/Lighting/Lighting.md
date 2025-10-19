# Lighting Window

## Scene

应用整体场景设置而不是单独的gameobject

### Environment

- Skybox Material：天空盒材质，出现在场景所有物体之后，模拟天空或者远距离背景
- Sun Source：当使用过程化天空盒时，指定一个带有directional light组件的gameobject来指示太阳的方向，或者任何远距离的平行光源
- Environment Lighting：环境光
  - Source：漫反射环境光diffuse environment light（又被称为背景光ambient light），呈现在场景的任何角落，并不来自任何具体的光源
    - Color：指定单色环境光，可以认为指定了一个单色的天空盒子
    - Gradient：分别指定天空、水平线、地面发射的环境光，并将它们平滑的融合在一起，可以认为Gradient指定了一个简单的天空盒，但是分别指定了天空盒的top（sky），bottom（ground）和周围（Equator）表面的颜色
      - Sky Color：指定从天空发射的环境光颜色
      - Equator Color：指定从场景侧面（水平周围，水平线方向）发生的环境光
      - Ground Color：指定从地面发射的环境光
    - Sky Box：直接使用天空盒的颜色作为环境光，决定从各个方向发射的背景光，比Color/Gradient更精确
    - Intensity Multipiler：设定漫反射环境光的亮度brightness，0~8，默认1
    - Ambient Mode: Realtime/Baked
- Environment Reflections：Reflection Probe和Global reflections全局设定
  - Source：反射源
    - Sky box：天空盒作为反射源
    - Custom：选择任何一个cube map作为反射源
  - Resolution：反射分辨率
  - Compression：反射贴图是否压缩
  - Intensity Multiplier：反射源在反射物体上的可见强度，模糊还是清晰，应该可用于模拟反射物体表面光滑程度
  - Bounces：多个反射物体之间反复反射的次数，想象两面面对面相对的镜子，如果设置为1，unity只计算初次反射（只计算天空盒或者cube map到反射物体的映射）

### Realtime Light

- Realtime Global Illumination：Unity实时计算计算并且更新全局光，Realtime Global Illumination

### Mixed Lighting

- Baked Glboal Illumination
- Lighting Mode
  - ShadowMask
  - Subtractive
  - Baked Indirect

### Lightmapping Settings

- Lightmapper
  - Enlighten
  - Progressive CPU
    - Prioritize View
    - Multiple Importance Sampling
    - Direct Samples
    - Indirect Samples
    - Environment Samples
    - Bounces
    - Filtering
      - Auto
      - None
      - Adanced
  - Progressive GPU(Preview)
- Indirect Resolution
- Lightmap Resolution
- LightMap Padding
- Lightmap Size
- Compress Lightmaps
- Ambient Occlusion
- Directional Mode: Yes/No
- Indrect Intensity
- Albedo Boost
- Lightmap Parameters
  - Default-Medium
  - Default-HighResolution
  - Default-LowResolution
  - Default-VeryLowResolution
  - Create New

### Other Setting

- Fog
  - Color
  - Mode
    - Linear
    - Exponential
    - Exponential Squared
  - Density
- Halo Texture
- Halo Strength
- Flare Fade Speed
- Flare Strength
- Spot Cookie

### Debug Setting

- Light Probe Visualization
  - Only Probes Used By Selection
  - All Probes No Cells
  - All Probes With Cells
  - None
  - Display Weights
  - Display Occlusion

### Genrate

- Auto Genrate
- Generate Lighting
  - Bake Reflection Probes
  - Clear Baked Data

## Global maps

GL lighting process产生的所有光照贴图lightmap

## Object maps

预览当前选择的gameobject的GL lightmap texture

## Light souces

- point light
  - 平方反比律
  - 模拟局部光源，火花或爆炸照亮周围场景
- spot light
  - 类似point light，但是限制在一个特定角度的光锥中
  - 模拟人造光源，手电筒、车灯、搜查灯、舞台灯
- directional light
  - 远距离来自场景之外的平行光，太阳、月亮
  - 没有位置，只有方向
  - 不衰减
  - Unity5之后，默认场景中的directional light连接到过程化天空盒的平行光物体，选择directional light将引起天空盒更新“太阳”的位置，如果天空盒被选择为环境光源，环境光将随着directional light和其角度而相应改变
- area lights
  - rectangle in space
  - 从rectangle的forward一侧，光源向所有方向一致发射光线，就像点光源一样，光线强度同样遵循平方反比律
  - only for baked lightmap
  - area lights有时会使baked的lightmap出现黑色方块，出现情形时area rectangle垂直ground plane并且和ground plane相交，怀疑是因为有光线和plane平行（夹角为0）导致的一些瑕疵，将area rect脱离地面使其光线不与plane平行，或者倾斜（即使略微倾斜）area rect使其不予plane垂直，不再出现瑕疵
  - Baked GI只对场景中的静态物体，Bake时注意是否已将场景中的物体设置为static
- Emissive materials
  - 类似area light，自发光材质从物体表面发射光线，它们可提供包含可在游戏运行时调整的诸如color、强度等属性的反弹光线。area light不支持precomputed realtime GI，自发光材质则可以，并且可提供相似的柔光效果，area light应该是遗留功能，因为使用一个自发光的plane就可以失去它的功能，而且更加强大
  - 自发光材质若要加入到GI bake过程中，需要设置gameobject为lightmap static，此外自发光材质shader的emission模块本身还包含一个Global Illumination，似乎应用于Lightmapper为Progressive（CPU/GPU）的情景。此外shader的Advanced Options模块还包含一个Double Sided Global Illumination选项，可以使材质向面片两个方向都发射光线，而不只是法向量一侧
  - Shader中的Emission属性允许场景中的static物体发射光线，光线只能被标记为lightmap static的物体接收。如果需要动态物体接收从自发光物体发射的光线，必须使用Light Probes
- Lightmap UV，所有lightmap static的模型必须先生成lightmap uv，lightmap uv不同于模型uv之处在于lightmap uv不能重叠，而模型uv是可以重叠，模型因为有许多面是重复对称的，建模时系统或手工经常将它们的uv坐标重叠在一起，这样纹理只需要绘制一次就可以了，但是对于light bake，即使相同的模型网格接受的光照也是不同的，因此lightmap uv必须不重叠，顶点数据包括一组uv channel，第一个channel就是模型uv坐标，通常使用第二个channel（UV2 channel）存储lightmap uv，它和模型uv一样都是顶点数据。如果在创建模型时生成了lightmap uv，它就存在于模型数据中；对于没有生成lightmap uv的模型，unity在import它的时候可以自动生成，基本上就是把重叠的uv triangle分离，然后将lightmap uv保存在模型顶点数据中
- Environment Light应该不需要bake到lightmap中，Environment Light是背景光，只需要运行时渲染到所有材质表面即可，Light Bake主要是得到那些明确光源（light gameobject）发出的光线在scene中bounced的结果。Ambient Light可以用于整体增加场景亮度而不用调整单独的光源
- Light Bake非常的精巧，经常出现各种奇异的问题，注意检查以下地方
  - 是否正确生成了lightmap uv
  - 是否设置了lightmap static
  - 如果在物体表面生成了奇怪的纹理，尝试调整物体和光线的角度，物体之间的距离（Bake AO时）
- Ambient Light设置为baked时，可以Bake进Lightmap
- Disable Realtime Global Illumination时，Ambient Light总是baked的；Enable Realtime Global Illumination时Ambient Light可以时realtime或者baked的，如果时baked的ambient参与GI bake
- 无论Realtime Global Illumination如何设置，当Ambient Light是baked时，调整Intensity Multiplier环境光只能影响非静态物体；当Ambient Light是realtime时，则环境光同时影响静态物体和动态物体
- 不必建模时生成Lightmap UV（UV2 channel），可以使用Unity自动生成Lightmap UV的功能，除非Lightmap UV有特殊需求只能手工创建
