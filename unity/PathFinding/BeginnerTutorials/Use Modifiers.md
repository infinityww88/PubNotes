# Using Modifiers

Modifiers是可以hook到Seeker中到小脚本，在将path返回给caller之前进行预处理或后期处理。

使用Modifiers就是简单将它挂载到Seeker组件所在到GameObject上，它们自动工作无需任何code修改。

![modifiers](modifier_comparison_grid.png)

SimpleSmoothModifier, RaycastModifier, FunnelModifier, RadiusModifier, StartEndModifier, AlternativePath, Modifiers

AIPath和AILerp移动脚本使用modifier，而RichAI移动脚本则忽略它们的绝大多数（全部的smooth和simplify modifiers）。RichAI内部包含自己版本的funnel modifier）。但是仍然可以挂载其他modifiers。

## Simple Smooth Modifier

平滑path。

subdividing path，移动vertices使得彼此接近，或者使用spline（贝塞尔曲线）拟合路径。

平滑path时，不可避免地切除corner。这可能是一个问题，因为这个过程不会考虑world geometry。

## Funnel Modifier

简化navmeshs或grid graphs的路径的快速而准确的方式。在path应用funnel algorithm。

## Raycast Modifier

Raycast Modifier通过执行一系列直线检查来简化路径。主要用于grid graphs，尽管有时也可以用于point graph。

## Custom modifiers

可以编写自定义路径modifiers
