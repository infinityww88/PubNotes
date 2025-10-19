# memoryview

memoryview objects允许Python代码访问一个支持buffer protocol的object的内部数据而不需要copy

memoryview通过一个支持buffer protocol的object创建

memoryview有一个element的概念，它是被object处理的原子单位。对于bytes，bytearray来说，element就是byte。但是array.array可以支持更大的element

len(view)返回tolist()的长度

itemsize给出一个element的byte数量

memoryview支持slicing和indexing来暴露数据

如果format属性是struct module指定的native format specifiers，还支持使用一个整数或者整数tuple索引并返回一个正确类型的element（specifiers指定的类型）。一维memoryview可以使用一个整数或一个整数的tuple索引。多维memoryview可以使用ndim个整数的tuple索引，ndim是memoryview的维度

如果底层object是可写的，memoryview支持一维slice赋值，但不允许resize

可哈希类型（format=B，b，c等）的一维memoryview仍然是可哈希的，hash(mv) == hash(mv.tobytes())

- \__eq__: 如果两个操作数的format使用struct语法表示，shapes相同，对应的值也相同，则为true
- tobytes(order=None): 将buffer中的data返回为bytestring，m.tobytes() == bytes(m)。对不连续数组（多维数组？）等价于所有元素的flattened list表示转换为bytes
- hex(\[sep\[, bytes_per_sep]]): 返回buffer中每个byte两个hex数值的字符串表示
- tolist()
- toreadonly(): 返回只读memoryview object版本，原始memoryview object不变，仍然共享buffer，只是新object不可写
- release(): 释放底层buffer。很多object在view引用buffer时会施加特殊动作（例如bytearray临时禁止resizing）。因此release释放buffer可以尽快移除这些限制。之后在mv上的任何操作都会触发ValueError，即release之后就不再可用了。mv在context management protocol中具有相同效果，推出block时，release
- cast(format[, shape]): 将memoryview转换成一个新format或shape。shape默认参数为\[byte_length//new_itemsize]，意味着默认返回一个一维mv。返回一个新mv，但是buffer是共享的。目标format限制为一个native format是struct语法的元素（B，b，c）。返回结果的byte长度必须和原始mv具有相同的长度，例如一个13个byte的bytes不能转换为6个short的shorts

只读属性

- obj
- nbytes：nbytes == product(shape) * itemsize == len(m.tobytes())
- readonly
- format：view中每个element的format（struct）
- itemsize：每个element的bytes数
- ndim：mv多维数组的维度，ndim=len(shape)
- shape：一个length=ndim的整数tuple，给定多维数组每个维度的大小
- strides：跨幅，一个length=ndim的整数tuple。mv表达的数组相对于底层buffer可以是不连续的。那么每个维度前一个item与后一个item之间就有一定的间隔。strides指定每个维度item之间的跨幅。
- suboffsts：被PIL-style arrays内部使用
- c_contiguous：指示memory是否是c-contiguous
- contiguous：指示memory是否是contiguous
