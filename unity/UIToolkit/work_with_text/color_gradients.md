# Color Gradients

可以为 text 应用最多 4 种颜色的 gradients。当添加 color gradient 时，TextCore 应用 gradient colors 到 text string 中的每个字符（逐字符应用，而不是整个 text 应用）。

Gradient preset 覆盖 text 的 local gradient type 和 colors。

## 创建一个 Color gradient preset

1. 在菜单中选择 Assets > Create > Text > Color Gradient 来添加一个 color gradient preset
2. 在 Color Gradient Inspector 中设置渐变值
3. 将 gradint asset 放到 Panel Text Setting asset 中设置的 Color Gradient Presets 路径

## 应用 color gradient presets

类似 sprite，在 rich tag 中使用 color gradient presets：

```plain
<gradient="name-of-the-color-gradient">Your text</gradient>
```

这样 text 的 color 会与 object's current vertex colors 相乘。

要对一个 text selection 应用纯渐变，使用 color 来重置 color 为 white。即先将文本颜色设置为纯白色，然后再应用渐变，这样渐变颜色就不会被文本原来的颜色影响。

```plain
<color=white><gradient="Light to Dark Green - Vertical">Light to Dark Green gradient</gradient></color>
```
