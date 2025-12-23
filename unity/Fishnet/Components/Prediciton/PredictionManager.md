PredictionManager 提供 states，callbacks，和 settings 来精细调整预测，以适应你的游戏类型。

PredictionManager 是一个核心组件，负责管理 prediction system。Prediction System 允许 clients 预测它们自己的 actions，并且在从服务端收到权威 updates 后 reconcile（修正）他们的状态。

PredictionManager 允许你调整各种预测设置，以及得到特定预测回调。
