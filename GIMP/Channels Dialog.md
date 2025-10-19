# Channels Dialog

## Overview

- edit, modify and manage your channels
- two usage
  - for color channels
  - for selection masks
- Color channels apply to the image and not to a specific layer
- Channel just a 256 depth grayscale image, in GIMP you can operate channel just like operate a image.

## Managing channels

- Edit Channel Attributes
  - Only available for selection masks.
  - Channel name
  - Overlay Color: the color to show the channel grayscale, just like the QuickMask mode to choose the mask color
  - Opacity: control the overlay color opacity, the more value, the more obvious overlay color display, has no impact on channel strength
- New Channel:
  - Create a new channel, 256 grayscale image
  - This new channel is a channel mask (a selection mask) applied over the image
- Channel to Selection
  - transform the channel to become a selection
  - replace/add/subtract/intersect with current selection

## Selection masks

- Selection Masks are the essential way to select part of image
- Selection Mask are just 256 grayscale images, like red/green/blue/alpha component of images
- When Selection Masks are active, you are operating(painting) the mask channel, not the image
- To operate image, you need to disable the selection mask
- To use selection mask, means to limit the image operation, you need convert the mask to selection. The eye-symbol beside channel item just control the visable of mask image, not the influence of it.
- QuickMask is just a temporary Selection Mask, just like the floating layer to layer, and will be destroyed after being converted to selection
- Toggle QuickMask button create a temporary Selection Mask, which will appear to channel list
- When QuickMask is active, just like Selection Mask, you are operating the temporary channel
- To use QuickMask to limit the image operation, you need to toggle off the QuickMask, which is just to convert the temporary channel to selection(ant line)
- You can use current selection to create either QuickMask(Temporary Selection Mask) or Selection Mask
- SelectionMask can configure the overlay color and it's transparent(for display), QuickMask is the same, the only difference is default overlay color for SelectionMask channel is gray, but red for QuickMask
- Once the channel is initialized, selected (highlighted in blue), visible (eye-icon in the dialog), and displayed as you want (color and opacity attributes), you can start to work with all the paint tools, to paint the mask channel(not the image)
- Use the chain button to active multiple selection mask
- Selection Masks are a graphical way to build selections into a gray level channel where white pixels are selected and black pixels are not selected and gray pixels are partially selected.
- Channels can be used to save and restore your selections.
- By adding many selection masks in your list you can easily compose very complex selections.
- One can say that a selection mask is to a selection as a layer is to an image.
- When QuickMask is active, it is just a normal item in channel list, you can change the overlay tint color and opacity, and hide/show QuickMask with eye-symbol button
- The mask is coded in gray tones, so you must use white or gray to decrease the area limited by the mask and black to increase it. If you paint with some color other than white, grey, or black, the color Value (luminosity) will be used to define a gray (medium, light, or dark). So it's meaningless to use color other than white/grey/black.
- Quick mask's purpose is to paint a selection and its transitions with the paint tools without worrying about managing selection masks(create/edit/delete)
- After the QuickMask Button is pressed, the command generates a temporary 8-bit (0-255) channel, on which the progressive selection work is stored. If a selection is already present the mask is initialized with the content of the selection.
- Any paint tool can be used to create the selection on the QuickMask.
- Only grayscale color for painting selection mask channel
