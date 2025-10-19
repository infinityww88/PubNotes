# Devices

物理上，Input Devices 表示挂载到计算机上的设备，player 可以使用它们来控制 app。

逻辑上，Input Devices 是 Controls 的顶层容器。

InputDevice 自身是一个特殊的 InputControl。

使用 InputSystem.devices 查询当前所有出现的 Devices。

## Device descriptions

一个 InputDeviceDescription 描述一个 Device。Input System 主要在 Device discovery 过程中使用它。

当一个新的设备被报告时（被 runtime 或被 player），report 包含一个 Device 描述。基于描述，system 试图发现一个匹配描述的 Device layout。这个过程是基于 Device matchers 的。Device layout 用来确定 Device 有哪些 Controls，解释设备发来的二进制数据，以将其转换为 input。

在 Device 被创建之后，通过 InputDevice.description 属性获得用来创建它的描述。

每个描述有一个标准 fields 的集合：

| Field | Description |
| --- | --- |
| interfaceName | 用在 interface/API 的 Id，使得 Device 可用。绝大多数情况下，它对应 platform 的名字，但是有一些常用的特定设备：HID，RawInput，XInput。这个字段是必须的 |
| deviceClass | Device 的广义分类，例如，Gamepad 或 Keyboard |
| product | Device/driver 自身报告的产品名 |
| manufacturer | Device/driver 自身报告的生厂商 |
| version | Device 驱动或硬件的版本号 |
| serial | Device 的序列号 |
| capabilities | JSON 格式的字符串，描述设备特定的能力 |

### Capabilities

capabilities 字段以 JSON 格式描述设备特征，帮助 Input System 解释来自设备的数据，并将它映射到 Control 表示。不是所有 Device 接口都报告 Device capabilities。

### Matching

InputDeviceMatcher 实例匹配一个 InputDeviceDescription 到一个 registered layout。每个匹配差不多类似于正则表达式一样工作（进行匹配）。这个描述的每个字段可以独立地匹配一个 plain string 或者 正则表达式。匹配不是大小写敏感的。要使一个匹配被应用，它所有的个体 expression 都必须匹配。

要匹配任何 layout，调用 InputSystem.RegisterLayoutMatcher。你还可以在注册一个 layout 时提供它们。

```C#
// Register a new layout and supply a matcher for it.
// MyDevice 是 layout，WithInterface/WithProduct/WithManufacturer 是 matcher
InputSystem.RegisterLayoutMatcher<MyDevice>(
    matches: new InputDeviceMatcher()
        .WithInterface("HID")
        .WithProduct("MyDevice.*")
        .WithManufacturer("MyBrand");

// Register an alternate matcher for an already registered layout.
InputSystem.RegisterLayoutMatcher<MyDevice>(
    new InputDeviceMatcher()
        .WithInterface("HID")
```

如果多个 matchers 匹配同一个 InputDeviceDescription，Input System 选择匹配更多属性的匹配。

### Hijacking the matching process

可以在外部覆盖内部匹配过程，来选择一个不同于系统正常选择的 layout。这也可以快速构建新的 layout。为此，添加一个自定义 handler 到 InputSystem.onFindControlLayoutForDevice 事件。如果你的 handler 返回一个 non-null layout string，然后 Input System 使用这个 layout。

## Device lifecycle

### Device creation

一旦系统为设备选择了一个 layout，它实例化一个 InputDevice 并按照 layout 中的声明在 InputDevice 中添加 InputControls。这个过程是在内部自动发生。

你不能通过 new 手动实例化它们来创建有效的 InputDevices 和 InputControls，必须使用 layouts。

在 Input System 组装完 InputDevice 之后，它在设备的每个 control 以及 device 自身上调用 FinishSetup。使用这个函数完成 Controls 的最终设置。

在一个 InputDevice 完全组装完后，Input System 将它添加到系统中。作为这个过程的一部分，Input System 在 Device 上调用 MakeCurrent，并且在 InputSystem.onDeviceChange 中标记 InputDeviceChange.Added。Input System 还会调用 InputDevice.OnAdded。

一旦被添加，InputDevice.added 标记被设置为 true。

要手动添加设备，你可以调用 InputSystem.AddDevice 方法，例如 InputSystem.AddDevice(layout)

```C#
// Add a gamepad. This bypasses the matching process and creates a device directly
// with the Gamepad layout.
InputSystem.AddDevice<Gamepad>();

// Add a device such that matching process is employed:
InputSystem.AddDevice(new InputDeviceDescription
{
    interfaceName = "XInput",
    product = "Xbox Controller",
});

```

### Device removal

当一个设备断开连接时，它从系统中移除。InputSystem.onDeviceChange 会被调用，并通知 InputDeviceChange.Removed，然后 Devices 从 devices 列表中移除。系统还调用 InputDevice.OnRemoved。

InputDevice.added 被设置为 false。

注意当设备移除后不会销毁。Device Instance 保持有效，你仍然可以在 code 中访问它们。但是尝试从这些 Devices 的 controls 读取 values 将导致异常。

### Device resets

在 player 中，当 window 失去焦点，Devices 将被重置。每个 reset 设置 Device 的状态到它的默认状态。一个例外是 noisy controls，它们保留当前 value，sensor。

Reset 在 Application.focusChanged 中发生。Resets 是可见的，触发 state change monitors 的 state changes，因此还会 cancel 正在进行的 Actions。

当 Application.runInBackground enable， 通过 InputDevice.canRunInBackground 标记为可以在后台运行的 devices 不会重置。这允许诸如 HMDs 和 VR 控制器的 Devices 连续地为 Unity app 提供输入，即使 app 没有焦点。

### Device enabling and disabling

当一个设备被添加时，Input System 向它发送一个 QueryEnabledStateCommand 来发现这个 device 当前是否 enabled。结果反映在 InputDevice.enabled 属性中。

当 disabled 时，不会为这个 Device 处理事件，即使它们被发送了。

一个 Device 可以通过 InputSystem.DisableDevice 和 InputSystem.EnableDevice 关闭和开启。

Sensors 默认处于 disabled state，需要 enable 使它们产生事件。

### Domain reloads

Editor 无论何时 reload 或 recompile scripts，都 reload C# application domain，包括当 Editor 进入 Play mode 时。这需要 Input System 在每次 reload domain 之后重新初始化 Devices。在这个过程中，Input System 试图重新创建 domain reload 之前实例化的 devices。然而，每个 Device 的 state 并不会带过来，这意味着 Devices 在 domain reloads 时重置到它们的默认状态。

注意 layout 注册不会在 domain reloads 之间保持。相反，Input System 依赖于所有的注册作为初始化过程的部分变得可用（例如，通过使用 [InitializeOnLoad] 来运行注册，作为 domain startup 的一部分）。这允许你在 script 中改变 registrations 和 layouts，并且改变在 domain reload 之后立即生效。

## Native Devices

native backend 报告的 Devices 被认为是 native（相对的是从 script code 中创建的 Devices）。要确定这些 Devices，检查 InputDevice.natvie 属性。

Input System remembers native Devices。例如，如果当设备第一次被报告时，如果系统没有匹配的 layout，但是匹配的 layout 稍后被注册，system 使用这个 layout 来重新创建 Device。

### Disconnected Devices

订阅 InputSystem.onDeviceChange 事件并查询 InputDeviceChange.Disconnected 来获知 Input Devices 断开连接。

Input System 在 InputSystem.disconnectedDevices 保持追踪 disconnected Devices。如果这些 Devices 中一个稍后重新连接，Input System 可以检测到这个 Device 之前连接过，并重用它的 InputDevice 实例。这允许 PlayerInputManager 重新将这个 Device 赋予同相同的 user。

## Device IDs

每个创建的 Device 接收一个 唯一 ID。InputDevice.deviceId。所有 ID 只在 Unity session 中有效。

## Device usages

就像任何 InputControl，一个 Device 可以具有关联的 usages。InputDevice.usages，InputSystem.SetDeviceUsage() 来设置它们。Usages 可以是任何意义的任意 strings。一个常见的例子是 XR controllers handedness，“LeftHand” 或 “RightHand” usages。

## Device commands

input events 从 Device 传出数据，commands 则是向 Device 发回数据。Input System 使用它们从 Device 接收特定信息，来触发 Device 上的功能（例如 rumble 效果，隆隆声，点亮灯光）和大量其他需求。

### Sending commands to Devices

发送命令：InputDevice.ExecuteCommand<TCommand>。
监控命令：InputSystem.onDeviceCommand。

Device Command 实现 IInputDeviceCommandInfo 接口，只需要 typeStatic 属性标识 command 的类型。Device 的 native 实现应该会理解如何处理 command。

### Adding custom device Commands

## Device State

就像任何 Control 类型，每个 Device 有一个内存块分配给它，其中存储关联到 Device 所有 Controls 的 state。

### State changes

#### Monitoring state changes

#### Synthesizing state

## Working with Devices

### Monitoring Devices

在设备添加或移除，以及其他设备相关变化时获得通知：InputSystem.onDeviceChagne。InputDeviceChange enum。

```C#
InputSystem.onDeviceChange +=
    (device, change) =>
    {
        switch (change)
        {
            case InputDeviceChange.Added:
                Debug.Log("New device added: " + device);
                break;

            case InputDeviceChange.Removed:
                Debug.Log("Device removed: " + device);
                break;
        }
    };
```

### Adding and Removing Devices

手动添加或移除设备：InputSystem.AddDevice() / InputSystem.RemoveDevice()

这允许你创建自己的设备，可以用于测试目的，或者创建虚拟设备，它们从其他事件中合成 synthesize input。一个例子是，Input System 提供的 on-screen controls。用于 on-screen Controls 的 Input Device 完全从 code 中创建，并且没有 native 表示。

### Creating custom Devices
