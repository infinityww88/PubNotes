## Google AdMob Mobile Ads SDK Unity

要展示 AdMob 广告并赚取收入，第一步是将 Google 移动广告 Unity 插件集成到应用中。集成完成后，可以选择原生广告或激励广告等广告格式。

借助 Google 移动广告 Unity 插件，Unity 开发者无需编写 Java 或 Objective-C 代码，即可在 Android 和 iOS 应用上投放 Google 移动广告。该插件提供了一个用于请求广告的 C# 接口，供 Unity 项目中的 C# 脚本使用。

### 初始化 SDK

加载广告之前，请先调用 MobileAds.Initialize()，以便让应用初始化 Google 移动广告 SDK。此操作仅需执行一次，最好是在应用启动时执行。

### 选择广告格式

在将 Google 移动广告 SDK 部署到 Android 或 iOS 平台时，您的 Unity 应用中现已包含该 SDK。现在，您可以植入广告了。AdMob 提供了许多不同的广告格式，您可以从中选择一种能够提供最佳用户体验的广告格式。

- 横幅

  横幅广告单元展示会占据应用部分布局的矩形广告。他们可以在设定的期限后自动刷新。这意味着，用户会定期查看新广告，即使他们停留在应用中的同一个屏幕上也是如此。这种广告格式也是最容易植入的广告格式。

- 插页式广告

  插页式广告单元会在您的应用中展示全屏广告。请将其放置在应用界面中的自然停顿点和过渡点，例如在游戏应用中通过关卡后。

- 原生

  借助原生广告，您可以自定义素材资源（如标题和号召性用语）在应用中的呈现方式。通过自行设置广告样式，您可以呈现出自然、不突兀的广告展示效果，从而使用户体验更加丰富。

- 激励

  激励广告单元可让用户玩游戏、填写调查问卷或观看视频，以赢取应用内奖励，例如金币、额外的生命或积分。您可以为不同的广告单元设置不同的奖励，并指定用户获得的奖励价值和奖品。

- 插页式激励广告

  插页式激励广告是一种激励用户的新型广告格式，可让您通过在应用中的自然过渡点自动展示的广告向用户提供奖励，例如金币或额外生命值。

  与激励广告不同，用户无需自行选择即可观看插页式激励广告。

  与激励广告中的选择观看提示不同，插页式激励广告需要一个介绍画面，在其中公布奖励，并为用户提供选择退出的机会（如果他们想要选择退出）。

- 打开应用

  开屏广告是一种在用户打开或切换回您的应用时显示的广告格式。这种广告会叠加在加载屏幕上。

### 启用测试广告

在开发过程中启用测试广告非常重要，这样就可以在不向 Google 广告主收费的情况下点击广告。如果在非测试模式下点击过多广告的帐号可能会因为无效活动而被举报。

获取测试广告的方法有两种：

- 使用 Google 的某个示例广告单元。

- 使用您自己的广告单元并启用测试设备。

#### 示例广告单元

最快的测试启用方法是使用 Google 提供的测试广告单元。这些广告单元未与 AdMob 帐号相关联，因此在使用这些广告单元时，帐号不会产生无效流量。

应根据平台选择使用 Google 提供的不同测试广告单元。在 iOS 设备上发出测试广告请求时您需要使用 iOS 测试广告单元，而在 Android 设备上发出请求时，需要使用 Android 测试广告单元。

以下是各格式在 Android 和 iOS 上的广告单元示例：

Android

| 广告格式		|	示例广告单元 ID |
| ---			|	---		|
| 开屏广告		|	ca-app-pub-3940256099942544/9257395921 |
| 横幅广告		|	ca-app-pub-3940256099942544/6300978111 |
| 插页式广告		|	ca-app-pub-3940256099942544/1033173712 |
| 激励广告		|	ca-app-pub-3940256099942544/5224354917 |
| 插页式激励广告	|	ca-app-pub-3940256099942544/5354046379 |
| 原生代码		|	ca-app-pub-3940256099942544/2247696110 |
|			|			|

iOS

| 广告格式		|	示例广告单元 ID |
| ---			|	---		|
| 开屏广告		|	ca-app-pub-3940256099942544/5575463023 |
| 横幅广告		|	ca-app-pub-3940256099942544/2934735716 |
| 插页式广告		|	ca-app-pub-3940256099942544/4411468910 |
| 激励广告		|	ca-app-pub-3940256099942544/1712485313 |
| 插页式激励广告	|	ca-app-pub-3940256099942544/6978759866 |
| 原生代码		|	ca-app-pub-3940256099942544/3986624511 |

这些广告单元指向特定的测试广告素材。

#### 启用测试设备

如果希望使用实际投放的广告进行更严格的测试，可以将设备配置为测试设备，并使用在 AdMob 界面中自行创建的广告单元 ID。可以在 AdMob 界面中添加测试设备，也可以使用 Google 移动广告 SDK 以编程方式添加测试设备。

系统会自动将 Android 模拟器和 iOS 模拟器配置为测试设备。

- 在 AdMob 界面中添加测试设备

  如需通过简单的非编程方式添加测试设备并测试新的或现有的应用 build，使用 AdMob 界面。

  新的测试设备通常会在 15 分钟内开始在您的应用中投放测试广告，但最多可能需要 24 小时。

- 以编程方式添加测试设备

  - 运行配置了移动广告 SDK 的应用，并使用上面列出的某个测试广告单元 ID 发出广告请求

    ```C#
    private void RequestBanner()
    {
        #if UNITY_ANDROID
            string adUnitId = "ca-app-pub-3940256099942544/6300978111";
        #elif UNITY_IPHONE
            string adUnitId = "ca-app-pub-3940256099942544/2934735716";
        #else
            string adUnitId = "unexpected_platform";
        #endif
    
        // Create a 320x50 banner at the top of the screen.
        bannerView = new BannerView(adUnitId, AdSize.Banner, AdPosition.Top);
        // Create an empty ad request.
        AdRequest request = new AdRequest();
        // Load the banner with the request.
        bannerView.LoadAd(request);
    }
    ```
  - 在控制台或 logcat 输出中检查如下消息:

    Android

    ```
    I/Ads: Use
      RequestConfiguration.Builder
        .setTestDeviceIds(Arrays.asList("33BE2250B43518CCDA7DE426D04EE231"))
      to get test ads on this device.
    ```

  - 将由字母和数字组成的测试设备 ID 复制到剪贴板。

  - 修改代码，将测试设备 ID 添加到 RequestConfiguration.TestDeviceIds 列表中。

    ```C#
    RequestConfiguration requestConfiguration = new RequestConfiguration();
    requestConfiguration.TestDeviceIds.Add("2077ef9a63d2b398840261c8221a0c9b");
    ```

  - 将 requestConfiguration 全局设置为 MobileAds。

    ```C#
    MobileAds.SetRequestConfiguration(requestConfiguration);
    ```

  - 重新运行应用。如果您将设备正确添加为测试设备，则会在横幅广告、插页式广告和激励广告顶部的中间部分看到一个 Test Ad 标签。

    凡是带有 Test Ad 标签的广告，均可以放心点击。对测试广告的任何请求、展示和点击都不会显示在您帐号的报告中。

  - 现在，设备已注册为测试设备，可以通过将测试 adUnitID 替换为自己的 adUnitID 来开始接收更真实的测试广告。

- 使用 Unity 编辑器进行测试

可以直接在 Unity 编辑器中测试广告。编辑器将添加一张 Prefab 图片，以提供与实际广告在移动平台上的行为类似的体验。

注意 ：由于模拟广告是 Prefab 对象，因此它们会显示在 Unity 编辑器中 GUI 的“下方”。但是，当您导出到移动平台时，广告会呈现在任何游戏视图之上。

## 激励广告

激励广告，指的是用户可以选择与之互动来换取应用内奖励的一种广告。

注意：务必用测试广告进行测试。

### 初始化 Mobile Ads SDK

加载 ads 之前，调用 MobileAds.Initialize() 初始化 Mobile Ads SDK。这只需要做一次，最好只在 app 启动时。

```C#
using GoogleMobileAds;
using GoogleMobileAds.Api;

public class GoogleMobileAdsDemoScript : MonoBehaviour
{
    public void Start()
    {
        // Initialize the Google Mobile Ads SDK.
        MobileAds.Initialize((InitializationStatus initStatus) =>
        {
            // This callback is called once the MobileAds SDK is initialized.
        });
    }
}
```

### 实施步骤

- 加载激励广告

  激励广告的加载是通过对 RewardedAd 类使用静态 Load() 方法完成的。已加载的 RewardedAd 对象会以回调处理程序中的参数的形式提供。

  ```C#
    // These ad units are configured to always serve test ads.
  #if UNITY_ANDROID
    private string _adUnitId = "ca-app-pub-3940256099942544/5224354917";
  #elif UNITY_IPHONE
    private string _adUnitId = "ca-app-pub-3940256099942544/1712485313";
  #else
    private string _adUnitId = "unused";
  #endif
  
    private RewardedAd _rewardedAd;
  
    /// <summary>
    /// Loads the rewarded ad.
    /// </summary>
    public void LoadRewardedAd()
    {
        // Clean up the old ad before loading a new one.
        if (_rewardedAd != null)
        {
              _rewardedAd.Destroy();
              _rewardedAd = null;
        }
  
        Debug.Log("Loading the rewarded ad.");
  
        // create our request used to load the ad.
        var adRequest = new AdRequest();
  
        // send the request to load the ad.
        RewardedAd.Load(_adUnitId, adRequest,
            (RewardedAd ad, LoadAdError error) =>
            {
                // if error is not null, the load request failed.
                if (error != null || ad == null)
                {
                    Debug.LogError("Rewarded ad failed to load an ad " +
                                   "with error : " + error);
                    return;
                }
  
                Debug.Log("Rewarded ad loaded with response : "
                          + ad.GetResponseInfo());
  
                _rewardedAd = ad;
            });
    }
  ```

  强烈建议不要在广告加载失败时尝试使用广告请求完成块加载新广告。如果必须使用广告请求完成块加载广告，请限制广告加载重试次数，以免在网络连接受限等情况下广告请求连续失败。

  提示：您可以使用广告加载调用在打算展示广告之前构建预加载广告的缓存，以便在需要时以零延迟展示广告。由于广告会在一小时后过期，因此您应该清除此缓存，并且每小时重新加载一次新广告。

- 验证服务器端验证（SSV）回调【可选】

  对于需要服务器端验证回调中额外数据的应用，应使用激励广告的自定义数据功能。在激励广告对象上设置的任何字符串值都将传递给 SSV 回调的 custom_data 查询参数。如果未设置自定义数据值，custom_data 查询参数值不会出现在 SSV 回调中。

  ```C#
  // send the request to load the ad.
  RewardedAd.Load(_adUnitId, adRequest, (RewardedAd ad, LoadAdError error) =>
  {
      // If the operation failed, an error is returned.
      if (error != null || ad == null)
      {
          Debug.LogError("Rewarded ad failed to load an ad with error : " + error);
          return;
      }
  
      // If the operation completed successfully, no error is returned.
      Debug.Log("Rewarded ad loaded with response : " + ad.GetResponseInfo());
  
      // Create and pass the SSV options to the rewarded ad.
      var options = new ServerSideVerificationOptions
                            .Builder()
                            .SetCustomData("SAMPLE_CUSTOM_DATA_STRING")
                            .Build()
      ad.SetServerSideVerificationOptions(options);
  
  });
  ```

  如果要设置自定义奖励字符串，则必须在展示广告之前设置。

- 通过激励回调展示激励广告

  展示广告时，必须提供一个回调，用于处理用户奖励。每次加载时，广告仅可展示一次。可以使用 CanShowAd() 方法验证广告是否已做好展示准备。


  ```C#
  public void ShowRewardedAd()
  {
      const string rewardMsg =
          "Rewarded ad rewarded the user. Type: {0}, amount: {1}.";
  
      if (rewardedAd != null && rewardedAd.CanShowAd())
      {
          rewardedAd.Show((Reward reward) =>
          {
              // TODO: Reward the user.
              Debug.Log(String.Format(rewardMsg, reward.Type, reward.Amount));
          });
      }
  }
  ```

- 监听激励广告事件

  若要进一步自定义您广告的行为，您可以在广告生命周期内加入许多事件，如打开、关闭等等。您可以通过注册代理来监听这些事件，如下所示。

  ```C#
  private void RegisterEventHandlers(RewardedAd ad)
  {
      // Raised when the ad is estimated to have earned money.
      ad.OnAdPaid += (AdValue adValue) =>
      {
          Debug.Log(String.Format("Rewarded ad paid {0} {1}.",
              adValue.Value,
              adValue.CurrencyCode));
      };
      // Raised when an impression is recorded for an ad.
      ad.OnAdImpressionRecorded += () =>
      {
          Debug.Log("Rewarded ad recorded an impression.");
      };
      // Raised when a click is recorded for an ad.
      ad.OnAdClicked += () =>
      {
          Debug.Log("Rewarded ad was clicked.");
      };
      // Raised when an ad opened full screen content.
      ad.OnAdFullScreenContentOpened += () =>
      {
          Debug.Log("Rewarded ad full screen content opened.");
      };
      // Raised when the ad closed full screen content.
      ad.OnAdFullScreenContentClosed += () =>
      {
          Debug.Log("Rewarded ad full screen content closed.");
      };
      // Raised when the ad failed to open full screen content.
      ad.OnAdFullScreenContentFailed += (AdError error) =>
      {
          Debug.LogError("Rewarded ad failed to open full screen content " +
                         "with error : " + error);
      };
  }
  ```

- 清理激励广告

  创建完 RewardedAd 后，请确保在放弃对它的引用前调用 Destroy() 方法：
  
  ```C#
  _rewardedAd.Destroy();
  ```

这会通知插件已不再使用该对象，且可回收它占用的内存。此方法调用失败将导致内存泄漏。

- 预加载下一个激励广告

  RewardedAd 是一次性对象。这意味着，在激励广告展示后，该对象就无法再使用了。若要再请求一个激励广告，需要创建一个新的 RewardedAd 对象。

  若要为下一次展示机会准备好激励广告，请在 OnAdFullScreenContentClosed 或 OnAdFullScreenContentFailed 广告事件引发后预加载激励广告。

  ```C#
  private void RegisterReloadHandler(RewardedAd ad)
  {
      // Raised when the ad closed full screen content.
      ad.OnAdFullScreenContentClosed += ()
      {
          Debug.Log("Rewarded Ad full screen content closed.");
  
          // Reload the ad so that we can show another as soon as possible.
          LoadRewardedAd();
      };
      // Raised when the ad failed to open full screen content.
      ad.OnAdFullScreenContentFailed += (AdError error) =>
      {
          Debug.LogError("Rewarded ad failed to open full screen content " +
                         "with error : " + error);
  
          // Reload the ad so that we can show another as soon as possible.
          LoadRewardedAd();
      };
  }
  ```

