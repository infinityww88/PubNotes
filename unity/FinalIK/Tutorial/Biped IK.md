被 FBBIK 取代

BipedIK 是一个 IKSolver 的容器/包装器，使用各种 IKSolver 解析 limb、head、body 的 IK。对四肢各自使用一个 IKSolverLimb，对 LookAt 使用一个 IKSolverLookAt，对 spine 使用一个 IKSolverFABR，对 Aim 使用 IKSolverAim。

但是 FBBIK 包含了一个 IKSolverFullBodyBiped，在一个 IKSolver 中专门解析人形骨骼的 IK，而不是用多个 IKSolver 来解析。
