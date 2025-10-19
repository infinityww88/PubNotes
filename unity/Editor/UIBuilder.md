# UI Builder

- UI Builder为UIElements可视化地创建和编辑UXML和USS UI资源
- Window/UI/UI Builder，或者双击uxml资源

## Explorer

- 访问打开文档的任何组件

### StyleSheet

- 在StyleSheet中创建选择器
  - StyleSheet列出main USS文档的所有USS选择器。使用它来创建和编辑selectors
  - 在StyleSheet中点击StyleSheet header(.uss)，Inspector中显示Selector输入框和CreateNewUSSSelector按钮，下面显示USS selector例子
  - 在selector输入框中输入有效的selector（示例中的任何一种），点击Create按钮创建一个选择器
- 在Explorer中直接创建selectors
  - 点击StyleSheet面板上方的Add new selector，会弹出和Inspector中一样的selector示例提示
  - 在Add new selector中直接输入要创建的selector，在States可以设置不同的pseudo state
  - 点击Add添加selector
- 可以将class selector直接拖拽selector到Viewport或者Hierarchy控件上，将这个class赋给这个控件
- 编辑selector
  - 选中一个selector，Inspector显示并编辑这个selector所有的style
  - 任何被selector选中的控件在Viewport中都会高亮
  - 修改selector的style，所有被这个selector选中的控件的显示都会相应地更新，除非控件上有更高优先级的style覆盖了这个selector的style，例如inline style
- StyleSheet的功能就是可视化编辑USS文件。因为USS就是包含一组selector: style的定义的文件，这个面板使得我们可以在GUI上创建selector并设置它的style，这与在文件中定义.myclass {color: red}是一样的

### Hierarchy

- Hierarchy显示UXML文档的实时dom树结构
- 选中一个元素，Inspector中显示这个元素的：
  - 控件特定数据
    - name，tabindex，focusable，bindingpath等等
    - 不同的控件有不同的数据
    - 所有控件从VisualElement基础一组相同数据
      - 所有控件都具有name属性，如果设置name属性，Hierarchy中元素以#name显示，否则一个controltype显示
      - 可以双击element编辑元素name
  - StyleSheet
    - StyleClassList：显示或添加style class
    - Matching Selectors：显示匹配的选择器selectors
  - Inlined Styles
    - 元素的inlined style
    - 在UXML文件中直接写在元素style属性的样式
- 右上角设置按钮弹出包含两个checkbox的菜单
  - 选中type：元素总是以controltype显示，如果有name，显示controltype#name
  - 选中class list，每个元素名称后面显示其属于所有style class

## Library

- Library面板和Unity的Project窗口类似，列出可用的UI elements
  - Unity部分列出Unity提供的标准elements。这些element包含标准所有被支持的Unity Editor和运行时主题的styling
  - Project部分列出项目中自定义的.uxml。还列出继承自VisualElement并且具有它们的UxmlFactory设置以从UXML实例化的C#元素
- 实例化一个元素
  - 将它从Hierarchy拖动到Explorer面板
  - 将它拖拽到Viewport
  - 双击它，将它添加为当前选中元素的兄弟元素如果没有任何元素被选中，这个元素将添加到root元素

## ViewPort

- Viewport在一个UI Builder提供的可以调整大小的编辑模式Canvas上显示一个UXML文档的输出
- 标题显示当前加载的document，星号表示文档有修改未保存
- toolbar包含UI Builder命令菜单，Viewport设置，和Preview按钮
- Viewport是你编辑，预览，以及与UI交互的地方

### Viewport toolbar menus

- File
  - 创建一个New文档
  - Save/Save AS当前文档
  - Open一个文档

### Resizing the canvas

- 在Viewport中拖动canvas的左、右、下handles
- 在Hierarchy中选中文档root元素，Inspector中显示Canvas的设置
  - Canvas Size：width/height，调整canvas大小

### Interacting with UI in the Canvas

- 在Canvas中选中UI元素
- 如果元素的Position>Position设置为Relative，只能调整它的height和width
- 如果元素的Position>Position设置为Absolute，可以完全控制它的大小和位置
- 不建议使用Absolute positioning，因为它忽略了UIElements的自动布局系统

### Setting a background

- 可以设置编辑时Canvas的背景，这个背景只在UI Builder中编辑UI时有效，与最终生成的UXML无关
- 在Hierarchy选中root元素
- 在Inspector中选择Canvas Background
  - None：没有背景
  - Color：纯色背景
  - Image：图片背景
  - Camera：实时camera渲染背景，这通常用于在不启动游戏是查看运行时UI

### Previewing UI

- 预览UI，点击控件不再是选择元素, 可以真正和UI交互，例如点击按钮，切换tab，输入文本

## Code Previews

- 显示UI Builder自动生成的UXML和USS文本

## Inspector

- 与Unity Editor Inspector一样，可以查看和修改element或selector的属性和样式

### Editing an element's attributes

- 当选中一个元素时，在Inspector的Attributes部分可以修改的它的UXML属性（例如Name，Tooltip，Text）
- 属性是每元素不同的，不能共享
- Attributes部分header显示element的类型，如果选中的是element，而不是USS selector

### Editing an element's StyleSheet

- USS selectors允许在多个不同的元素之间共享style。当修改一个shared的样式，所有被这个selector选中的元素都会自动更新
- USS selectors可以通过name，class，C# type，3者组合，父子关系匹配
- 最简单的共享style的办法是创建一个style class和对应的selector，将这个class赋给不同元素
- 添加style class到元素
  - 选中元素
  - 在Inspector中，在Style Class List中输入style class名字
  - 点击Add Style Class To List按钮为元素添加style class
  - 如果基于class的selector以及存在，可以立刻看到style应用的效果
- 为style class创建selector
  - 在元素的Inspector中，StyleSheet>Style Class List部分为元素的每一个style class显示一个pill
  - 双击一个pill，在Explorer/StyleSheets中创建对应这个class的selector，如果这个selector以及存在则会选中它
- 从元素的inlined style创建一个selector/style class
  - 在元素的Inspector中的StyleSheet>Style Class List部分，输入新的class selector的名字
  - 点击Extract Inlined Styles to New Class按钮，创建一个新的class selector，并且将相应的style class添加到当前element
- 从elements中移除styles
  - 在元素的StyleClassList pill上点击X，删除对应的style class
  - 可以移除Unity为标准控件添加的默认style class，例如unity-text-element，unity-button

### Editing inlined styles for element

- 选中一个元素时，可以在Inspector的Inlined Styels部分编辑元素的内联样式
在UXML文档的元素中的style属性上
- 对于元素，inlined styles覆盖来自StyleSheet样式表中的样式，保存在UXML文档的元素中的style属性上
- 对于USS selectors，inlined styles，保存为样式表中的selector对应的样式规则中
- 当修改了一个元素或USS selector的inlined styles时，对应style属性及其所有祖先属性名字的左边显示一个实色边框块，并且名字变成粗体，标识这个属性有所修改
