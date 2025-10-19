# User Manual

## Playing Animations

基本用法
- 添加一个 AnimancerComponent
- 添加一个要播放的 AnimationClip asset
- 简单调用 animancer.Play(clip) 或者 animancer.CrossFade(clip)
- Play 立即从当前动画切换到要播放的 clip，CrossFade 则是渐变切换

AnimancerState：控制动画的类
- Play/CrossFade的返回值
- 访问和控制播放的动画片段
- Speed: 缩放的播放时间
- Time: 当前播放时间头
- NormalizedTime: 标准化的播放时间头
- OnEnd: animation结束的回调

Waiting for Animations: 当你开始一个 animation 之后，你会经常想要等待它完成以做一些其他的事情
- AnimancerState.OnEnd
- 在 coroutines 中, yield return AnimancerState
- 每次 update 检查 AnimancerState.NormalizedTime(当 value 达到 1 时，动画播放完成)

Edit Mode
- Animancer 可以在 Edit Mode 下播放动画，在 scene 中预览动画
- 在 Edit Mode 下无论何时脚本的实例被加载或者 value 在 Inspector 中被修改，UnityEditor 调用 MonoBehaviour.OnValidate
  
  调用 AnimancerUtilities.EditModePlay
  
  这个方法考虑了一些额外的事情，但是它的核心是它仍然是一个对 AnimancerComponent.Play 的调用

  ```C#
  [SerializeField] private AnimancerComponent _Animancer;
  [SerializeField] private AnimationClip _Idle;
  
  private void OnValidate()
  {
      AnimancerUtilities.EditModePlay(_Animancer, _Idle);
  }
  ```

- Rig Types
  - Playables API(and thus Animancer) 支持 Humanoid and Generic animations

## Component Types

- AnimancerComponent
  - Main entry point for controlling animations.
  - Bacially just a wrapper wround an Animator component and the internal AnimancerPlayable where all the magic happens
- NamedAnimancerComponent
  - Also has an Animations array
  - Registers animations by name so you can refer to them using strings, much like Unity's Legacy Animation component
- HybridAnimancerComponent
  - Has an animator controller
  - most of the same functions that are normally found on an Animator
  - You can have some animations in that Animator Controller while still makeing use of Animancer's ability to play other AnimationClips directly
- SoloAnimation
  - Plays one animation
  - assigned in Inspector
  - Doesn't support fading or layers or OnEnd event or any other features of Animancer
- Inherit from AnimancerComponent and add some AnimationEventReceivers to listen for certain Animation Events
- Animator Members
  - AnimancerComponent.Animator
  - Some of its members work normally with Animancer, others are not(in most cases they are simply not relevant)

## Blending

- Blending is the process of interpolating between multiple animations to combine them into a single output
- Different kinds of blending in Animancer
  - Transition/Fading: smoothly transition between two sequential animations instead of instantly snapping to the new pose suddenly
    - Play(): immediately snap to the specified animation
    - CrossFade(): smoothly transition to it over time
  - Layers: Play multiple separate animations at the same time using layers, allowing you to animate different body parts independently and add animations on top of each other
  - Blend Trees/Mixers: Use MixerStates to interpolate between multiple animations(all parts instead of different part like layers does) based on a parameter
- All states and layers in Animancer have an AnimancerNode.Weight which is a value between 0 and 1 that determines how much they affect the blended result.
- So rather than being explicitly in either a Walking and Running state, a character could be mixing a combination of both while Waving with their upper body on a second layer and fading towards a Standing animation, all at once

### Fading

- Calling AnimancerComponent.Play will immediately stop all other animations and snap the character's pose to the start the new one.
- Cross Fading: the animation weights cross over each other(in graph, like x)
  - AnimancerComponent.CrossFade
    - Within the duration, the currently active aniamtions weight fade to 0 from current weight, new animation weight fade to 1 from 0, no matter how length their remain time is
    - if the animation is already playing, it will continue to play, means CrossFade has no effect
  - AnimancerComponent.CrossFadeFromStart
    - Like CrossFade
    - Except if the target animation is already playing, it will be faded out as other currenty animations, at the same time a new state of the same animation fades in from the start of the clip. This ensures that it will always smoothly transition from the current pose into the start of animation.
  - AnimancerConponent.Transition
    - Provide a serializable way to configure Animation Transition in the inspector, instead of coding in script
    - takes an IAnimancerTransition as parameter
      - contains the details of a state
      - the way it should be played
      - it uses these details to automatically choose between Play/CrossFade/CrossFadeFromStart
  - AnimancerNode.StartFade
    - Start fading a specific node without affecting any others
    - AnimancerLayer and AnimancerState both inherit from AnimancerNode
      - AnimancerState: node connected sequential
      - AnimancerLayer: node played parallelly at the same time
    - Commonly used to fade Layers out when they aren't in use
    - There is no CrossFade for layers because they are not commonly used in that manner(CrossFade is sequential, Layer is parallel)
    - But you can get layer crossfade effect by calling StartFade(0) to fade some layers out and StartFade(1) for fade others in

### Layers

- When play an animation, it stops all others on the same layer without affecting animations on other layers
- This allows you to play multiple separate animations at the same time, using the layers to determine how they combine to form the final output
- AnimancerComponent.Play/CrossFade has a in layerIndex = 0 parameter that determines which layer the animation will be played on
  - Defalut: 0, Player(clip) == Player(clip, 1)
  - Creating Layers
    - automatically create a layer that does not exist
    - AnimancerPlayable.maxLayerCount = 4
  - Changing Layers
    - if an AnimancerState already exists for the animation and you specify a different layer, the state will be moved to that layer
    - You can also move states to a different layer by setting animancerState.LayerIndex
  - AnimancerComponent.GetLayer
  - AnimancerLayer inplicit cast to int
  - Factors which determine how the output of each layer is combineed to form the final result
    - Weight
      - each layer has weight
      - StartFade: fade layer in and out over time
      - StartFade only affects layer you call it on, there is no CrossFade for layers because it is not common to swap them like state, layers usually means to play parallelly
      - Layers start at weight = 0 be default
      - calling Play() targeting a layer at 0 weight will automatically set its weight = 1
      - CrossFade will actually Play the animation at weight = 1 immediately and fade the layer in instead of fading the animation
      - if you want a layer to stop affecting the final output, you can simply fade its weight to 0 or set Weight = 0 to do it instantly
    - Masks
      - each layer can be given an AvatarMask to determine which bones it affects
      - You can create a mask using Assets/Create/Avatar Mask menu function and then assign it to layer using AnimancerComponent.SetLayerMask so that animations on that layer will only affect the parts of the model included in the mask
    - Additive Blending
      - each layer will override the previous layer by default, entirely replacing its output
      - Additive: add a layer's animations on top of the previous layer using AnimancerComponent.SetLayerAdditive
    - Names
      - AnimancerComponent.SetLayerName: give any layer a name
      - name will be displayed in the inspector
    - Play an animation on multiple layers at once, you will need to create multiple states for it and register them with different Dictionary Keys, or not register them at all and simply keep references to them yourself

### Mixers

- MixerState serve the samepurpose as Mecanim Blend Tree
- blend multiple animations based on a parameter
- parameter controls how much each animation affects the final output
- Mixers are usually setup in the Inspector using Mixer Serializables, but they can also be created manually
- Mixer types
  - ManualMixerState
    - Simply control the AnimancerNode.Weight of each state manually without any automated calculations
    - useful for additive animations and blend shapes for things like facial expressions
  - LinerMixerState
  - CartesianMixerState
  - DirectionalMixerState
- Mixers other than ManualMixerState have a Parameter property and Thresholds array(same type) which are used to calculate the weight of each state for you
  - When parameter is exactly equal to a particular threshold, the corresponding state will be at exactly 1 weight
  - When parameter is between Thresholds, Animancer will calculate fractional weights for these corresponding states based on the **interpolation algorithm** being used, then blending them using these weights to generate the final output
- MixerState are a type of AnimancerState
  - Clip property is null(it's for ClipState)
  - States inside an MixerState are not generally registered in the internal Dictionary
  - access these internal state: their index in the mixer itself, All inbuilt mixers expose their States as an array
  - Mixers don't have a duration or time of their own, so the OnEnd callback; pass on anything they are give to all of their child states
- Manual Creation
  - new LinearMixerState
  - Call Initialize()
    - Initialise(portCount)
      - allocates room for the specified number of states which can be filled individually using CreateState of by passing the mixer into the constructor or SetParent method of any state type(Mixer is also a state). This even let you nest mixers inside each other.
    - Initialise(clips, thresholds)
      - allocates a ClipState for each of the clips and assigns their corresponding thresholds
  - Make sure all states have been assigned thresholds to determine the parameter values
    - Using optional parameters in Initialise and CreateState methods
    - SetThreshold or SetThresholds
  - Store a reference to the mixer so you can set its Parameter later on to control its blending
  - In play mode, inspector show MixerState's child states with ability to expand the details of both the mixer and child states

- Blend Trees vs Mixers
  - Mixers are created dynamically at runtime
  - You can directly access the details of individual states
  - You can create your own mixer types that inherit from any of the existing ones to implement custom blending algorithms or add other feature
  - Blend Tree are created manually in the UnityEditor, cannot be changed at runtime

## State Serializables

- AnimancerComponent.Transition
  - IAnimancerTransition parameter
    - contains the details necessary to create an AnimancerState and choose which of the Play or CrossFade methods to actually use
  - This interface is implemented by a series of serializable classes corresponding to **each type of AnimancerState** which allow you to **specify animation details in the Inspector** so they can be edited as part of the scene(or prefab) rather than being hard coded
  - a ClipState.Serializable will create a ClipState to play a single AnimationClip
- Basic Serializables
  - AnimancerState.Serializable\<TState>
    - abstract base class for all other serializables. Only has a FadeDuration field
  - ClipState.Serializable
    - Inherits from AnimancerState.Serializable\<ClipState>
    - add an AnimationClip, Speed, and optional StartTime(either AnimancerState.Time or AnimancerState.NormalizedTime)
    - non-serialized OnEnd callback which is assigned to AnimancerState.OnEnd
      - means this property only used in runtime, will not serialize into asset
      - In runtime, it can be used to cache a delegate so the same instance is used every time the animation is played
  - AnimancerTransition
    - A ScriptableObject with a single ClipState.Serializable field
    - define the ClipState.Serializable' detail(AnimationClip, Speed, StartTime) as an asset that can be shared in multiple place rather than as part of a specific object in a scene
    - You can add more parameters to transition by inheriting from AnimancerTransition or create transitions for other state types by inheriting from AnimancerTransition\<TState>
  - ClipState.SerializableWithEndEvent
    - Inherits from ClipState.Serialiable to add a UnityEvent that it uses as the OnEnd callback so it can be configured in the inspector
- Controller Serializables
  - ControllerState.Serializable\<TState>
    - abstract base class for serializables that create states derived from ControllerState
    - ControllerState plays AnimatorControllers
    - Only has a RuntimeAnimatorController field
  - ControllerState.Serializable
    - Inherits from ControllerState.Serializable\<ControllerState> to create base serializable ControllerState(so it can be configured in inspector)
  - FloatControllerState.Serializable
    - Inherits from ControllerState.Serializable\<FloatControllerState>
    - adds a ParameterName field to create a FloatControllerState which wraps that particular parameter
    - The field uses a dropdown menu in the Inspector to allow you to select the name of any Float parameter
  - Vector2ControllerState/Vector3ControllerState
- Mixer Serializables
  - ManualMixerState.Serializable\<TMixer>
    - State means Node(in playble graph)
    - abstract base class for serializables that create states derived from ManualMixerState
    - Has an AnimationClip array and Speeds array
  - ManualMixerState.Serializable
    - Inherits from ManualMixerState.Serializable\<ManualMixerState> to create a base serializable ManualMixerState
  - MixerState.Serializable\<TMixer, TParameter>
    - abstract base class for serializables taht create states derived from MixerState
    - Has a Thresholds array and DefaultParameter field
  - LinearMixerState.Serializable
    - Inherits from MixerState.Serializable\<LinearMixerState, float> to create serializable LinearMixerState
  - MixerState.Serializable2D
    - Inherits from MixerState.Serializable\<MixerState\<Vector2>, Vector2> to create serializable MixerState\<Vector2>
- Custom Serializables
  - You can create your own serializables
    - implementing IAnimancerTransition from scratch
    - inheriting from AnimancerState.Serializable or any its derived types
  - You may want to alter the way it is drawn in the inspector
    - create another class that inherits from the Drawer class inside the Serializable you are inheriting from
    - implementing your own propertyDrawer


## Animation Events

- You will often have the need to do things at certain time during an animation
  - playing a footstep sound each time a foot touches the ground during a walk cycle
  - applying the effects of an attack at a specific point during a sword swing
  - You can script these things using coroutines or other timer
  - using Animation Events allows you to more easily coordinate the script with the animation
- Using the animatin Event Systemis the same with Animancer as without it
- Simply attach a script to the same object as the Animator Component, and the engine will look for methods with appropriate names in that script
- Just like how will you use the event in Mecanim, you define event in AnimationClip time line, configure the callback function name and it's parameter, then when the clip is playing, the events trigger all the callback function. It does so in Animancer.
- Special Event function name
  - "Event"
    - Can trigger SimpleEventReceiver component's onEvent property
    - SimpleEventReceiver can be useful in a simple game if you set up all of your animations with only one event, and each that uses "Event" as the Function name
    - SimpleEventReceiver is a component, so the "onEvent" property can be set both in Inspector or Script
      - When setup in Script, SimpleEventReceiver.onEvent.Set(state, ...)
  - "End"
    - trigger AnimancerState.OnEnd callback
    - AnimancerState.OnEnd callback normally only gets called when the animation finish
    - CrossFading need a event trigger before animation finish
    - "End" function can be set as Event ahead of animation clip end, so the AnimancerState.OnEnd can be called earlier
    - if you haven't registered one or the one you have registered doesn't stop animation(usually be starting a different one by Play/CrossFade) then the current animatin will continue playing and will still trigger the OnEnd callback when it ends normally, otherwise OnEnd be called at the time "End" event is anchored
    - Specify fadeDuration when use "End" to CrossFade
      - use static AnimancerPlayable.GetFadeOutDuration to get value from Float parameter of the triggering event, so you can configure the fadeDuration in the Function Inspector
        - if call this method when there is no event, returns the minDuration
        - if the Float parameter <= 0, return remaining time of current animation
        - othewise, return the Float parameter
      - hard code in script
