# Introduction

Python脚本是扩展Blender功能的万能工具。Blender绝大多数领域都可以被脚本化，包括animation、rendering、import和export、object creation和自动化重复性任务

要使用Blender，脚本可以使用紧密集成的API

## Extending Blender

Add-ons是你可以在Blender中获得额外功能的scripts，它们可以从Preferences中开启

在Blender可执行程序之外，有成百上千被很多人们编写的add-ons。Blender内置了官方支持的各种add-ons

## Scripts

除了add-ons，还有各种scripts可以用来扩展Blender的功能

- Modules：用来import到其他scripts中的Utility libraries
- Presets：Blender工具的setting和key configuration
- Startup：这些文件在Blender开始的时候被import。它们定义了Blender绝大部分UI以及以下附加的核心操作
- Custom scripts：区别于add-ons，它们通常用来通过Text Editor一次性执行

## Saving your own Scripts

### 文件位置

所有的scripts从local、system、user paths的scripts目录中加载

可以在Preferences>File Paths中添加更多的搜索路径

### Installation

Add-ons在Preferences中安装。点击Install...按钮并选择.py或.zip文件

要手动安装scripts或add-ons，将它们按照类型放在addons、modules、presets、或startup目录

还可以通过在Text Editor中加载它们来运行scripts
