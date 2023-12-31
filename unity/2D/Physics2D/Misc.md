# Physics2D

如果场景中有 Collider2D（无 rigidbody2d）在脚本控制下运动或旋转，会阻止其他
rigidbody2d sleep，尽管其速度或角速度都已经小于阈值。

可能的原因是：sleep 是物理引擎的一个优化，当 rigidbody
进入休眠后，不再进行物理模拟，直到对它施加一个力或者被其他 rigidbody
碰撞。因此通常不会影响正常物理效果。但是对于没有 rigidbody2d
的碰撞体 Collider 碰撞休眠的
rigidbody，就没办法唤醒它了。因此为了得到正确的结果，Unity 索性当场景中有
static collider 在脚本控制下运动时，直接禁止其他 rigidbody 休眠，以便在 static
collider 碰撞它时能正确反应。

毕竟 Sleep 只是一个优化措施，Unity
不对它何时生效进行任何保证。因此尽量不使用它做逻辑判断，如果需要自己通过速度和角速度来判断
rigidbody 是否进入静止状态。这是业务层的判断，物理层的 rigidbody 仍然在
awake，因此它仍然能对接下来可能的碰撞进行响应。

如果一定要使用 rigidbody 的 sleep，一种修复措施是将所有通过脚本控制运动的
collider 加上 Kinematic rigidbody，这样与 static collider
效果一样，但是此时就不会阻止其他 rigidbody 进入 sleep 状态了。

Rigidbody2D sleep 后，不会在触发 OnTrigger2DStay，即使它仍然在 Trigger2D 内部。3D 则始终会触发 OnTriggerStay。
