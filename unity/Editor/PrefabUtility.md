# PrefabUtility

Prefab 相关的任何操作。

可以不创建 Editor 或 EditorWindow，直接创建一个菜单项来执行编辑器逻辑，随便创建一个类，作为静态函数容器，然后再函数上声明 MenuItem 即可：

```c#
// This script creates a new menu item Examples>Create Prefab in the main menu.
// Use it to create Prefab(s) from the selected GameObject(s).
// It is placed in the root Assets folder.
using System.IO;
using UnityEngine;
using UnityEditor;

public class Example
{
    // Creates a new menu item 'Examples > Create Prefab' in the main menu.
    [MenuItem("Examples/Create Prefab")]
    static void CreatePrefab()
    {
        // Keep track of the currently selected GameObject(s)
        GameObject[] objectArray = Selection.gameObjects;

        // Loop through every GameObject in the array above
        foreach (GameObject gameObject in objectArray)
        {
            // Create folder Prefabs and set the path as within the Prefabs folder,
            // and name it as the GameObject's name with the .Prefab format
            if (!Directory.Exists("Assets/Prefabs"))
                AssetDatabase.CreateFolder("Assets", "Prefabs");
            string localPath = "Assets/Prefabs/" + gameObject.name + ".prefab";

            // Make sure the file name is unique, in case an existing Prefab has the same name.
            localPath = AssetDatabase.GenerateUniqueAssetPath(localPath);

            // Create the new Prefab and log whether Prefab was saved successfully.
            bool prefabSuccess;
            PrefabUtility.SaveAsPrefabAssetAndConnect(gameObject, localPath, InteractionMode.UserAction, out prefabSuccess);
            if (prefabSuccess == true)
                Debug.Log("Prefab was saved successfully");
            else
                Debug.Log("Prefab failed to save" + prefabSuccess);
        }
    }

    // Disable the menu item if no selection is in place.
    [MenuItem("Examples/Create Prefab", true)]
    static bool ValidateCreatePrefab()
    {
        return Selection.activeGameObject != null && !EditorUtility.IsPersistent(Selection.activeGameObject);
    }
}
```

## InteractionMode

一些 Unity API 方法允许指定操作是 user 触发的还是自动执行的。这影响 Unity 是否显示对话框，操作是否记录到 undo history。Automated 操作不记录到 undo history，也不显示对话框。

- AutomatedAction
- UserAction

## Static Properties

- prefabInstanceUpdated

  当 Scene 中的 Prefab Instance 有更新，Unity 自动调用这个 delegate：

  ```c#
  public delegate void PrefabInstanceUpdated(GameObject instance);
  ```

## Static Methods

- void ApplyAddedComponent(Component component, string assetPath, InteractionMode action)

  在给定的 asset path 的 Prefab Asset 上添加 component。

  这个方法允许你应用一个 added component 到现有 Prefab 上。这与在编辑器上添加 Component 并 apply override。要使用这个方法，你必须首先添加一个 component 到现有 Prefab instance 上。

  添加的 component 是一个 Instance Override 类型。应用 added component 到 prefab 的动作意味着 component 变成 Prefab Asset 的一部分，不再是 Prefab Instance 上的一个 override。

  当应用一个 added component 到 Prefab Asset，必须提供 asset path 作为参数。这是因为有一些场景会有多个可能的 targets 来应用改变。例如，added component 被添加到 nested prefab 的 gameobject，你必须选择应用改变到 inner nested Prefab Asset 还是 outer root Prefab Asset。通过提供 asset path，可以清楚地告诉 Unity 改变必须应用到哪个 Prefab Asset。

- void ApplyAddedGameObject(GameObject gameObject, string assetPath, InteractionMode action)
- void ApplyAddedGameObjects(GameObject[] gameObjects, string assetPath, InteractionMode action)

上面两个函数与 ApplyAddedComponent 类似，只是 change 是添加 child GameObject，而不是 component。

- void ApplyObjectOverride(Object instanceComponentOrGameObject, string assetPath, InteractionMode action)

  应用一个 Prefab Instance 的所有 overridden 属性到给定的 assetPath 的 Prefab Asset 上。这应用的是属性的改变，而不是添加 component 或 gameobjects。

  Prefab Asset 是 Project 中的 Prefab 资源，Prefab Instance 是在 Scene 中创建的连接 Prefab Asset 的 GameObject。

  这个方法允许你应用修改既有 Prefab 的属性值。

  如果传递 GameObject 为 object 参数，只有 GameObject 自身上的 overrides 被应用（例如 layer，tag，或 static flags），而不是它的 component 或 GameObjects。如果传递 Component 为 object 参数，只有哪个 Component 的 override 被应用。

  要应用一个 Prefab 的所有 overrides，可以使用 PrefabUtility.ApplyPrefabInstance。

  其他行为与上面的方法一样。

- void ApplyPrefabInstance(GameObject instanceRoot, InteractionMode action)

  应用一个 Prefab instance 上的所有 overrides 到它连接的 Prefab Asset 上。

  这个方法允许你应用一个 Prefab Instance 的全部 modified state 到它的 source Prefab Asset 上，包括所有的属性修改，添加或移除的 components，添加或移除的 Child GameObjects（包括添加的 child Prefab instances）。

  这等价于 editor 中 overrides menu 的 Apply All。

  Prefab Instance 上还没应用的 Modifications 称为 Instance overrides。应用修改的操作意味着这些修改变成 Prefab Asset 的一部分，而不再是 overrides。

  当使用这个方法应用所有 Prefab Asset 的 modifications 到 nested Prefabs 或 Prefab variants，改变总是应用到 outermost Prefab。要应用 inner Prefabs，可以使用其他方法，例如 PrefabUtility.ApplyAddedComponent, PrefabUtility.ApplyAddedGameObject, PrefabUtility.ApplyRemovedComponent, PrefabUtility.ApplyRemovedGameObject and PrefabUtility.ApplyObjectOverride，并提供 Prefab Asset path.

  一个 Prefab Instance 的 root GameObject的 position 和 rotation 不能被应用，其他 default override 的属性也如此。

- bool IsDefaultOverride(PropertyModification modification)

  判断一个 property modification 是否是一个 default override。
  
  Prefab instance 的 root gameobject 上的特定属性被认为是 default override。这些是被默认 override 的，通常很少被 apply 和 revert。绝大多数 apply 和 revert 操作会忽略这些 override。

  Default override 是：

  - Root GameObject：name
  - Root Transform：localPosition，localRotation
  - Root RectTransform：localPosition，localRotation，anchoredPosition，sizeDelta，anchorMin，anchorMax，pivot

  这些属性是 default overrides，以防止 apply 或 revert 整个 prefab instance 时导致的一些常见错误。通常，你不会想一个 Prefab instance 的 position 或 rotation 从它的 Prefab asset 上得到更新，更新一般都是 Component 或 child GameObject，以及自己的 tag 或 layer 或 static flags 这些属性。

  在一个 Prefab Instance 上使用 ApplyAll 或 RevertAll 不会影响 default overrides。Apply 或 revert 一个 default override 的唯一方法是使用 property 自身的 context menu，这对应 PrefabUtility.ApplyPropertyOverride and PrefabUtility.RevertPropertyOverride 方法。

- Texture2D GetIconForGameObject(GameObject gameObject)

  获取一个 GameObject 的 icon，它出现在 Hierarchy 和 Project Browser 中。

- void ConvertToPrefabInstance(GameObject plainGameObject, GameObject prefabAssetRoot, ConvertToPrefabInstanceSettings settings, InteractionMode mode)

  将一个普通的 GameObject 使用给定的 Prefab Asset root object 转换为一个 Prefab instance。

- FindAllInstancesOfPrefab

- GetAddedComponents
- GetAddedGameObjects
- GetObjectOverrides
- GetRemovedComponents
- GetRemovedGameObjects
- ReplacePrefabAssetOfPrefabInstance
- RevertAddedComponent
- RevertAddedGameObject
- RevertObjectOverride
- RevertPrefabInstance
- RevertPropertyOverride
- RevertRemovedComponent
- RevertRemovedGameObject

- GameObject LoadPrefabContents(string assetpath)

  加载一个给定 assetpath 的 prefab asset 到 isolated scene 中，返回这个 prefab 的 root gameobject。

  你可以使用这个方法获得 prefab 的内容，直接修改它，而不需要通过这个 prefab 的一个 instance。这在批处理时很有用。

  一旦修改了 prefab，必须使用 SaveAsPrefabAsset 将它保存，然后调用 UnloadPrefabContents 从内存中释放 Prefab 和 isolated。

  ```C#
  using UnityEngine;
  using UnityEditor;
  
  public class Example
  {
      [MenuItem("Examples/Add BoxCollider to Prefab Asset")]
      static void AddBoxColliderToPrefab()
      {
          // Get the Prefab Asset root GameObject and its asset path.
          GameObject assetRoot = Selection.activeObject as GameObject;
          string assetPath = AssetDatabase.GetAssetPath(assetRoot);
  
          // Load the contents of the Prefab Asset.
          GameObject contentsRoot = PrefabUtility.LoadPrefabContents(assetPath);
  
          // Modify Prefab contents.
          contentsRoot.AddComponent<BoxCollider>();
  
          // Save contents back to Prefab Asset and unload contents.
          PrefabUtility.SaveAsPrefabAsset(contentsRoot, assetPath);
          PrefabUtility.UnloadPrefabContents(contentsRoot);
      }
  
      [MenuItem("Examples/Add BoxCollider to Prefab Asset", true)]
      static bool ValidateAddBoxColliderToPrefab()
      {
          GameObject go = Selection.activeObject as GameObject;
          if (go == null)
              return false;
  
          return PrefabUtility.IsPartOfPrefabAsset(go);
      }
  }
  ```

- void LoadPrefabContentsIntoPreviewScene(string prefabPath, SceneManagement.Scene scene);

  和上面一样，但是不是加载 isolated scene，而是使用一个给定的 scene。

- IsPartOfPrefabAsset
- IsPartOfPrefabInstance
- IsPartOfVariantPrefab
- IspartOfAnyPrefab

- GameObject SaveAsPrefabAsset(GameObject instanceRoot, string assetPath)

  使用一个给定的 gameobject 在给定 path 上创建一个 Prefab Asset，包含 Scene 中的任何 children，而不修改 input objects。

  有时，一些 children 是 Prefab instances，它们会自动变成新 prefab asset 的 nested prefab。

  instanceRoot 必须是普通的 GameObject，或者 Prefab instance 的 outermost root。不可以是 prefab instance 的 child。

  如果 input object 是一个 prefab instance root，结果 Prefab 将是一个 Prefab Variant。如果想创建一个完全新的 Prefab instead，需要先 unpack prefab instance。

- GameObject SaveAsPrefabAssetAndConnect(GameObject instanceRoot, string assetPath, InteractionMode action)

- GameObject SavePrefabAsset(GameObject asset)

- UnloadPrefabContents

- UnpackAllInstancesOfPrefab
- UnpackPrefabInstance

## Events

- prefabInstanceUnpacked
- prefabInstanceUnpacking

## EditPrefabContentsScope

这是一个 Disposable helper 结构体，用于自动加载 prefab 文件的内容，保存内容，然后卸载。

它允许你临时加载一个 Prefab 文件的内容，在一个 code block 内部修改内容，然后自动保存结果到 Prefab，同时在退出 scope 时自动卸载临时内容。

这个 scope struct 包装 LoadPrefabContents, SaveAsPrefabAsset and UnloadPrefabContents 这几个 API。

```c#
using UnityEditor;
using UnityEngine;

public static class PrefabUtilityTesting
{
    [MenuItem("Prefabs/Test_EditPrefabContentsScope")]
    public static void Test()
    {
        // Create a simple test Prefab Asset. Looks like this:
        // Root
        //    A
        //    B
        //    C
        var assetPath = "Assets/MyTempPrefab.prefab";
        var source = new GameObject("Root");
        var childA = new GameObject("A");
        var childB = new GameObject("B");
        var childC = new GameObject("C");
        childA.transform.parent = source.transform;
        childB.transform.parent = source.transform;
        childC.transform.parent = source.transform;
        PrefabUtility.SaveAsPrefabAsset(source, assetPath);

        using (var editingScope = new PrefabUtility.EditPrefabContentsScope(assetPath))
        {
            var prefabRoot = editingScope.prefabContentsRoot;

            // Removing GameObjects is supported
            Object.DestroyImmediate(prefabRoot.transform.GetChild(2).gameObject);

            // Reordering and reparenting are supported
            prefabRoot.transform.GetChild(1).parent = prefabRoot.transform.GetChild(0);

            // Adding GameObjects is supported
            var cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.transform.parent = prefabRoot.transform;
            cube.name = "D";

            // Adding and removing components are supported
            prefabRoot.AddComponent<AudioSource>();
        }

        // Prefab Asset now looks like this:
        // Root
        //    A
        //       B
        //    D
    }
}
```