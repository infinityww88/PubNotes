# Layer mask

- A transparency mask can be added to each layer, it's called Layer mask
- A layer mask has the same size and same number of pixels as the layer to which it is attached
- The mask is a set of pixels in gray-tone on a value scale from 0 to 255. The pixels with a value 0 are black and give a full transparency to the coupled pixel in the layer. The pixels with a value 255 are white and give a full opacity to the coupled pixel in the layer.
- initialize the content of the mask
  - White (full opacity, 255): the mask is white, all pixels of the layer are visible, paint with black to make layer pixels transparent.
  - Black (full transparency): the mask is black, the layer is fully transparent, Painting with white will remove the mask and make layer pixels visible.
  - Layer's alpha channel: the mask is initialized according to the content of layer Alpha channel. If the layer still contains transparency it's copied in the mask.
  - Transfer layer's alpha channel: same as "Layer's alpha channel", except it also reset layer's alpha channel to full opacity
  - Selection: the mask is initialized according to pixel values found in the selection, new mask fills selected area with white, and unselected area with black, be careful, the selection is still active for now, if you want to paint, you can only affect the selected area, you need cancel the selection to paint the whole mask
  - Grayscale copy of layer: the mask is initialized according to pixel values of the layer, internally convert the image to grayscale image, then use this grayscale image to initialize the mask
  - Channel: just like "Selection", he layer mask is initialized with a selection, but the selection comes from selection mask you have created before, stored in the Channel dialog.
  - Invert mask: This checkbox allows you to invert : black turns to white and white turns to black.
- When the mask is created it appears as a thumbnail right to the layer thumbnail. Both layer and layer mask can be edit, be careful which one is active at the moment. By clicking alternatively on the layer and mask thumbnail you can enable one or other.
- Click layer mask thumbnail, make layer mask editable. Click layer thumbnail make layer editable. This is equal to toggle "Layer/Mask/Edit layer mask" menu
- be default the image window display the masked layer. Enable "Layer/Mask/Show layer mask" menu to just display layer mask, disable to display the masked layer.
- "Layer/Mask" menu has items that convert mask to selection
- "Layer/Mask/Apply layer mask" apply the layer mask to layer, and disappear.
