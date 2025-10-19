# IMGUI common pattern

- 函数就是控件，调用函数就是创建了一个控件
- 组合函数就是组合控件
- 对于交互控件（处理输入事件）申请一个controlID
- 在函数最外层调用GetControlID，GUILayout，GUI绘制等函数
- 针对特定事件类型进行分类处理
- 如果有动态控件创建，调用GUIUtility.ExitGUI退出当前GUI循环，重新开始Layout，以将新控件加入进来
- IMGUI总是把任何事件发送给每一个控件函数
- 通过控件Rect是否包含鼠标位置和event.button==0判断鼠标是否在控件上按下
- 把controlId设置到hotControl上什么都不会发生，其他控件仍然能够收到任何事件，需要其他控件主动考虑hotControl并在hotControl不等于自身时忽略鼠标事件
- IMGUI只提供了实现GUI系统的基础设施，并不是完整的GUI系统
- 封装好的控件直接调用并使用返回值而无需处理任何事件
- 调用event.Used()，将事件类型修改为used，以便其他控件可以忽略事件
