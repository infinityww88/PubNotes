## Misc

Quantum Console 使用 TextMeshPro Text 作为文本区。使用 Quantum Console 时，注意使用的字体要包含打印的字符，尤其是非 latin 字母（例如中文）。否则，在打印日志 Debug.Log 时会出现严重的卡顿问题，甚至打印不出日志。因为当 TextMeshPro 字体和各种 fallback 不包含要打印的字符（中文）时，会执行大量的查找，甚至造成整个程序的卡顿（有时会错误地认为是程序的其他地方导致的卡顿）。为此添加一个中文字体作为 fallback 即可。

```
The character with Unicode value \u5740 was not found in the [OfficeCodePro-Regular SDF] font asset or any potential fallbacks. It was replaced by Unicode character \u25A1 in text object [Text].
\u5740 - 址
```