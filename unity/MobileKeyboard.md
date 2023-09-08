# Mobile Keyboard

当用户点击一个 editable GUI 元素时，虚拟键盘会自动弹出。也可以使用 TouchScreenKeyboard.Open() 手动开启 keyboard。

## Keyboard Layout 选项 (TouchScreenKeyboardType)

- Defalut: 字母键盘，可以切换到数字和符号键盘
- ASCIICapable: 字母键盘，可以切换到数字和符号键盘
- NumbersAndPunctuation：数字和符号键盘，可以切换到字母键盘
- URL：字母和 斜线/ .com 按键，可以切换到数字和符号键盘
- NumberPad：0-9 数字键
- PhonePad：用于输入 phone numbers 的键盘
- NamePhonePad：字母键盘，可以切换到 phone keyboard
- EmailAddress：字母和 @ 按键，可以切换到数字和符号键盘

## Text Preview

默认在键盘弹出后，会创建一个 edit box 在它上面，用于 preview 用户的输入，因此 text 对用户总是可见的。但是可以通过 TouchScreenKeyboard.hideInput = true 来关闭 text preview。注意这只对特定类型的 keyboard types 和 input modes 有效。例如，对 phone keypads 和 multi-line text input，hideInput 无效，virtual keyboard 总是可见。这是个全局变量，影响所有 keyboards。

## Visibility and Keyboard Size

- visible：如果 keyboard 在屏幕上 fully visible 则为 true
- area：返回 keyboard 的 position 和 dimensions
- active：如果 keyboard is activated 返回 true。它不是静态属性，必须通过 keyboard 实例访问这个属性

注意在 keyboard 完全可见之前，会返回 position 和 size = 0 的 rect。在 TouchScreenKeyboard.Open() 之后不能立即查询 rect。Keyboard 事件的序列是：

- TouchScreenKeyboard.Open() 被调用。TouchScreenKeyboard.active 返回 true
- TouchScreenKeyboard.visible 返回 false。TouchScreenKeyboard.area 返回 (0, 0, 0, 0)
- TouchScreenKeyboard 滑入屏幕，所有属性保持不变
- Keyboard 停止滑动，TouchScreenKeyboard.active 返回 true，visible 返回 true，area 返回 keyboard 的 position 和 size

## Secure Text Input

可以配置键盘隐藏输入的符号，用于输入一些敏感信息（例如密码）。

## Alert keyboard

可以配置键盘外观为黑色半透明背景，而不是传统完全不透明的键盘。
