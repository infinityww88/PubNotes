# Volume Mesh

从一个Volume（理论上的体积）生成VMesh（理论上的Mesh数据）

## Slots

### Input

- Volume

### Output

- VMesh[]：结果VMeshes

## 通用选项

- Generate UV：是否计算UV

- Split：Volume分割成chunks。**Split Length**定义多少世界单位长度之后创建一个新的chunk（一个新的VMesh，即submesh）

    这对于快速lightmap计算以及Unity优化（诸如Culling）非常有用

- Reverse Normals

- Add Material

    添加一个额外的material mapping

## Materials选项

这里定义的materials被映射到存储在Volume中的Material IDs。至少要有一个材质，可以添加额外的材质

- Material ID：下面的材质参数应用到的Material ID

- Swap UV/Keep Aspect/UV Offset/UV Scale/Material参见VolumeCaps

- Remove：移除这个材质映射
