# Sculpting

## Introduction

Sculpt Mode类似Edit Mode用于修改model的形状。但是Scult Mode使用非常不同的workflow。相比直接处理独立的元素（vertices，edges，和faces），Sculpt使用一个brush修改模型的一个区域。换句话说，相对于选择一组vertices，Sculpt Mode操作brush影响区域的geometry

Sculpt Mode使用和其他painting modes相似的brush，但是它更高级一些。所有正常的brush控制依然可用，并且行为相同。Brush的影响区域仍然是View空间投影在mesh上的区域

## Tools

- Draw：Brush绘制的“颜色”是vertices沿着normal向内向外的偏移，基于包含在brush stroke中的vertices的平均normal

- Clay：类似Draw，包含setting来调整brush操作的plane。它像Flatten和Draw brushes的联合

- Clay Strips

- Clay Thumb

- Layer

- Inflate

- Blob

- Crease

- Smooth

- Flatten

- Fill

- Scrape

- Multiplane Scrape

- Pinch

- Grab

- Elastic Deform

- Snake Hook

- Thumb

- Pose

- Nudge

- Rotate

- Slide Relax

- Cloth

- Simplify

- Mask

- Draw Face Sets

- Mesh Filter

- Transforms

## Tool Setting

- Brushes

- Brush Setting

- Dyntopo

- Remesh

- Symmetry

- Options

## Adaptive Sculpting

- Dynamic Topology
- Multiresolution Modifier

## Editing

- Sculpt
- Mask
- Face Sets

## Hiding & Masking

- Hide
- Mask
