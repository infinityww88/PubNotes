# Player Setting

## Package Name

需要设置好 link.netripple.EnglishLearn，否则打包部署到手机上会失败：

```text
CommandInvokationFailure: Unable to install APK to device. Please make sure the Android SDK is installed and is properly configured in the Editor. See the Console for more details.
C:\Program Files\Unity\Hub\Editor\2022.3.0f1c1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe -s "PVK0222715005206" install -r -d "C:\Users\13687\Documents\Unity\Language\Build\Language.apk"
```

## Allow downloads Over HTTP

UnityWebRequest 是不允许 HTTP 连接的，除了 127.0.0.1 和 localhost。

这些选项可以开启 HTTP 连接。
