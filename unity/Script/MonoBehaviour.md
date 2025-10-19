# MonoBehaviour

## Description

MonoBehaviour 是每个 Unity script drive 的基类。

这类不支持 null-conditional operator(?.) 和 null-coalescing operator(??)

有一个 checkbox 用于在 Editor 中 enabling 和 disabling MonoBehaviour。当 uncheck 时，它 disables functions。如果这些 functions 没有任何一个出现在 script，Unity Editor 不会显示 checkbox。这些 functions 是：

- Start()
- Update()
- FixedUpdate()
- LateUpdate()
- OnGUI()
- OnDisable()
- OnEnable()

## Properties

- runInEditMode：允许一个 instance 在 edit mode 中运行
- useGUILayout：关闭这个跳过 GUI layout phase

## Public Methods

- CancelInvoke

- Invoke

- InvokeRepeating

- StartCoroutine

- StopAllCoroutines

- StopCoroutine

## Static Methods

- print

## Messages

- OnAnimatorIK(int layerIndex)

  layerIndex：IK solver 被调用的 layer 的 index

  设置 animation IK 的回调

  OnAnimatorIK() 在 Animator Component 上它开始 update 它的内部 IK system 之前立即调用。这个 callback 可以被用来设置 IK goals 的 position 和它们各自的权重。

  ```C#
  using UnityEngine;
  using System.Collections;
  
  public class ExampleClass : MonoBehaviour
  {
      float leftFootPositionWeight;
      float leftFootRotationWeight;
      Transform leftFootObj;
  
      private Animator animator;
  
      void Start()
      {
          animator = GetComponent<Animator>();
      }
  
      void OnAnimatorIK(int layerIndex)
      {
          animator.SetIKPositionWeight(AvatarIKGoal.LeftFoot, leftFootPositionWeight);
          animator.SetIKRotationWeight(AvatarIKGoal.LeftFoot, leftFootRotationWeight);
          animator.SetIKPosition(AvatarIKGoal.LeftFoot, leftFootObj.position);
          animator.SetIKRotation(AvatarIKGoal.LeftFoot, leftFootObj.rotation);
      }
  }
  ```

- OnAnimationMove

  用于处理动画运动的 callback，用来修改 root motion。

  这个 callback 在每帧 state machines 和 animations 被求值之后（已经输出动画数据）但是在 OnAnimationIK 之前被调用

  ```C#
  using UnityEngine;
  using System.Collections;

  public class Example : MonoBehaviour
  {
      void OnAnimatorMove()
      {
          Animator animator = GetComponent<Animator>();

          if (animator)
          {
              Vector3 newPosition = transform.position;
              newPosition.x += animator.GetFloat("Runspeed") * Time.deltaTime;
              transform.position = newPosition;
          }
      }
  }
  ```

- OnApplicationFocus

- OnApplicationPause

- OnApplicationQuit

- OnAudioFilterRead

- OnBecameInvisible

- OnBecameVisible
