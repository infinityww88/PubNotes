# Directional Animation Sets

Directional Animation Set 是一种管理 up/right/down/left animations groups 的方便的方式（包括或不包括 diagonals），以及一种选择你想要哪一个的标准化的方法。

DirectionalAnimationSet 类包含相当多的功能，但是它的核心只是一个包含一些 AnimationClips 的 ScriptableObject，以及一个方法来选择最接近给定 direction Vector 的那个。

```C#
public class DirectionalAnimationSet : ScriptableObject
{
    [SerializeField] private AnimationClip _Up;
    [SerializeField] private AnimationClip _Right;
    [SerializeField] private AnimationClip _Down;
    [SerializeField] private AnimationClip _Left;

    public virtual AnimationClip GetClip(Vector2 direction)
    {
        if (direction.x >= 0)
        {
            if (direction.y >= 0)
                return direction.x > direction.y ? _Right : _Up;
            else
                return direction.x > -direction.y ? _Right : _Down;
        }
        else
        {
            if (direction.y >= 0)
                return direction.x < -direction.y ? _Left : _Up;
            else
                return direction.x < direction.y ? _Left : _Down;
        }
    }
}
```

DirectionalAnimationSet8 继承自 DirectionalAnimationSet 使得它有相同的字段，以及另外 4 个对角方向的 AnimationClips，并且它覆盖 GetClip 方法来选择 8 个 animations 中的一个。

## Creation

DirectionalAnimationSet 继承自 ScriptableObject，意味着你将它们创建为资源 assets，并在脚本中引用。Create/Animancer/Directional Animation Set/...

| Function | Effect |
| --- | --- |
| 4 Directions | 创建一个 empty DirectionalAnimationSet |
| 8 Directions | 创建一个 empty DirectionalAnimationSet8 |
| From Selection | 选择一些 AnimationClips，然后使用这个功能来创建一个 DirectionAnimationSet 或 DirectionAnimationSet8，它们引用那些动画。这需要动画名字是相同的，除了 "Up", "Right", "Down", and "Left" |
| | |

一旦你创建了一个 set，你可以手动为每个字段赋予一个动画，或者使用它的 Find Animations context 菜单在同一个目录下自动使用相同的名字（只有方向不同）赋值动画。例如，下面的 video 显示一个称为 Mage-Idle 的集合，它查找名为 Mage-IdleUp, Mage-IdleRight, Mage-IdleDown, and Mage-IdleLeft 的动画。

![find-animations](../../../Image/find-animations.gif)

Also note that DirectionalAnimationSets are not limited to only Sprite animations. For example, the Directional Blending example originally used a set to reference its movement animations before Mixer Transitions were implemented.

## Usage

在 scripts 中使用 DirectionalAnimationSets 非常容易：

1. 声明一个 Serialized 字段:

   ```C#
   [SerializeField] private DirectionalAnimationSet _Idles;
   ```

2. 确定你想使用的方向:

   ```C#
   // Input Vector:
   var direction = new Vector2(Input.GetAxisRaw("Horizontal"), Input.GetAxisRaw("Vertical"));
   
   // Or Enum (4 Directions):
   var direction = DirectionalAnimationSet.Direction.Right;
   
   // Or Enum (8 Directions):
   var direction = DirectionalAnimationSet8.Direction.UpRight;
   ```

3. 从集合中获得那个方向的 Get the AnimationClip for that direction from the set and Play it normally:

   ```C#
   // Assuming you also have a reference to an AnimancerComponent somewhere:
   // [SerializeField] private AnimancerComponent _Animancer;

   var clip = _Idles.GetClip(direction);
   _Animancer.Play(clip);
   ```

## Snapping

DirectionalAnimationSet.Snap 方法返回一个给定 Vector 的副本，指向那个 set type 包含动画最近的 direction。这可以用于 clamping 一个 input vector 为这个动画精确面向的方向使得你可以限制 character 只能在那些方向上移动。
