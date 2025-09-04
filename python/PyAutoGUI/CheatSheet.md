PyAutoGUI 是一个跨平台 GUI 自动化模块。你可以控制鼠标和键盘，并只需基本的图像识别，来自动化完成计算机上的工作。

## 一般函数

```py
import pyautogui

pyautogui.position() # 返回当前光标的位置 (968, 56)
pyautogui.size() # 返回当前屏幕分辨率 (1920， 1080)
pyautogui.onScreen(x, y) # 判断 (x, y) 点是否在屏幕中
```

## 故障保险 Fail-Safes

在每个 PyAutoGUI 调用后设置一个 2.5 秒的暂停。

```py
pyautogui.PAUSE = 2.5
```

当 Fail Safe mode 为 True，当鼠标移动到屏幕左上角，会引发 pyautogui.FailSafeException 错误而终止程序。关闭命令如下（不建议关闭）：

```py
pyautogui.FAILSAFE = False
```

## 鼠标函数

XY 坐标的原点在屏幕左上角，X 向右，Y 向下

### 鼠标移动

```py
# 用 num_seconds 秒将鼠标移动到 (x, y) 的位置
x, y = 200, 100
num_seconds = 1
pyautogui.moveTo(x, y, duration=num_seconds)

# 用 num_seconds 秒将鼠标从当前位置移动 (xOffset, yOffset) 偏移
# 如果 duration 为 0 或未指定，则立即移动
xOffset, yOffst = 30, -30
num_seconds = 0.5
pyautogui.moveRel(xOffset, yOffset, duration=num_seconds) # Rel = Relative
```

### 鼠标拖动

```py
# 用 num_seconds 秒将鼠标拖动到 (x, y) 的位置，并释放鼠标
# 鼠标拖动是按下鼠标左键并移动
x, y = 200, 100
num_seconds = 1
pyautogui.dragTo(x, y, duration=num_seconds)

# 用 num_seconds 秒将鼠标从当前位置拖动 (xOffset, yOffset) 偏移
xOffset, yOffset = 30, -50
num_seconds = 0.5
pyautogui.dragRel(xOffset, yOffset, duration=num_seconds)
```

### 鼠标单击

