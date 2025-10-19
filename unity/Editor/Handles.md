# Handles

## Overview

- 不涉及3d空间transform的数值编辑，直接在Inspector中调整就可以了，Handles是用来直观地操作那些涉及3D transform的数值编辑的工具，因为在Inspector中修改transform的数值然后再SceneView中观察修改的结果很不直观

## How to use Handles

- Editor.OnSceneGUI message
- 订阅SceneView.onSceneGUIDelegate来实现自己的OnSceneGUI
  - EditorWindow
  void OnEnable() {
      SceneView.onSceneGUIDelegate += onSceneGUI;
  }
  void OnDisable() {
      SceneView.onSceneGUIDelegate -= onSceneGUI;
  }
  void OnSceneGUI(SceneView sv) {
      //Draw your handles here
  }
- 这个方法还可以允许访问SceneView，SceneView中包含大量操作SceneView的功能，这些就是你再Editor中使用的各种能影响SceneView功能的API接口
  - audioPlay：是否开启SceneView中的audio effects
  - cameraMode：SceneView中的摄像机模式
  - drawGizmos：是否绘制Gizmos
  - in2DView：是否切换到2D模式
  - 总之能再Editor界面中能找到的修改SceneView状态的功能在这里都能找得到响应的API
- 一旦你拥有了一个Handles的上下文，你只需要选择Handles中的哪一个handle
- 有一些Handle的设置不能通过参数传递给handle函数，它们通过全局状态进行传递，就像GUI.color, Gizmos.color一样
- Handles包含一组HandleCap函数，可以用来绘制各种handle的抓取grab部分，包括：
  - ArrowHandleCap
  - CircleHandleCap
  - ConeHandleCap
  - CubeHandleCap
  - CylinderHandleCap
  - DotHandleCap
  - RectangleHandleCap
  - SphereHandleCap
- Handles有一个函数委托CapFunction，所有HandleCap函数都是这种委托类型。一些Handle使用这个委托绘制cap（handle capture），因为委托中可以注册多个cap函数，因此你可以让一个handle拥有多个cap（sphere，cube，cone等等）
- 在Handles类中，有3组函数以及一些utils函数
  - Draw函数
    - 这些函数绘制一些东西到当前Handle camera，可以使用它们来调试和改善工具的可视化表示，但是它们不与用户输入交互
  - Cap函数
    - 这些函数用于同时操作handle的可视部分和控制部分。它们在两个事件passes中采取行动，Layout和Repaint
      - Layout：它们调用HandleUtility.AddControl函数来记录mouse到可视图形的距离
      - Repaint：它们绘制各自的可视图形表示
  - Handle函数
    - 这些函数在cap之上提供了封装好的handle，可以直接被使用的handle。Cap只是用来实现Handle的组件（函数），不能直接使用。这些Handle是封装好的handle。它们生产ControlID，捕获和handle相关的事件，并使用controlID调用cap函数，然后返回handle操作的数值。例如FreeMoveHandle允许它的cap 函数在scene view的3d空间中被拖拽，并返回更新的位置，这个位置就可以被用来赋予任何需要位置的对象，如此，这个对象就可以被FreeMoveHandle在SceneView中直接编辑了
- Handles实现被鼠标抓取（点击并拖拽）不是通过collider实现的，而是通过比较当前鼠标到handle cap的距离来判断的，可以认为是2D的碰撞计算（圆形碰撞，半径），因此每个Cap向Handles报告鼠标到它的距离（买个cap有各自的形状，因此需要每个cap自己计算并报告这个距离），然后Handles判断当前哪个handle被抓取，这个handle就成为当前被选中的handle了，之后的输入事件全部发送给这个handle。这就是为什么cap函数需要一个controlID，与IMGUI的controlID是相同的，用来标识一个控件，并把输入事件只发送给当前被抓取的controlID（即hotControl）。因此每一个和输入交互的handle cap都需要申请一个controlID（等价于IMGUI的交互控件）
- HandleCap函数的size参数是世界空间中的units。如果size保持static的话，那么随着handle距离摄像机的变化，handle cap的大小也随之变化（它们只是普通的3D空间中的mesh而已）。通过调用 float HandleUtility.GetHandleSize(Vector3 position)，可以得到一个与距离无关的cap大小，无论摄像机距离cap如何变化，cap总是保持相同size
- OnSceneGUI中，内置的Handle也使用GUIUtility.GetControlID获得controlID，基于GUI.changed记录判断状态是否有所修改（进而可以使用EditorGUI.BeginChangeCheck/EditorGUIEndChangeCheck），通过Undo.RecordObject来添加Undo history。Handles本质上只是提供了3D空间中的control绘制和基于距离的hotControl判断的功能（对应IMGUI的GUI 2D绘制和基于Rectangle的hotControl判断功能），仅此而已，剩下所有的GUI功能都依然依赖IMGUI。可以认为，IMGUI在control绘制和判断hotControl的部分分为了2D和3D两个分支，前者就是普通的2DGUI，后者就是SceneView中的3DGUI，但是除此之外的所有GUI基础设施仍然是一套。因此Handle（3DGUI）和2DGUI除了绘制和判断热点不同之外，是完全相同的
  - 绘制
    - Handle通过Handles.Draw和Handles.HandleCap绘制
    - IMGUI通过GUIStyle.Draw绘制
  - 判断是否选中
    - Handle在Layout事件中通过AddControl报告鼠标到handle的距离，在其他事件时，nearestControlId就是Handles认为被选中的handle，每个handle函数通过判断nearestControlId是否等于自身的controlId判断自己是否被选中
    - IMGUI通过GetRect获得控件的Rect，通过计算鼠标位置是否在矩形中判断自己是否被选中
- 一些Draw和Cap函数不能修改可视图形scale，但是有一个简单的办法改变它：DrawingScope。所有Handle的绘制都是在Handles.matrix中进行的。DrawingScope允许在一个代码块中临时设置Handles.color和/或Handles.matrix，并利用析构函数在离开作用域时自动将它们恢复为之前的值。Handles.matrix就是最终的矩阵，不像OpenGL中的矩阵堆栈（最终矩阵是矩阵自顶向下相乘的结果），因此设置Handles.matrix时要注意设置最终矩阵。例如如果向基于某个object的局部坐标系绘制handle，应该将Handles.matrix设置为transform.localToWorldMatrix。这也是唯一可行的方式，如果使用矩阵堆栈，当切换操作对象时，如何记得之前的对象应该从堆栈中弹出哪些矩阵
- HandleUtility.Repaint可以用来重新绘制当前camera，如果有不需要用户输入自动移动的动态handle
- 如果需要从当前鼠标位置发射射线，使用HandleUtility.GUIPointToWorldRay
- 如果需要计算世界位置在屏幕空间中的位置，使用HandleUtility.WorldToGUIPoint
- Handle(3Dgui)与2Dgui是IMGUI的两个自部分，前者是3D空间中数据编辑工具，后者2d界面上的数据编辑工具

## 创建自定义Handles

- int controlId = EditorGUIUtility.GetControlID(controlIdHash, FocusType.Keyboard);
  - GetConntrolIDs是EditorGUIUtility从GUIUtility继承而来
  - 第一个参数是一个id生成的提示，最好将其设置为你的handle的名字的hash值 "Free2DMoveHandle".GetHashCode()
  - 第二个参数指出这个control是否可以捕获键盘焦点（当这个control激活时，将收到键盘事件）
- switch (Event.current.type)
  {
    case EventType.MouseDown:
      // check if the nearest controlId == this controlId
      // if so, set the hot control and keyboardControl
      break;
    case EventType.MouseUp:
      // check if i'm controlled, hotControl == this controlId
      // if so, set hotControl = 0
      break;
    case EventType.MouseDrag:
      // if i'm controlled, hotControl == this controllId, move the point
      break;
    case EventType.Repaint:
      // draw point visual
      break;
    case EventType.Layout:
      // register distance from mouse to my point, so Handles can calculate the nearest controlId
      break
  }
- 每个GUI循环中，Layout Pass最先执行，handle在这里计算鼠标当cap的距离，调用HandleUtility.AddControl(controlId, distance)进行报告。HandleUtility.nearestControl在Layout pass中所有handle报告的距离时记录最小距离的控件。nearestControl在接下来的pass中（MouseDown）被用来判断自己（handle）是否被选中。AddControl在每次GUI循环中总会执行，不依赖于当前的事件。因此在MosueDown pass中，需要判断是否是鼠标左键按下同时handle是距离鼠标最近的control，作为handle被选中的依据。如果handle被选中，将hotControl和keyboardControl设置为handle的控件ID，这样接下来的GUI循环中鼠标和键盘事件总是发送给这个控件，直到hotControl和keyboardControl被重置为0
- Event.Use()将Event.current.type设置为EventType.Used。对于每个事件，GUI pass都会自定向下调用GUI函数，通知每个控件处理事件。对于输入事件，如果一个control（尤其是hotControl）使用的事件，并且不想其他的control再处理这个事件，就调用Use将事件设置为Used，这样的其他的GUI control就会忽略这个事件，类似于dom中的stopPropagation，只是其他control仍忽然会被调用GUI函数(EventType = used)
- 再Layout中调用AddControl报告鼠标到handle的位置，HandleUtility有一些辅助函数帮助完成计算。例如 float DistanceToRectangle(Vector3 position, Quaternion rotation, float size)，接受一个Rectangle在世界空间中的位置，旋转，和大小，计算鼠标指针到矩形的屏幕空间像素距离
- 自定义显示
  - 在Repaint pass，你需要绘制你handle的图形。有多种方式可以绘制，依赖于你想画什么
  - 如果你想绘制动态的几何图形geometry，就必须使用legacy Opengl instant模式（它是旧有的并被标记为过时的方式，用来在render loop中绘制objects，但是unity仍然在editor中使用它，或许因为用它绘制一些简单的动态图形更简单）
  - 如果你只使用静态的几何图形，你可以简单地使用一个mesh，通过Resources.Load和EditorGUIUtility.Load加载它，并使用Graphics.DrawMeshNow绘制它，Mesh方式明显被legacy Opengal快（10x左右）即使在每次Repaint frame时从头开始创建mesh，但是生成mesh的过程很繁琐，因此opengl在绘制动态简单的图形时更加方便
- GL.Begin(GL.QUADS);
  {
    GL.Vertex(pos0);
    GL.Vertex(pos1);
    GL.Vertex(pos2);
    GL.Vertex(pos3);
  }
  GL.End();
- 仅做完这一步是看不见图形的，因为赋予geometry的材质来自于被editor绘制的最后一个object，因此你必须在GL.End()之前赋予geometry以材质。首先需要有一个material（它可以从资源中加载，也可以在运行中创建。一旦你拥有了一个材质，你需要调用SetPass函数来绑定材质，SetPass指定使用material中的哪个shader pass进行绘制（对于multiple pass shader）。对于普通单pass shader的材质，只需要传递0即可。如果需要使用每个vertex的uv，则应该在每个GL.Vertex之前调用GL.TexCoord2(uv.x, uv.y)设置顶点的uv。同样如果使用顶点颜色，对每个vertex调用GL.Color(color)，但需要你的材质支持逐顶点颜色。
- Unity绘制Mesh的过程是：
  - mesh包含模型各种信息：顶点位置，顶点vu，顶点颜色，顶点法向量，每个三角形/四边形使用的顶点索引
  - material包含绘制的各种渲染管线状态信息，使用的shader程序，传递给shander的各种参数（纹理，颜色等等）
  - Unity通过material设置渲染关系的当前状态，然后从mesh中取出顶点信息，依次发送到渲染关系，这样图形就被绘制出来了。正常情况下，这些过程都是自动的，我们只需要设置mesh和material就可以了。使用Legacy Opengl绘制是把这个过程显式地执行了一遍，仅此而已。GL.Begin设置当前绘制的图元类型，使渲染管线知道如何将输入的顶点组装成图元（三角形还是四边形）。GL.Vertex/GL.TexCoord2/GL.Color向渲染关系发送顶点数据，Material.SetPass和material本身无关，不是设置material本身的，而是将这个material shader的某个pass以及material的数据设置到渲染管线上，即修改渲染管线的当前状态（应该称为SetPassToPipeline）。最后GL.End向渲染关系发送绘制命令，绘制当前geometry。Graphics.DrawMeshNow相当于将GL.Begin/GL.End这段向渲染管线发送顶点数据的部分封装起来而已
- 当控件/handle操作的对象数据有所变化时，设置GUI.changed=true非常重要，如果你想你的handle支持Undo/Redo的话。但是如果你使用SerializedObject/SerializedProperty时，就不必手工考虑这些事情了，它们的代码已经包含了这些处理了
- Undo/Redo在创建新的工具（以及任何software）时非常重要。如果它没有实现好，将会毁掉用户体验。Unity的Undo/Redo只支持unity objects和派生类的对象。AnimationCurve和Vector3等是结构体，不是objects，因此无法使用undo/redo系统，需要将它们保持到一个object中，然后依赖这个object实现undo/redo。Handle/IMGUI控件本身没有undo/redo，是哪些它们操作的数据支持undo/redo，Handle/IMGUI控件只是实时地显示这些数据而已，这就是为什么说SerializedObject只是在操作数据，而不是操作UI元素，即使没有UI，SerializedObject也在支持数据的undo/redo
- GUI.changed和GUIUtility.hotControl一样，只是简单的变量而已，并没有什么特殊的功能，是使用它们的Handle/GUI控件在利用它们实现GUI功能。一个控件标记GUI.changed是在向外部使用的函数通知，这个控件修改了数据，但是控件自身不知道修改的数据是什么，因此让上层函数自行处理。上层函数知道这个控件修改的是什么数据，如果是重要的数据，通过读取GUI.changed就知道这个数据被修改了，因此可以将它记录到Undo history中
- Undo.RecordObject(object, "desc")将object当前状态记录到Undo history中，然后将控件修改后的数据设置到object中，这样当按下Ctrl-Z或者点击Edit/Undo时，将从undo history中得到之前的object的数据，并将其恢复到object中
- GenericMenu，动态创建Editor菜单
- InitializeOnLoad属性装饰一个类，这个类将会在Editor中加载并运行，而在类的静态构造函数中，可以注册SceneView.onSceneGUIDelegate，这样我们就不需要创建一个Editor/EditorWindow脚本，就可以绘制SceneView了。Editor脚本需要在GameObject被选中时才绘制SceneView，而EditorWindow则需要window打开时才绘制SceneView
- [InitializeOnLoad]
  public class SnapHandleEditor {
      static SnapHandleEditor() {
          SceneView.onSceneGUIDelegate += OnSceneGUI;
      }
      static void OnSceneGUI(SceneView sv) {
          //draw scene view
      }
  }
