# Layers

## Introduction

- think of layers as stack of slides
- construct an image of serveral conceptual parts, each of which can be manipulated without affecting any other part of the image.
- Layers dialog: second most important type of dialog window in GIMP after Main Toolbox
- Each open image has a single **active drawable** at any time
  - drawable is a GIMP concept: layers, channels, layer masks, selection mask
  - basicall a drawable is anything that can be drawn on with painting tools
  - only one drawable can be active at any time

## Layer Properties

- name
- alpha channel
  - for background layer(bottom layer)
    - create alpha channel at creation
    - add alpha channel
  - each layer other than bottom layer has alpha channel automatically
- layer type: determined by image type
  - RGB
  - RGBA
  - Gray
  - GrayA
  - Indexed
  - IndexedA
- Visibility
  - remove a layer from image
  - Most operations on an image treat toggled-off layers as if they did not exist
  - only work on specific layer, hide other layers
- Active layer
- Linkage to other layers: group layers for operations on multiply layers
- Size and boundaries
  - boundaries of layers do not necessarily match the boundaries of the image
  - each text item goes into its own separate layer, which precisely sized to contain the text
  - new layer created by cut-and-paste is sized just large enough to contain the pasted item
  - you cannot do anything to a layer outside of its boundaries
- Opacity
  - determines the extent to which it lets colors from layers beneath it in the stack show through
- Mode
  - determines how colors from the layer are combined with colors from the underlying layers to produce a visible result
  - sufficiently complex, sufficiently important
- Layer mask
  - in addition to alpha channel
  - extra grayscale drawable associated with layer
  - a layer does not have a layer mask by default, must be added specifically

## Layer modes

- blening modes
- determines how current layer pixel color and color from beneath layers blend together as a final color, which goes to up layer
- Painting tools also has similar way to layer modes, to blend painting color and drawable color
- Layer modes permit complex color changes in the image. They are offten used with a new layer which acts as a kind of mask

## Creating New Layers

- Layer/New Layer
- Layer/Duplicate Layer
- cut or copy something, and paste, the result is a floating selection
- a floating selection is a temporary layer, before you can do anything else
  - anchor the floating selection to a existing layer(merge to current active layer)
  - convert it into a normal layer(new layer will be sized just large enough to contain the pasted material)

## Layer Groups

- group layers that have similarities in a tree-like way
- Create a layer group
  - You can create layer groups and embbed them
- Adding layers to layer group
  - add existing layers to a layer group by click-and-dragging
  - create new layer to the current layer group
- Visibility
- Layer Mode and Groups
  - layer mode applied to a layer group acts on layers that are in this group only
- Pass Through Mode
  - While with Normal mode, layers within a group are treated as if they were a single layer, which is then blended with other layers below in the stack; a modifier on a layer inside the group blends layers below in the group only.
  - While pass through, Layers inside the layer group will behave as if they were a part of the layer stack, not belonging to the group. Layers within the group blend with layers below, inside and outside the group.
- Opacity
  - opacity changes are applied to all the layers of the group.
- Layer Mask
  - similarly to ordinary-layer masks, extra alpha adjustment
  - group mask size is the same as group size (bounding box of its children) at all times. When the group size changes, the mask is croped to the new size. areas of the mask that fall outside of the new bounds are discarded, and newly added areas are filled with black (and hence are transparent by default).