# Glossary

## Spline

载有CurvySpline组件的对象

## Control Point（CP）

控制spline曲率的点。Curvy的控制点是常规的GameObject对象，附加有CurvySplineSegment组件，总是一个spline对象的子对象并且被自动管理

## CG

Curvy Generator

## Tangent

切向量是一个spline点的方向

## Up

方向或向上向量，定义一个spline点的上方向。与Tangent一起组成了一个给定spline点的被controller使用的旋转（例如，沿着曲线运动时，在每个点将运动的物体与所在曲线点的方向对齐）

## Total Fragment（TF）

spline上的相对位置，[0, 1]

## F

曲线被控制点分割成多个片段segment，F表示一个segment上的相对位置

## Orentation Anchor

被dynamic orientation模式使用，这个控制点选项告诉Curvy使用这个控制点的transform rotation作为方向目标。将orientation想象成waypoint
