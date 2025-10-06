使用 blending properties 来指定 Cinemachine Brain 组件如何在 CinemachineCamera 之间执行混合过渡。

Cinemachine 混合并不是淡入淡出、擦除或溶解效果。相反，Cinemachine Brain 会对 Unity 相机从一个 CinemachineCamera 到另一个 CinemachineCamera 的位置、旋转以及其他设置进行平滑动画过渡（即平滑插值 position，rotation，lens，FOV 等所有相机属性）。

如需在特定的 CinemachineCamera 之间进行混合，使用 Cinemachine Brain 组件中的“自定义混合(Custom Blends)”列表。如需为没有自定义混合的 CinemachineCamera 之间指定混合方式，请使用 Cinemachine Brain 中的“默认混合(Default Blend)”属性。

![CinemachineCustomBlends](../Images/CinemachineCustomBlends.png)

“From”和“To”设置是基于名称而非引用的。这意味着Cinemachine通过将相机名称与这些设置进行匹配来查找相机。它们并未链接到具体的游戏对象(GameObject)。您可以使用内置的下拉菜单从当前场景中选择一个CinemachineCamera，或者直接在文本框中输入名称。如果输入的名称与当前场景中的任何CinemachineCamera都不匹配，该字段将以黄色高亮显示。

使用保留名 \*\*ANY CAMEEA\*\* 指定 blend from 或 to 的任何 Cinemachine Camera。

当 Cinemachine 开始从一个 CinemachineCamera 过渡到另一个时，它将在该资源中查找与即将发生的过渡相匹配的条目，并应用相应的混合定义。

- 如果没有找到匹配项，则将应用 CinemachineBrain 的 DefaultBlend 设置。
- 如果 Custom Blends 资源中有多个条目与即将发生的过渡相匹配，Cinemachine 会选择特异性最强的那一个。例如，当从 vcam1 混合到 vcam2 时，如果自定义混合资源中包含一个 vcam1-to-AnyCamera 的条目，以及另一个 vcam1-to-vcam2 的条目，那么将应用 vcam1-to-vcam2 这个条目。  
- 如果 Custom Blends 资源中有多个条目与即将发生的过渡具有相同强度的特异性，则将应用最先找到的那个条目。

