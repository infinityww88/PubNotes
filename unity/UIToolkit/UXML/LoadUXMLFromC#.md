# Loading UXML from C#

要从一个 UXML 模板构建 user interface，必须先加载一个 template 到一个 VisualTreeAsset：

var template = EditorGUIUtility.Load("path/to/file.uxml") as VisualTreeAsset;

或者更直接地

var template = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>("path/to/file.uxml");

然后你可以构建它表示的 visual tree，并将它挂载到 parent element。

template.CloneTree(parentElement, slots);

在上面的语句中，模板中的 \<UXML> 元素没有转换为一个 VisualElement，相反，它所有的 children 附加到指定的 parentElement。

一旦 template 被实例化，可以使用 Query 获取 visual element tree 中特定的元素，JQuery/Linq 的 Unity 实现。

例如，下面的例子展示如何创建一个新的 EditorWindow，并加载一个 UXML 文件为它的内容：

```C#
public class MyWindow : EditorWindow  {
    [MenuItem ("Window/My Window")]
    public static void  ShowWindow () {
        EditorWindow w = EditorWindow.GetWindow(typeof(MyWindow));

        VisualTreeAsset uiAsset = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>("Assets/MyWindow.uxml");
        VisualElement ui = uiAsset.CloneTree(null);

        w.rootVisualElement.Add(ui);
    }

    void OnGUI () {
        // Nothing to do here, unless you need to also handle IMGUI stuff.
    }
}
```