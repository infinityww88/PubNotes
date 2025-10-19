# QuickMask

## Overview

- A GIMP selection is actually a full-fledged grayscale channel, covering the image, with pixel values ranging from 0 (unselected) to 255 (fully selected).
- The marching ants are drawn along a contour of half-selected pixels.
- QuickMask showing the full structure of the selection.
- more powerful than selection
- Toggle QuickMask on and off, switches between QuickMask mode, and marching ants mode.
- In QuickMask mode, the selection is shown as a translucent screen overlying the image.
- By default the mask is shown in red, but you can change this if another mask color is more convenient.
- In QuickMask mode, many image manipulations act on the selection channel rather than the image itself, in particular, paint tools.
- Painting with white selects pixels, and painting with black unselects pixels.
- Advanced users of GIMP learn that “painting the selection” is the easiest and most effective way to delicately manipulate the image.
- save a QuickMask selection to a new channel: switch to selection mode instead of QuickMask mode, "Select/Save to Channel"
- In QuickMask mode, Cut and Paste act on the selection rather than the image. You can sometimes make use of this as the most convenient way of transferring a selection from one image to another

## Properties

- Right click QuickMask button
- Normally the QuickMask shows unselected areas “fogged over ” and selected areas “in clear”, but you can reverse this by choosing “Mask Selected Areas” instead of the default “Mask Unselected Areas”.
- Use “Configure Color and Opacity” to open a dialog that allows you to set these to values other than the defaults, which are red at 50% opacity.
