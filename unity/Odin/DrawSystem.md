# Odin draw system

## Overview

通过仅仅继承一个类，你就获得了访问 odin 完整而强大 drawing system 的能力。你不在需要担心你的窗口如何绘制，而是只需要关注真正重要的事情：它们应该提供的功能。

通过简单地继承 OdinEditorWindow，而不是 EditorWindow，你就获得了在 window 中渲染 fields，properties，和 methods 的能力，而无需编写任何自定义 editor GUI code，和使用 Odin 定制 inspector 一样。使用 attributes 设计你的 editor window，就像它一个 MonoBehavior 或者 ScriptableObject，可以使用 Odin 和 Unity 所有可用的 attributes。

你可以覆盖 GetTarget 方法，为它赋予任何类型的任何示例进行渲染。它不需要是可序列化的，甚至不必是一个 Unity object，你有完全的控制权。

继承 OdinMenuEditorWindow，而不是 OdinEditorWindow，可以很容易地为项目数据建立一个强大，良好组织的 editor overview，在坐标具有 navigation menu。

OdinMenuTrees 非常强大和灵活。你可以很容易地定制 menu tree 的外观。

Drawer chain system 让 Odin 可以组合小的，模块化的简单绘制代码。

模块化的核心是契约，使得 clients 十分清楚什么可以假设，什么不可以。在 IMGUI 模块中，契约就是 rect，使得任何其他 GUI 控件知道这个 UI 占据的控件，但是不关心它如何使用这个空间。

Odin Serializer 提供一个可扩展的，简单明了的 API，你可以用来实现自己的复杂功能，例如保存游戏等等。

使用 Odin Validator，你可以很容易地扫描整个 project，查找 warnings 和 errors，并在 validator 中 inline 修复它们。

## Make an OdinEditorWindow

通过继承 OdinEditorWindow 而不是 EditorWindow，你可以使用和制作 inspector 一样的方法制作 Unity editor windows：只使用 attributes。

Odin 使用 attributes 隐藏或生成渲染 UI 控件的 IMGUI code，因此你不需要像传统方式那样手动编写它们。但是你仍然可以混合 Odin-drawn 属性和 hand-writen IMGUI code，通过 OnInspectorGUI

你不应该覆盖 OdinEditorWindow 中的 OnGUI 方法，相反地，如果你想要注入自定义 GUI code，则你可以覆盖 DrawEditors 方法，或者你可以在一个自定义 GUI 方法上使用 OnInspectorGUI 属性。

如果你必须覆盖 OnGUI 方法，则确保调用 base.OnGUI()。否则，将不会发生 Odin 魔法，你则基本上在编写一个常规的 EditorWindow。

## Create Custom Drawers

- Declare attribute itself with necessary member fields
  - public class HealthBarAttribute : Attribute
- Creating actual drawer in Editor folder, inherit from OdinAttributeDrawer\<TAttribute>
  - public class HealthBarAttributeDrawer : OdinAttributeDrawer<HealthBarAttribute, float>
- override the DrawPropertyLayout method
  - draw the normal float field for the property first
    - manually call SirenixEditorFields.FloatField to draw this
    - call the CallNextDrawer method
      - This goes into Odin's drawer chain and allows for the combination of different attributes to realy customize the inspector
  - draw custom things using IMGUI code (EditorGUILayout/SirenixEditorGUI)

## Create a custom value drawer

- Create a simple custom Odin value drawer for a custom struct type(or any type).
- Value drawers are the most basic types of drawers in Odin, and are often the drawers that actually end up doing the final drawing of a property in the inspector. For this reason, they are often among the last drawers in the drawer chain, and will usually not continue the chain.
- Create drawer class inherits from OdinValueDrawer\<TStruct>
- override DrawPropertyLayout method
  - EditorGUILayout.GetControlRect() get area to draw in. This also lets our drawer work with the rest of Unity's IMGUI system
  - Get the current value of the property from ValueEntry.SmartValue. We can also use this property to assign any changes.

## Make a custom group

- Odin comes with many built-in group attributes
- Create a group attribute that can be used on any field, property or method and can be combined with Odin's other group attribute using **group paths**.
- Define group attribute itself first, inherit from PropertyGroupAttribute class.
  - C# does not allow passing custom structs directly to attribute constructors.
  - need a **group path** parameter passed into PropertyGroupAttribute
  - Override CombineValuesWith method. This method is called for all attributes with the same path
    - Parameter: PropertyGroupAttribute other
- Create the group drawer class in editor folder, inherit from OdinGroupDrawer\<TGroupAttribute>
  - Have a persistent state by getting a LocalPersistentContext\<T> from Odin's persistence system. If enabled, that will save the state of the drawer between Unity reloads and even opening and closing the editor
    - private LocalPersistentContext\<bool> isExpanded;
    - this.GetPersistentValue\<bool>
- override DrawPropertyLayout method
  - Use EditorGUILayout/SirenixEditorGUI to draw GUI (Begin()/End())
  - this.Property.Children.Count
  - this.Property.Children[i].Draw();

## Use PropertyTree

- By using the propertyTree class, you can implement the full power of Odin's drawing system: attributes, property resolvers, and everything else, pretty much anywhere you need it.
- Using the PropertyTree is very straightforward: use one of the *PropertyTree.Create* methods to create an instance for your target object, and then just call the Draw() method every frame.
  - this.myObjectTree = PropertyTree.Create(this.myObject);
  - this.myObjectTree.Draw(false)
  - It is important that you retain the reference to the original created tree. Do not call PropertyTree.Create every GUI call.
  - You can create a PropertyTree for multiple targets, and edit them all at once.
    - this.mutliTargetTree = PropertyTree.Create(this.myObjectArray);
    - this.mutliTargetTree.Draw(false);
  - when creating the PropertyTree you have the option of inserting your own custom OdinPropertyResolverLocator and OdinAttributeProcessorLocator instance. This lets you pretty much completely customize how the PropertyTree handles properties and attributes.

## Understanding Generic Contraints On Odin Drawers

- 基于范型使用Odin Drawers
- When inheriting from an Odin drawer class, such as OdinValueDrawer, you can use C#'s generic constraints to specify which type and values you want the drawer to draw
- Just like how to use Generic in Collection, you cannot use a Generic class type to reference a derived-class type directly, you need to declare that in generic constraints
  - public class GenericItemDrawer\<T> : OdinValueDrawer\<T> **where T : Item**
  - The same rule also applies to abstract classes and interfaces, you cannot use them as Generic Type parameter, but need to declare generic type parameter take any class that extends this abstract class or implements this interface.

## Tips, Tricks, Best Practices

- Usings IMGUI's layout system is great for many usecases, but often it is simpler to just get a single Rect and use math to manipulate and place elements manually with the Rect. As a bonus this will also result in much faster drawing code as opposed to using layout groups.
- Odin defines a lot of helpful extension methods for the Rect struct that are useful for this kind of manipulation and positioning.
- With Unity editor drawing system, you can
  - Create PropertyDrawer for a type (custom appearance of any field of that type)
  - Create PropertyDrawer for a attribute(custom appearance of any field applied with that type)
  - Create Custom Inspector Editor for a MonoBehaviour(inherit Editor)
  - Create general Editor Window, which is not for inspecting a specific object, but using some data to do/preview something
- With Odin drawing system, you can
  - Create an attribute drawer for a attribute (custom appearance of any field applied with that attribute)
  - Create an type drawer for a type (custom appearance of any field of that type)
  - Create general editor window
  - Custom Group attribute, odin only, to control how to layout a group of fields with same group path
  - Odin attribute/type drawer are used both in inspector window or custom editor window
- In Odin, the PropertyTree and InspectorProperty types correspond to respectively Unity's SerializedObject and SerializedProperty types, and provide similar functionality. Just like Odin exposes its serialization mechanism with SerializeUtility, so you can use it anywhere you need, not just in Odin serialization system. Odin drawing system exposes its drawing mechanism with PropertyTree, so you can use it anywhere you need, not just in Odin drawing system. For example, you can create a Unity EditorWindow that contains a few fields, but instead manually draw these fields with IMGUI utilities, you can just create a PropertyTree and pass all the fields to it as parameter, then in the OnGUI callback method, you only need to call PropertyTree.Draw(), all the fields will be drawn in Odin way just like in Inspector, and all the fields can use all the odin attribute to custom their appearance and layout, so cool.
- PropertyTree is how odin exposes its draw mechanism, it is not a custom mechanism, but is a building block to build a custom mechanism.

## AttributeProcessor

- Attribute affect code in a extendsion way just like C# Extension Methods.
  - Extension methods enable you to "add" methods to existing types without creating a new derived type, recompiling, or otherwise modifying the original type.
  - Extension methods are a special kind of static method, but they are called as if they were methods on the extended type.
  - The most common extension methods are the LINQ standard query operators that add query functionality to existing System.Collections.IEnumerable and System.Collections.Generic.IEnumerable\<T>.
  - Extension methods are defined as static methods but are called by using instance method syntax. Their first parameter specifies which type the method operates on, and the parameter is preceded by the this modifier. However, the intermediate language (IL) generated by the compiler translates your code into a call on the static method.
  - Because extension methods is just static method outside class, it cannot access private variables in the type they are extending.
  - Extension methods are only in scope when you explicitly import the namespace into your source code with using directive.
  - Attribute doesn't modify the original code they apply to, but define data and behaviour in a separate place, this is called Aspect-oriented programming.
- Odin not only just let you apply odin attributes to class/struct in literal way, but also in programmable way - Custom attribute processors.
  - Dynamically add, edit and remove attributes and even completely change the layout of the inspector according runtime context of application.
  - public class MyProcessedClassAttributeProcessor : OdinAttributeProcessor\<MyProcessedClass>
  - Override ProcessSelfAttributes method. Odin call this method for any fields or properties of the MyProcessedClass type.
    - AttributeListExtension utility class ot operate property's attribute list.
  - Override ProcessChildMemberAttributes method. Odin call this method for all direct child properties of the MyProcessedClass property.
  - When odin prepare draw gui for MyProcessedClass, it will not just check out the literal attributes, but also call the processor to modify the attribute list, and the result is the final attributes for the MyProcessedClass.
  - OdinAttributeProcessor only work with inspector attributes(and so in editor window). This system doesn't affect serialization
    - Adding or removing *serialization attributes* will result in nothing.
    - Odin will even ignore attributes such as SerializeField and OdinSerialize in the attribute list when determining whether it should draw a member.
    - Serialization attributes will be fetched directly from the inspected members in question, completely by passing the processor system.
- PropertyTree is where Odin exposes its drawing system totally. It contain all odin drawing features, attributes, property resolvers and everything else, pretty much anywhere you need it. When creating the PropertyTree you can inserting your own OdinPropertyResolverLocator and OdinAttributeProcessorLocator instance, by which you can specify custom policy to provide PropertyResolver and AttributeProcessor according concrete runtime context. If you don't use custom implement, PropertyTree will fallback to a default implement.
  - InspectorProperty represents a property in the inspector, and provides the hub for all functionality related to that property
  - OdinPropertyResolver responsible for bringing the member into the property tree, **what is it??**
  - PropertyTree represents a set of values of the same type as a tree of properties that can be drawn in the inspector, and provides an array of utilities for querying the tree of properties.

