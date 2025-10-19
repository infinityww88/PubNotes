# Canvas

Canvas使用EventSystem辅助MessagingSystem。

## 元素绘制顺序

元素按照在Hierarchy中的顺序绘制，后面的覆盖前面的。

## 渲染模式

- screen space overlay

  所有元素都是gameobject。所有元素都在UI layer。Unity内部使用一个camera渲染这个layer，然后将结果overlay到main camera渲染的结果上。

  如果screen改变大小或分辨率，Canvas自动改变以匹配screen。


- Screen Space Camera

  和Overlay类似，但是Canvas被放置在main camera前面，和视锥体大小匹配的。

  但是Camera（通常是main camera）的透视效果影响UI元素。同时，GameObject可以出现在UI元素之前，因为UI元素就是常规GameObject。Overlay的内部camera是平行投影的。

- World Space

  Canvas就像任何GameObject一样被放置在场景中，不需要平行camera。Canvas的size可以使用RectTransform手动设置。