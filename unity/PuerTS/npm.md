npm 是 node.js 生态的包管理器，可以安装各种其他人发布的 js 包和应用程序（CLI 等）。

node 命令是 Node.js 引擎本身，用来执行 js 代码。

npx 是 node 的附带工具，可以局部、临时执行 npm 包中的命令（CLI）。

npm 安装的 package 可以是全局安装，整个电脑的都可以使用，也可以局部安装，只在一个 js 工程（例如 ts 工程）中局部安装（只存在于局部工程目录的 node_modules 中），此时这个 package 只在这个工程中可用。npx 就是用于执行这种局部 package 中的 cli 的。

首先确保安装了 Node.js 和 npm（类似 Python 和 pip）

全局安装：

```bash
npm install -g typescript # 全局安装
tsc -v
```

局部安装：

```bash
# 进入你的项目目录（若无 package.json先初始化）：
npm init -y
npm install --save-dev typescript
# 安装完成后，项目中会出现：node_modules/.bin/tsc
# 局部使用 tsc
npx tsc
```

