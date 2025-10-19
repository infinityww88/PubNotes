# Numeric Input

按下transform快捷键后输入一个数字来精确地操作transform，enter确认，esc取消

也可以在Properties面板输入数字

- Simple Mode：只接收简单数字
  - Decimals(.)：可以输入小数点
  - Negate(-)：可以输入负号
  - Inverse(/)：1/num，2/=0.5，20/=0.05
  - Reset(backspace)：删除所有输入字符，回到初始状态，可以重新输入，但是再按一次backspace则取消输入数字模式，回到鼠标操作模式
  - Next/Previous组件(Tab/Ctrl-Tab)：输入多个axes的数据，G 1 + Tab 1 + Tab 1沿着每个坐标轴移动一个单位
  - Axis Locking + Number Input：G X 1
- Advanced Mode：可以输入表达式和单位
  - 使用=进入高级模式，Ctrl-=返回简单模式
  - Units(cm, deg, etc.)
  - 基本python运算符（+, *, /, **, etc.)
  - python数学模块的数学常量和函数（pi, sin, sqrt, etc.)
  - 仍然可以使用负数和倒数（-，/），但是必须按住Ctrl来激活它们
