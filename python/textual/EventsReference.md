# Events Reference

- AppBlur：app 失去 focus 时发送
- AppFocus：app 获得 focus 时发送
- Blur：widget 失去 focus 时发送
- Click：widget 被点击时发送
- DescendantBlur：child widget 失去 focus 时发送
- DescendantForcus：child widget 获得 focus 时发送
- Enter：鼠标进入 widget 时发送
- Focus：widget 获得 focus 时发送
- Hide：widget 隐藏时发送
- Key：按键事件
- Leave：鼠标从 widget 移除时发送
- Load：App 开始运行，但是 terminal 进入 application mode 之前发送
- Mount：widget 被 mount 时发送，此后 widget 开始接收 messages
- MouseCapture：当 mouse 被 captured 时发送，此后 mouse events 将一直发送到这个 widget，不管鼠标的坐标是否位于 widget 内
- MouseDown：鼠标 button 按下时发送
- MouseMove：鼠标移动时发送
- MoveRelease：captured 鼠标释放时发送
- MoveScrollDown：鼠标滚轮向下滚动时发送
- MouseScrollUp：鼠标滚轮向上滚动时发送
- MouseUp：鼠标按钮释放时发送
- Paste
- Print
- Resize：app 或 widget 被 resize 时发送
- ScreenResume：screen 变成 active 时发送
- Screenuspend：screen 变成 inactive 时发生
- Show：widget 第一次显示时发送
- Unmount：widget 被 unmounted 时发送，此后不再接收 messages

