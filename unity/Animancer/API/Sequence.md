一个可变 size 的 AnimancerEvents，根据它们的 AnimancerEvent.normalizedTime 排序。

## 属性

- Count

- IsEmpty

- Names：事件的名字，不包括 AnimancerEvent.Sequence.endEvent

- NormalizedEndTime：endEvent.normailedTime 的 shorthand

- Action OnEnd：endEvent.callback 的 shorthand

## 方法

所有添加方法根据 AnimancerEvent.normalizedTime 将 Event 添加到 Sequence 中的合适位置使它保持递增有序，并返回添加后所在的索引。

- Add(AnimancerEvent)

- Add(int indexHint, AnimancerEvent animancerEvent)

- Add(float, Action)

- AddCallback(int index, Action callback)

  将 callback 指定给 index 位置的 event 的 callback

- AddCallback(string name, Action callback)

  将 callback 指定给名为 name 的 event 的 callback

- AddRange(IEnumerable<AnimancerEvent>)

  添加 enumerable 中的每个 event 到 sequence 中。

- CopyFrom(Sequence)

- CopyTo(AnimancerEvent[], int)

- GetEnumerator()

- GetName(int)

- IndexOf(string, int)

- Remove(AnimancerEvent)

- Remove(int)

- Remove(string)

- RemoveAll()

- RemoveCallback(int, Action)

- SetCallback(int, Action)

  替换指定 index Event 的 action

- SetCallback(string, Action)

  替换指定 name Event 的 Action

- SetName(int, string)

  设置指定 index Event 的名字