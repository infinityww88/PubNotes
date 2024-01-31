# ShaderLab command: Blend

Blender 觉得 GPU 如何合并 fragment shader 输出的颜色到 render target（颜色缓冲区中），即将 framement shader 的计算结果和当前屏幕颜色合并。

通过 BlendOp 命令决定 blending 操作。

Enabling blending disables some optimizations on the GPU (mostly hidden surface removal/Early-Z), which can lead to increased GPU frame times.

## Usage

开启 blending 之后：

- 如果使用 BlendOp 命令，blending operation 被设置为那个操作，否则默认为 Add
- 如果 BlendOp 命令是 Add，Sub，RevSub，Min，Max，GPU 将 fragment shader 的输出乘以 source factor（BlendOp 命令指定的 source 因子）
- 如果 BlendOp 命令是 Add，Sub，RevSub，Min，Max，GPU 将 render target 的颜色乘以 destination factor（BlendOp 命令指定的 dest 因子）
- 对于上面的两个结果，进行 blending 操作，blender 公式是：

  ```
  finalValue = sourceFactor * sourceValue <operation> destinationFactor * destinationValue
  ```

blending 公式中:

- finalValue 是 GPU 写入到目标缓冲区的最终值
- sourceFactor 是 Blend command 定义的 source 因子
- sourceValue 是 fragment shader 输出的颜色
- operation 是 blending 操作
- destinationFactor 是 Blend command 定义的 dest 因子
- destinationValue destination buffer 中已有的颜色

### Blend Command

- Blend On/Off

  默认 Off。关闭默认 render target 的 blending。

- Blend \<render target\> \<state\>

  关闭指定 render target 的 blending。例如 Blending 1 Off。

- Blend \<source factor\> \<destination factor\>

  例如 Blend One Zero。开启默认 render target 的 blending。为 RGBA 值设置 blend 因子。

- Blend \<render target\> \<source factor\> \<destination factor\> 

- Blend \<source factor RGB\> \<destination factor RGB\>, \<source factor alpha\> \<destination factor alpha\>
  
  例如 Blend One Zero, Zero One。分别为 source 和 destination 设置 RGB 和 Alpha 的因子。

- Blend \<render target\> \<source factor RGB\> \<destination factor RGB\>, \<source factor alpha\> \<destination factor alpha\>

## Blender 参数值

- render target：整数，1-7，render target index
- state：Off，关闭 blending
- \[source | destination\] factor:

  - One：因子为 1，直接使用 source 或 destination 的颜色
  - Zero：因子为 0，移除 source 或 destination 的颜色
  - SrcColor：GPU 将公式此项的颜色值[source 或 destination 的颜色]乘以 source color，即 source color * source color 或 destination color * source color
  - SrcAlpha：GPU 将公式此项的颜色值[source 或 destination 的颜色]乘以 source alpha 的值，即 source color * source alpha 或 destination color * source alpha
  - SrcAlphaSaturate：GPU 将输入的颜色值乘以 source alpha 和 1 - destination alpha 中的最小值
  - DstColor：GPU 将公式此项的颜色值乘以 frame buffer 的 color 值
  - DstAlpha：GPU 将公式此项的颜色值乘以 frame buffer 的 alpha 值
  - OneMinusSrcColor：因子等于 (1-SrcColor)
  - OneMinusSrcAlpha：因子等于 (1-SrcAlpha)
  - OneMinusDestColor: 因子等于 (1-DstColor)
  - OneMinusDstAlpha: 因子等于 (10-DstAlpha)

## Common blend types

- Traditional transparency: Blend SrcAlpha OneMinusSrcAlpha
- Premultiplied transparency: Blend One OneMinuxSrcAlpha
- Additive: Blend One One
- Soft Additive: Blend OneMinusDstColor One
- Multiplicative: Blend DstColor Zero
- 2x multiplicative: Blend DstColor SrcColor

