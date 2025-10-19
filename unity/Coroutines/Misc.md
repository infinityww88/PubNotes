# Misc

yield return null vs yield return new WaitForEndOfFrame()

二者非常类似，但是在一个 frame 的不同点返回。

Unity 在一个 frame 中执行非常多的操作，包括：

- Input processing
- Main update（包括 Update()）
- Main coroutine updates（包括 yield return null）
- Late update（包括 LateUpdate()）
- Scene rendering
- Gizmo/UI rendering
- End of frame（包括 WaitForEndOfFrame）

One returns just before rendering, the other returns just after (but just before the frame is displayed). When the difference isn't important, I usually use and recommend yield return null, as it's closer to the way other Update and coroutine functions work.

![UnityLoop](../Image/UnityLoop.jpeg)

当在 Start 开始一个 Coroutine 时，StartCoroutine(MyCoroutine())，MyCoroutine 函数调用生成一个 Coroutine。这个函数会立即执行第一个 yield 之前的逻辑，在任何 Update 之前，然后停在 yield 之前。第一个 Update 执行之后，开始调度这个 Coroutine，但是因此现在这个 Coroutine 停在 yiled 语句，因此执行这个 yield 语句，这个语句导致 Coroutine 被立刻挂起，因此第一次执行 Coroutine 时什么都没有做，只是将它挂起。第二次 Update 执行后，这个 Coroutine 恢复执行，从 yiled 之后开始，知道运行到下一次 yield 语句，然后被再次挂起，以此类推。
