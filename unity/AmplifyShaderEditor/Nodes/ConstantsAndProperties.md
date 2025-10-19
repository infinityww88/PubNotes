# Constants And Properties

## Color Node

- float4
- 定义shader中的常量，或者暴露为Property（在Material Inspector中调整）
- 类似Vector4 Node，但是通过color picker修改颜色
- Type
  - Constant
  - Property
  - Instanced Property
  - Global：只能通过script设置，static变量，被所有shader共享，全局修改一个颜色
- Name：Property名字
- Variable Mode
  - Create：在当前shader创建Property或Global变量
  - Fetch：使用included cginc中全局变量
- Auto-Register：即使没有连接Output端口，也创建Property/Global变量
- Precision：定义变量使用的bytes，决定值的精确度
  - Float
  - Half
- Default Value：创建新material使用的默认值
- Property Name：shader真正使用的变量名，使用Name参数自动生成，不可编辑。移除特殊字符、空白，开头添加下划线（“My Property Name”变成“_MyPropertyName“）。只对Property、Instanced Property、Global类型有效，标识script使用的变量名
- Material Value：当这个shader被一个material使用时，表示这个属性在material中的值
- Hide In Inspector：在material inspector中隐藏该属性
- HDR：标识这个属性期望一个high-dynamic range（HDR）值（128位，每个颜色channel32位）
- 输出float4

## Float Node

- float常量或变量
- Min Max

## Global Array Node

- 创建和访问一个global数组
- Type，Array Length，Name
- Type：Float，Color，Vector4，Matrix4x4

## Int Node

- int常量或变量

## Matrix3x3 Node/Matrix4x4 Node

- 不能作为Property，只能是Constant/Global
- 用于不同坐标空间转换
- 对大多数转换矩阵已经被特定节点提供，例如Object To World或者World To Object

## PI Node

- 输出PI以及一个系数的乘积

## Tau Node

- 输出2*PI

## Template Parameter Node（TODO）

- ASE允许自定义shader模板，模板中可以包含很多定义好的Properties和Global Variables
- ASE在核心功能就是可视化编辑shader模板
- Template Parameter允许动态访问shader模板中的Properties和Global Variables
- 节点的输出根据引用的引用的变量类型自动变化

## Vector2/3/4 Node
