# Volume Spots

这个模块沿着一个Path或者Volume（生成Volume使用的Path）放置Bounds，每个Bounds生成一个Spot。更精确地说，它使用bounds信息生成一个Spots集合。通过使用一个Bounds（立方体）数组而不是真实的物体提供了许多灵活性。你可以使用这个模块放置meshes，GameObjects，以及任何你想到的物体，只要你能够提供一个bounds数组

为了简化，bounds数组中的索引下标在这里被称为“item”

这里的意图是你将items组织成groups，允许你构建某种程度上的复杂物体来使用。例如，如果你有一个栅栏分割为3个mesh（start，middle，end），你可以将他们放在一组，以确保这个3个mesh被精确地放置在一起，而不是随机的排列。另一个用例是将items放在一组，然后在一个步骤中应用相同的randomization设置。

另一个关键概念是定义group里的items和range里的groups之间如何重复

## Repeating Groups/Items

你可以以顺序或者随机（基于权重）的方式放置groups/items。在随机模式中，你可以定义任何数量的start或end的groups/items为固定的，而不是随机产生start或end的groups/items。这样你可以很好的定义start或end的放置物体，而中间是随机的

## Slots

### Input

- Path/Volume
- Bounds[]

### Output

- Spots：计算生成的Spots的集合

## 通用选项

### Volume Path

- Range：定义spots放置的range

### Volume Cross

- Use Volume's Surface：如果输入是Volume，可以选择使用它的path还是volume表面进行放置（TODO）

- Cross Base：将Cross原点移动一个常量值。如果是Volume，初始基础值定义在Shape Extrusion

- Cross Base Variation：将Cross原点沿着Volume长度动态偏移。Curve的X轴在[0, 1]中，表示Range的起始和结束。对于Volume，初始基础值定义在Shape Extrusion中

### 高级设置

- Simulate：dry run without actually creating spots

### Groups

管理groups。添加、删除、重命名、排序groups

- Repeating Groups：被沿着volume重复放置的groups的范围。不在这个范围的groups只会被放置一次

- Repeating Order：定义重复模式，或者random，或者row（按照groups顺序重复迭代）。在random模式，你可以为每个groups设置随机选择的权重

- Fits The End：只在end有非重复的group时有效

    最后一个非重复的group被精确地放置在spots使用的volume的end。否则最后一个group被放置在第一个可用的spot，这可能在它和volume的end中留下一些空间

### Group

管理每个group的items

- Randomize Items：items将被随机选择

- Items：随机选择的items的索引

- Keep Together：group只在所有item都可以被放置在剩下的空间中时才被放置

- Space Before：group之前添加的空白空间

- Space After：group之后添加的空白空间

- Cross Base：为这个Group偏移Cross的原点

- Ingore Module Cross Base：对于这个group，Cross Origin将不会考虑General tab中的Cross参数

#### Translation

- Relative Translation：translation将会在global/world空间中执行

- Translation X/Y/Z

#### Rotation

- Rotation Mode：如何相对于Volume/Path数据定义旋转轴

  - Full：使用direction和orientation
  - Direction：只使用direction
  - Horizontal：在投射到XZ平面后只使用direction
  - Independent：不实用Volume/Path数据

- Rotation X/Y/Z

#### Scale

- Uniform Scaling：是否一致缩放

- Scale X/Y/Z
