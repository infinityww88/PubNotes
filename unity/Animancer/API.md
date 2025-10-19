# Animancer API

## Class Types

### Animancer Component

- Summary
  - substitute for a UnityEngine.RuntimeAnimatorController
  - Mostly just a wrapper that connects an Animancer.AnimancerPlayable to an Animator
- Properties
  - Animator
    - the UnityEngine.Animator component which Animancer controls
  - CurrentState(AnimancerState)
    - the state of animation currently being played on layer 0
    - Specifically, the most recently started state using Play/CrossFade methods on Layer 0
    - individually controlled state(directly new/create) will not register in this property
  - IsPlayableInitialised
  - LayCount: the number of animation layers in the graph
  - Playable(AnimancerPlayable)
    - the internal system which manages the playing animations
  - StopOnDisable
    - ture: disabling this object will stop and rewind all animations
    - false: animations will simply be paused and will resume from their current state when it is re-enabled
    - default: true
  - UpdateMode:
    - when animation are updated and which time source is used
    - Wrap around the UnityEngine.Animator.updateMode
    - Change to or from UnityEngine.AnimatorUpdateMode.AnimatePhysics at runtime has no effect
- Methods
  - AddLayer() -> AnimancerLayer
    - create and return a new AnimancerLayer
    - New Layer are set to override earlier layers by default
  - CreateState(AnimationClip clip, int layerIndex) -> ClipState
    - Creates and returns a new Animancer.ClipState to play the clip
  - CreateState(Object key, AnimationClip clip, int layerIndex) -> ClipState
    - create state and register it with key
  - CrossFade(AnimancerState state, float fadeDuration) -> AnimancerState
    - Starts fading in the state over the course of the fadeDuration while fading out all others in the same layer, return the same state.
    - if the state was already playing, it will continue doing so from the current time, unlike CrossFadeFromStart
    - if the state was already playing and fading in with less time remaining than the fadeDuration, it will complete the existing fade rather than starting a slower one
    - if the layer currently has 0 weight, this method will instead start fading in the layer itself and simply Play(UnityEngine.AnimationEvent) the state(just for triggering event)
  - CrossFade(AnimationClip, float fadeDuration, int layer) -> AnimancerState
    - Starts fading in the clip over the course of the fadDuration while fading out all others in the same layer. Return its state
  - CrossFadeFromtStart(AnimancerState state, float fadeDuration) -> AnimancerState
    - if the fading in state isn't currently at 0 weight, this method will actually fade it out to 0 along with the others and (and the same time) create and return a new state with the same clip to fade to 1
    - This ensures that calling this method will always fade out from all current states and fade in from the start of the desired animation
    - States created for this purpose are cached so they can be reused in the future
