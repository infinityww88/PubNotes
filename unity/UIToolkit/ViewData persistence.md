# ViewData persistence

ViewData API 解决的问题是，使一个 UI 特定状态，不是 data 的一部分，在 domain reload 和 Editor restarts 之间保持。

这里的想法是时一个持久化数据保存在每个 EditorWindow 上。每个 VisualElement 有一个 viewDataKey，它必须被设置以 enable ViewData persistence。

## Usage

要为支持 view data persistence 的 element enable 这个功能，设置 viewDataKey 为 EditorWindow 中的一个 unique key。

只要一个 element 具有一个 valid viewDataKey，view data Persistence 就是 enable 的。唯一的例外是，当一个 element 是在它的 parent 的 shadow tree 中，并且不是它的逻辑 parent 的 contentContainer 的 一个 physical child。此时，parent 必须具有自己的 viewDataKey 使得它 shadow tree 中的 children 被持久化。

例如，在 ScrollView 中，每个 scrollbar 有它自己的 viewDataKey，在 ScrollView 元素中时唯一的。当 ScrollView 没有设置 key，scroll bars 不会被持久化。否则 scroll bars 将会组合它们的 viewDataKey 和 parent viewDataKey 来创建全局唯一的 key。
