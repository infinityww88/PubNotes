# ListView

```C#
suggestionListView.makeItem = () => searchItemAsset.CloneTree().Q<Label>();
suggestionListView.itemsSource = new List<ZHWord>();
suggestionListView.bindItem = (e, i) =>
{
    Label t = (Label)e;
    var w = (ZHWord)suggestionListView.itemsSource[i];
    t.text = $"{w.word} {w.meaning.Replace("\n", " ")}";
};

private void OnSearchFieldChange(ChangeEvent<string> evt) {
    if (evt.newValue.Length < 2)
    {
        suggestionListView.itemsSource.Clear();
        suggestionListView.Rebuild();
        return;
    }
    List<ZHWord> ret = dbManager.QueryZHDictSuggest(evt.newValue, 50);
    suggestionListView.itemsSource = ret;
    suggestionListView.Rebuild();
}
```

初始化时为 itemSources 设置一个数组，makeItem 和 bindItem 回调。更新时，更新 itemSources，然后调用 ListView.Rebuild。

除了 makeItem 和 bindItem，还有 unbindItem、destroyItem、select 相关的回调。

默认 ListView 是 FixedHeight 的，它控制了 item 的高度。设置 DynamicHeight 来让 item 自己控制自己的 height。

visualTreeAsset.CloneTree() 默认克隆出的 off-screen 的 tree 是有一个 TemplateContainer 元素作为 root 包装的。只有指定 Clone Target 才会去掉这个包装元素。直接将 CloneTree 挂载到当前 UIDocument 上会将包装元素也加上去，而这个包装元素没法在 UIBuilder 中设定样式。

ListView 用于在一个已知固定范围 Rect 内显示更多内容的。因此 ListView 通常具有固定 size，不用于动态 List，动态 List 直接使用 VisualElement 即可。
