快捷键

OS X 上用 cmd 键代替 ctrl.

# Cursor navigation（所有这些都会清空当前选择的文本）

- 箭头键：移动光标
- 鼠标点击：设置光标位置
- Ctrl + LeftArrow 和 Ctrl + RightArrow：移动光标到前一个或下一个单词（Windows 上，OS X 上 用 Alt 键替换 Ctrl 键）
- Ctrl + UpArrow 和 Ctrl + DownArrow：滚动代码一行
- PageUp 和 PageDown：移动光标一页
- End：将光标移动到行尾
- Home：将光标移动到一行第一个非空字符之前，或者一行的开头
- Ctrl + Home：移动光标到整个 script 的开头
- Ctrl + End：移动光标到整个 script 的结尾

# Cursor 导航和历史

- Ctrl + G（OS X：Cmd-L）：导航到制定行
- Alt + LeftArrow（OS X：Alt-Cmd-LeftArrow）：Go Back，到上一个位置
- Alt + RightArrow（OS X：Alt-Cmd-RightArrow）：Go Forward，到下一个位置
- Alt + M（OS X：Ctrl-M）：打开最近一次 code navigation breadcrumb button（只用于 C# 文件）

# Selections

- Shift+任何 cursor navigation 快捷键或 mouse click：选择当前光标位置与新光标位置之间的文本
- 鼠标双击 或 Ctrl+鼠标点击：选择整个单词
- 鼠标双击并拖拽 或 Ctrl+鼠标点击并拖拽：用鼠标移动整个单词
- 鼠标点击 line numbers：选择一行
- 鼠标三击：选项光标所在行
- 鼠标点击并拖拽 line numbers：鼠标拖拽选择的行
- 鼠标三击并拖拽：鼠标拖拽选择的行
- Ctrl + A：选择全部
- Escape：清空当前选择

# Editing

- Typing text（输入文本）：插入文本，或者替换当前选择的文本
- Backspace：删除选择的文本，或光标前的字母
- Delete：删除选择的文本，或者光标后的字母
- Ctrl + Backspace：删除选择的文本，或者光标前的单词（如果光标在单词结尾）或它的部分（如果光标在单词中间）
- Ctrl + Delete：删除选择的文本，或者光标前的单词（如果光标在单词开头）或它的部分（如果光标在单词中间）

# Cut，Copy，Paste，Duplicate

- Ctrl + X：剪切
- Ctrl + C：复制
- Ctrl + V：粘贴
- 鼠标拖拽选择的文本：移动选择文本
- Ctrl+鼠标拖拽选择的文本：重复 duplicate 选择的文本并拖拽放置它们
- Ctrl+D（OS X：Alt-Cmd-Down）：重复 duplicate 光标所在的行，或者选择 lines

# More editing

- Ctrl + Z：Undo
- Shift + Ctrl + Z：Redo
- Alt + UpArrow/DownArrow：将当前一行或选择的 lines 向上移动或向下移动一行，并重新调整缩进
- Ctrl+K：对光标当前行或选择的 lines 切换 code comments（只用于 C# 文件）
- Ctrl + [：对当前 line 或选择的 lines 减少要给缩进
- Ctrl + ]：对当前 line 或选择的 lines 增加要给缩进
- Tab：如果没有选择的文本，插入一个 tab，如果有选择的文本，增加一个缩进
- Shift+Tab：如果没有选择的文本，删除光标之前的 Tab 字符，如果有选择的文本，减少一个缩进

# Automatic completion（只用于 C# 文件）

- Ctrl + Space：打开自动补全弹出窗口
- Escape：取消自动补全弹出窗口
- Up/Down arrow keys：选择要自动补全的单词
- Typing 输入文本：过滤自动补全列表
- Enter、Tab、或一个非数字字母字符（non-alphanumeric character）：接收选择的补全

# Searching & Replacing

- F12：Go to Definition
- Shift + F12 (Shift-F12 或 OS X 上 Shift-Cmd-Y)：查找所有 References
- Shift + Ctrl + F：在所有文件中查找
- Shift + Ctrl + H：在所有文件中替换
- Shift + Ctrl + Up：查找当前光标之前或选择的文本中，word 的前一个出现的位置
- Shift + Ctrl + Down：查找当前光标之前或选择的文本中，word 的前一个出现的位置
- Ctrl + F：在 toolbar 上的 search field 中输入要搜索的文本，即将 keyboard focus 设置到 search field 上
- 在 search field 中按 Escape：将 keyboard focus 返回给 code editor
- 在 search field 中按 Enter：搜索 searched text 的下一个出现的位置
- 在 search field 中按 Shift + Enter：搜索 searched text 的上一个出现的位置
- 在 search field 中按 UpArrow 或 DownArrow：和 Enter/Shift-Enter 一样，搜索 searched text 的上一个和下一个出现的位置

# Si3 tab 相关

- Alt + T 或菜单 Window > Toggle Si3 Tabs：切换所有浮动 Si3 tabs 的显示、隐藏状态
- Ctrl + F4 或 Ctrl + W：关闭 active（当前）的 Si3 tab
- Ctrl + Tab 或 Shift + Ctrl + Tab：Tab History 导航（按住 Ctrl 查看全部的 history，然后使用箭头键或者 tab or shift+tab 导航，放开则切换到选择的 tab）
- Ctrl + PageUp 或 Ctrl + Alt + LeftArrow：激活（切换到）当前这个 tab 的左边的第一个 Si3 tab
- Ctrl + PageDown 或 Ctrl + Alt + RightArrow：激活（切换到）当前这个 tab 的右边的第一个 Si3 tab
- Shift + Ctrl + Alt + Left：将当前 active Si3 tab 向左边移动一个位置
- Shift + Ctrl + Alt + Right：将当前 active Si3 tab 向右边移动一个位置

# Font Size

Ctrl + 加号键，Ctrl + 减号键，Ctrl + 鼠标滚轮，触摸板缩放手势：增大、减小 font size。

# 打开，保存，新建 Tab，外部 IDE

- Shift + Ctrl + O：通过系统文件选择对话框选择一个要编辑的文件
- Shift + Alt + O：通过 Unity Asset 搜索框选择一个要编辑的文件
- Ctrl + S：保存修改
- Ctrl + R：保存所有未保存的修改
- Ctrl + T：在新的 tab 打开同一个文件
- Ctrl + Enter 或上下文菜单中 Open at Line：在 external editor 中打开这个 script，并将光标放在同一行上
