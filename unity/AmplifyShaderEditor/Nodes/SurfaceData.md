# Surface Data

## Depth Fade

输出线性渐变，表示物体表面和它后面的geometry直接的距离。渐变的范围或fading距离可以通过调整Distance参数设置

更具体地说，这个参数创建了一个[0, 1]直接的值，当物体表面和它背后的geometry之间的距离在指定的值之间的时候

shader必须设置Render Queue为Transparent或者更高（Blend Mode设置为Transparent或Translucent），因此object不会写入Depth buffer。这是基本配置因为node内部通过将Surface Depth减去Depth buffer的值来计算距离

## Fresnel

输出菲涅尔效果的结果。菲涅尔效果定义当光线到底两种发射率和折射率不同的材质的交界处时如何进行反射和折射

这个节点主要处理反射部分，通过两种材质的反射率和折射率，计算菲涅尔反射系数。输出结果就是计算后的反射系数。将它乘以一个颜色就可以得到菲涅尔效果

节点的输入用来调整计算公式的各个参数

- Normal：用于计算的表面法向量。默认是表面的世界空间法向量。通过Normal Space指定Tangent还是World空间的法向量
- Bias/Scale/Power：可选公式参数

## Surface Depth Node

输出object surface到camera的距离，可以设置为[0, 1]之间的值，可以是View空间的真实值

通过变换每个vertex position到view空间然后返回z值，这样就不依赖于Depth buffer

## Template Fragment Data

这个节点可以访问在shader模板中声明的插值过的fragment数据。通过Data属性选择访问哪个数据。输出端口根据选择的数据的类型不同而不同

选择哪个SubShader/Pass/Data

## World Bitangent

逐像素计算世界空间中表示surface副切线的一个向量，考虑来object和tagent符号。副切线（副法线）向量是World Normal和World Tangent的叉乘积

## World Normal

逐像素计算世界空间中surface的法向量。这个数据对于光照计算非常重要。

这个节点还允许接收一个切线空间的法向量来偏移normal。最重用的用例是使用一个切线空间的normal map纹理来扰动objects空间的法向量

## World Position

逐像素计算表面像素在世界空间的位置。通常用于类似映射世界位置到surface uv 坐标的全局效果。使用这种技术的效果通常非常识别，因为绝大多数时间，它显示某种纹理晕眩效果，当物体移动时，纹理也随之移动，看起来纹理总是相对世界空间静止的。因此它通常用于静态物体效果

## World Reflection

输出世界空间中的camera视线在surface像素处基于normal的反射结果

基于逐像素法向量map的反射也可以通过将normal map连接到Normal来计算得到。如果没有map input，则使用surface的法向量，否则使用map中的法向量

## World Tangent

逐像素计算一个表示世界空间中的表面切线的向量。
