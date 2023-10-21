# Prefab

Unity Prefab 系统可以创建、配置、存储一个 GameObject 的全部组件、属性、子 GameObjects 到一个可重用的 Asset 中。Prefab Asset 就像一个模板，可以使用它在 Scene 中创建新的 Prefab instances。

对 Prefab asset 的任何编辑都会自动同步到这个 Prefab 连接的所有 Prefab instances 上。这可以让你在整个项目中进行广泛的改变，而无需重复地编辑每个 Asset 的 Copy（GameObject）。

还可以在 Prefab 中嵌套其他 Prefab。这创建一个 Prefab 的链式结构，每个 Prefab 负责统一改变它包含的组件或属性。这是一种引用机制，就像一个在一个文件系统的某个目录上 mount 另一个文件系统一样，或者文件系统的中的软连接。

连接到 Prefab asset 的 GameObject 称为 Prefab Instance，否则就是普通的 GameObject。

但是，这不意味着所有的 Prefab Instance（Prefab 实例化并连接的 GameObject）必须是完全一样的。Prefab 只是为 Instance 提供初始值，并连接到它。之后还可以再 Instance 进行编辑，就像任何 GameObject。这些修改称为 Override。Override 并不改变 Prefab。当加载一个 Prefab Instance 时，先从硬盘上反序列化 Prefab 到 Scene 中，然后再上面应用这些 override。这类似 Docker 的联合文件系统，是一个 non-destructive 的系统，底层不变，上层修改。

还可以创建 Prefab variant，这可以认为是硬盘上的带 Override 的 Prefab Instance。它引用一个 Prefab，以及在它上面进行的修改（Override），保存为 asset。带 Override 的 Prefab Instance 只保存在 Scene 中。Prefab Variant 允许你将一组 override 组合到一个有意义的 Prefab variation 中。

- Prefab：硬盘上的 GameObject asset
- Prefab Instance：Scene 中连接到 Prefab 的 GameObject，具有和 Prefab 完全一样的属性、组件
- Prefab Instance(Override)：Scene 中连接到 Prefab 的 GameObject，并携带一组 override，应用到原始 Prefab 之上（包括属性的变化，组件的添加和移除）
- Prefab Vairant：硬盘上的 Prefab + Override

## Instance Override

Instance Override 允许在 Prefab Instance 之间创建变化，即同一个 Prefab 创建的 Instance 具有不同的属性，同时为 override 的共同属性仍然可以被 Prefab 统一修改。

当修改 Prefab Asset 时，更新被反映到它的所有 instances 上。但是你还可以直接在单独的 instance 上做修改。这样会在特定的 instance 上创建 instance override。

有 4 种类型的 instance override：

- 修改属性值
- 添加组件 component
- 移除组件 component
- 添加一个 child GameObject

但是有一些限制：

- 不可以 reparent 作为 Prefab 一部分的 GameObject。但是那些不是 Prefab 一部分的 GameObjects 可以任意修改，因为 Prefab 不需要序列化和反序列化它们
- 不可以移除作为 Prefab 一部分的 GameObject。同样对那些不是 Prefab 的 GameObjects，可以任意修改


但是你可以 deactivate 一个 GameObject，这可以作为 removing GameObject 的很好的代替方案。Deactivate 算作 property override。

在 Inspector 窗口中，instance overrides 以 bold 显示它们的名字，并在前面显示一个蓝色的竖线，指示这是一个 override。当添加一个新的组件到 Prefab instance 上，蓝色的属性跨越整个 component。这与 UI Builder 类似。

添加和移除的组件前面还有一个加号和减号，添加的 GameObjects 在 Hierarchy 上也有一个加号，指示这是一个 override。

在 Hierarchy Window 上，带有 overridden 或 non-default 值的 Prefab instances，有一个 override indicator 来显示它们是被编辑的，Unity 在左边显示和 Inspector 中一样的蓝色竖线。

### Overrides 优先级

Prefab instance 上一个 overridden 属性值总是优先 Prefab asset 的值。这意味着，如果改变 prefab asset 上的属性值，不会影响 prefab instance 的属性。

最佳实践是只在严格需要的时候使用 Prefab Instance Override。

### Alignment 特例

Prefab instance 的 alignment 是一个特殊情况，和其他属性不同处理。Alignment 的值从不会从 prefab asset 上传播的 instance 上。这意味着它可以和 Prefab asset 不同，而不需要 instance override。具体的说，alignment 是 Prefab root 的 position 和 rotation 属性（不包括 scale 和 child gameobject 的 alignment）。对于 Rect Transform 还包括 Width，Height，Margins，Anchors，和 Pivot 属性。

这是因为修改 Prefab 的 instances 使他们在相同的位置和旋转的情况很罕见，而如果这样做会导致很多不便。更常见的是，你会希望每个 Prefab Instance 都有不同的 position 和 rotation。因此 Unity 不把 Prefab Root 的 position 和 rotation 算作 Prefab overrides。

Prefab 的一些属性不会连接到 Instance 上，包括 name，flag，position，rotation。在 prefab 上更改它们不会同步到 instance 上。

### Unused Overrides

表示 instance overrides 值的数据，在脚本声明它们被修改或删除时，会变成 unused。此时可以移除 unused override data。

## Editing Prefab via instances

Prefab Instance 的 Root 的 Inspector 上比普通的 GameObject 多了 3 个控制选项：Open，Select 和 Overrides。

- Open：在 Prefab Mode（单独的 Prefab 编辑场景）打开 Instance 来自的 Prefab Asset，让你可以编辑 Prefab Asset，进而改变它的所有 instances
- Select：在 Preject window 中选择 Prefab Asset
- Overrides：打开 overrides drop-down 窗口

### Overrides dropdown 窗口

Overrides dropdown 穿了个显示 Prefab instance 上的所有 overrides。它还让你可以应用 overrides 到 Prefab Asset 上（写入 override 到硬盘），或者 revert overrides 到 Prefab asset 的状态。Dropdown 只在 isntance root 上显示，对于嵌套的子 Prefab 不会显示。

Dropdown 允许你单独或一次性全部 apply 或 revert prefab override。

应用修改只收，Prefab asset 被修改，而 Instance 上不再有这个 override。

Dropdown 窗口显示 instance 上的一个 changes 列表。对每个修改项，点击它弹出一个 floating 窗口显示修改的内容，并允许你 apply 或 revert 这个修改。

对于值被修改的 components，floating 窗口显示一个 side-by-side 对比，比较 Prefab Asset 中的值和 Instance 上的值。这可以让你决定是否 apply 或 revert。

Override Dropdown 还有 Revert All 和 Apply All 按钮，来一次 revert 或 apply 全部修改。如果在 Prefab 中嵌套有其他 Prefab，Apply All 总是只应用最外层的 Prefab，即 Dropdown 所在的 root GameObject。

如果同时选择了多个修改，Revert All 和 Apply All buttons 被替换为 Revert Selected 和 Apply Selected，这同样只适用于最外层的 Prefab。

在任何选择 objects 上，如果有 unused overrides，Downdown 显示一个选项允许你移除它们。

### Context menus

还可以再单独的 overrides 上使用 inspector 中的 context menu 来 revert 和 apply，而不是 Override Dropdown 窗口。

Overriden 属性显示未 Bold。它们可以通过 context menu 来 revert 或 applied。

还可以通过右上角的 cog dropdown menu 的 Modified Component 项目来 apply 或 revert 修改。

新添加的组件在 icon 上有一个 + 号，移除的组件在 icon 上有一个 - 号。它们都可以通过 context menu 或 cog dropdown menu 来 revert 或 apply。

新添加的 GameObject 和嵌套 Prefab 在 Hierarchy 上有一个 + 号。它们可以通过 Hierarchy 上 Object 的 context menu 来 revert 或 apply。

## Nested Prefabs

可以子啊 Prefab 中嵌套其他的 Prefab。嵌套 Prefab 就像代理，或文件系统中的 mount 点或软连接。每个 Prefab 只管各自负责的 instances。Prefab 只序列化嵌套连接本身。

嵌套 Prefab 保持到它们 Prefab Asset 的连接。

### 在 Prefab Mode 中添加一个嵌套 Prefab

双击一个 Prefab asset 会进入 Prefab Mode，这是一个单独的 Scene，在里面可以像在普通的 Scene 中编辑 GameObject 来编辑 Prefab Asset，而不需要只在 Inspector 中编辑 Prefab asset，因此可以使用各种 3D Gizmos，并且实时预览编辑效果。

你可以从 Project window 中拖拽一个 Prefab Asset 到 Hierarchy 或 Scene view，来创建一个 Prefab instance 到 Prefab Mode 打开的 Prefab Asset，这就创建了一个嵌套 Prefab。

注意：在 Prefab Mode 中打开的 Prefab 的 Root GameObject 不会显示蓝色的 cube prefab icon，但是其中嵌套的任何 Prefab 仍然会显示。你还可以添加 override 到这些 Prefab intance 上，就像普通 scenes 中的 Prefab Instance。

### 通过 instance 添加 Nest Prefabs

还可以在 scene 中添加一个 Prefab instance 为另一个 Prefab instance 的 child 来创建嵌套 prefab，而无需进入 prefab mode。这样添加的 Prefab instance 上有一个 plus 在 icon 上。

添加的嵌套 prefab 除非 unpack，否则绝不会序列化到外层的 prefab 中，它们各自分工明确，只管理自己的数据。因此不用担心数据被意外写入到外层 prefab 中。

添加的 Prefab 可以被 apply 或 revert 到外层 Prefab，就像其他 overrides 的方式一样（Dropdown，context menu）。Overrides dropdown 只在外层 prefab 上显示。一旦 apply，Prefab 不再显示 + 号，因为它不再是 override 了，但是嵌套到外层 Instance 的 Prefab 的 asset 中。但是它仍然保持蓝色的 cube icon，因为它自己是一个 Prefab instance，而不是普通的 GameObject，它保持到它自己的 Prefab Asset 的连接，并管理它自己的范围内的属性。

## Prefab Vairants

Prefab Instance Override 只能单独存在于 Scene 中。如果你想将 Prefab + override 也作为模板，来创建更多的 instance，可以使用 Prefab Variants。它本质就是硬盘 asset 版的 Prefab Instance + override。

Prefab Variant 继承原始 Prefab 的所有属性，称为 base。Override 覆盖 base prefab asset 的值。一个 Prefab Variant 可以以任何同类 Prefab 作为它的 base，包括原始的 Prefabs 或另一个 Prefab Variant，只要它们的 base 相同。

### 创建 Prefab Variant

可以在 Project 中右键点击 Prefab 选择 Create > Prefab Variant。这创建了选择的 Prefab 的一个副本，并且初始没有任何 overrides。然后就可以在 Prefab Mode 中打开 Prefab Variant 做任意的 override。

还可以从 Hierarchy 中拖拽一个 Prefab Instance（无论有没有 override）到 Project 中。此时会弹出一个对话框询问你想要创建一个全新的 Prefab 还是一个 Prefab Variant。Instance 上的任何 overrides 现在变成一个新的 Prefab Variant 内的 override，而 Instance 不再具有 override。然后可以在 Prefab Mode 打开这个 Prefab Variant 进行进一步 override。

Prefab Variant icon 显示为带箭头的蓝色 prefab icon。

### 编辑 Prefab Variant

在 Prefab Mode 中打开一个 Prefab Variant 时，root 显示为一个 Prefab Instance，带有一个蓝色的 Prefab Icon（而原始 Prefab 则显示为普通的 GameObject）。这个 Prefab Instance 表示 Variant 继承的 base Prefab。它不表示 Prefab Variant 自身。你对 Prefab Variant 进行的任何编辑变成这个 base 的 override。

就像任何 prefab instance，修改包括修改属性值，添加组件，移除组件，添加 child gameobjects。限制也相同，包括不能 reparent 或移除 来自 base Prefab 的 GameObject。但是可以已通过 deactive GameObject 来达到相同的效果。Deactivate 视为 override。

在 Prefab mode 中编辑一个 prefab variant 时，应该立即，apply overrides 会将这些 variant 应用到 base prefab asset 中。这通常不是想要的结果。Prefab Variant 的目的是提供一个方便的方式来存储有意义和可重用的 overrides 集合，它们应该保持为 overrides，而不应该应用到 Prefab Asset。因此 Prefab Variant 一般不 apply override，而是将 override 保持在自身中，因为 Prefab Variant 也可以创建 Prefab Instance。

当打开 Overrides dropdown widnow 时，总是可以在它的 header 中查看 overrides 属于那个 object，以及 override 在那个 context 中存在。对于一个 Prefab Variant，header 会说 overrides 是到 base Prefab 的，并存在于 Prefab Variant。为了是它更加清楚，Apply All 按钮变成 Apply All to Base。

apply 总是应用到 base Prefab，revert 则从 Prefab Variant 中重置。

## Overides at multiple levels

当同时使用嵌套 Prefab，Prefab Variant 时，Override 同时存在于两个 level，相同的 overrides 可以有多个不同的 Prerfabs 上。

### 选择 apply target

如果你有一个 Prefab instance，其有嵌套的 prefab ，或者其是一个 Prefab Variant，你可能需要选择 override 应用到哪个 Prefab。

如果 Table 嵌套另一个 Vase，场景中一个 Table 的 instance 的 Vase 的 instance 被 override，则 override 既可以应用到 Vase 上，也可以应用到 Table 上。

Override Dropdown 上的 Apply All 只允许应用 override 到最外层的 Prefab 上，即 Table。但是 context menu 或 side-by-side 比较窗口可以选择 override 目标：

- Apply as Override in Prefab "Table"

  value 变成 Table 内 Vase instance 的一个 override。属性在 Scene 中的 Instance 上不再标记为 override，但是如果你在 Prefab Mode 中打开 Table，Vase Prefab instance 上的属性被标记为 override。Vase asset 自身不被 override 影响。

  这其实是 Table asset 变化了。尽管 Table 是原始的 Prefab，但是它的数据包含可以带有 override 的 Vase instance。因此 Vase instance 的 override 也成为了 Table asset 的一部分。这样所有连接到 Table Prefab 的 Table Instance 都会出现 Vase 的 override，但是 Vase asset 本身没有变化，其他的 Vase Instance 也不被影响。

  嵌套 Prefab 的 override 数据包被视为原始外部 Prefab 的数据的一部分，就像其他普通的属性、组件一样。因此一个 Prefab 的数据其实包括属性、组件、child GameObject，嵌套 prefab 的 override。

- Apply to Prefb "Vase"

  value 应用到 Vase Prefab Asset，并对 Vase 的全部 instance 可见。

Override 要么作为外层 Prefab 的一部分，要么应用到嵌套的 Prefab 的 asset 上。

### Apply 到 inner Prefabs 可能也会影响外部的 Prefabs

应用一个或多个属性到 inner Prefab Asset 有时也会修改外部 Prefab Assets，因为这些属性得到它们在外部 Prefabs 的 overide。如果选择 Apply to Prefab "Vase"，而 Table Prefab 有一个这个属性的 override，则这个 override 也会同时被 revert，这样 instance 上的这个属性才能保持 apply 时的 value。否则，instance 上的 value 在 apply 之后将会改变。

## Unused Overrides

Instance override values 被存储为 scene 或它们定义所在的 prefab 中的 data。但是如果它的 target object 不再有效，或者它的 Property Path 变成未知的，override data 将变成 unused，但是它仍然存储在 scene file 中，但是它是多余的。

例如，如果你 override Prefab 上一个脚本的 public field 的 values，然后删除了脚本，包含 override values 的数据将变成 unused 的，因为它的反序列化的目标已经不存在了。

此外，如果你删除了一个 public field definition，或重命名了它，override data 也会变成 unused 的，同样是因为反序列化失败，因为 Property Path 不再匹配存储的 data，尽管脚本组件仍然存在。

因为 Unity 不会自动删除 unused override data，如果你重新恢复了删除的脚本，或字段定义，override 的数据会重新变的有效，并且就像之前一样应用为一个 override。

如果你不想保持 unused override data，你可以使用 inspector 中的 override menu，或者 Hierarchy window 中的 context menu 来检查并移除它们。所有 unused overrides 都会被移除，并且 Unity 将所有移除的细节写到 Editor log。

Unityu Editor 不会自动确定你的 unused data 何时以及是否应该清理，因为你可能想要临时或意外地移动了 data 引用的 object 或 property，但是你可能会稍后改回来。

最好移除你知道的不再需要的 unused override data，因为它意味着你的 scene file 只包含有用的数据，这可以使版本控制或合作更简单。

注意：你可以重命名 public fields 并保留关联的 overridden value，通过使用 FormerlySerializedAsAttribute，它执行命名转换来影响字段的 old name 到它的 new name。

## Unpacking Prefab instances

Unpack Instance 使得它变成普通的 GameObject。如果上面有 Override，则 Override 会保留下来。

如果 unpack 的 Instance 包含嵌套的 Prefab，它仍然保持为 Prefab Instance，并连接到 Prefab asset。

如果 unpack prefab vairant，则会得到一个新的 Prefab Instance，它是 base Prefab 的 一个 instance。如果需要得到普通的 GameObject，需要再 unpack 一次。

通常 unpack 一个 prefab instance 会得到在 Prefab Mode 中的相同的内容（普通的 prefab 变成 GameObject，Prefab Variant 变成 Prefab Instance）。这是因为 prefab mode 显示一个 prefab 内部的内容，而 unpack 一个 Prefab instance 正是 unpack prefab 的内容。

每次 unpack 只会 unpack 最外层的 prefab（Prefab 变成 GameObject，Prefab Vairant 变成 Prefab）。Unpack Prefab Completely 会递归地 unpack 整个 prefab，直到没有任何 prefab。

可以 unpack scene 中的 Prefab Instances，也可以 unpack Prefab 嵌套的 Prefab。

## Misc

只要是在 Editor 中可以进行的编辑操作，都可以通过 Script 进行，需要的只是找到对应的 API。

unpack 的 GameObject 还可以重新 link 到 Prefab 上。可以将一个 Prefab 或 Prefab Variant 替换为另一个 Prefab Variant，只要它们是基于同一个 Prefab 的，这种替换只是重新反序列化 Prefab（最原始的数据版本），然后依次应用各个 override（先应用 Prefab Variant 的 override，然后应用 Instance Override）。

Prefab -> Prefab Variant(Prefab + override) -> Prefab Instance(Prefab + override) -> Prefab Instance Override(Prefab + override + override)

将 Prefab 作为中心化数据源，在项目范围内传播改变。

AssetDatabase.LoadAssetAtPath("...") as GameObject 加载一个 Prefab 资源，注意这是硬盘上的 asset，不是实例化的 GameObject，多次调用 LoadAssetAtPath 返回同一个 Prefab asset。

如果直接调用 Object.Instantiate(prefab asset) 得到的是完全独立的 GameObject。要创建 Prefab Instance（连接到 Prefab），需要使用 PrefabUtility.Instantiate(prefab asset)。

无论是 GameObject 还是 Prefab Instance，销毁都是用 Object.Destroy() 或 Object.DestroyImmediate()。

一个 Prefab Instance 中不可以改变被 Prefab 管理的 GameObject 的层级关系，否则 Prefab 无法进行正常的反序列化。就像动画重定向的前提是骨骼结构必须一样。

如果需要不同的 GameObject 层级，那么很可能需要不同的 Prefab。

Prefab Instance 还可以 replace 以及 replace with override。就是更换底层的 base Prefab，并可以保持上面的 override 数据。

