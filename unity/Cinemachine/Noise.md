添加 noise 来模拟真实世界相机的震动

- 在 Cinemachine Camera 组件中，选择 Noise，然后选择 Basic Multi Channel Perlin。这会添加要给 noise behavior 到 Cinemachine Camera
- 在 Basic Multi Channel Perlin 中，Noise Profile 下面，选择一个既有的 noise profile asset 或创建你自己的 profile
- 使用 Amplitude Gain 和 Frequency Gain 来精细调整 noise

Noise 被用来添加诸如手持相机类似的摇动效果，noise 是连续的。对于突然的震动（例如响应爆炸），建议使用 Impulse 而不是 Noise。