# RuntimePanelUtils

这个类主要包含一组静态方法，提供 World（Scene），Screen，Panel 坐标系之间的转换。

- Vector2 CameraTransformWorldToPanel(IPanel panel, Vector3 worldPosition, Camera camera)

  转换 3D 场景中的一个 World 坐标，转换为指定的 panel 坐标系，使用给定的 Camera（渲染 3D 场景的相机）的 WorldToScreen。

- Rect CameraTransformWorldToPanelRect(IPanel panel, Vector3 worldPosition, Vector2 worldSize, Camera camera)

- void ResetDynamicAtlas(this IPanel panel)

  重置 panel 的动态图集（batch）dynamic atlas。Textured elements 将会被重绘。

- Vector2 ScreenToPanel(IPanel panel, Vector2 screenPosition)

  转换一个屏幕的绝对位置到给定 panel 的虚拟坐标空间。

- void SetTextureDirty(this IPanel panel, Texture2D texture)

  通知 panel 的 dynamic atlas，提供的 texture 的内容已被改变。如果 dynamic atlas 包含这个 texture，它将会更新它。
