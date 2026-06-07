# CommonJS
JavaScript 唯一的官方语言标准是 ECMAScript，

ECMAScript 从未包含 require, module.exports, exports

2009 年左右，JavaScript 还没有官方模块系统，社区为了给 服务端 JS​ 设计模块方案，于是诞生了 CommonJS 规范，被 Node.js 实现。

很多人误以为 CommonJS 是标准？原因是 Node.js 早期只支持 CommonJS，而且 npm 生态全部基于 CommonJS，require 无处不在。

官方模块标准是 ES Module（ESM）。

Node.js 的态度是：

- CommonJS 是历史实现，ESM 是未来
- Node 现在支持 两种模块系统
- 但新代码推荐使用 ESM
- 未来会逐步弱化 CommonJS

CommonJS 不是语言标准​，它是 Node.js 采用的社区模块规范​，ES Module 才是 JavaScript 官方的模块标准。

# TypeScript

TypeScript 不是 JavaScript 的语言标准​，它是 JavaScript 的超集 + 编译期类型系统。

- ECMAScript​	是 JavaScript 官方语言标准
- JavaScript​	是 ECMAScript 的实现
- TypeScript​	非标准，微软主导

TypeScript 的本质，官方定义（准确版）：TypeScript = JavaScript + 静态类型系统

```
TypeScript ⊃ JavaScript
✅ 所有合法 JS 都是合法 TS
❌ TS 不能直接运行在引擎(Node.js, V8, QuickJS)中
```

TypeScript 的“准标准地位”（现实层面），虽然 技术上不是标准，但在现实中：

|   维度    |   地位    |
|   --- |   --- |
|前端工程 | ✅ 事实标准 |
|大型项目 |	✅ 主流选择 |
|npm 生态 |	✅ 大量包用 TS |
|类型生态 | ✅ DefinitelyTyped |
| | |

在工程界是事实标准，在语言层面不是，它是可以运行的 js 之上的一个编译工具。

# Javascript 模块

## ES Module（ESM，官方标准）

```js
// 导出
export const name = 'foo'
export function hello() {}
export default {}

// 导入
import mod from './mod.js'
import { name } from './mod.js'
```

特点：

- 语言层面标准，浏览器 & Node.js 均支持
- 静态分析（编译期确定依赖）
- 支持 tree-shaking
- 严格模式自动生效
- 顶层 await支持

使用场景：

- 现代前端（Vite / Webpack / Rollup）
- Node.js（.mjs或 "type": "module"）

## CommonJS（CJS）

Node.js 早期事实标准：

```js
// 导出
module.exports = {}
exports.foo = 1

// 导入
const mod = require('./mod')
```

特点：

- 运行时加载（动态）
- 同步加载
- 不适合浏览器直接使用
- npm 生态几乎全部基于 CJS

使用场景：

- Node.js（传统项目）
- 老项目、服务端代码
- 正在逐步被 ESM 替代，但仍在大量存量代码中

## IIFE（立即执行函数）

不是正式模块标准，但是早期模块化手段：

```js
(function () {
  var a = 1
})()
```

用于隔离作用域, 常见于老式 SDK / 库。

现代开发建议：新项目：统一使用 ES Module，Node 项目逐步迁移到 ESM。

## TypeScript

TypeScript 使用的是 JavaScript 的模块标准，主要是 ES Module（ESM）。

TypeScript 默认 / 推荐：ES Module，TypeScript 的模块语法 完全等同于 ES Module，但是它可以编译为 ESM 或者 CommonJS 的模块（即 import/export => module.exports/require）。

TS 只负责类型 + 语法，真正决定模块标准的是：tsconfig.json里的 module 配置：

```json
{
  "compilerOptions": {
    "module": "ESNext"
  }
}
```

常见 module 标准：

| module 值 |  对应模块标准   |  说明  |
| --- | --- | --- |
| ESNext/ ES2020|  ✅ ES Module |   现代浏览器 / Vite   |
| CommonJS |  ⚠️ CommonJS   |   Node 老项目 |
| AMD | ❌ AMD  |   老浏览器    |
| UMD |  ⚠️ UMD	|   库打包  |
| System | ❌ SystemJS  | 极少用    |
| | | |

TypeScript ≠ 模块运行时，TS 只是 “描述模块”，最终运行的是 JS 模块标准。

TS 源码：

```js
export const foo = 1
```

编译为 CommonJS（"module": "CommonJS"）:

```js
exports.foo = 1
```

编译为 ESM（"module": "ESNext"）：

```js
export const foo = 1
```

TypeScript 使用的是 ES Module 标准，通过 module配置决定最终输出哪种 JS 模块格式。

# 文件扩展名 .ts .mts .cts .mjs .cjs .js

V8 只负责执行 js，不关心模块加载的规则。

Node.js（V8 + 模块系统 + 系统 API）同时支持 CommonJS 模块规范(require/module.exports) 和 ESM 模块规范(import/export)，两套模块系统不完全互通。

Deno：V8 + 原生 ESM，不支持 CommonJS 模块规范。

Bun（JavaScriptCore）：支持 ESM 和 CommonJS。

QuickJS（轻量引擎）：支持 ESM，不支持 CommonJS。

**模块规范不属于 ECMAScript 语言核心**

ES 只规定了：```import x from 'x'```

没规定：

- 文件怎么找
- 路径怎么解析
- 缓存机制
- require是什么

这些都是运行时自己决定的。

- 语言标准（语法）：引擎之间基本一致​
- 模块规范：由运行时决定，差异巨大​

Node.js 是唯一长期混用 CJS + ESM 的环境。

js 的程序只是普通的文本，引擎不关心文本从哪里来，因此文件的扩展名本身没有意义，但它是一个约定，不同的工具会对文件名进行不同的处理，而且处理的方式也不相同（甚至无视不处理）。

每个 js 模块本身是一个文件，不一定需要标注为 .mjs .cjs .mts。

扩展名 = 给运行时看的信号。

对于 Node.js，.mjs 明确表示这个文件是遵循 ESM 的模块，.cjs 明确表示这个文件是遵循 CommonJS 的模块，Node 会明确拒绝 .mjs 中的 require 或 .cjs 中的 import/export 用法。

Node package.json决定 .js是什么

```json
{
  "type": "module"
}
```

表示 .js 是 ESM 规范模块。

```json
{
  "type": "commonjs"
}
```

表示 .js 是 CommonJS 模块规范。

没有 type默认是 CommonJS

当同一个项目中混用 ESM 和 CJS 又不想改 package.json 时，使用 .mjs 明确告诉工具或环境，这是 ESM 模块，例如：

```
util.mjs
index.cjs
```

Node.js 会明确使用 ECM 模块规范解析 util.mjs，使用 CommonJS 模块规范解析 index.cjs。

对于 TypeScript，.mts 会被明确编译为 .mjs，.cts 会被明确编译为 .cjs，会跳过 tsconfig.json 的配置。至于 .mjs 和 .cjs 如何被解析，则是运行时引擎的责任。

|   扩展名  |   语言	|   模块类型	|   典型使用场景    |
|   --- |   --- |   --- |   --- |
|   .js |   JS	|   ⚠️ 由环境决定	|   最常见  |
|   .mjs    |   JS	|   ✅ ESM	|   Node ESM    |
|   .cjs    |   JS	|   ✅ CommonJS	|   Node CJS    |
|   .ts |   TS	|   ⚠️ 由配置决定	|   TS 源码 |
|   .mts    |   TS	|   ✅ ESM	|   TS + ESM    |
|   .cts    |   TS	|   ✅ CJS	|   TS + CJS    |
|   |   |   |   |

之所以存在这么多扩展名，是因为 JS 历史上同时存在两套模块系统，而扩展名被用来“消除歧义”。

现在的趋势是统一使用 ESM。

.js 没有明确指定哪个模块规范，可能是 ESM，可能是 CJS，看不同工具的配置，例如 Node.js 的 package.json 中的 type="module" 说明是 ESM 模块，否则是 CommonJS 模块。

.mjs 明确告诉工具，这是 ESM 模块，但是否处理，要看引擎运行时。

.cjs 明确告诉工具，这是 CommonJS 模块，但是否处理，要看引擎运行时。

TypeScript 不直接运行，它是上层抽象语言和工具，最终要编译为真正的 js 文件。

.ts 使用 tsconfig.js 的 module 选项告诉编译器编译为哪种模块：

```json
{
  "compilerOptions": {
    "module": "ESNext" // 或 CommonJS
  }
}
```

.mts 会明确编译为 .mjs，不受 tsconfig.module 影响。

.cts 会明确编译为 .cjs，不受 tsconfig.module 影响。

## 为什么 Node 需要 .mjs/.cjs？

因为 Node 有一个历史包袱：

```
npm 生态 = CommonJS
Web 标准 = ESM
```
Node 必须同时支持两者:

- 不想改 package.json 就使用扩展名指示：.mjs/.cjs
- 想统一就使用 package.json 指示："type": "module"

## 前端项目为什么几乎不用 .mjs？

因为 前端 只认 ESM，打包工具（Vite / Webpack）忽略扩展名，源码统一用 .js / .ts。

扩展名不是语言特性，而是“给工具和运行时的信号”，无论是哪种扩展名的文件，里面都是 js 源代码。

浏览器、V8（纯引擎）、QuickJS 完全不关心扩展名，QuickJS 甚至没扩展名也行。

## QuickJS

QuickJS 基本不区分 .mjs / .cjs / .js 扩展名​，它只认 ES Module 语法，扩展名不影响模块类型判定​，不支持 CommonJS（require / module.exports）。

扩展名只是文件名，不是协议。

```bash
qjs a.js
qjs b.mjs
qjs c.cjs   # 只要内容是 ESM 就能跑
```

QuickJS 只支持一种模块系统：ESM，它实现了

- import / export
- import()动态导入
- top-level await（较新版本）

不支持

- require()
- module.exports
- exports.xxx
- CommonJS 模块解析算法

QuickJS 如何判断是不是模块？不是看扩展名，而是看文件内容：

- 包含 import / export，就是模块
- 不包含，就作为脚本

如果使用 TypeScript + QuickJS，统一使用 ESM 规范，文件扩展名固定使用 .ts 和 .js，不需要 .mjs .mts 这些，这是最推荐的做法。

TypeScript 的 .mts / .cts是为 Node 设计的，QuickJS 不需要“强制输出”，因为它只认 ESM，甚至不看扩展名。

### 推荐的文件结构，最简洁、最干净：

```
src/
 ├─ main.ts
 ├─ math.ts
 └─ utils.ts

dist/
 ├─ main.js
 ├─ math.js
 └─ utils.js
```

所有 .ts文件都用 ESM

所有 .js文件都能被 QuickJS 执行

### tsconfig 正确配置（面向 QuickJS）

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "moduleResolution": "Node",
    "strict": true,
    "outDir": "dist"
  }
}
```

关键点：

- module: ES2020（或更高）
- 不使用 CommonJS
- 不生成 .mjs

# 模块 vs 脚本

不是所有 JS 脚本都是模块，JS 有两种脚本：普通脚本（Script）和模块（Module）。

普通脚本使用全局作用域，而模块有自己的独立作用域。

所有的普通脚本都在同一个全局作用域运行，而模块都在自己的独立的作用域运行。

只要使用了 import 和 export，就是模块，否则就是普通脚本。

脚本引擎运行普通脚本和模块文件的过程也不同，因此引擎运行模块文件时通常需要显式指定这是模块，否则执行不了。

例如，浏览器环境中，要运行普通脚本，只需指定 \<script src='main.js'>，而对于模块，则必须指定 \<script type="module" src='util.js'>

在 QuickJS 中，运行普通脚本：

```bash
qjs app.js
```

运行模块则是：

```bash
qjs --module app.js
```

## 为什么模块不能“随便直接运行”？

因为模块有 前置约束：

- 必须解析 import
- 必须解析 export
- 必须构建依赖图
- 必须保证执行顺序

普通脚本没有这些约束

## 模块直接运行的方式

显式声明：

```html
<script type="module">
  import './app.js'
</script>
```

命令行参数：

```bash
qjs --module app.js
```

在普通脚本中，使用 import() 动态导入

```js
import('./app.js')
```

引擎的一次运行过程，模块 只执行一次，但是脚本每次都会重新运行。

## QuickJS 只是脚本引擎，不包含任何系统 api

QuickJS 只提供了纯语言能力：
- 变量、函数、对象
- Promise
- ES module（import / export）
- BigInt
- RegExp
- JSON
