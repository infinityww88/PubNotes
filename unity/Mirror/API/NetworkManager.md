# NetworkManager

public class NetworkManager : MonoBehaviour

NetworkRoomManager : NetworkManager

每一个 scene 有自己的 NetworkManager。如果多个 scene 有相同的逻辑，则可以使用同一个 NetworkManager。否则，不同用途的 scene 使用各自不同的 NetworkManager。

Room 也是一个 scene，和 game scene 的逻辑不同，因此使用不同的 NetworkManager。

## Fields

- authenticator：public NetworkAuthenticator

- autoCreatePlayer：public bool

  控制在 connect 时，或者 scene change 时，是否自动创建 player objects。

- autoStartServerBuild：public bool

  如果 application 是一个 Server Build，StartServer 自动调用。

  在 build menu 选中 Server build，或者在 BuildOptions 中选择 BuildOptions.EnableHeadlessMode，则是 Server build

- clientLoadedScene：public bool

  如果 client 连接 server 时加载了一个新的 scene，则为 true。

  这在 OnClientConnect 调用之前被设置，因此如果发生一个 sceneload，可以在 OnClientConnect 检查这个标记来执行不同的逻辑。

- disconnectInactiveConnections：public bool

  server 是否应该断开静默超过 Server Idle Timeout 的远程连接。

- disconnectInactiveTimeout：public float

- dontDestroyOnLoad：public bool

  当 scene 改变时，NetworkManager 是否销毁。

  如果你的游戏有一个贯穿进程生命周期的单个 NetworkManager，则应该设置。如果每个 scene 有各自的 NetworkManager，则不应设置。

- isNetworkActive：public bool

  如果 server 或 client 已经开始并运行。

  这在 StartServer / StartClient 设置为 true，在 StopServer / StopClient 设置为 false。

- loadingSceneAsync：public static UnityEngine.AsyncOperation

- maxConnections：public int

  并行 network connections 的最大数量。这影响网络层的内存使用。

- networkAddress：public string

  对于 clients，这是 server 的地址。对于 server，这是监听的 local address

- offlineScene：public string

  当离线时切换到的 scene。网络连接是全局维护的，在 NetworkServer 和 NetworkClient 单例中。当网络连接断开时，游戏切换到这个 scene（无论之前在哪个 scene）。

  当一个 network session 完成时，将会切换到这个 scene，例如 client 断开连接时，或者 server 关闭时。

- onlineScene：public string

  当 client online 时，切换到的 scene。

  当一个 network session 开始时，将会切换到这个 scene，例如一个 client 连接时，或者一个 server 开始监听时。

- playerPrefab：public GameObject

  默认 prefab，用于在 server 上创建 player objects。

  Player objects 在 server 上的 AddPlayer() 的默认 handler 中创建。实现 OnServerAddPlayer 来覆盖这个行为。

- playerSpawnMethod：public PlayerSpawnMethod

  用于生成 players 的方法（随机和循环）

- runInBackground

  程序是否在 background 运行。

  当网络程序的多个实例在同一个机器上运行时，这是必须的，例如使用 localhost 测试时。当部署到移动平台时，不建议使用这个选项。

- serverTickRate：public int

  Server 每秒更新的频率。对快节奏的游戏，例如 Counter-Strike 使用 60Hz 来最小化延迟。对于诸如 WoW 游戏使用 30Hz 来最小化计算。对于诸如 EVE 这样慢节奏的游戏使用 10Hz。

- showDebugMessages

  在 console 开启 verbose 调试消息

- spawnPrefabs：public List<GameObject>

  注册到 spawning system 的 prefabs 列表。对于这些 prefabs 的每一个，ClientScene.RegisterPrefab() 将会自动调用。

- startPositionIndex：public static int

- startPositions：public static List<Transform>

  场景中所有 NetworkStartPosition 组件的 Transform

- transport：protected Transport

## Properties

- isHeadless：public static bool {get;}

  headless mode 检测

- mode：public NetworkManagerMode

  server/client/host

- networkSceneName：public static string

  当前 network scene 的名字。

  当 NetworkManager 进行 scene 管理时，填充这个字段。调用 ServerChangeScene() 导致它发生变化。连接到 server 的新的 clients 将会自动 load 这个 scene。

  这用来确保所有的 scene 变化被 Mirror 初始化。

  手动 Loading 一个 scene 不会设置 networkSceneName，因此 Mirror 仍然会在 start 时仍然会重新 load 它。

- numPlayers：public int

  连接到 server 上的 active player objects 的数量，只在 host / server 上有效。

- singleton：public static NetworkManager

- startOnHeadless：public bool

## Methods

- Awake()

- ConfigureServerFrameRate()：public virtual void

  为一个 headless server 设置 frame rate。覆盖这个方法，如果你想 disable 这个 behaviour，或者设置你自己的 tick rate。

- GetStartPosition()：public Transform

  基于场景中的 NetworkStartPosition objects 查询一个 spawn position。

  被 OnServerAddPlayer 的默认实现使用。

- IsSceneActive(string scene)：public static bool

  指定名字的 scene 是否是当前 active 的 scene

- LateUpdate()

- OnApplicationQuit()

  当应用程序退出，或者停止 editor。

- OnClientChangeScene(string newSceneName, SceneOperation sceneOperation, bool customHandling)

  SceneManager.LoadSceneAsync 执行之前，在 ClientChangeScene 中立即调用。

  这允许 client 在 scene 改变之前执行 work / cleanup / prep。

  customHandling：指示 scene loading 将通过 overrides 被处理。

- OnClientConnect(NetworkConnection conn)：public virtual void

  当连接到 server 时在 client 上调用。

  这个函数的默认实现设置 client 为 ready，并添加一个 player。覆盖这个函数来指定当 client 连接时发生什么。

- OnClientDisconnect(NetworkConnection conn)：public virtual void

  当从 server 断开连接时，在 client 上调用。

- OnClientError(NetworkConneciton conn, int errorCode)

  当发生一个 network error 时在 client 上调用

- OnClientNotReady(NetworkConnection conn)

  当 server 通知 client 它不再 ready 时，在 client 上调用。通常用在当切换场景的时候。

- OnClientSceneChanged(NetworkConnection conn)

  当一个 scene 被 server 初始化并在 client 完成加载时，在 clients 上调用。

- OnDestroy()

- OnServerAddPlayer(NetworkConnection conn)

  当一个 client 使用 ClientScene.AddPlayer 添加一个新的 player 时，在 server 上调用。

  默认实现是从 NetworkManager 的 Player Prefab 创建一个新的 player object。

- OnServerChagneScene(string newSceneName)

  在 SceneManager.LoadSceneAsync 执行之前，在 ServerChangeScene 中立即调用。

- OnServerConnect(NetworkConnection conn)

  当一个新的 client 连接到 server 上时调用。

- OnServerDisconnect(Connection conn)

  当一个新的 client 断开到 server 的连接时调用

- OnServerError(NetworkConnection conn, int errorCode)

  当一个 client connection 发生错误时，在 server 上调用。

- OnServerReady(NetworkConneciton conn)

  当一个 client ready 时调用。默认实现是调用 NetworkServer.SetClientReady() 来继续 network setup process。

- OnServerSceneChanged(string sceneName)

  当一个 scene 完成加载时在 server 上调用。

- OnStartClient()

  当 client 开始时被调用

- OnStartHost()

  当 host 开始时被调用

- OnStopClient()

  当 client 停止时调用

- OnStopHost()

  当 host 停止时被调用

- OnStopServer()

  当 server/host 停止时调用

- OnValidate()

- RegisterStartPosition(Transform start)

  注册一个 transform 作为一个 player spawn location。

  这可以通过 NetworkStartPosition 组件自动完成，也可以在 code 中手动完成

- ServerChangeScene(string newSceneName)

  导致 server 切换 scenes，并设置 networkSceneName。

  连接到 server 上的 clients 自动切换到这个 scene。如果 onlineScene 或 offlineScene 被设置，这个函数被自动调用。但是它也可以从 code 中调用，在 game 进行中再次切换 scene。这个调用自动设置 client 为 not-ready。Clients 必须重新调用 NetworkClient.Ready() 来加入新的 scene。

- Shutdown()

  这是清理 singleton 的唯一方法，使得另一个 instance 被创建

- Start()

- StartClient()

  启动一个 network client（NetworkClient 实例）。它使用 networkAddress 属性作为连接的地址。这使得新创建的 client 立即连接到 server。

- StartClient(Uri)

  连接 Uri 指定的 server 地址

- StartHost()

  启动一个 network host - server 和 client 在同一个应用程序中。

  当 StartHost() 中返回的 client 是一个特殊的 “local” client，它使用一个消息队列和 in-process server 通信，而不是真实的 network。但是几乎所有其他情况下，它都可以被当做一个 normal clinet。

- StartServer()

  启动一个新的 server（NetworkServer.Listen()）

- StopClient()

  停止 manager 使用的 client

- StopHost()

  停止 manager 使用的 server 和 client

- StopServer()

  停止 manager 使用的 server

- UnRegisterStartPosition(Transform start)

  反注册一个 transform 作为一个 player spawn location。

  这可以通过 NetworkStartPosition 组件自动完成，但是也可以从 code 手动调用。
