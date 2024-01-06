# Create a new tank

## 准备场景

可以从头开始创建一个新坦克，但是 remodel 一个具有相似结构的现有坦克更容易。

- 为新 tank 准备 3d 模型和 materials

  要使用外部 tank 模型有一些规则。绝大多数情况下，你需要使用 3d 建模工具 remodel 它们。需要的建模弓箭包括：

  - 将 object 分离为几部分，例如 Turret 分离为 Turret, Cannon, Barrel
  - 合并 objects 为一个整体，例如 Hull + Skirts + Hatches 为 MainBody
  - 改变 position，rotation，scale
  - 重置 pivot
  - 使用基本 objects 创建简单 mesh
  - 以正确 scale 和 rotation 导出模型到 Unity 中

- 打开 demo scene Exam_Field

  这个 scene 有一个平坦的 ground，可以方便用于创建新坦克。

- 从场景中移除所有坦克

- 设置 base tank

  拖拽一个 base tank 到场景中，确保 tank 放在 origin 上。

  使用带有 Physics_Track 的 tank prefab 作为 base tank，例如 \#\#\#\_PT.

  带有 Static Track（\#\#\#\_ST）和 \#\#\#\_AI 的坦克 prefab 不适合用来 remodel 它们的 wheels 和 tracks。

  例如，使用 Prefab_Tanks/PhysicsTrack/目录下的 Cromwell_PT prefab 作为 base tank。

- Unpack prefab instance 来 remodel 它

- 起一个新的名字

## 替换 Turret

- 改变 Turret 的外观

  选中 Turet_Base，改变：

  - Mesh

    设置 turret 的 mesh asset。

  - Material

    设置 turret 的 material。

  - MeshColldier
  
    设置用作 turret collider 的 mesh。
  
- 设置 Turret_Base 的 position

  设置 turret 的 rotation pivot。

  turret 从不移动，即使移动了 Turret_Base。

  如果需要调整 turret 的位置，改变 Offset X/Y/Z 的值。

- 改变 Cannon 的外观

  和 Turret 一样，选中 Cannon_Base，然后改变 Mesh，Material，MeshCollider。

- 设置 Cannon_Base rotation pivot 的 position

- 改变 Barrel 的外观，设置 Barrel center 的位置。

- 设置 Bullet_Generator 和 Gun_Camera 的位置

- 在运行时测试新的 turret，检查以下几点：

  - turret 绕着它的 pivot 旋转
  - cannon 绕着它的 pivot 旋转
  - bullet 和 muzzle fire 在 muzzle 前面生成
  - gun camera（reticle screen）可以帮助你瞄准目标

## 替换 MainBody

- 替换 MainBody 外观

  选中 MainBody，修改 Mesh，Material，MeshCollider。

  MainBody 的 collider 如果是凹多面体，应该分成多个凸多面体部分，例如 Upper，Lower。否则如果 track 部分可能会与它碰撞并断开。因为 collider 的凹面被物理模拟忽略。


- 调整 Extra_Collider

  Extra_Collider 是挂载的一个特殊 collider，用于检测其他坦克。没有这个 collider，Wheels 会因为 collision settings 侵入其他坦克。

  调整 Extra_Collider 的 Transform values（position，scale）使其大体匹配 body 大小。

### 替换 RoadWheels

RoadWheels 是路轮，既压在履带上，支持车体的轮子。

可以在 tank 上的 Create_RoadWheel 中替换 RoadWheels。

首先进入 Prefab Mode 或 Unpack Prefab，以替换 wheels。

- 替换 suspension arms 和 wheels 的外观

  选中 Create_RoadWheel 并改变：

  - Left Arm Mesh/Right Arm Mesh
  - Wheel Mesh
  - Material
  
  如果不需要悬挂臂的外观，可以将 Arm Mesh 设置为 None。

- 调整位置

  移动 Create_RoadWheel 到第一个悬挂臂的 mouting position，注意保持 Position X = 0。

- 设置 arms 的 layout

  - Arm Distance：设置 left arm 和 right arm 的距离。
  - Number：设置一侧 arms(wheels) 的数量。
  - Spacing：设置两个 arm(wheesl) 之间的间距。
  - Length：设置 arm pivot 和 wheel pivot 之间的距离

- 设置 Wheel Distance，左右 wheel 之间的距离

- 设置 wheels 的半径，Wheel Collider Raidus

- 调整 spring 和 angles

  spring 和 angles 设置对 tank 很重要，但是 track 还没有 remodel。因此可以先临时设置，并在完成新的履带后再修复。

  - Sus Spring Force

    设置每个悬挂臂的弹簧力。当路面不平整时，增加这个值。

  - Sus Damper Force

    设置每个悬挂臂的阻尼力。当这个值增加时，悬挂臂工作的很慢（弹性恢复慢）。

  - Sus Spring Target Angle

    设置弹簧的目标角度。当悬挂臂旋转到这个角度，弹力将变成 0.

  - Forward Limit Angle/Backward Limit Angle

    设置悬挂臂的角度范围。

### 替换铰链轮 SprocketWheels

铰链轮的齿对履带片段 track pieces 没有任何作用。track pieces 通过 wheels 和 track pieces 之间的摩擦力移动。

可以通过 tank 上的 Create_SprocketWheel 替换铰链轮。

- 替换 SprocketWheel 的 Mesh，Material

- 调整位置

  将 Create_SprocketWheel 移动到 SprocketWheels 的 mounting position，保持 Position X = 0.

- 设置左右 wheels 的距离，Wheel Distance

- 设置 wheel 的半径，Wheel Collider Raidus

  the cogs of the SprocketWheel have no effect on the track pieces. Therefore set the value a little smaller than the apparent size.

### 替换传导轮 IdlerWheels


IdlerWheel 被挂载到一个用于调整 tracks tension（松紧程度）的小 arm 上。

在 Create_IdlerWheel 上替换 IdlerWheels。

- 改变 arms 和 wheels 的 Mesh，Material

- 调整位置，将 Create_IdlerWheel 移动到 tensioner arms 的 mouting position 上，保持 Position X 为 0。如果 tank 没有任何 tensioner arm，将它移动到 IdlerWheels 的 mounting position。

- 设置 arms 和 wheels 的距离

  - Arm Distance：left arm 和 right arm 之间的距离

  - Wheel Distance：left wheel 和 right wheel 之间的距离

- 设置 arm 的 Length，arm pivot 和 wheel pivot 之间的距离

  如果坦克没有 tensioner arm，可以跳过这一步。

- 设置 wheels 的 radius, Wheel Collider Radius

- 调整 arm 的 angle

  tensioner arms 的角度对调整 tracks 的 tension 很重要。但是 tracks 还没有 remodel，可以先临时设置，等到创建新的履带后再修复。如果坦克没有 tensioner arm，跳过这一步。

### 替换支撑轮

支撑轮在路轮上方，支撑履带传导。

有的坦克没有 SupportWheel。如果作为模板的坦克没有 SupportWheel，首先需要添加 Create_SupportWheel 到坦克上。

- 添加 Create_SuportWheel

  可以在 Prefabs/Tank_Components 找到 Create_SupportWheel。将它拖拽到 MainBody 上，然后 Unpack Prefab。确保 Create_SupportWheel 是 MainBody 的 child。

- 替换 SupportWheels

  选择 Create_SuportWheel 并修改 mesh，material。

- 调整位置，将 Create_SupportWheel 移动到第一个 SupportWheel 的 mounting position，保持 Position X = 0.

- 设置 wheels 的 layout

  - Wheel Distance：左右 wheel 的距离
  - Number：支撑轮的数量
  - Spacing：同一侧两个轮之间的距离

- 设置 wheel 的半径，Wheel Collider Radius

### 替换 Physics_Track

这个项目中有三种类型的履带：

- Physics_Track

  所有 pieces 被物理模拟移动。Motion 非常真实，但是在游戏场景中有很大的性能消耗。

- Static_Track

  所有 pieces 被脚本控制。Motion 不算太糟糕，很适合游戏场景。

- Scroll_Track

  一个具有 texture-scrolling 和 deforming 的简单 belt-shaped track。Motion 和 appearance 很糟糕，但是具有最小的性能消耗。

Physics_Track 在编辑器中有一个简单的椭圆形状，但是在运行时会物理地变形。另外，Physics_Track 很容易转换为 Static_Track。

- 修改 pieces 的外观

  选中 Create_TrackBelt，在 Create_TrackBelt_CS 中修改：

  - Left Piece Mesh/Right Piece Mesh

  - Material

  - Use Secondary Piece

    如果 track 有两种 pieces，开启这个选项，为第二块履带片设置 mesh 和 material。

  - Use Shadow Mesh

    可以设置一个简单的 shaped mesh 用作 pieces 的 shadow，以提升 GPU 性能。

    - Left Shadow Mesh/Right Shadow Mesh
    - 为 pieces 设置用作 shadow 的 mesh

- 设置 pieces 的 layout

  - Distance：左右 piece 的距离
  - Spacing：两个 piece 的间距

- 调整位置和形状

  移动 Create_TrackBelt 到差不多 front wheel 下面的地方。然后通过调整下面的值来 deform track shape，使得 wheels 大致在 tracks 内部。

  - Front Arc Angle/Rear Arc Angle
    
    履带弧度部分每个 piece 之间的角度差。值越小，履带弧度越大。

  - Number of Straight

    履带平直部分的 piece 数量。

  注意，使履带比理想形状略小一点，因为 Physics_Track 很容易在运行时拉伸履带。

  可以通过调整 Transform 的 Rotation X 旋转 tracks。

- 设置 piece 的 colliders

  track pieces 有两个交叉的 Capsule Colliders。根据 piece 的外观设置 Center，Size。

- 调整 fender 挡泥板的 colliders

  一些 prefab tanks 有 Fender_Colldier 放在 tracks 上面，使得 pieces 不会穿过 fenders。根据 fenders 的 shape 调整 collider。

  注意 collider 的摩擦力 friction 被设置为 0，这样 pieces 可以平滑的移动，只是限制不会穿越 fenders。

- 在运行时测试 tracks。可能会发现以下问题：

  - tracks 穿越了 wheels
  - tracks 在开始时断裂
  - tracks 在运行或转弯时拉伸
  - 一些 pieces 总是抖动
  
  下面会描述如何修复这些问题。

## Fix Physics_Tracks

当 tracks 在停下时已经具有理想的形状后，可以将 tracks 转换为 Static_Track，以适合游戏场景。履带不需要再运行时表现的完美，只需要静止时理想就可以。

- 调整位置和形状

  当履带被卡在 body 或 fenders 中，调整 Create_TrackBelt，然后改变 tracks 的形状。

  可以改变履带形状而不改变 pieces 的数量。通过 Front/Rear Arc Angle 改变履带形状。还可以通过调整 Transform 的 Rotation X 旋转 tracks。

- 开启 Wheel Resize 选项

  当 wheel 从履带中突出出来，尝试开启 Create_\#\#\#Wheels 中的 Wheel Resize 选项。Wheels 会在第一帧 resized 到指定的 scale。然后再指定的速度回到原始 size。

  当 tracks 穿过了 small wheels，设置 Scale Size 大于 1.

- 调整 RoadWheels 的 angle

  当 Road Wheels 从 tracks 中突出出来，调整 Create_RoadWheel 的 Angle，使得 RoadWheels 在 tracks 内部。

- Enable Soft Landing 选项

  当 tracks 在开始时由于与地面撞击而断裂，在 MainBody 上尝试开启 Soft Landing。这样坦克开始时会慢慢 fall down。

- 调整 tracks 的 tension

  如果 track pieces 在停下时抖动，Loosen tension of tracks：

  - 增加 track pieces 的数量。可以通过改变 Front Arc Angle 或 Rear Arc Angle 一次增加一个 piece。
  - 调整 Tensioner Arms。当 IdlerWheels 有 tensioner arms，可以通过改变它们的角度调整 tension。调整 Create_IderWheel 的 Angle 使得 tension 更宽松。
  - 增加 pieces 之间的 Spacing。
    pieces 之间的 spacing 应该更加 piece 的外观设置。但是如果不是特别明显，可以略微调整。在 Create_TrackBelt 上调整 pieces 的 spacing。

- 增加 physics simulation 的 quality

  不幸的是，track pieces 在默认的物理设置中，在高速运行下不能保持它们的连接。如果 tracks 在高速行驶时抖动或断开，需要提高物理模拟的质量，尽管这需要消耗更多的性能。

  physics 的 quality 通过减小 Game_Controller 的 Fixed TimeStep 来提升。

  如果需要一个适合于 battle scenes 的 tank，将 tracks 转换为 Static_Tracks。Static_Track 在默认的 physics settings 中可以在高速下工作。

## 创建 Static_Track

Static_Track 通过转换在运行时基于物理变形的 Physics_Track 而来。因此 Physics_Tracks 必须在停止时具有理想的形状。

注意，不需要 Physics_Tracks 在行驶时表现完美。

需要 Unpack Prefab 来创建 Static_Track。

- 备份坦克

  通关创建新的 Prefab 备份 tank。

- Unpack Prefab instance

  选择 Create_TrackBelt，点击 Unpack Prefab。

- 开启 for Static Track 选项

- 进入 play mode

- 确保 tracks 是基于物理地变形，并具有理想的形状，点击 Create Prefab in 'User' folder 按钮。

  Camera operation 在几秒钟后会 cancel，因为 scene 被暂停以保持 tracks。

- 在 User folder 中找到新的 Static_Track，命名为 Static_Track \#\#\#\_\#\#\#

- 将新的 Static_Track 拖拽到 MainBody。确保它是 MainBody 的 child

- Physics_Track 不再需要，移除或 inactive Create_TrackBelt GameObject。

- 点击 Static_Track 的 Unpack prefab 按钮，unpack prefab instance。

- 设置 Static_Track

  Statci_Track 的基本设置几乎是自动设置的。

  - 点击 SetAutomatically 按钮
  - 确保 Left/Right Reference Wheel 等个属性值被设置好

- 选择 MainBody，点击 Update Values 按钮

  Mass 和 Solver Iteration Count 被自动更新。body 的 weight 将会增加和所有 track pieces 一样的重量，因为 Static_Track 的 piece 没有重量。

  Solver Iteration Count 被降低到 10，因为 Static_Track 在物理模拟中不需要很高的精度。

- 更新 RoadWheels

  点击 Create_RoadWheel 中的 Update using stored values 按钮。确保 RoadWheels 已被更新来适应新的 tracks。

- 更新 tank 的其他 wheels

  分别点击以下组件的 Update Values：

  - Create_IdlerWheel
  - Create_SprocketWheel
  - Create_SupportWheel

- 在运行时测试新的 tracks

  在地面上行驶和转弯坦克，测试新的 Static_Track，检查：

  - 根据地形变形 tracks
  - wheels 随 tracks 运动同步旋转
  - tank 可以平滑转弯

## 修复 Static_Track

Static_Track 有三种类型的 track pieces：

- Static：只根据 tank 速度值移动到下一个 piece
- Dynamic：更具 front 和 rear pieces 移动和旋转
- Anchor：根据特定 wheel 上下移动

这些类型的 pieces 在它们创建时自动设置。但是也可以手工重置。

- 当 tracks 没有按预期变形

  使用 Static_Track 中的以下功能重置 pieces 的类型：

  - Set Types with RoadWheels

    靠近每个 RoadWheel 的 pieces 被设置为 Anchor type，因此这些 pieces 跟随 RoadWheels。

  - Set Types with SwingBalls

    靠近每个 SwingBall 的 pieces 被设置为 Anchor type，因此这些 pieces 跟随 SwingBalls。

  - Make Upper Pieces 'Static'

    所有 upper pieces 被设置为 Static 类型，不跟随任何东西。如果 upper pieces 在 skirts（裙板）后面，这可以用于优化，因为不用再模拟 upper pieces。

  - Make All Pieces 'Static'

    所有 pieces 被设置为 Static type，不跟随任何东西。


  结果将展示在 Console window 中。如果不能得到满意的结果，调整每个 Effective Range 的值。

  还可以通过选择 piece，改变每个 piece 的 type。piece 对侧的 piece 自动跟着改变。

- 如果路轮之间的 pieces 穿越了路面的突出物体

  挂载不可见的 RoadWheels 到 gaps，使附近的 pieces 跟随 wheels。Static_Track 的 piece 是跟随 wheel 来变形和移动的，物理引擎只模拟 Wheels 的效果，不模拟履带的效果。

  - 复制 tank 中的 Create_RoadWheel
  - 调整 wheels 的位置和数量，使得 wheels 填充 gaps
  - 使新的 wheels 的 mesh 为空，这样 arms 和 wheels 都不可见
  - 重新设置 pieces 的类型

## 使用 SwingBalls

SwingBalls 是不可见的 physics objects，使用 Configurable Joints 挂载到 MainBody 上。

它们根据坦克在运行时的运动上下摇摆。

通过使用 SwingBalls 可以在 Static_track 中实现摇摆运动。

Scroll_track 不能和 SwingBalls 一起使用，来得到摇摆效果。

- 挂载 Create_SwingBall 到 MainBody 上

  在 Prefab/Tank_Components 目录中找到 Create_SwingBall，拖拽到 MainBody 上，确保是 MainBody 的子节点。

- Unpack prefab

- 设置 Create_SwingBall

  绝大多数情况下，可以只点击 Align With RoadWheels 或 Align with SupportWheels 按钮就可以设置它们。然后 SwingBalls 被分别设置到 RoadWheels 或 SupportWheels 上面。

  然后复制 Create_SwingBall 并向前移动它，使得 SwingBalls 被设置在 wheels 之前的空隙。

- 设置 Static_Track

  选择 Static_Track，点击 Set Types with SwingBalls/RoadWheels 按钮。

  如果得不到满意的结果，调整 Effective Range 的值。

- 在运行时测试 Motion，确保 pieces 根据 tank motion 而摇摆。

  如果 track pieces 穿过了 fender，移除 Fender_Collider。

## 使用 Track_Colliders

Track_Collider 是一个特殊的 collider，用作 Static_Track 和 Scroll_Track 的 weak point。当 bullet 或 explosion hit 到这个 collider 时，track 的 hit points(hp) 将减少。当 hit points 减少到 0，Static_Track 断开。对于 Scroll_Track，track 简单消失。

- 挂载 Track_Collider 到 Static_Track。可以在 Prefabs/Tank_Components 找到 Track_Collider。将它拖拽到 Static_Track 中作为 child。
- Unpack Prefab

- 调整 position。Track_Collider 是一个透明的 box，将它移动到 track 的前面
- 设置 Linked Piece

  点击 Track_Collider 中的 Find the closest piece 按钮。最近的 track piece 将被设置为 Linked Piece。履带被摧毁后将在这个里断开。此外，position 和 scale 也被自动调整。

- 复制任意多个 Track_Colldier，并以相同的方式设置，不要忘记设置 Linked Piece。

  通常在履带前后设置 4 个。

- 在运行时测试，用其他坦克设计 Track_Collider。

还可以创建 Scroll_Track 在 battle scene 中进一步提升性能。Scroll_track 可以和 Static_Track 一起用于 Track_LOD 功能。

