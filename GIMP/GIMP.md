# Painting

## Selection

- when operation on image, only want part of it to be affected
- Each image has a selection associated with it, shared by all layer
- Most, not all, GIMP operations act only on the selected portions of the image
- Actually the selection is implemented as channel
  - Channel internal structure: identical to the red, green, blue, and alpha channels of a image, 2d array with element 0~255, which define the degree of influence for the GIMP operation
    - 0: unselected
    - 255: fully selected
    - (0, 255): partially selected, there are many situations where it is desirable to have smooth transitions between selected and unselected regions
    - selection dashed line: contour line, dividing areas more than half selected（>128）from areas that are less than half selected
    - selection dashed line tell only part of the story
    - mask tells the complete detail，QuickMask，selected ares are unaffected，unselected areas are reddened，the more completely selected an area is, the less red it apprears
  - Feathering
    - Feathering is particularly useful when you are cutting and pasting, so that the pasted object blends smoothly and unobtrusively with its surroundings
    - It is possible to feather a selection at any time, even if it was originally created as a sharp selection, Select/Feather menu
    - opposite operation Select/Sharpen
    - feathering works by applying a Gaussian blur to the selection channel, with the specified blurring radius
  - Making a selection partially transparent
    - you can set layer opacity, but you cannot do that directly for a selection
    - For simple selections: use Eraser tool with the desired opacity, erase image selected part with opacity
    - For complex selections: Selection/Floating to create a floating selection, this create a new layer with selection called "Floating Selection", set opacity slider in Layer Dialog to the desired opacity, then anchor the selection, the floating selection disappears from the Layer Dialog and image parted in the selection became partially transparent. floating selection is a temporary layer, can be convert to a new layer, or anchor to orinary layer(merge float layer to orinary layer), no matter which type the layer is, floating or a new layer, image part in selection has be cutted to the new layer, and cutted away from orinary layer
    - floating selection just like cut-and-paste to create new layer, "Float a selection" means the selection part deatched from current layer, and formed a new layer above(floating) it
