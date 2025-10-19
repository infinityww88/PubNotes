# Path

## Path properties

- Paths, like layers and channels, are components of an image
  - layers, channels, paths are resource data included into image, even they are not visible
  - they are saved in GIMP' native XCF file, for further work
  - When created, they are stored with image, and can be access in respective dialog(Layer Dialog/Channel Dialog/Path Dialog)
  - When selected from respective dialog, they can be used or edited
- GIMP paths belong Bezier paths
  - defined by anchors and handles
  - anchors are points the path goes through
  - handles define the direction of path when it enters or leaves an anchor point
  - each anchor point has two handles attached to it
- Creation
  - by hand using path tool
  - by transforming a selection into a path
  - by transforming text into a path
- Components
  - a part of a path, anchor points are all connected to each other by path segments
  - the ability to have multiple components in paths allows you to convert them into selections having multiple disconnected parts
  - each component of a path can be either open or closed
    - closed: the last anchor point is connected to the first anchor point
    - if you transform a path into a selection, any open components are automatically converted into closed components by connecting the last anchor point to the first point with a straight line
- Path segments can be either straight or curved

## Path and selection

- transform the selection into a path
  - any information about partially selected areas are lost
- transform paths into selections

## Transforming Paths

- Transform tools can be set to act on layer, selection, or path
- select transform tools, then select which type to transform in the Tool Options dialog(Layer/Selection/Path)
- This gives you a powerful set of methods for altering the shapes of paths without affecting other elements of the image.
- transform-locked
  - Add current element to the set that transform tool will affect. If you transform one element that is transform-locked, all others will be transformed in the same way.
  - lock layer/channel/path

## Stroking a Path

- Paths do not alter the appearance of the image pixel data
- Be stroked, "Edit/Stroke Path" or Paths dialog right-click menu or "Stroke Path" button in Tool Options dialog for path tools
- Stroke Path dialog
  - control the way the stroking is done
  - you can choose from a wide variety of line style
  - or stroke with any of the paint tools, including Clone/Smudge/Eraser, etc
- when choose stroke with paint tools, you can adjust the selected paint tool in Tools dialog by keep the stroke dialog open and select the paint tool in Main toolbox dialog, then stroke the path
- You can further increase the range of stroking effects by stroking a path multiple times, or by using lines or brushes of different width.

## Paths and Text

- transform text item into path
  - Stroking the path
  - text to path, path to selection, filling selection with variety tools, often leads to much higher-quality results than rendering the text as a layer and transforming the pixel data
