# Canvas Group

在一个地方整体控制一组UI元素的特定方面，而不需要一个一个地控制。Canvas Group影响GameObject（自身）和所有的children元素。

- Alpha

  group中UI元素的不透明度。每个元素也有自身的透明度。Canvas Gropu的alpha和单独UI元素的alpha相乘在一起。

- Interactable

  决定控件是否接受输入

- Block Raycasts

  组件是否作为Raycasts的collider。针对graphic raycaster的RayCast，而不是Physics.Raycast

- Ignore Parent Groups

  Group是否被更上层Canvas Group组件影响
