Unity UI **Input Module**（输入模块）是Unity UGUI事件系统的核心组件之一，负责将硬件输入（如鼠标、键盘、触摸等）转换为UI交互事件（如点击、拖拽等）。以下是其核心要点：

---

### **1. 核心功能**
- **输入映射**：将物理设备输入（如鼠标点击、触摸滑动）转换为UI事件（如`IPointerClickHandler`接口事件）。
- **事件分发**：通过射线检测（`Graphic Raycaster`）确定当前交互的UI元素，并触发对应事件。
- **多设备支持**：不同模块适配不同设备（如`StandaloneInputModule`处理键鼠，`TouchInputModule`处理触摸）。

---

### **2. 主要模块类型**
- **`StandaloneInputModule`**  
  - 用于PC端，处理鼠标和键盘输入。  
  - 支持配置轴（如水平/垂直移动）和按钮（如提交/取消键）。

- **`TouchInputModule`**  
  - 专为移动设备设计，处理多点触控（已弃用，现由`StandaloneInputModule`统一处理）。

---

### **3. 工作原理**
1. **输入监听**：在每帧`Update`中检测设备输入状态。  
2. **射线检测**：通过`RaycastAll`确定交互的UI目标（如按钮、滑动条）。  
3. **事件触发**：调用对应接口（如`OnPointerClick`）执行逻辑。

---

### **4. 关键属性与方法**
- **属性**  
  - `forceModuleActive`：强制激活模块（即使无输入设备）。  
  - `inputActionsPerSecond`：控制输入事件处理频率。

- **方法**  
  - `Process()`：核心处理函数，将输入转换为事件。

---

### **5. 实际应用示例**
```csharp
// 点击事件示例
public class ClickHandler : MonoBehaviour, IPointerClickHandler {
    public void OnPointerClick(PointerEventData eventData) {
        Debug.Log("UI被点击！");
    }
}
```
需配合`EventSystem`和`StandaloneInputModule`组件使用。

---

### **6. 性能优化建议**
- **减少射线检测对象**：通过`Layer`或`Canvas`层级过滤无关UI元素。  
- **合并输入模块**：避免同时激活多个模块（如键鼠和触摸）。

---

通过合理配置Input Module，可实现跨平台的高效UI交互。