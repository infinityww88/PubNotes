# Custom Comparers

Fishnet 为 prediction data 生成 comparers 来执行内部优化，但是特定情形下，无法自动生成 comparers。

你可能在 console 中看到 custom comparer 类型缺失的错误。例如，尤其是泛型和数组，必须提供一个 custom comparer。

```C#
/* For example, this will create an error stating
 * byte[] needs a custom comparer.
 */
public struct MoveData : IReplicateData
{
    public Vector2 MoveDirection;
    public byte[] CustomData;
    //rest omitted..
}
```

尽管对于 byte[] 类型可以自动生成 comparer，我们仍然需要你创建自己的，因为我们不能准确知道你想要如何比较这些 types。下面的 code 通过比较每个 byte 检测 mismatches，来比较 byte arrays。基于 prediction data 发送的频率，这可能潜在加重 processor 的负担。

```C#
[CustomComparer]
public static bool CompareByteArray(byte[] a, byte[] b)
{
    bool aNull = (a is null);
    bool bNull = (b is null);
    //Both are null.
    if (aNull && bNull)
        return true;
    //One is null, other is not.
    if (aNull != bNull)
        return false;
    //Not same lengths, cannot match.
    if (a.Length != b.Length)
        return false;
​
    //Both not null and same length, compare bytes.
    int length = a.Length;
    for (int i = 0; i < length; i++)
    {
        //Differs.
        if (a[i] != b[i])
            return false;
    }
​
    //Fall through, if here everything matches.
    return true;
}
```

上述代码是创建自定义比较器的示例，但可能并非最适合你需求的比较器，因此需要你根据具体类型自行实现比较器。

创建自定义比较器很简单：定义一个带任意名称的静态方法，返回值为布尔类型，用 \[CustomComparer\] 特性标记该方法，并包含两个参数（需比较的类型）。方法逻辑可按需编写。
