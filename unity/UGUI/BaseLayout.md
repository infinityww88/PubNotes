# BaseLayout

## Rect Tool

为了布局目的，每个UI元素都是一个Rect矩形。Rect Tool可以移动、缩放、旋转UI元素。将鼠标悬停在矩形corner附近，就可以出现旋转提示。

Rect Tool和其他工具一样使用toolbar当前的pivot mode（pivot/center）和space（global/local）。对于UI元素，最好使用Pivot模式和Local空间。

缩放改变的是RectTransform的width和height，而不是scaling，不影响字体大小，sliced image的border等等。

## RectTransform

RectTransform是Transform的子类，并且是所有UI元素的transform组件，它具有position、rotation、scale，还有width和height，用于制定rect的大小。

## Pivot

Rotation，size，scale围绕着pivot发生。只有在Pivot Mode下才可以调整pivot。

## Anchors

Anchors定义为parent RectTransform rect的百分比。左下角为（0，0），右上角为（1，1）。Anchors可以定义在parent rect内外的任何区域。Anchors不能超过0～1范围，但是Pivot可以超过0～1区间。

## Anchor presets

RectTransform提供了一组预定义的anchor定义。

## Inspector

RectTransform显示的信息根据anchor定位不同而不同。Anchors Min/Max显示为anchors在Parent Rect中的百分比。

Offset Min/Max定义为RectTransform Rect和Anchor Rect的Offset Vector。当Parent大小改变时，这个Offset保持不变，因此Anchor Rect随着Parent Rect改变，RectTransform Rect随着Anchor Rect改变。当Anchor在一起时（可以水平/垂直分开考虑），Anchor Rect=0，Offset Min/Max保持不变，RectTransform Rect的大小也不会变，只会随着Anchor改变位置；否则，RectTransform Rect随着Anchor Rect大小改变而改变。

如果Anchor在一起（水平/垂直可以分开考虑），RectTransform Inspector显示为Pos X/Y和Widht/Height，因为Width/Height不会随着Anchor Rect改变而改变，改变的是位置。否则，显示Left/Right，Top/Bottom，即Offset Min/Max的值。

改变anchor或pivot字段的值会相应调整positioning的值，使得Rect保持在原地不动，即根据Rect当前位置和新的Anchor/Pivot重新计算position。如果开启Raw Edit Mode，改变anchor导致Rect随着改变（保持Offset Min/Max不变），改变Pivot字段，Pivot保持不动，RectTransform移动以满足新的Pivot设置（Offset Min/Max也相应改变）。


