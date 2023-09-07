# Font

```gpt
在Unity中，Font和FontAsset是用于处理文本和字体的两个不同的概念，它们之间有一些区别。

Font（字体）：

Font是Unity中的基本字体对象，通常用于处理文本渲染。
Font通常是从操作系统或其他字体源导入的字体文件，例如TrueType字体（.ttf）或OpenType字体（.otf）。
Font对象包含了字体的字符集、字形、字号、字重等信息，可以在UI元素、文本框等组件中使用。
使用Font时，需要在项目中导入字体文件，并将其分配给文本渲染组件（例如Text组件）。
FontAsset（字体资源）：

FontAsset是Unity TextMeshPro插件中的概念，用于增强文本渲染的功能。
TextMeshPro是Unity的一个插件，用于处理高级文本和字体渲染，提供更多的控制和功能。
FontAsset是TextMeshPro中的字体资源，它包含了字体的各种信息，如字符集、字形、字号等，但它是TextMeshPro的一部分，具有更多的可定制性和性能优化。
使用TextMeshPro时，你可以创建FontAsset对象，并将其与TextMeshPro的文本元素一起使用，以实现更高质量的文本渲染效果，如文字描边、阴影、富文本等。
总结一下，主要的区别在于Font是Unity的基本字体对象，而FontAsset是TextMeshPro插件中的字体资源，用于增强文本渲染的功能。如果你需要更高级的文本渲染效果和控制，可以考虑使用TextMeshPro和FontAsset，否则，使用普通的Font对象可能已经足够了。
```

Back in the day, UI Toolkit used TextNative for its TextEngine, which is the same text engine used by IMGUI. After Unity acquired TextMesh Pro, we slowly started to deprecate TextNative (now also known as the Legacy TextSystem) and replace it with TextCore. TextCore is a copy of the TextMesh Pro engine adapted to support all of Unity’s UI Fameworks (IMGUI, UGUI and UITK).

To answer your question, the -unity-font USS style was introduced while UITK was still on the legacy text system. When we switched to TextCore, we kept the -unity-font property and converted Font to FontAsset automatically in the background to ensure a seamless transition and backward compatibility.

The recommended way is to use -unity-font-definition with a FontAsset.
