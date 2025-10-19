# Editor

GUI（in game 和 editor）有一个 matrix（Matrix4x4），控制之后所有绘制的 transform，就像 gizmos 的 matrix。可以使用它来 平移、旋转、缩放一个绘制，例如一个纹理。

绝大多数 GUI 绘制方法有一个 rect 作为它的第一个参数，控制绘制的区域，但是使用 GUI.matrix，rect 可以被任意地变换。

GUIUtility 包含 RotateAroundPivot 和 ScaleAroundPivot 使得操作 GUI.matrix 更容易。

Editor GUI 不包含 drawline 功能。可以使用 GUIUtility.DrawTexture 以一个 1x1 rect 和一个 1x1 texture2d 绘制一个 pixel，并使用 GUI.matrix 来旋转和缩放这个 pixel，使它成为一个 line。这是 Editor Window 和 Inspector Window 绘制任何 line 和 curve 的方法。

EditorWindow是定义从菜单打开的窗口，不依赖于任何gameobject，就像Animation窗口，Console窗口，Project窗口等等。

Editor是定义针对一个特定MonoBehaviour组件的Inspector UI，每个MonoBehaviour初始都使用Unity默认的Inspector UI绘制（字符串输入框，数字输入框，颜色选择器），在Editor中可以自定义如何一个MonoBehaviour在检视面板Inspector上如何显示绘制（例如将一个数值显示可以操作的进度条），并且根据用户对数值的修改进行相应的响应，这就是Editor在Inspector上的主要工作。而这部分就是Odin针对实现的部分。Editor在Inspector上主要确定如何显示MonoBehaviour中各个字段以及在字段有变化时进行响应，Odin通过直接在MonoBehaviour的字段上添加Attribute就直接修改了字段的显示，通过另一些Attribute（OnValueChanged）可以对字段变化进行响应。就是说Odin完全解决了Editor中在Inspector中的绘制部分的工作（OnInspectorGUI），而这些功能还可以用于EditorWindow/OnSceneGUI中的GUI绘制，因为它们都是使用的IMGUI的绘制系统。但是Editor除了在Inspector中的绘制之外，还有在SceneView中绘制的功能，即选中一个gameobject，SceneView上会显示它上面的组件自定义的SceneView绘制，可以用来操作SceneView。这部分是Odin所没有包含的，因此如果要实现SceneView的自定义，仍然需要创建Editor脚本（相反如果只是自定义Inspector就不需要Editor脚本，只需要在字段/方法上添加Odin属性就可以来），然后重写OnSceneView函数。对SceneView的绘制和IMGUI绘制是相同的，只不过是2d绘制变成来3d绘制，仅此而已，其他IMGUI绘制需要考察的问题在这里也是相同的

PropertyDrawer 有两个用途：
- 自定义一个 Serializable class 的每个实例的 GUI
  - 使用 custom Property Drawer，每一个 class 实例在 Inspector 中的 GUI 都会改变
  - 通过 CustomPropertyDrawer 属性将 PropertyDrawer 和相应的 class 绑定，就像 Editor 使用 CustomEditor 将 Editor 脚本和对应的 MonoBehaivour 绑定一样
    ```C#
    using System;
    using UnityEngine;
    
    enum IngredientUnit { Spoon, Cup, Bowl, Piece }
    
    // Custom serializable class
    [Serializable]
    public class Ingredient
    {
        public string name;
        public int amount = 1;
        public IngredientUnit unit;
    }
    
    public class Recipe : MonoBehaviour
    {
        public Ingredient potionResult;
        public Ingredient[] potionIngredients;
    }

    [CustomPropertyDrawer(typeof(Ingredient))]
    public class IngredientDrawer : PropertyDrawer {
        public override void OnGUI(Rect position, SerializeProperty property, GUIContent label) {
            EditorGUI.BeginProperty(position, label, property);
            EditorGUI.PropertyField(...);
            EditorGUI.EndProperty();
        }
    }
    ```
- 使用自定义 Property Attributes 定制脚本中的成员的 GUI
  - 定义一个 PropertyAttribute 和它对应的 PropertyDrawer
  - 将 PropertyAttribute 应用到 MonoBehaviour 中的某个字段，则这个字段的绘制将由 PropertyDrawer负责
  - 通过 CustomPropertyDrawer 将 Attribute 和 Drawer 绑定在一起
  - Attribute 不包含所装饰字段的任何信息，只包含绘制所需要的信息
  - 被 Attribute 装饰的字段，将由 Drawer 负责绘制，字段被发送给 Drawer，同时 Drawer 中的 attribute 就是字段上的 Attribute 实例
    ```C#
    using UnityEngine;

    public class MyRangeAttribute : PropertyAttribute {
        readonly float min;
        readonly float max;
        void MyRangeAttribute(float min, float max) {
            this.min = min;
            this.max = max;
        }
    }

    [CustomPropertyDrawer(typeof(MyRangeAttribute))]
    public class RangeDrawer : PropertyDrawer {
        void OnGUI(Rect position, SerializedProperty property, GUIContent lable) {
            MyRangeAttribute range = (MyRangeAttribute)attribute;
            EditorGUI.Slider(...);
        }
    }
    ```

Conclusion
- EditorWidow：Unity Editor中普通的任何窗口
- Editor：针对MonoBehaviour，修改Inspector GUI和SceneView GUI
- PropertyDrawer：针对serializable对象（普通的C#class，int，float，string等），修改Inspector GUI

Odin=Editor自定义OnInspectorGUI渲染部分，主要是onvaluechagne和button，这是Editor在Inspector的主要工作，另一个主要工作在OnSceneGUI自定义场景，当gameobject被选中时绘制这个gameobject定义的SceneGUI

HandlesUtility = GUIUtility

OnInspectorGUI和OnSceneGUI都是针对每个event调用一遍，因此对于这些对调函数处理的首要事情就是判断事件Event.current

自定义Editor中获得鼠标的位置通过Event.current.mousePosition，而不是Input.mousePosition

从screen向world发射ray：HandlesUtility.GUIToWorldRay

将world位置转换为screen 位置：HandlesUtility.WorldToGUIPoint

Odin是在Unity原有自定义Editor基础上添加了新的功能，仍然可以在OdinEditor/OdinEditorWindow中按照原来的自定义Editor方式使用

Odin的全称是OdinInspector，可见它是主要针对Editor Inspector的
