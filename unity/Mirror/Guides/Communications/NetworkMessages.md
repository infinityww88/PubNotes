# Network Messages

对于绝大部分内容，建议使用 high level Commands 和 RPC 调用 和 SyncVar，但你还可以发送 low level network message。

如果你想 clients 来发送不绑定在 gameobjects 的消息，例如 logging，analytics，或者 profiling information，这非常有用。尽管也可以使用 tcp/http 发送，但是 Mirror 提供了更高级的 API，更加简单易用。

你可以扩展 MessageBase 来生成可序列化 network message 类。这个类具有 Serialize 和 Deserialize 函数，使用 objects 的 writer 和 reader。

你可以自己实现这些函数，但是建议让 Mirror 为你生成它们。

```C#
public abstract class MessageBase
{
    // Deserialize the contents of the reader into this message
    public virtual void Deserialize(NetworkReader reader) {}

    // Serialize the contents of this message into the writer
    public virtual void Serialize(NetworkWriter writer) {}
}
```

自动生成的 Serialize/Deserialize 可以有效地处理任何 Mirror 支持的类型。使你的 members 为 public 的。如果你需要类成员或者复杂容器，例如 List 或 Dictionary，则你必须自己实现 Serialize 和 Deserialize。

要发送消息，使用 NetworkClient，NetworkServer，以及 NetworkConnection 的 Send() 方法，它们使用方法都相同。它使用一个 MessageBase 的派生类 message object 作为参数。

```C#
using UnityEngine;
using Mirror;

public class Scores : MonoBehaviour
{
    public class ScoreMessage : MessageBase
    {
        public int score;
        public Vector3 scorePos;
        public int lives;
    }

    public void SendScore(int score, Vector3 scorePos, int lives)
    {
        ScoreMessage msg = new ScoreMessage()
        {
            score = score,
            scorePos = scorePos,
            lives = lives
        };

        NetworkServer.SendToAll(msg);
    }

    public void SetupClient()
    {
        NetworkClient.RegisterHandler<ScoreMessage>(OnScore);
        NetworkClient.Connect("localhost");
    }

    public void OnScore(NetworkConnection conn, ScoreMessage msg)
    {
        Debug.Log("OnScoreMessage " + msg.score);
    }
}
```

注意源代码中没有 ScoreMessage 的序列化代码，Mirror 自动生成序列化函数。
