# Fallback font

每个 font asset 都有受限数量的字符。当你使用一个不在当前 font asset 中的字符，TextCore 搜索 Fallback List，直到它找到一个包含那个字符的 font asset。然后这个 Text element 使用那个 font asset 来渲染这个字符。

你可以设置一个 fallback fonts 列表，在多个 textures 中分布 fonts，或者对不同的 fonts 使用不同的 fonts。它需要额外的计算资源来搜索缺失的字符，以及额外的 draw calls 来使用更多的 fonts。

你可以对 fallback list 中的多个 font assets 使用同一个字符。尽力保持 fallback list 的字符的 style 与 main font asset 保持一致。

## Fallback font usage

通常 fallback font assets 用于：

- 使用包含大量字符的语言，例如 CJK。使用 fallback fonts 在多个 assets 中分布字符
- 在你的 text 中包含其他字母表的特殊字符

Dynamic OS font asset 是 fallback font assets 最好的 candidates。

## Fallback font chain

你可以创建 local 和 global fallback font asset lists。在 font asset 资源文件的属性中设置 local font asset，在 Panel Text Settings 中设置 global font asset lists。除了 fallback fonts，TextCore 对缺失的 glyphs 还搜索其他 assets，例如 default sprite asset。最终，这些 assets 构成了 fallback chain。

下面是 fallback chain 的 asset 顺序：

1. Local fallback font assets list
2. Global fallback font assets list
3. Default sprite asset
4. Default font asset
5. Missing glyphs characters
