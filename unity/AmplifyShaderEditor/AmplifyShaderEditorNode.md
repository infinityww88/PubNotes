# ASE Node

## Note

- Model is composed of triangles, triangle risrasterized as fragments, fragment is interpolated from vertex of triangle, so everything do with vertex will be interpolated to fragments, everything do with fragment means to do with triangle, and then means to do with the whole model
- To make a transparent shader, In the left shader setting panel, set Blend Mode to Transparent/Custom, RenderType to Transparent, RenderQueue to Transparent
  - default Transparent Blend Mode has the common transparent effect
  - custom Blend Mode let you set the various blend factors
- In Surface Shader Output node, Albedo Input Port only contains RGB channels, A channel needs to connect the Opacity Input Port

## Camera And Screen

### Camera Depth Fade

- Output difference between mesh surface depth and the cameras near plane
- Value is set on a linear [0,1] range
- Parameter
  - Vertex Position(Float4)
    - custom vertex position
    - use current vertex position if left unconnected
    - Don't use this internal data as it's ignored internally
  - Length(Float)
    - Define the distance in viewport coordinates(nearplane) over which the fade between 0 and 1 values should occur
  - Offset(Float)
    - Define an offset in viewport coordinates to the cameras near plane on which the fade from 0 to 1 should start
- Start from nearplane, distance between mesh surface and nearplance:
  - [0, offset] -> 0
  - [offset, offset + length] -> [0, 1]
  - [offset + length, infinity] -> 1

### Clip Plane

- Output the camera frustum plane world space equations selected by its Plane option
- Select a frustum plane, output the plane equations factor ABCD
- Parameter
  - Plane: Left/Right/Bottom/Top/Near/Far

### Compute Grab Screen Pos

- Converts a position in clip space into normalized screen space texture coordinates taking also vertical orientation API differences(Y axis:top-to-down or down-to-top)into account
- The outputted result can then be directly used into a **Grab Scren Color** node as its UV coordinates
- ASE clip space == NDC
- Parameter
  - Input(Float4)
    - Position in clip space to be converted to normalized and currectly oriented screen position

### Compute Screen Pos Node

- Converts a position in clip space into screen space texture coordinates
- These coordinates can then be used directly on a **Texture Sample** as its UV coordinates for doing a screen space-mapped texture sample
- Parameter
  - Input(Float4)
    - Position in clip space to be converted to screen position
  - Normalize(Bool/False)
    - Automatically performs the perspective division(divide by W on the same above) over the result(NDC)
  - *Compute Grab Screen Pos Node* is *Compute Screen Pos Node* with Normalize == false
  - *Compute Grab Screen Pos Node* is just ComputeScreenPos() in UnityCG.cginc
  - *Compute Screen Pos Node* is also just ComputeScreenPos(), but when Normalize == ture, it will do H-Divide(Homogeneous-Divide) to the result
  - No matter which way to use, the final result is just vertex's screen space normalized coordinates, called *screen space uv coordinates*.

### Grab Screen Color

- Allows a Grab Pass to be used
- The special pass grabs(capture) the contents of the screen when the object is about to be drawn into a texture which can then be fetched using screen space uv coordinates
- This node can either generate its internal UV coordinates or use custom ones if specified on the UV input port.
  - if UV input port left unconnected, it use internal UV coordinates
    - automatically compute vertex screen space UV coordinates
    - it equals connected GrabScreenPosition Node, GrabScreenPositionNode do the same thing
    - it also can be done manually
      - Creating a Vertex Position Node
      - Connect to a series nodes to compute vertex screen space UV coordinates
        - Connect to a ComputeGrabScreenPos, then a BreakToComponents node, then tow Divide node to divide x/y component with w component, then a Append node to gether x/y component as a vector
        - Connect to a ComputeScreenPos node with Normalized = false, then do same as above
        - Connect to a ComputeScreenPos with Normalized = true
      - At last connect to the GrabScreenColor node
- By using the Grab Screen Position node along side with this node, it becomes very easy and intuitive to achieve effects like refraction(折射).
- For custom grab texture
  - activating Custom Grab Pass toggle and specifying a new name into Name field
- Grab passes only works in Forward rendering path, not deferred rendering path
- For this node to correctly work on ScripableRenderingPipelines(both Lightweight and HD), you must go to their pipeline asset's inspector and activate the Opaque Texture toggle
- Pamameter
  - Auto-Register(False)
    - Creates Grab Pass even if not connected to an output node
  - Mode: if this node is to register a new Grab Pass or use one already created from another Grab Screen Color as reference
    - Object: Register a new Grab Pass
    - Reference: referenced another Grab Screen Color node in the same shader graph
    - A complicate shader graph may need use Grab texture multiple time with different input, but a single GrabScreenColor only accept one input, so you need add multiple GrabScreenColor to accept different input
    - non-custom grab pass execute once for each object that uses it
    - custom grab pass execute once per frame for the first object that used the given texture name, and reused by other objects that do the same, mean grab pass may execute multiple time for each texture name
    - whether a grab pass execute is determined by texture name, not objects or passes
    - so you can define multiple Grab pass with different texture name in the same shader
    - In ASE, you can add multiple Grab Pass node
      - it can be a new Grab Pass
      - or it's just a reference for a already exists Grab texture, but use it multiple time with different input
    - Reference mode is just a way to use a single grab texture multiple time in ASE, because a node can only accept one input each time
    - Node reference is the grab texture name
  - Normalize: Automatically performs the perspective division over the input UVs
    - So you don't need manually do it on ComputeGrabScreenPos node
    - perspective divide all components(x/y/z/w) by w, so the output will be (x/w, y/w, z/w, 1), so there is no harm to do perspective division on the vector that already did, because the w components has became to 1
  - Custom Grab Pass
    - when turned on, a custom texture name can be used on the grab register
    - when turned off, the default _GrabTexture sampler will be used
    - when turned on and no name is specified, or turned off, a screen grab(_GrabTexture) is done for each object that uses it, as opposed to when a name is specified the screen grab is only done once per frame for the first object that used the give texture name
  - Name: Specify a custom texture name which will have the current screen contents
  - Property Name
    - texture name used in shader
    - automatically generated using the Name parameter
    - greyed out and not editable
  - Reference: Property Name from other grab screen color node (in the same shader) to be used as reference
  - UV: vertex screen space UV coordinate
- Output
  - RGBA
  
## Constants And Properties

### Color

- Color Node generates a float4 value containing four float components
  - define a Constant value directly used in shader calculations
  - define an exposed Property value that can be modified by material inspector that uses it
- This node is very simiplar to the Vector4 Node, the difference is the convenience of representing and changing the values with color picker
- Parameter
  - Type
    - Constant: the valus is assigned directly in shader code and can't be dynamically changed
    - Property: the value becomes available in the properties of the material that uses the shader and can be changed in the material inspector or by script
    - Instanced Property: the value can only be set by script and this defines the shader as an instanced shader(GPU Instaning)
    - Glboal: the value can only be set by script and this defines a static variable that is shared between all shaders that use it. It's useful to change a value globally
  - Name: Name of the property holding the value.
    - if type is set to Property, this is the name that will be shown in material properties label
    - if type is not Property, the name is ignored but still useful for organization purposes or generate a Property Name
  - Variable Mode: define if the current property/global variable is to be created on the current shader
    - Create(default): Property and/or global variable is created in the shader
    - Fetch: No variable nor property is registered on shader
      - useful when there's need to using global variables declared over a included cginc
  - Auto-Register: create the property and/or global variable even if not connected to an Output node
  - Precision
  - Default Value: This is the value the shader currently holds. It's also the default value that is used when a new material is created with this shader
  - Material Value: This is the value the material currently when ASE in material mode, only in Property and Instanced Property type, which let you chagne the value per material
  - Property Name: This is the variable name that contains the value
    - automatically generated using the Name parameter
    - greyed out and not editable
    - This parameter is only visible in Property, Instanced Property and Global types to indicate **what's the variable name to use when editing this value by script**
  - Hide in Inspector(Off)
  - HDR(?): Indicates that a property expects a high-dynamic range value
  - Gamma: color space
  - Per Renderer Data(?)
  - Custom Attribute(?)
- Output
  - RGBA

## Functions

## Image Effects

## Light

### Fog And Ambient Color

- outputs specific data(Color) regarding both fog and ambient light
- The required data is selected via the Color parameter
- Ambient Light(Legacy) output a single color and not the current configured skybox
- Parameter
  - Ambient Light(Legacy): Ambient lighting color(sky color in gradient ambient case)

## Logical Operators

## Math Operators

## Matrix Operators

## Matrix Transform

## Miscellaneous

## Object Transform

### Object Space View Dir

- Just a node represention of a UnityCG.cginc function
- Calculate a non-normalized direction in object/local space from a position also in object/local space given by its **Input** towards the camera
- Return the direction from the current game object to camera if Input is left unconnected and its default internal value of (0,0,0,1) is used
- Parameter
  - Input: when input is left unconnected, use this value as position that node transforms
- Input Port
  - Input: Position in object/local space
- Output Port
  - XYZ(float3)

### Object To Clip Pos Node

- Transform a position in object/local space to the camera's clip space in homogeneous coordinates
- Clip space coordinates differ between Direct3D-like and OpenGL-like platforms
  - Direct3D-like: Clip space depth ranges from 0.0 at the near plane to +1.0 at the far plne
  - OpenGL-like: Clip space depth ranges from -1.0 at the near plane to +1.0 at the far plane
- Parameter
  - Input(float3)
- Input Port
  - Input(float3)
- Output Port
  - XYZW(float4)

### Object To View Pos Node

- Transform an Input Position in object/local space into camera's view space
- Coordinates in view space are called eye coordinates and will represent the Input local position as its relative position according to where the camera is
- Parameter
  - Input(float3)
- Input Port
  - Input(float3)
- Output Port
  - XYZ(float3)

## Surface Data

- Fragment shader functions, deal with every fragment, which means to deal with the surface

### Depth Fade Node

- Output a linear gradient representing the distance between the surface of an object/geometry behind it
- The gradient range or fading distance can be set by adjusting the Distance parameter
- More specifically that this parameter does is to create a value in a [0, 1] range when the distance between the surface of an object/geometry behind it is within the value specified
- The shader must have its RenderQueue value set to Transparent of higher, so the object is not writen on Depth buffer. This is an essential configuration since the node is internally calculating the distance value by subtracting the Surface Depth by the value fetched on the Depth buffer. If the object is being written on the depth buffer, then this operation will give unintended results
- Unlit objects are not written on the Depth buffer, so this node cannot get depth info from Depth buffer for Unlit objects
- Parameter
  - Vertex Position: Don't use this internal data as it's ignored internally. Only visible if the respective input port is not connected.
  - Distance: Distance in world space coordinates to which the fade should take place. Only visible if the Dist input port is not connected
  - Convert to Linear(True): Convert depth values read from depth buffer from a logarithmic to a linear scale(perspective division convert z axis from linear to logarithmic)
  - Mirror(True): Applies an Abs over the final value, guaranteeing the final value is always positive.
  - Saturate(饱和): Applies a Saturate over the final value, guaranteeing that the final value is on a 0 to 1 range
- Input Port
  - Dist: Distance in world space coordinates to which the fade should take place
  - Vertex Position: Allow the specification of a custom vertex position. Use current vertex position if left unconnected
- Output Port
  - normalized distance(float)

### World Position

- Per pixel calculation of the surface position in world space
- Retrieve the true world position of each point in the surface
- The position values take into account the game object transform so they change accordingly to the game object position, rotation and size
- Usually useful for global effects like mapping the world position to the surface UV coordinates
- Do not confuse with Vertex Position, Vertex Position is used to fetch vertex position in local space from model, this node is used to calculated fragment position in world space
- Output Port
  - XYZ: return the surface position in world space

### Surface Depth

- Output the distance between the object surface(each fragment) and the camera
- Can be set in a [0, 1] range or use its real value directly in View Space by changing the View Space parameter
- The distance value is obtained by transforming each vertex position into view space and returning its Z value thus it's not dependent on the Depth buffer
- Parameter
  - View Space: Define how the distance value between camera and surface is to be presented
    - Eye Space: Real distance value between camera and surface
    - 0-1 Space: Distance value in a linear [0, 1] range, corresponding [near-plane, far-plane]

## Textures

### Texture Object

- Reference to a texture that can be sampled by several **TextureSample** nodes
- Reference all types of texture, diffuse texture, normal map, cube texture...
- Texture Sample Node can directly reference a texture, but instead needlessly duplicating reference a single textures in multiple Sample node, you can use Texture Object Node to reference the texture, and connect it to every Sample node that use the texture, so you can change the texture for all these Sample nodes once
- 与其他属性类型不同，每个纹理属性还需要声明一个float4类型的变量_TextureName_ST，ST表示ScaleTranslation，可以通过ST来控制纹理的缩放和平移。ST.xy存放的是缩放，ST.zw存放的是偏移。每个纹理在材质的inspector上都会出现相应的ST属性，S是Tiling，T是Offset
- Another use for it would be pass the reference of a texture inside a shader function
- Parameter
  - Type
    - Property: the value becomes available in the properties of the material that uses the shader and can be chagned in the material inspector or by script
    - Global: the value can only be set by script and this defines a static variable that is shared between all shaders that use it. It's useful to change a value golbally
      - CG program is just like normal program, the main difference is it is executed in GPU instead of CPU
      - Just like CPU program can have global variable, means it stays in global data memory, instead of stack, can always be accessed. GPU program also have global variable, that resident in GPU memory constantly, don't need load from CPU every time. When script set the global variable, the data goes to GPU global data memory from CPU, then stay there, every shader executed by GPU that reference the global variable can use it directly, and do not transfer data from CPU to GPU
    - Name: Name of the property holding the value. This is the name that will be shown in the material properties label, useful for organization purposes or to **generate a Property Name**
    - Property Name
      - This is the variable name that used in script
      - it is automatically generated using the Name parameter
      - it's greyed out and not editable
    - Default Texture: a fallback texture value that will be used if the default value is not set
      - White
      - Black
      - Gray
      - Bump
    - Auto-Cast Mode: This option makes the node either adjust automatically from the input texture provided(texture import type) or lock it to a specific type
      - Auto: Detects and uses any type of texture changing input ports accordinly
      - Locked To Texture 1D: Locks to only accept 1D textures(in unity these are actually normal 2D textures, but just use the first row pixels)
      - Locked To Texture 2D: Locks to only accept regular 2D textures
      - Locked To Texture 3D: Locks to only accept 3D textures
      - Locked To Cube: Locks to only accept Cube map textures
      - Locked To Texture 2D Array: Locks to only accept Texture2DArray asset files
    - Default Value: This is the value the shader currently holds. It's also the default value that is used when a new material is created with this shader
    - Material Value: current material holds value. Only in material mode
  - Attribute
    - No Scale Offset: Hides the scale(Tiling) and offset value properteis besides a texture property and if ASE custom material inspector is being used it will also turn it into a mini thumbnail texture property
    - Normal: Tells the inspector to expect the texture property to be a normal map which warns the user when that's not the case

## Time

## Trigonometry Operators

## UV Coordinates

### Texture Coordinates

- Texture Coordinate node uses the mesh UVs and manipulates it according to the texture tiling and offset parameter to define how a texture is mapped onto a 3d asset
- Use mesh UVs data internally, use Input Port parameter to modify the UVs value
  - if Tex Port is connected to a Texture Object or one Texture Object is referenced in the node property panel, the UVs is tranformed by that texture object's Tiling/Offset parameter, and Tiling/Offset port is disabled.
  - Otherwise the UV coordinates are transformed with Tiling/Offset port input or node's parameters in node prameter panel
- Node Parameter
  - Reference: Points to an existing TextureObject or TextureSample node
    - None: turn off referencing altogether
    - Option: Point to any available texture node in the graph
  - Coord Size: The size of the main output port which allows you to read more packed data from vertex coordinates. Dynamically changes output ports accordingly
    - Float2: uv
    - Float4: uvwt
  - UV Set: The UV channel used, also knows as UV Index in some application. Set1 is texture UV coordinates, Set2 is usually used for lightmap UV coordinates
    - [1, 4]: UV channel1 to channel4
  - Tilling: Serves as a constant multiplier of UVs that make them change in size, effectively creating a tilling pattern. Only available if Reference is set to None or if the equivalent input port is not connected, means there is no available ST info to used
  - Offset: Adds a constant value to UVs that makes them move in a desired direction, effectively offseting it from the original position. Only available if Reference is set to None or if the equivalent input port is not connected
- Input Port
  - Tex: This port accepts a Texture Object which allows the use of it's texture UV parameters(ST). Overriding the node tilling and offset and using the material inspector instead
  - Tilling/Offset: Dynamic version of the parameter Tilling/Offset. Only available if Reference is set to None, otherwise get locked to indicate that uses the tilling/offset of the texture property in the material inspector
- Output Port
  - UV/UVW/UVWT

### Rotator

- Rotates a UV or other Vector2 position(UV is just a Vector2) by an angular value of Time from an Anchor Point
- If Time input port is unconnected, Unity timer is used to continuously increment an internal angular value and provide a rotation animation
  - In this case, parameter panel will appear a Time parameter, which acts as a multiplier over the Unity timer value
- If Time input port is connected, then it will assume that the value as the final one and do not use any kind of timer internally
- Parameter: Parameter appear on node parameter panel, some of parameters are node configuration, some of them are substitute to the Input Port when port is unconnected, so they act as default values
  - UV: Point to be rotated
  - Anchor: Anchor Point to be used on rotation
  - Time: Time multiplier, allows to scale Unity internal timer
- Input Port
  - UV: should be connected with a texture coordinates to get mesh uv, otherwise the input uv is constant vector2, make all the fragments the same color(the sample of the constant UV)
  - Anchor
  - Time: Angle of rotation in radians to be applied to the specified point

## Vector Operators

## Vertex Data
