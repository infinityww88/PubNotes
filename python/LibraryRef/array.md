# array

数值类型的高效数组

这个模块定义了一个array对象可以紧凑表示基本类型的数组：characters，integers，floating point numbers

类型在object创建时被指定（typed），通过一个单字符的type code

| type code | c type | python type | minimum size in bytes |
| --- | --- | --- | --- |
| 'b' | signed char | int | 1 |
| 'B' | unsigned char | int | 1 |
| 'h' | signed short | int | 2 |
| 'H' | unsigned short | int | 2 |
| 'i' | signed int | int | 2 |
| 'I' | unsigned int | int | 2 |
| 'l' | signed long | int | 4 |
| 'L' | unsigned long | int | 4 |
| 'q' | signed long long | int | 8 |
| 'Q' | unsigned long long | int | 8 |
| 'f' | float | float | 4 |
| 'd' | double | float | 8 |

实际数值的表示被机器架构（严格地说是C实现）决定。实际size可以通过itemsize属性访问

array.array(typecode[, initializer])创建一个array对象。typecode指定数组元素类型，initializer必须是相应类型的list，bytes-like object，或者迭代器。如果给出一个list或者string，initializer被传递给新array的fromlist，frombytes，fromunicode来添加元素到array，否则迭代器被传递给extend方法

array.typecodes：所有可能的type code

array支持常规的sequence操作（indexing，slicing，concatenation，multiplication）。当使用slice赋值时，被赋值的value必须是一个具有相同type code的array object，否则抛出TypeError。Array objects还实现来buffer接口，可以用在任何需要bytes-like objects的地方

- array.typecode
- array.itemsize
- array.append(x)
- array.buffer_info()：返回(address, length) tuple，给出buffer的内存地址和item数量。buffer的大小可以通过length * itemsize得到
- array.byteswap()：bytes swap array中所有的items。只支持1，2，4，8 bytes大小的item，否则抛出RuntimeError。用于转换字节序
- array.count(x)：返回数组中x出现的次数
- array.extend(iterable)
- array.frombytes(s)：将bytes中的items追加到array
- array.fromfile(f, n)：从file object f中读取n个item（机器格式）并追加到array之后。如果可用item不足n个，抛出EOFError指示文件结束
- array.fromlist(list)
- array.fromunicode(s)：将给定的unicode string追加到array之后。array必须是一个u数组，否则抛出ValueError。使用array.frombytes(unicodestr.encode(enc))将unicodestr追加到其他类型的array之后
- array.index(x)
- array.insert(i, x)
- array.pop(\[i])
- array.remove(x)
- array.reverse()
- array.tobytes()
- array.tofile(f)：将所有item以机器格式写入file object f
- array.tolist()
- array.tounicode()：只用于short array
