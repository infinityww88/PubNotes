# Lean Touch Components

## LeanFinger

这个类存储一个单个 touch（或 simulated touch）的信息。

主要方法包括：计算当前位置，历史位置，位置的距离之差，位置和参考点之间的角度，角度之差，世界位置，世界位置之差，屏幕空间位置、距离的分辨率无关版本。

Finger position 有 4 个版本：start，last，current，snapshot，很多计算都提供针对这4个 position 相应的版本。

- 属性

- int Index

  这是 finger 的硬件 ID。Simulated fingers 将使用 hardware ID -1 和 -2

- float Age

  finger 以及 active（或 inactive）多长时间（seconds）

- bool Set

  这个 finger 当前是否 touching screen

- bool LastSet

  最后一帧的 Set 值

- bool Tap

  这个 finger 是否刚刚 tap screen（for polling）

- int TapCount

  finger 已经 tap 多少次

- bool Swipe

  这个 finger 是否刚刚 swipe screen（for polling）。所有 bool flag 都是用于 polling 的，在 Update 中。

- bool Old

  如果 finger 已经 touching screen 超过 TapThreshold，则为 true

- bool Expired

  如果 finger 已经 inactive 超过 TapThreshold，则为 true

- float LastPressure

  最后一帧的 Pressure

- float Pressure

  这个 finger 的当前 pressure（只在支持压力检测的设备上）

- Vector2 StartScreenPosition

  finger 开始 touching screen 时的 ScreenPosition

- Vector2 LastScreenPosition

  finger 的上一帧 ScreenPosition，每次 Update 时，finger 将上一帧的 ScreenPosition 设置为当前帧的 LastScreenPosition

- Vector2 ScreenPosition

  finger 当前的像素 ScreenPosition，0,0 位于左下角

- bool StartedOverGui

  当前 finger 开始 touching screen 时 IsOverGui 是否为 true。记录 touching 开始时 finger 是否位于 GUI 上

- List<LeanSnapshot> Snapshots

  用来存储 position snapshots，使得 RecordFingers 可以使用它。因为很多手势都需要知道 touching 从开始的历史数据。Lean touch 提供了快照功能，可以记录一个 touch 的历史数据，而且快照主要是 position 信息，因为手势只使用 position 数据（而不是压力，或角度）。LeanTouch 还提供了各种基于历史快照的计算。另外，快照是基于 LeanTouch 组件上指定的条件产生的，例如每隔多长时间，每移动多少距离产生一个快照，记录 finger 的 position 和 timestamp。当你请求计算两个快照之间的数据时，使用两端的快照进行插值。

- bool IsActive

  如果 finger touching screen，则返回 true

- float SnapshotDuration

  finger 的连续的快照列表存储了多长时间

- bool IsOverGui

  如果当前 finger 位于 Unity GUI 元素之上，则为 true

- bool Down

  finger 是否在这一帧开始 touching screen

- bool Up
  
  finger 是否在这一帧停止 touching screen

- Vector2 LastSnapshotScreenDelta

  finger 从最后一个记录的快照移动的 pixels 距离

- Vector2 ScreenDelta

  返回 分辨率独立 resolution-independent 的 LastSnapshotScreenDelta value

- Vector2 ScreenDelta

  返回自最后一帧（last frame = 当前帧的上一帧）finger 移动的 pixels 距离

- Vector2 ScaledDelta

  返回 分辨率独立的 ScreenDelta

- Vector2 SwipeScreenDelta

  finger 自它开始 touching screen 移动了多远

- Vector2 SwipeScaledDelta

  返回 分辨率独立的 SwipeScreenDelta

  ```C#
    public Vector2 SwipeScaledDelta
    {
        get
        {
            return SwipeScreenDelta * LeanTouch.ScalingFactor;
        }
    }
  ```

- float SmoothScreenPositionDelta

  ```C#
    public float SmoothScreenPositionDelta
    {
        get
	    {
	        if (Snapshots.Count > 0 && Set == true)
		    {
                var c = Snapshots[Mathf.Max(0, Snapshots.Count - 3)].ScreenPosition;
                var b = Snapshots[Mathf.Max(0, Snapshots.Count - 2)].ScreenPosition;
                return Vector2.Distance(c, b);
		    }

            return Vector2.Distance(LastScreenPosition, ScreenPosition);
        }
    }
  ```

- Vector2 GetSmoothScreenPosition(float t)

  返回一个前一个和当前 screen position 之间的 smooth point，基于一个 0~1 进度值 t

  ```C#
    public Vector2 GetSmoothScreenPosition(float t)
    {
        if (Snapshots.Count > 0 && Set == true)
        {
            var d = Snapshots[Mathf.Max(0, Snapshots.Count - 4)].ScreenPosition;
            var c = Snapshots[Mathf.Max(0, Snapshots.Count - 3)].ScreenPosition;
            var b = Snapshots[Mathf.Max(0, Snapshots.Count - 2)].ScreenPosition;
            var a = Snapshots[Mathf.Max(0, Snapshots.Count - 1)].ScreenPosition;

            return Hermite(d, c, b, a, t); // Hermite 插值
        }

        return Vector2.LerpUnclamped(LastScreenPosition, ScreenPosition, t);
    }
  ```

- Ray GetRay(Camera camera = null)

  返回一个指定 camera 在 finger position 上的一个 ray（ camera = null 时，为 Main Camera）

- Ray GetStartRay(Camera camera = null)

  类似 GetRay，但是返回从 touching start position 的 ray

- Vector2 GetSnapshotScreenDelta(float deltaTime) / Scaled

  基于 Snapshot 历史记录 计算在过去 deltaTime seconds 中 finger 移动的距离（如果 deltaTime 位于 两个 Snapshots 之间，通过它们的插值得到）

- Vector2 GetSnapshotScreenPosition(float targetAge)

  类似 GetSnapshotScreenDelta，但是是返回 targetAge 时间点的 position 记录插值

- Vector3 GetSnapshotWorldPosition(float targetAge, float distance, Camera camera = null)

  LeanTouch 不仅返回屏幕空间位置，还计算一个相应的世界空间位置，计算的方式通过 Screen depth 指定。它使用相应的 Screen Position 方法返回的屏幕空间位置来计算 3D 坐标。

  GetSnapshotWorldPosition 使用 GetSnapshotScreenPosition 的屏幕位置。

- float GetRadians(Vector2 referencePoint)

  返回 finger 和给定 reference point 之间的角度，相对于屏幕（x 向右，y 向上）

- float GetDegrees(Vector2 referencePoint)

  类似 GetRadians，但是返回度而不是弧度

- float GetLastRadians(Vector2 referencePoint) / Degrees

  类似 GetRadians，但是计算的是 finger 的 last position

- float GetDeltaRadians(Vector2 referencePoint, Vector2 lastReferencePoint) / Degrees

  类似 GetRadians，但是计算两个角度，然后计算它们的差

- float GetScreenDistance(Vector2 point) / Scaled

  返回 finger 和给定点之间的距离

- float GetLastScreenDistance(Vector2 point) / Scaled

  返回上一次的 finger 的位置和参考点之间的距离

- float GetStartScreenDistance(Vector2 point) / Scaled

- Vector3 GetStartWorldPosition(float distance, Camera camera = null) / Last / Current

  返回 touching start position 从 camera 开始 distance 的世界位置，distance 也是世界单位

- Vector3 GettWorldDelta(float distance, Camera camera = null)

  返回上一次 finger position 和当前 finger position 对应的世界位置的差

- Vector3 GettWorldDelta(float lastDistance, float distance, Camera camera = null)

  为 last position 和 current position 指定不同的 distance

- void ClearSnapshots(int count = -1)

  清除这个 finger 的snapshots，并将它们放入 pool 中，count 指定 清理的 snapshot 的数量，-1 为所有

- void RecordSnapshot()

  调用这个函数立即记录当前 finger position 为一个 snapshot


## LeanGesture

这个类基于 touching screen 的所有 fingers 计算手势信息。这个类不是组件，只能在 C# 中直接使用。

- static Vector2 GetScreenCenter()/Try

  获得所有 fingers 的平均 ScreenPosition

  可以指定 fingers

  Try 版本返回 bool 类型，指示至少有一个 finger，返回值通过一个 ref 参数传递

- static Vector2 GetLastScreenCenter() / Try

  获取所有 fingers 的 last screen position 的平均位置

- static Vector2 GetStartScreenCenter() / Try

- static Vector2 GetScreenDelta() / Try / Scaled

  获得所有 fingers 的平均 ScreenDelta

  GetScreenDelta() * LeanTouch.ScalingFactor

- static Vector3 GetWorldDelta(float distance, Camera camera = null) / Try

  获得所有 fingers 的 world delta 的平均值

- static float GetScreenDistance() / Try / Scaled

  fingers 之间平均 ScreenPosition 距离。

  先计算所有 fingers 的 start position 的 center，然后计算每个 finger 到 center 的距离，最后计算这些距离的平均值

  可以指定 center，而不是使用所有 finger start position 的平均位置。

- static float GetLastScreenDistance / Try / Scaled

  使用 fingers 的 last position（上一帧 ScreenPosition） 计算

- static float GetStartScreenDistance / Try / Scaled

- static float GetPinchScale(float wheelSensitivity = 0.0f) / Try

  获得 fingers 的 pinch（挤捏） scale 程度

  可以指定 fingers

- static float GetPinchRatio(float wheelSensitivity = 0.0f) / Try

  pinch scale 的 倒数

- static float GetTwistDegree() / Try / Radians

  返回 fingers 的平均 twist（扭转）角度 / 弧度

  可以指定 fingers，center，lastCenter

## LeanSnapshot

这个类存储一个指定时刻一个 finger 的 snapshot，并提供方法回溯查找历史时刻的 finger 位置

- float Age

  snapshot 创建的时间戳

- Vector2 ScreenPosition

  snapshot 创建时 finger 的位置

- Vector3 GetWorldPosition(float distance, Camera camera = null)

  获得这个 snapshot 记录的 position 对应的世界位置，指定 distance

- static LeanSnapshot Pop()

  返回最后一个 inactive snapshot，或分配一个新的

- static bool TryGetScreenPosition(List<LeanSnapshot> snapshots, float targetAge, rev Vector2 screenPosition)

  返回这个 finger 在指定的 targetAge 的历史时刻记录的位置，通过在 snapshots 之间进行插值

- static bool TryGetSnapshot(List<LeanSnapshot> snapshots, int index, ref float age, ref Vector2 screenPosition)

  返回指定 index 的 snapshot 的信息：age 和 position

- static int GetLowerIndex(List<LeanSnapshot> snapshots, float targetAge)

  返回 age 小于 targetAge 的最近 snapshot 的 index

## LeanTouch

如果添加这个组件到场景中，它将转换所有 mouse 和 touch 数据为易于使用的数据。

你可以通过 Lean.Touch.LeanTouch.Instance.Fingers 访问这些数据，或者监听 Lean.Touch.LeanTouch.OnXXX 事件。

如果你遇到 touch 事件总是比自己脚本的 Update 延迟一帧，调整 ScriptExecutionOrder，强制 LeanTouch 在你的脚本之前执行。

- static List<LeanTouch> Instances

  包含所有 active 和 enabled LeanTouch instances

- static List<LeanFinger> Fingers

  包含当前所有 active fingers（包括 simulated 的 fingers）

- static list<LeanFinger> InactiveFingers

  包含当前所有 inactive fingers（这允许 polling 和 tapping）

- static event System.Action<LeanFinger> OnFingerDown

  当一个 finger 开始 touching screen 时发射（LeanFinger = 当前 finger）

- static event System.Action<LeanFinger> OnFingerUpdate

  当 finger touching screen 时，每一帧发射（LeanFinger = 当前 finger）

- static event System.Action<LeanFinger> OnFingerUp

  当 finger touching screen 停止时发射（LeanFinger = 当前 finger）

- static event System.Action<LeanFinger> OnFingerOld

  当一个 finger 的 ages 超过 TapThreshold，导致它不能再成为 tap 和 swipe 手势事件时发射

- static event System.Action<LeanFinger> OnFingerTap

  当 finger tap screen 时 发射（当一个 finger 在 TapThreshold 时间内开始和停止 touching screen）

- static event System.Action<LeanFinger> OnFingerSwipe

  当 finger swipe screen 时 发射（在 TapThreshold 时间内开始和停止 touching screen，并在其中移动超过 SwipeThreshold 距离）

- static event System.Action<List<LeanFinger>> OnGesture

  当至少一个 finger touching screen 时，每一帧发射（List = Fingers）

- static event System.Action<LeanFinger> OnFingerExpired

  当一个 finger 停止 touching screen 超过 TapThreshold 时发射，并且 finger 从 active 和 inactive fingers lists 中移除

- static event System.Action<LeanFinger> OnFingerInactive

  当一个 finger 停止 touching screen 之后发射，并从 active finger list 中移除。

  一个 finger 停止 touching screen 之后，从 active list 移动到 inactive list 中并发射 OnFingerInactive，因为这个 finger 稍后还会使用，例如 tap 手势。只有 停止 touching screen 超过 TapThreshold 之后，finger 才从 inactive 中移除，并发射 OnFingerExpired 事件。

- float TapThreshold

  设置一个 tap/swipe 手势需要的 finger down/up 之间的时间

- float SwipeThreshold

  设置 swipe 需要的在 TapThreshold 内 finger 移动的距离

- float ReclaimThreshold

  设置一个新的 touching finger 被回收时，必须的距离前一个 finger 的 pixels 距离（相对于 ReferenceDpi）（小于这个距离的 fingers 被认为是一个 figner）。这可以用于给出错误 finger ID 数据的平台。

- int ReferenceDpi

  你想 scaling input 基于的默认 Dpi

- LayerMask GuiLayers

  设置 GUI 位于哪个 layer 上，使得它可以被每个 finger 忽略

- bool RecordFingers

  每个 finger 是否应该记录它们的 screen positions 的 snapshot

- float RecordThreshold

  产生新的 snapshot finger 必须移动的距离

- float RecordLimit

  设置生成新的 record 的最大时间间隔，0 = unlimited

- float SimulateMultiFingers

  允许在不支持的设备上模拟 multi touch

- KeyCode PinchTwistKey

  设置哪个 key 用于模拟 multi key twisting

- KeyCode MovePivotKey

  设置哪个 key 用于改变 pinch/twist gesture 的 pivot point

- KeyCode MultiDragKey

  设置哪个 key 用于模拟 multi fingers dragging

- Texture2D FingerTexture

  设置用于显示模拟 fingers 的 texture

- static LeanTouch Instance

  第一个 active 和 enabled 的 LeaTouch instance

- static float ScalingFactor

  如果你乘以这个 value 到任何其他 pixel delta（例如 ScreenDelta），则它将变成相对 设备 DPI 分辨率独立的。不同 DPI 的设备应该具有不同的 ScalingFactor

- static float ScreenFactor

  如果你乘以这个 value 到任何其他 pixel delta（例如 ScreenDelta），则它将边长相对 屏幕 pixel size 分辨率独立的

- static bool GuiInUse

  如果鼠标或任何 finger 当前使用着 GUI，返回 true

- static bool PointOverGui(Vector2 screenPosition)

  如果指定的 screen point 位于任何 GUI 元素上面，返回 true

- static List<RaycastResult> RaycastGui(Vector2 screenPosition)

  使用当前 layer Mask 返回指定 screen point 下的所有 RaycastResults。第一个 result（0）是第一个遇到的 top UI 元素

- static List<RaycastResult> RaycastGui(Vector2 screenPosition, LayerMask layerMask)

- static List<LeanFinger> GetFingers(bool ignoreIfStartedOverGui, bool ignoreIfOverGui, int requiredFingerCount = 0)

  使用各种条件过滤 fingers

  如果 ignoreIfStartedOverGui 为 true，将移除任何 start 时在 GUI 上的 fingers

  如果 ignoreGuiFingers 为 true，将移除任何当前位于 GUI 上的 fingers

  如果 requiredFingerCount 大于 0 而 finger count 不匹配，将返回 null

- static void SimulateTap(Vector2 screenPosition, float pressure = 1.0f, int tapCount = 1)

  允许 screen 指定位置上模拟一个 tap
