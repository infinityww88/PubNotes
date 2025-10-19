# Rasterize Path

栅格化一个Path，基于提供的栅格化参数产生实际的采样点

## Slots

### Input

- Path

### Output

- Path：rasterized path

## 参数

- Range：定义用来extrude的path部分。对于闭合曲线，From会无限重复，而对于开放曲线它将会被clamp

- Resolution：定义path的平滑程度，细分（栅格化）细节

- Optimize：采样点将基于曲线的曲率而不是沿着曲线的固定长度创建。曲率越高的地方越细分

- Angle Threshold：仅用于Optimize。设置曲率角度，每当曲线弯曲超过这个角度就创建一个采样点
