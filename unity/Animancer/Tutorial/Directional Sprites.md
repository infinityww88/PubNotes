```C#
DirectionalAnimationSet animations;
AnimationClip clip = animations.GetClip(Vector2);
_Animancer.Play(clip);
_Animancer.States.Current.Speed = ...;
```