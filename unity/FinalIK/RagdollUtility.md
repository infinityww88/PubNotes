FinalIK（以及 PuppetMaster）提供了一个非常易于使用的 Ragdoll 工具。

1. 在模型（Animator GameObject）上添加 BipedRagdollCreator，点击 Create a Ragdoll，就可以自动在模型上创建 ragdoll。创建 ragdoll 就是在模型骨骼 hierarchy 上的每个 bone 创建 rigidbody、collider、configurable joint。如果自动创建的 ragdoll 不理想，还可以在 Reference 中手动指定 bones

2. 添加 Ragdoll Editor 编辑 Ragdoll（可选），或者手动在骨骼 hierarchy 的 bone 上直接编辑 rigidbody、collider，configurable joint，尤其是 joint 的旋转的范围夹角

3. 添加 Ragdoll Utility

4. 添加控制脚本，开启或关闭 Ragdoll

   ```C#
   private RagdollUtility ragdoll;
   
   void Start()
   {
       ragdoll = GetComponent<RagdollUtility>();
   }

   void Update()
   {
       if (Input.GetKeyDown(KeyCode.D)) {
           ragdoll.EnableRagdoll();
       }
       if (Input.GetKeyDown(KeyCode.A)) {
           ragdoll.DisableRagdoll();
       }
   }
   ```

   Ragdoll 是 pose 的后处理，完全覆写动画的输出数据


Ragdoll Utility 控制切换 character 进入和离开 ragdoll mode。它还允许你在 ragdoll 模拟之上使用 IK effector。

- IK ik

  If you have multiple IK components, then this should be the one that solves last each frame.

  如果你有多个 IK 组件，则这应该是每帧最后一个 solve 的那个

- float ragdollToAnimationTime

  从 ragdoll 混合到 animation 需要的时间

- bool applyIkOnRagdoll

  如果为 true，IK 可以被用在 physical ragdoll 模拟上面

- float applyVelocity = 1, applyAngularVelocity = 1

  从 animation 向 ragdoll 传导多少线性速度和角速度

  动画在运行时 bone 是有一定线性和旋转速度的，切换到 ragdoll 物理模拟之后，将动画的速度传导给 ragdoll，更加真实

- void EnableRagdoll()

  切换到 ragdoll

- void DisableRagdoll()

  混合回 animation

