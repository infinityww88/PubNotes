# Tips

I've read many times that triangles should be avoided in meshes, too give one reference: "Introducing Character Animation with Blender by Tony Mullen" says that equilateral triangles work fine as long you don't deform them. It seems to be common in game development that the models are triangulated.

- What issues are introduced by using triangles?
- Does the same apply for n-gons?

Rather than thinking of limitations with using triangles (I think this is an over simplification of the topic), you need to understand common workflows that take advantage of quad-dominant meshes.

- adding and removing edge loops (to increase or remove detail)
- using loops to better define features of the mesh (such as facial features, around eyes etc).
- operations on faceloops and edge-loops that speed up selection loop selecting, loop sliding for example.
- operations on grids. ripping & grid-fill for example.
- better deformation with shape keys (a lot could be written on this, read up on mesh topology, facial shapes, deformation).
- better subsurface results (edge loops along important features of the form allow your to use creases too).

However in a specific situation you may find it's not a problem to have a 100% triangle mesh so don't be single minded about this.

Instead of defining triangle meshes as bad, try to learn to use these tools and you'll better understand why in most cases, triangle heavy meshes are not ideal for character animation.

Blender中存在大量基于一个或几个少量元素（object、vertices、mouse cursor）按权重transform一组vertices的工具。例如比例编辑工具，lattice，mesh deform，hook等等。它们都是Blender内部自动将被操作的vertices绑定到少数元素，自动计算分配权重而已。然后每当作为anchor（target）的元素transform时，按照权重将transform施加给其影响的vertices。蒙皮骨骼只是这种众多工具中的一种，通过bone影响mesh的vertices。唯一的区别是，除了Blender自动计算vertices影响权重之外，还可以手动绘制调整权重。

Blender Texture可以直接创建程序化纹理，在New Texture的类型中选择相应的类型就可以。程序化纹理可以用在各种使用texture的modifier上，对mesh进行deform。

start with something that can work with

建模不是按照计划设计好的过程，而是随机应变的过程

从Blender内置的Cube开始工作，使用不适合的基础完成最终目标需要涉及大量的技巧，反而有助于提高建模的能力

战略计划只是一个可以开始工作的基础，几乎不可能是最终的过程，最终的胜利都是要随机应变，从既有事实向着最终目标发展的结果

模仿是最简单的，尽可能将工作导向模仿方向

总是现在草纸上绘制（GIMP、Inkscape）、或者在网上下载模型的XYZ三个侧面的投影图，然后基于每个侧面进行建模。绝不要空想建模，这将模型设计和模型构建的复杂度混合在一起了。而先建立草图再作为参考建模则将复杂度分离

任何作品都是要先设计在实现的，这是非常关键而又经常被忽视的。对于创建新的模型，就需要先绘制原画、概念图，然后在以其作为参考创建模型，但这需要深厚的绘画功底。通常我们只会构建现有世界物体的3D模型，此时Blender只是构建模型的工具，而不是设计工具，这时也需要有类似“原画”、“概念图”之类的参考图，但是这些参考图非常容易在网上搜索到，如果有现实的物体，使用手机也非常容易拍摄各个角度的图像

除非使用Blender做设计创建新的事物，否则Blender只是构建工具，而不是设计工具。没有参考图的情况下直接使用blender创建模型就是把设计和构建的复杂度混合在一起。使用参考图的话，就可以专心地想怎么构建，而不是构建什么。

也可以使用Blender做设计，创建一些最基础的kitbash模型，然后任意拼装组合它们设计新的模型

做任何事情都要先了解它的详细的过程流程，知道怎么做才能去做，否则就只能通过四处碰壁把前人的走过的弯路重新走一遍，而这就是经验教训的力量，让你不必重新陷入那些曲折就可以获得知识。

任何作品的丰富程度完全在于细节。细节越多越丰富。模型也是一样。即使LowPoly模型也不能面数过少，同时也不是以尽可能少的poly为目标。如果LowPoly模型看起来过于简陋，就需要创建更多的面数添加细节了。对于纹理贴图也是一样的

对于编程，优美的设计是几个核心原理以各种形式的应用，例如抽象、中心化、去重复、模块化、自底向上、高聚合低耦合等，所谓的各种设计模式只是这几个基本原理primitive principle的各种表现而已。建模也是如此。当前已知的核心原理就是分解与组合。仔细观察参考图，将模型自然分解为肉眼可见的直观的组件，只要将这些组件构建完成，模型就可以通过它们组合出来。如果一个组件不够简单，就递归地继续分解，知道每个组件都足够简单。

分解组合是通用的原理，基于object的分解和组合只是基本的应用形式。使用一个mesh创建整个模型（或复制组件）也可以应用这个原则。通过extrude或者subdivide，以及基本元素操作，先构建模型的轮廓，将每个部分通过edge loop分割开来，这样每个组件都局限在自己的区域，但是它们又通过edge loop连接在一起。然后每个组件就可以在自己的local area进行建模，而每个组件又可以递归地应用这种分割技术。这样虽然模型是在一个mesh被构建的，但是仍然使用的是分解和组合的原理。

基于Object的分解组合也是一种非常尤其有趣的艺术风格，而且还有一个巨大的优势就是允许进行组件替换和动画，这对于游戏性来说非常重要

基本元素操作（vertex/edge/face）和高级地程序化工具（tools、modifiers）同样重要，二者交替应用就可以创建各种mesh

建模务必有参考，这是基本必要条件，即使自由设计也要先在草纸上绘制出原型图像，如果使用网络图片/视频就更简单了。对于lowpoly/卡通风格模型，参考图只作为参考，分辨物体的主要特征即可，不必须沿着按照参考图建模
