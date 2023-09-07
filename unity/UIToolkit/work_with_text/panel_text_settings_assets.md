# Panel Text Settings assets

UI Toolkits 在 Panel Text Settings asset 中存储项目范围的 text settings。UI Toolkit 使用一个默认 Panel Text Settings asset 用于 text objects。

当前不可以改变 Editor UI 的 default Panel Text Settings。

可以编辑存储 font assets，sprite assets，自定义 style sheets，和其他 color gradient presets 的路径。这个路径必须是 Resources 目录的子目录。

## Default Font Asset

当从一个 font file 创建一个 font asset 之后，必须将它放在存储所有 font assets 的路径中。

- Default Font Asset：当创建一个新的 text object 的时默认使用的 font
- Path：存储所有 font assets 的路径

## Font Assets Fallback

为这个 font asset 管理全局 Fallback font assets list。

Font Asset 文件中的 local fallback set 优先这个 global fallback。

- Fallback Font Assets

## Dynamic Font System Settings

项目范围内的设置来处理 missing glyphs。当 text object 遇到一个缺失字体的字符（不在任何 fallback 字体），就用这个 missing glyphs 来代替。

- Missing Character Unicode：missing glyph 的字符的 Unicode。
- Clear Dynamic Data on Build：清理 dynamic data，将 font asset 重置到它创建时的 empty 状态
- Disable Warnings：每次 text object 遇到缺失字符时，产生一个 log，开启这些选项关闭 log

## Default Sprite Asset

在创建一个 sprite asset 之后，必须将它放在存储所有 sprite assets 的路径中。你可以设置一个 default sprite asset，rich sprite tag 不指定 sprite asset 时，就会使用这个 sprite asset，然后通过 name 或 index 引用某个 sprite。

- Default Sprite Asset：默认使用的 Sprite asset（rich tag 不指定 sprite asset 的时候）
- Missing Sprite Unicode：缺失的 sprite 使用 Unicode
- Path：存储所有 sprite assets 的路径，必须是 Resources 的子目录

## Sprite Asset Fallback

Panel Text Setting 中的 fallback list set 称为 global fallback。Sprite Asset 资源文件内可以指定一个 Fallback Sprite sset List，这是 local fallback，它优先于 global fallback。

Sprite Asset 和 Font Asset 一样，有一个 Defalut XXX Font，有一个 Default XXX Asset Fallback。Default XXX Font 用于新创建的 text object 默认设定的 asset（即一个初始值）。Fallback 用于当在当前 asset 找不到 glyph 时的 fallback。

## Default Style Sheet

被项目中所有 text objects 使用的默认 style sheet（text 初始样式）。

同样，必须放在指定的 Resources 子目录中。

## Color Gradient Presets

- Path：指定存储所有 color gradients presets 的路径。

## Line Breaking for Asian Languages

要对亚洲语言获得正确的 line-breaking 行为，指定那些字符作为 leading 和 following 字符。
