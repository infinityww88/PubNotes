# Settings

## Driving Settings

Driving Settings 在 Tank MainBody 上的 Drive_Control_CS 上设置。

### Maximum Speed

- Torque：每个 wheel 的扭矩。如果这个值太小，坦克可能无法达到最大速度
- Maximum Speed：最大速度，米/秒

### Turning

- Turn Brake Drag

  设置刹车力，来旋转运行中的坦克。如果坦克转弯困难，增大这个值。

- Switch Direction Lag

  设置 brake-turn 和 pivot turn 之间的切换时间。如果你想更平滑的架势感觉，将这个值设置为 0。

- Allow Pivot Turn

  如果坦克具有 pivot-turning 装置，例如 Tiger-I，设置这个选项。

- Pivot Turn Rate

  pivot-turning 的速度被这个 rate 限制。

### Acceleration

- Acceleration

  如果不需要加速度计算（瞬间启动），取消这个选项。

- Acceleration Time

  设置从 0 加速到最大速度需要的时间。

- Deceleration Time

  设置从最大速度减到 0 需要的时间。

- Acceleration Curve

  设置加速度曲线（速度随时间的变化）。

### Parking Brake

当 tank 几乎停下来时，parking brake 自动工作。

- Work Velocity

  当 tank 的速度小于这个值的时候，paring brake 自动工作。如果坦克在停下时，沿着斜坡向下滑动增加这个值。

- Lag Time

  坦克停下后，parking brake 工作的延迟时间。如果需要快速刹车，减小这个值。

### Stability & Controllability

有两个方案可以提升坦克的稳定性和控制性。

#### Anti-Slipping

- Use Anti-Slipping

  Anti-Slipping 对于减少 tank 沿着斜坡滑动有很强的效果。另外，高速下的控制性也会有很大提升，尽管行为略微有点不自然。

- Ray Distance

  设置从 MainBody pivot 到 ground 的近似距离。

  这个功能通过从 MainBody 的 Pivot 向下投射 ray 检测地面。

  如果这个值设置的太高，坦克会浮在空中。

#### Add Downforce

根据 tank 的速度应用一个向下的力到 tank body 上，将它亚到地面。downforce 可以自然地提升稳定性和控制性，massive feeling 更好，尤其在高速的情况下。

- Downforce：设置最大 downforce
- Downforce Curve

  通常设置一个增长曲线，downforce 随着 speed 的变化曲线。

## Suspension

Suspension Settings 在坦克的 Create_RoadWheel 上修改。

注意，进入 Prefab Mode 或 Unpack Prefab 再编辑它们。

当悬挂系统的外观和 Wheels 被改变，需要用新的形状来重建 tracks。

### Spring & Damper

- Sus Spring Force

  设置每个悬挂臂 suspension arm 的弹性力 spring force。当地面太崎岖时，增加这个值，提升坦克的稳定性。

- Sus Damper Force

  设置每个悬挂臂 suspension arm 的阻尼力 damping force，即弹簧恢复到原来形状时的容易程度。增加这个值，悬挂臂将会工作的很慢。

当 tank 具有 Static_Track，在编辑了 suspension 后，点击 Static_Track_Parent_CS 脚本上的 Update the scripts 按钮。

### Spring Angles

- Sus Spring Target Angle

  设置悬挂臂的 target angle。当悬挂臂旋转到这个角度时，spring force 将为 0。

- Forward Limit Angle/Backward Limit Angle

  可以通过调整这些值来设置悬挂臂的角度范围。

## Turret settings

tank turret 包含 3 个物体：Turret，Cannon，Barrel，它们放在 Turret_Objects 下面。

- Barrel_Base

  - Bullet_Generator：bullet 在这里生成
  - Gun_Camera：用于显示瞄准具的 Camera
  - Barrel：barrel 的 mesh 和 collider

- Cannon_Base

  cannon 的 rotation pivot。

  - Cannon：cannon 的 mesh 和 collider

- Turret_Base

  Turret 的 rotation pivot。

  - Turret：Turret 的 mesh 和 collider

注意，进入 Prefab Mode 或 Unpack Prefab 来改变 turret 的外观。

### Turret Rotation

Turret rotation settings 可以在 Turret_Base 上的 Turret_Horizontal_CS 中修改。

- Limit

  如果 turret 具有角度限制，例如 Jagdpanzer，开启这个选项，然后用 Max Right Angle 和 Max Left Angle 设置 turret 的角度范围。

- Speed

  设置 turret 的旋转速度，度/秒。

- Acceleration Time

  设置旋转从 0 达到最大旋转速度的时间。

- Deceleration Time

  设置旋转从最大速度减低到 0 的时间。


### Cannon Rotation

Cannon rotation settings 可以在 Cannon_Base 上的 Cannon_Vertical_CS 上修改。

Turret 负责水平旋转，Cannon 负责垂直旋转。

- Max Angle/Min Angle：设置 Cannon 的旋转角范围
- Speed：Cannon 的旋转速度
- Acceleration Time
- Deceleration Time
- Upper Course：当 Tank 具有一个很高角度的炮时，例如 mortar，开启这个选项。

### Bullet Settings

Bullet settings 可以在 Bullet_Generator 上的 Bullet_Generator_CS 中进行修改。

- AP Bullet Prefab/HE Bullet Prefab

  设置每种 bullet 类型的 prefab（Armor Picercing shell 和 High Explosive shell）。可以在 Prefabs/Bullets 目录下找到 bullet prefabs。

- MuzzleFire Prefab

  设置 muzzle fire 效果的 prefab。可以在 Prefabs/Explosion_Effects 目录下找到 muzzle fire prefabs。

- AP Attack Point/HE Attack Point

  设置每种 bullet type 的 attack points。对于 AP bullet，damage value 基于 attack points 和 impact angle 来计算。对于 HE bullet，damage value 基于 attack points 和到 explosion point 的 distance 来计算。

- AP Initial Velocity/HE Initial Velocity

  设置 bullet 的初始速度，米/秒。

- Life Time

  bullet 的生存时间。

- Initial Bullet Type

  初始选择的 bullet 类型。

  玩家可以在运行时切换 bullet 类型，但是 AI tanks 不能根据 target 选择 bullet 类型。

- Offset

  从 Bullet_Generator 到实例化 bullet prefab 的 offset 距离。

  如果 AP bullet 不能对 target 造成伤害，或者 HE bullet 在 muzzle 爆炸，尝试增加这个 value。bullet 可能与 barrel 的 collider 碰撞。

- Debug Mode

  开启这个选项，在 Console 中检查 damage value。

### Reloading Speed

在 Cannon_Base 上调整装弹时间。

### Recoil Force

在 Cannon_Base 上调整后坐力。

## Damage settings

Damage settings 被 MainBody 上的 Damage_Control_Center_CS 控制。可以在脚本中改变 Hit Points(HP) 和 destroyed effects。

有 3 中类型的 hit points：Turret，Body，Tracks。

当 body 的 HP 或 main turret 的 HP 变成 0 时，tank 被摧毁。当 track 的 HP 变成 0，只有 track 被摧毁，tank 无法移动，但是还能开火。

### Body Damage

- MainBody Hit Point

  当这个值变为 0 时，tank 被摧毁。

- MainBody Damage Threshold

  当 Damage value 小于这个值时，body 不产生任何伤害。

- Destroyed Effect Prefab

  设置 destroyed effects 的 prefab。在 Prefabs/Explosion_Effects 目录下可以找到 prefabs。

- Destroyed Effect Offset

  Destroyed effect prefab 在 MainBody 的 pivot 处实例化，设置这个字段添加 offset。

### Turret Damage

- Number of Turrets

  设置 turrets 的数量，如果 tank 有多个 turrets 的话。

  - Turret Base Transform

    设置 turret 的 Turret_base。第一个 turret 时 main turret。

  - Hit Points

    当这个值变为 0 时，turret 被摧毁。如果 main turret 被摧毁，body 也被摧毁。

  - Damage Threshold

    如果伤害小于这个值，不造成任何伤害。

  - Blow Off

    炮塔被摧毁时，从 body 飞离。

  - Mass

    turret 的 weight。

    在正常情况下，turret 是没有 weight 的。当 turret 被 blow off 后，一个 rigidbody 被挂载到 turret 上，将这个值设置为它的 mass。

- Destroyed Effect

设置炮塔的摧毁效果。

### Tracks Damage

- Left Track Hit Point/Right Track Hit Point

  左右履带的生命值，当这个值变成 0 时，履带被摧毁。

- Track Damage Threshold

  伤害值小于这个值，不造成伤害。

## Weak/Strong Points

tank 的 weak 和 strong points 是通过挂载 Armor_Collider 实现的。Armor_Collider 是一个特殊的 collider，显示为 tank 上的一个透明的特殊的 collider。

可以使用这个 collider 作为 tank 的一个 weak 或 strong point，并调整 Damage_Multiplier 值。当 Damage_Multiplier 大于 1，是一个 weak point。当它小于 1，是一个 strong point。

Armor_Collider 必须放在 MainBody 或 Turret 下面作为 child。

### How to use Armor_Collider

- 进入 Prefab Mode 或 Unpack Prefab
- 选择 tank 上的 Armor_Collider，任意调整位置，旋转，缩放。可以在 Prefabs/Tank_Components 目录下找到 Armor_Collider prefab。将它拖拽到坦克里，然后 Unpack prefab instance

  Track_Collider 用于 track 的 weak points。

- 设置 Hierarchy。如果 Armor_Collider 是 body 的一个 weak/strong point，将它作为 MainBody 的 child。如果是 turret 的一个 weak/strong point，将它作为 turret 的 cihld。

- 设置 Damage_Multiplier

  小于 1 是 strong point，大于 1 是 weak point。

### Change Camera Settings

可以在 tank 中设置多个 viewpoints(Camera_Points)。在每个 viewpoint 中可以开启或关闭以下功能：

- Rotation

  可以为 rotation type 选择 first person view 或 third person view。

- Zooming

- Auto Look

  当 Locking-on 时，look at target。locking-on 在 version 3.2 中默认是关闭的。

- Pop Up

  根据 zooming rate pop up camera。

- Avoid Obstacle

  当 view 被阻挡时，向前移动 camera。

设置可以在 Camera_Pivot 上的 Camera_Points_Manager_CS 中修改。

### 如何设置 viewpoints

- 进入 Prefab Mode 或 Unpack Prefab

- 选择 tank 中的 Camera_Point。如果 tank 没有 Camera_Point，在 tank 中创建一个空的 GameObject

- 设置好 position。注意，确保使 Camera_Point 作为 MainBody 的一个 child。如果 point 设置在 Turret 下面，将会很难瞄准目标，因为 aiming point 也会随着 turret 旋转。

- 在 Camera_Pivot 中的 Camera_Points_Manager_CS 中设置属性

  - Number of Camera Points 设置 tank 上的 viewpoints 的数量
  
  对于每个 Camera Point，设置属性：

  - Camera_Point：Camera Point GameObject。第一个元素设置为初始 viewpoint
  - FOV：设置 Camera 的初始 field of view
  - Clipping_Planes_Near

    设置 camera 的 near clipping distance。如果靠近的物体不能渲染在 view point 中，可以减小这个值，让近平面靠近相机。

  - Rotation_Type

    - 0 = disable
    - 1 = Third person view（camera 在一个距离上绕着 Camera Point 旋转）
    - 2 = First person view（camera 绕着 camera point 旋转）

  - Enable Zooming

    允许 zoom in/out 功能

  - Enable Auto Look

    当 locking-on 时，camera 自动 look at target（默认关闭）。

  - Enable_Pop_Up

    根据 zooming rate pop up camera。

  - Enable_Avoid_Obstacle

    当 view 被阻挡时，向前移动 camera。

- 在运行时测试 View Points

  按 F 键切换 viewpoints。

### 如何调整功能

- Rotation

  在 General_Settings_CS 中调整一下 values：

  - Camera_Horizontal_Speed = 2.0f
  - Camera_Vertical_Speed = 1.0f
  - Camera_Invert_Flag = false
  - Camera_Use_Clamp = true
  - Camera_Simulate_Head_Physics = false

- Zooming

  在 Main Camera 上的 Camera_Zoom_CS 脚本中调整：

  - Min FOV
  - Max FOV

- Pop Up

在 Camera_Pivot 上的 Camera_Pop_Up_CS 脚本中调整：

- Pop Up Start Length
- Pop Up Start Start FOV
- Pop Up Start Goal FOV
- Pop Up Start Motion

- Avoid Obstacle

  在 General_Settings_CS 脚本中调整：

  - Camera_Avoid_Move_Speed = 30.f
  - Camera_Avoid_Min_Dist = 2.f
  - Camera_Avoid_Max_Dist = 30.f
  - Camera_Avoid_Lag = 0.1.f

## Change Sound Settings

可以添加 3 中音效到 tank 上：

- Engine sound

  引擎声音有 tank 的 Engine_Sound 产生。音量和音调根据指定 wheels 的速度而改变。

- Turret motor sound

  Turret motor 声音由 tank 的 Turret_Base 产生。音量根据 turret 的旋转速度改变。如果需要，还可以挂载 cannon rotation 声音。

- Impact sound

  驾驶时的碰撞声音有 MainBody 产生。音量和音调根据 tank 的 motion 改变。

爆炸效果在它们的 prefabs 中有音效片段。开火音效挂载在 muzzle fire prefab 中。

### 引擎声音

选择 Engine_Sound 并在 Sound_Control_Engfine_CS 脚本中设置以下值：

- Left Reference Wheel/Right Reference Wheel

  引擎声音将根据这些 wheels 的速度控制。可以通过点击 Set Automatically 按钮自动设置它们。

- Left Reference Parent Name
- Left Reference Name
- Right Reference Parent Name
- Right Reference Name

但 Left Reference Wheel 和 Right Reference Wheel 设置好时自动设置。通常你不需要改变它们。

- Idling Pitch

  设置坦克停止时的音调。

- Max Pitch

  坦克以最大速度运行时的音调

- Idling Volume/Max Volume

还可以再 Audio Source 中改变 Audio Clip。

### Turret Sound

选择 Turret_Base 并在 Soudn_Control_Motor_CS 中设置：

- Max Motor Volume：turret 以最大速度旋转时的音量

还可以在 Audio Source 中改变 Audio Clip。

如果需要，还可以挂载 cannon motor sound。添加 Sound_Control_Motor_CS 和 Audio Source 到 Cannon_Base 上。

### Impact Sound

选择 MainBody 并在 Sound_Control_Impact_CS 中设置：

- Min Variation

  当每秒垂直速度变化大于这个值时才产生声音。

- Max Variation

  当每秒垂直速度变化大于这个值时，pitch 和 volume 将达到最大。

- Min Pitch/Max Pitch

  设置 Pitch 范围。

- Min Volume/Max Volume

  设置音量范围。

- Interval

  产生声音的周期。当设置为 0 时，将产生噪音。

还可以在 Audio Source 中改变 Audio Clip。

### Explosion Sound

在 Prefabs/Explosion_Effects 中的 Prefab 中找到 AudioSource，设置 AudioClip。

## Change Dust Settings

Dust effects 在 Engine_Sound 下面的 Dust_L/Dust_R 下放出。

它们也可以用于 engine 排除的废气。

首先设置好 Dust_# 的 Particle System。

然后，调整 Dust_# 中的 Emission_Control_CS 的属性：

- Reference Wheel

  emission rate 根据这个参考 wheel 的速度控制。

- Reference Parent Name
- Reference Name

  如果设置了 Reference Wheel，它们被自动设置，通常不需要改变。

- Max Velocity

  当速度超过这个值的时候，emission rate 将达到最大。

- Type

  根据 particle system 的 Emission 模块选择类型：

  - Time：脚本将控制 Rate Over Time 属性
  - Distance：脚本将控制 Rate Over Distance 属性

- Curve

  设置 emission rate 的 curve。

- Max Rate

  当 curve value = 1 时的 emission rate。

- Adjust Alpha

  Particle System 的 Start Color 的 alpha，可以根据 scene 中的 light 的强度自动降低。

  注意：要使用这个功能，需要挂载 Main_Light_Control_CS 脚本到 main light 上。

  这个功能可以是 particles 在黑暗的 scene 中更自然。

  - Standard Light Intensity

    设置 light 的标准强度。只有当 light 的强度小于这个值的时候，alpha 才会减小。

## Change Noticeability

Noticeability 是 tank 被 AI tanks 注意到的程度，它依赖于坦克 AI_Headquaters_Helper_CS 中的 Visibility Upper Offset 属性。

通常设置这个值为从 MainBody pivot 到 turret top 的距离。

如果这个值很大，tank 将很容易被检查到，即使在障碍物后面。

