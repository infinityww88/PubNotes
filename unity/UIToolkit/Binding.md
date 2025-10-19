# Bindings

Bindings 的目的是序列化 objects 中的 properties 到 visible UI。一个 binding 指的是 属性和修改它的可视化控件 之间的连接。

Binding 在一个 object 和派生自 BindableElement 或实现 IBindable 接口的任何 UIElement 之前完成。

## 来自 UnityEditor.UIElements namespace：

### Base Class

- BaseCompositeField
- BasePopupField
- CompoundFields
- TextValueField

### Controls

- InspectorElement
- ProgressBar
- BoundsField
- BoundsIntField
- ColorField
- CurveField
- DoubleField
- EnumField
- FloatField
- GradientField
- IntegerField
- LayerField
- LayerMaskField
- LongField
- MaskField
- ObjectField
- PopupField
- ObjectField
- PopupField
- PropertyControl
- RectField
- RectIntField
- TagField
- Vector2Field
- Vector2IntField
- Vector3Field
- Vector3IntField
- Vector4Field

## 来自 UnityEngine.UIElement namespace

### Base class

- BaseField
- BaseSlider
- TextInputBaseField
- TemplateContainer

### Controls

- Foldout
- MinMaxSlider
- Slider
- SliderInt
- TextField
- Toggle

当使用以上 control 时，Binding 通过以下步骤完成：

1. 在 Control 中，指定来自 IBindable 接口的 bindingPath，使得 UI 知道要绑定到哪个属性。你可以在 C# 或 UXML 完成。
2. 为要绑定的 object 创建一个 SerializedObject。
3. 绑定 object 到 Control 或者它的祖先中的一个。

## 在 C# 中绑定

```C#
using UnityEditor;
using UnityEngine;
using UnityEditor.UIElements;
using UnityEngine.UIElements;

namespace UIElementsExamples
{
   public class SimpleBindingExample : EditorWindow
   {
       TextField m_ObjectNameBinding;
      
       [MenuItem("Window/UIElementsExamples/Simple Binding Example")]
       public static void ShowDefaultWindow()
       {
           var wnd = GetWindow<SimpleBindingExample>();
           wnd.titleContent = new GUIContent("Simple Binding");
       }
    
       public void OnEnable()
       {
           var root = this.rootVisualElement;
           m_ObjectNameBinding = new TextField("Object Name Binding");
           m_ObjectNameBinding.bindingPath = "m_Name";
           root.Add(m_ObjectNameBinding);
           OnSelectionChange();
       }
    
       public void OnSelectionChange()
       {
           GameObject selectedObject = Selection.activeObject as GameObject;
           if (selectedObject != null)
           {
               // Create serialization object
               SerializedObject so = new SerializedObject(selectedObject);
               // Bind it to the root of the hierarchy. It will find the right object to bind to...
               rootVisualElement.Bind(so);
    
               // ... or alternatively you can also bind it to the TextField itself.
               // m_ObjectNameBinding.Bind(so);
           }
           else
           {
               // Unbind the object from the actual visual element
               rootVisualElement.Unbind();
              
               // m_ObjectNameBinding.Unbind();
              
               // Clear the TextField after the binding is removed
               m_ObjectNameBinding.value = "";
           }
       }
   }
}
```

## Binding with UXML

在 UXML 中，binding-path 在 TextField control 中定义。这是 control 有效绑定的 object 的属性。

```XML
<UXML xmlns:ui="UnityEngine.UIElements">
 <ui:VisualElement name="top-element">
   <ui:Label name="top-label" text="UXML-Defined Simple Binding"/>
   <ui:TextField name="GameObjectName" label="Name" text="" binding-path="m_Name"/>
 </ui:VisualElement>
</UXML>
```

```C#
using UnityEditor;
using UnityEngine;
using UnityEditor.UIElements;
using UnityEngine.UIElements;


namespace UIElementsExamples
{
   public class SimpleBindingExampleUXML : EditorWindow
   {
       [MenuItem("Window/UIElementsExamples/Simple Binding Example UXML")]
       public static void ShowDefaultWindow()
       {
           var wnd = GetWindow<SimpleBindingExampleUXML>();
           wnd.titleContent = new GUIContent("Simple Binding UXML");
       }

       public void OnEnable()
       {
           var root = this.rootVisualElement;
           var visualTree = AssetDatabase.LoadAssetAtPath<VisualTreeAsset>("Assets/Editor/SimpleBindingExample.uxml");
           visualTree.CloneTree(root);
           OnSelectionChange();
       }
    
       public void OnSelectionChange()
       {
           GameObject selectedObject = Selection.activeObject as GameObject;
           if (selectedObject != null)
           {
               // Create serialization object
               SerializedObject so = new SerializedObject(selectedObject);
               // Bind it to the root of the hierarchy. It will find the right object to bind to...
               rootVisualElement.Bind(so);
           }
           else
           {
               // Unbind the object from the actual visual element
               rootVisualElement.Unbind();
              
               // Clear the TextField after the binding is removed
               // (this code is not safe if the Q() returns null)
               rootVisualElement.Q<TextField>("GameObjectName").value = "";
           }
       }
   }
}
```

## 在 InspectorElement 中使用 Binding

InspectorElement 是 UIElement 在 Inspector 中的对应体，用于一个特定类型的 Unity object。使用 InspectorElement 来 inspect objects 有以下优势：

- 创建 UI
- 自动绑定 objects 到 UI

```C#
using UnityEditor;
using UnityEngine;
using UnityEditor.UIElements;

namespace UIElementsExamples
{
   public class SimpleBindingExampleUXML : EditorWindow
   {
       [MenuItem("Window/UIElementsExamples/Simple Binding Example UXML")]
       public static void ShowDefaultWindow()
       {
           var wnd = GetWindow<SimpleBindingExampleUXML>();
           wnd.titleContent = new GUIContent("Simple Binding UXML");
       }

       TankScript m_Tank;
       public void OnEnable()
       {
           m_Tank = GameObject.FindObjectOfType<TankScript>();
           if (m_Tank == null)
               return;
    
           var inspector = new InspectorElement(m_Tank);
           rootVisualElement.Add(inspector);
       }
   }
}
```

```C#
using UnityEngine;

[ExecuteInEditMode]
public class TankScript : MonoBehaviour
{
   public string tankName = "Tank";
   public float tankSize = 1;

   private void Update()
   {
       gameObject.name = tankName;
       gameObject.transform.localScale = new Vector3(tankSize, tankSize, tankSize);
   }
}
```

```C#
using UnityEditor;
using UnityEngine;
using UnityEngine.UIElements;

[CustomEditor(typeof(TankScript))]
public class TankEditor : Editor
{
   public override VisualElement CreateInspectorGUI()
   {
       var visualTree = Resources.Load("tank_inspector_uxml") as VisualTreeAsset;
       var uxmlVE = visualTree.CloneTree();
uxmlVE.styleSheets.Add(AssetDatabase.LoadAssetAtPath<StyleSheet>("Assets/Resources/tank_inspector_styles.uss"));
      return uxmlVE;
   }
}
```

```C#
<UXML xmlns:ui="UnityEngine.UIElements" xmlns:ue="UnityEditor.UIElements">
   <ui:VisualElement name="row" class="container">
       <ui:Label text="Tank Script - Custom Inspector" />
       <ue:PropertyField binding-path="tankName" name="tank-name-field" />
       <ue:PropertyField binding-path="tankSize" name="tank-size-field" />
   </ui:VisualElement>
</UXML>
```

```CSS
.container {
   background-color: rgb(80, 80, 80);
   flex-direction: column;
}
Label {
   background-color: rgb(80, 80, 80);
}
TextField:hover {
   background-color: rgb(255, 255, 0);
}
FloatField {
   background-color: rgb(0, 0, 255);
}
```
