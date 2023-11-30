C# 中任何 MonoBehavior 脚本出现的异常都被捕获，并打印错误日志，然后程序继续向下执行，因此不会导致整个程序崩溃，但是因为很多逻辑可能都没有执行，很多变量也没有初始化，因此继续执行还是会导致很多错误，例如变量未初始化导致的空指针引用。
在编辑器中，抛出异常时，还会触发 Debug.Break，暂停 play mode，并打印错误日志，但是点击 resume 按钮之后仍然可以继续执行。

默认一个 VisualElement 不接收 keyboard events。只有 focusable 和当前具有焦点的
VisualElement 才接收 keyboard events（因为 keyboard 先 trickling down 然后
bubbling up，因此接收 keyboard event 的元素的 parent 也会接收到 event）。

简单的说，使元素 focusable=true 并使用 element.Focus()
使它具有焦点，足可以使它接收 keyboard events。 

UIToolkit 使用 InputSystem 开启 TouchSimulation 后，UIToolkit 的 :hover
伪类将不能工作（开启 TouchSimulation 意味着要为移动平台 build，:hover
没有意义）。

GameView 切换到 Simulator（模拟各种移动设备分辨率）后，:hover 也不会工作。

UIToolkit 的元素都是 rect 的，当旋转 element 时，旋转的是整个矩形。如果在
:hover 时触发元素的 transform 旋转而且 cursor 在 rect 的角落时，rect
旋转可能导致 cursor 离开 rect，切换到非 :hover 状态，rect
则反向旋转回来，然后有导致 cursor 进入
rect，重新开始旋转，这样来回切换导致元素不断抖动。解决办法有两个：

- 定义一个 parent 元素，它的矩形固定不动，在其上定义 :hover，然后 :hover
  时旋转 child 元素（负载 css selector 也可以指定伪类）
- 自定义 VisualElement 元素，重写 bool ContainsPoint(Vector2
  localPoint)，使元素判断一个点是否在元素内变成一个 Circle，而不是默认的
Rect

  ```C#
  public class MyButton : Button
  {
  	public new class UxmlFactory : UxmlFactory<MyButton, Button.UxmlTraits> {}
  	
  	public override bool ContainsPoint(Vector2 localPoint) {
  		float width = this.resolvedStyle.width;
  		float height = this.resolvedStyle.height;
  		Vector2 mid = new Vector2(width/2, height/2);
  		Vector2 d = localPoint - mid;
  		//Debug.Log($"{localPoint} {mid} {d}");
  		float radius = Mathf.Min(width, height) / 2;
  		return d.magnitude <= radius;
  	}
  }
  
  ```

  完全自定义一个控件非常麻烦，但是可以直接继承一个现有控件，只重写
ContainsPoint 即可。而且这样的自定义控件可以直接出现在 UIBuilder
的控件库中被使用。

Background 不是 content。元素的 background image
从不决定元素的大小，元素的大小只被自身 width/height 或子元素元素的内容决定。background image
只是在元素大小确定之后，绘制在背景上。当 image 的 aspect 和
元素大小不匹配时，有 3 中缩放方式：

- fill：无视 image 的 aspect，直接缩放到元素大小
- crop：保持 image 的
  aspect，是最小的维度（宽或高）匹配到元素大小，另一个将超过元素矩形而被剪裁
- fit：与 crop 相反，保持 image 的
  aspect，使最大的维度匹配到元素大小，另一个总会小于等于元素的大小

background 还可以自定义九宫格区域（定义左上右下的距离），如果 background 选择 sprite 还可以直接使用
sprite 定义的九宫格区域。

background 覆盖元素的内容区域，不包括 margin。

元素的大小被自身的 width、height 或子元素的内容决定。margin 定义元素 border
之外的空白区域，padding 定义 border 内部的空白区域。

如果定义一个 position=absolute 元素，要使它扩展到整个 parent 的 rect
区域，定义 flex-grow 是不够的，因为 absolute 元素已经不在 flex
布局流中了，要设置 wdith=100% 和 height=100%。

list view 中元素的高度被元素的 itemHeight 控制，而不是 item 元素自身。

有一些伪类只被特定交互控件处理，因为这设计控件的处理 code，而不是任何一般的
VisualElement 都支持它们，例如 :active, :selected。

VisualElement 的 SetEnable 只影响元素是否能进行交互，要控制元素 disable
的外观，使用 :disabled。:disabled 对应 SetEnable(false) 的 VisualElement。

IEnumerable 的遍历要使用 Linq（Select，Where，Filter，First，Last 等等）。

