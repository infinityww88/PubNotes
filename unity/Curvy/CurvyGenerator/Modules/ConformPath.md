# Conform Path

通过投射射线使Path适应colliders

## Slots

- Input：Path
- Output：Path

## Reference

- Direction

    射线投射的方向，即适应的方向

- Max Distance

    最大投射距离

- Offset

    沿着投射方向定义一个偏移

    这可以用来使一个path浮动于一个物体之上，或者应对可见mesh的缝隙

- Warp

    整个path移动到最近可能距离。否则每个path point独立的移动

    disable时，每个point独立投射，并且落在投射hit point上

    enable时，整个path不会变形，而是移动到最小hit距离上

- Layer Mask

    射线投射检测的layer mask
