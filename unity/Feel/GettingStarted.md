Feedbacks are one of the most useful tools in Feel, and the ones you’ll likely end up using very often. 

The MMF_Player (for More Mountains Feedbacks Player) is our way to play sequences of feedbacks.

Rendering.Volume 是最新管线的后期处理，Rendering.PostProcessing.Volume 是旧系统（Builtin 管线）的后期处理。

Feel 是一款即开即用的解决方案，可为你的 Unity 游戏提供按需调用的游戏手感（Game Feel），且几乎无需复杂配置或繁琐设置。它是一个模块化、用户友好且极易扩展的系统，你可以在此基础上进行二次开发与功能增强。

游戏手感（或称为“视觉反馈”“微交互”或“反馈机制”）是游戏设计中最重要的组成部分之一。确保玩家能够理解自己行为的后果，是让交互变得有意义且引人入胜的最佳方式。当玩家执行某个操作，或者游戏中发生重要事件时，提供恰当的反馈是必不可少的。无论是画面震动、闪烁效果、物体缩放跳动，还是将这些效果同时呈现，都能让游戏体验更加令人满足。

Feel 支持 Unity 所兼容的所有平台。Feel 的脚本经过高度优化，运行开销尽可能低。不过需要注意的是，Feel 是基于 Unity 的原生 API 和系统构建的，它本身并不会改变这些底层系统的性能成本。因此，像后处理特效这类功能，在移动设备上通常都会比较吃性能，无论你是否使用 Feel。

Feel 并不会阻止你在游戏中使用大量反馈效果，比如实例化上亿个粒子系统——但如果你真这么做了，那在 Switch 这样的平台上肯定跑不动。诸如此类的情况还有很多。

所以，你真正应该问自己的是：你打算用 Feel 来实现什么？确保你有一个明确的帧率预算，并保证你使用 Feel 实现的那些效果，都在这个预算范围之内。

四种主要组件：

- Manager：全局管理器
- MMF_Player：播放器，feedbacks 容器
- MMF_Feedback：反馈
- 一些反馈需要在目标物体、组件上进行额外操作，因此提供了一些挂载到 target 上的组件，用来和 feedback 配合，操作 target，例如各种 shaker

