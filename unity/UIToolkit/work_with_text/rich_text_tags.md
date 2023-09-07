# Rich text tags

你可以使用 USS 来 style 整个 text string，但是如果只想 style text string 中的一个 word 则很困难，但是使用 rich text tags 则很简单。

当前 rich tags 不支持 Text Field。

```xml
<a href="https://www.unity.com">Visit Unity</a>

<align="left>Horizontal alignment</align>

<allcaps>Convert text to uppercase</allcaps>

<alpha="FF">Change text opacity</alpha>

<b>Boldface</b>

<color="red">Red</color>
<color=#005500>Red</color>

<cspace=1em>Spaceing between characters</cspace>

<font="Impace SDF">a differenct font</font>

<font-weight="100">Thin</font-weight>

<gradient="Light to Dark Green - Vertical">gradient</gradient>

<i>Render text in italics</i>

<indent=15%>Indent all text between the tag and the next hard line break</indent>

<line-height=50%>Height relative to defalut line height</line-height>

<line-indent=15%>Indent the first line after every hard line break</line-indent>

<margin=5em>Set text horizontal margins</margin>
<margin-left=5em>Set text horizontal left margins</margin>
<margin-right=5em>Set text horizontal right margins</margin>

<mark=#ffff00aa>Highlight text with colored overlay, alpha must less 1</mark>

<mspace=2.75em>Override a font's character spacing and turn it into a monospace</mspace>

<nobr>Keep a segment of text together, no break</nobr>

<noparse>Prevent parsing of rich text tags. <b> no effect</noparse>

<pos=75%>Set horizontal caret position on current line，pixels，font units，percentages</pos>

<rotate="45">Rotate each character about its center</rotate>

<s>Render a line across the text<s>

<size=100%>Adjust the font size, in pixels, font units, or percentage, absolute or relative</size>

<smallcaps>Convert text to lowercase</smallcaps>

<space=5em>Add horizontal offset after the text</space>

<sprite name="spriteName">Add a sprite from sprite asset into text</sprite>
<sprite index=3>Inserts the fourth sprite from the default Sprite Asset</sprite>

<strikethrough>Draw a line slighty above the baseline so it crosses out the text</strikethrough>

<style="H1">Apply a custom style to the text</style>

<sub>Convert the text to subscript</sub>

<sup>Convert the text to superscript</sup>

<u>Underline the test</u>

<uppercase>Convert text to uppercase</uppercase>

<voffset=1em>Give the baseline a vertical offset</voffset>

<width=60%>Change the horizontal size of text area</width>
```

