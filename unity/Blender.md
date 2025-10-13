Unity 现在已经支持直接导入加载 Blender 的工程文件 .blend，不再需要 Blender 将模型转换为 FBX 文件或 Obj 文件了。而且导入的文件和 FBX 或 Obj 文件一样，都变成统一的 Unity 资源。这样在 Blender 中编辑模型后，可以直接保存工程文件即可，然后回到 Unity 中，它会自动 reimport .blend 文件。

Blender 的问题：

Blender 相比 UModeler 最大的不便就是，Blender 每次创建或打开新的文件，都需要通过繁琐的导航才能保存到 Unity 的目录中。编辑导入到 Unity 的 .blend 文件也需要通过繁琐的导航才能找到要编辑的文件。除此以外，UModeler 并不比 Blender 便捷多少。UModeler 的 Mesh 文件也需要进行规范化命名，并保存到有意义的地方。

默认 UModeler 以 GUID 为文件名，统一保存到 UModeler 的目录中，确实方便，但是只适合用于测试和快速模型，用于正常的工作流程中，还是必须保存到合适的目录，并提供有意义的名字，这就与 Blender 一样了。

UModeler 的问题：

- 编辑操作的 Handler 和场景中的其他的对象容易冲突，一不小心就可能点击到其他对象
- 快捷键容易与 Unity 快捷键和其他插件的快捷键冲突，并且很难记住其快捷键，因为它们跟 Unity 快捷键在一个空间，而 Blender 在单独的工作空间有完全不被影响的快捷键。很多功能还没有快捷键
- 编辑点线面只能通过 Handler 进行，而 Handler 太大，经常遮挡要选择的点线面，使得很难选中想要编辑的元素，必须旋转场景，让 Handler 远离要选择的元素。经常地，操作 Handler 和选择元素两个工作相互冲突
- UModeler 不能创建处理面数太多的模型，否则就会导致 UnityEditor 宕机，只能重启
- UModeler 的选择、编辑功能太少，使得很多情况只能手动操作，例如 Loop Edges Bridge
- UModeler 不能使用 Modifier 和 Sculpt 等工具
- UModeler 的 Smooth Face Group 功能并不总是正确
- UModeler 的 Extrude 很简陋，并且不能在原来的 faces 处封闭，以创建封闭的模型
- 和 Blender 一起使用有违做一件事情有且仅有一种方法，需要同时记住两种工具的操作

模型编辑还是要有单独的工作空间，避免与其他工作冲突，因此应该使用单独的建模软件。

只要解决了 Blender 翻山越岭地寻找目录和文件的问题，Blender 的便捷性就不会比 UModeler 差多少，而它的建模功能则不是 UModeler 能比的。

解决这个问题的方法是，在 Unity 的 Project 中创建右键菜单（它们本身也添加到主菜单中），在当前的 Project 目录直接创建想要的 .blend 文件，这样就不用打开 Blender 然后翻山越岭地寻找 Unity 工程目录了。创建 .blend 文件的方法是，提前创建一个模板 .blend 文件，然后要创建新的 .blend 文件时，直接复制这个文件到选择的目录即可。然后在 Unity Project 中双击 .blend 文件就可以直接打开 Blender 程序来编辑它，还可以将 .blend 文件拖拽到 Blender 窗口，在当前已经打开的 Blender 中编辑它。如果当前打开的 Blender 窗口被其他程序窗口遮挡或最小化，可以将 .blend 文件拖拽到任务栏的图标上，这会显示 Blender 窗口，然后再拖拽到 Blender 窗口中，就可以打开这个 .blend 文件。

下面的 BlenderMenu.cs 文件由 AI 创建，它使得在右键点击 Project 中的目录时，获取当前选择的目录，然后以这个目录，打开 CreateBlenderModelWindow 窗口。CreateBlenderModelWindow 窗口的作用是可以输入要创建的模型文件的文件名，创建文件的过程就是从指定的模板复制过来而已。

```C#
#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using System.IO;
using System;

using Debug = UnityEngine.Debug;

public static class BlenderMenu
{
	// 菜单项：Project 右键 -> Tools -> CreateBlenderModel
	[MenuItem("Assets/Tools/CreateBlenderModel", false, 10)]
	private static void OpenProjectFolderOfSelection()
	{
		var path = GetCurrentSelectionDirectory();
		if (string.IsNullOrEmpty(path))
		{
			Debug.LogWarning("无法获取当前目录。");
			return;
		}

		CreateBlenderModel(path);
	}

	// 可选：验证菜单是否可用（例如仅在选中资源时可用）
	[MenuItem("Assets/Tools/CreateBlenderModel", true, 10)]
	private static bool ValidateOpenProjectFolderOfSelection()
	{
		var path = GetCurrentSelectionDirectory();
		return !string.IsNullOrEmpty(path);
	}

	// 获取“当前选中项所在目录”的项目相对路径（若未选中则回退到 Assets）
	private static string GetCurrentSelectionDirectory()
	{
		var obj = Selection.activeObject;
		if (obj == null) return "Assets"; // 未选中时默认 Assets

		var assetPath = AssetDatabase.GetAssetPath(obj);
		if (string.IsNullOrEmpty(assetPath)) return "Assets";

		// 选中的是文件夹时，直接返回
		if (Directory.Exists(assetPath)) return assetPath;

		// 选中的是文件时，返回其所在目录
		return Path.GetDirectoryName(assetPath);
	}
	
	private static void CreateBlenderModel(string path) 
	{
		var wnd = EditorWindow.GetWindow<CreateBlenderModelWindow>();
		wnd.Folder = path;
		wnd.Show();
	}
}
#endif
```

```C#
using UnityEngine;
using UnityEditor;
using Sirenix.OdinInspector;
using Sirenix.OdinInspector.Editor;
using System.IO;

public class CreateBlenderModelWindow : OdinEditorWindow
{
	[SerializeField]
	private string name;
	
	public string Folder { get; set; }
	
	[Button]
	private void Create()
	{
		if (name != null && name.Trim() != "") {
			string path = Path.Join(Folder, name) + ".blend";
			if (!File.Exists(path)) {
				//从指定的模板 .blend 文件复制一份过来
                File.Copy("Assets/Test/Editor/Cube.blend", path);
				//注意调用一下 AssetDatabase.Refresh()，这会触发 Unity reimport，以加载新创建的模型文件
                //通常 Unity 只会在用户操作时才 reimport，通过程序新建文件，不会触发 Unity reimport
                AssetDatabase.Refresh();
			}
			else {
				Debug.LogError($"Blend File {path} already exists");
			}
		}this.Close();
	}
}
```

![](image/OpenBlenderInUnity.gif)

1. 在 Unity Project 中双击 .blend 文件，可以直接打开 Blender 并编辑这个文件
2. 将导入的 .lend 文件中的 mesh（其实可以是 Unity 中任何 mesh 资源）拖拽到 scene 中，会自动创建一个新的 GameObject，并带有这个 mesh，但是 material 是空的，为新的 GameObject 选择合适的 Material
3. 点击 GameObject 的 mesh，可以 ping 这个 mesh 所在的 .blend 文件，将 .blend 文件拖拽到任务栏中的 Blender 图标，会显示 Blender 程序窗口，然后再拖拽到 Blender 的工作窗口中，选择下拉菜单中的 Open，就可以在现有的 Blender 程序中打开这个 .blend 文件。如果 Blender 已经显示，则可以直接拖拽到 Blender 窗口

而且 Blender 现在的打开速度飞快，占用内存也不多，因此就没有使用 UModeler 的必要了。

UModler 虽然带来一些很方便的东西，但是也带来了很多问题，而且功能远没有 Blender 强大和方便、干净。

UModeler X 不仅收费，即使免费的 UModeler X Basic 在 Unity 进入 Play Mode 时还会显著拖慢进入时间，影响迭代的速度。
