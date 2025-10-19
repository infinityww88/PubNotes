# Audacity

- Setting
  - 在macOS Mojave上，确定赋予Audacity麦克风权限
    - Security & Privacy/Privacy/Microphone/Audacity
  - 在Mac上安装Soundflower
    - Soundflower是用于Mac上开源软件，可以不使用线缆将电脑输出的音频重新路由回input。将Soundflower设置为系统的output，然后在Audacity中设置Soundflower为recording设备
  - 在Mac上，如果你需要听见你当前正在录制的内容，需要在Audio MIDI Setup中设置Multi-Output Device
    - 在左侧列表中点击+号创建一个Multi-Output Device
    - 在Multi-Output Device中会显示当前所有的音频输出设备
    - 勾选Built-in Output和任意一个Soundflower设备
      - Built-in Output用来输出当前声音
      - Soundflower（2ch）/Soundflower（64ch）用来接受输出的声音作为其他程序（audacity）的输入设备
  - 同样在Audio MIDI Setup中，在左侧列表中选中要使用作为Audacity输入设备的Soundflower（2ch/64ch），确保Master dB调整到最大，否则audacity得到的声音比原始输出的声音要小
  - 设置系统音频设备的输入输出
    - Input设备指录音时的输入设备，Output设备指系统声音的输出设备，将Output指定为Multi-Output可以使系统声音同时输出到Built-in Output和Soundflower，然后将SoundFlower指定为Input设备，就可以将系统声音输出作为录音的输入，即系统声音->Output->Multi-Output->Soundflower->Input->Audacity。因此重点是指定系统输出设备和Audacity输入设备为同一个Soundflower
    - Preferences/Sound
    - Output设备选择Multi-Output Device
      - 同时将声音输出到系统默认输出和Soundflower，这样就可以在使用audacity录制的同时听见录制的内容
    - Input设备选择一个Soundflower
  - 在audacity中设置音频设备
    - 输入设备选择系统音频中设置的Soundflower
    - 输出设备选择Built-in Output或者Multi-Output Device都可以，因为此时只是audacity输出声音，不会录制，只用来回放audacity的音频处理结果
- As with any new tool, there is often some terminology that comes along with understanding how it works
- Common audio editing terms
  - Project
    - includes all of the files, timing, and information on how you combined and edited different pieces of audio into your file or project
  - Clip
    - a short segment of audio
    - it can be combined with others to make an audio track
  - Track
    - one continuous audio element
  - Library
    - a collection of audio files or tracks
  - Effect
    - two type
      - generator: 在audio track中人工生成或添加sounds
      - processing: 修改既有audio来得到想要的效果
  - Noise
    - 干扰主audio（你想从track听到的声音）的杂音
  - Bit or Sample Rates（比特率/采样率）
    - 每个时间单位传递/处理的比特数量（kbps）
    - 更大采样率意味着track的质量更好
  - Export
    - 保存audio为另外的格式
- Art is just compose, layer, and iterate
- Search game sound effects from google
- 在Youtube上找包含想要的sound的场景视频，用audacity录制，去除noise，得到sound clip，然后进行进一步处理，施加特殊的effect，得到想要SFX（鹰鸣，加农炮/冲锋枪开火，飞机起飞，航船破浪，引擎等等等等）
- 音频由一组track组成，音频最终效果是所有track同时播放的混合
- track由一组clip组成，clip可以在时间线上移动
- track/clip又由1个或2个声道channel组成
  - 1个声道时（mono，单声道），音频同时在左右两个扬声器播放
  - 两个声道时（stereo，立体声），可以分别控制每个声道的音频
- Tools Toolbar：一组可以操作录制的音频track的工具
  - Selection Tool：选择音轨的一部分
    - 使用选区来只对一段特定部分的音轨audio track进行修改
  - Zoom Tool：放大缩小音轨细节，来删除不想要的noise
  - fade in/out track的开始/结束
  - 在时间线上前后移动audio clip（对于要添加一个介绍或退出音频来说这尤其重要
  - 复制一段特定的声音
- Meter Toolbar
  - 显示音频轨道的单声道（mono）或立体声（stereo）声道（channel）
  - 当录制一首歌曲时，不同的乐器被放在不同的声道中
- Edit Toolbar
  - the most useful toolbar
  - cut pieces out of the audio tracks
  - paste new items in
  - trim，link，and silence any unwanted noise
  - undo/redo
  - zoom into a certain area of the recorded track
  - adjust the viewing window so that it works with your preferences
  - fit the audio tracks to window size
- Project Rate：设置项目的比特率。比特率越高，录制的音频质量越高
  - CD音频的比特率是44100Hz，这是audacity默认的比特率，也是绝大多数音频录制的最常用比特率


Soundflower

https://github.com/mattingalls/Soundflower/releases/download/2.0b2/Soundflower-2.0b2.dmg

This is a total guess, but standard 2 channel is just stereo like most recordings you will come across or are playing through your computer.

The 64 channel one is for demanding recordings like grabbing a live recording directly from a soundboard at a live music event, or perhaps in a recording studio where every instrument is being recorded independently and mixed back together later in the desired proportions.

I don't know though. You might want to use 64 channel if you're recording a surround sound movie that has 8 channels or more. I assume the 64 number was just to be sure to cover most use cases of recording things with more than stereo output.

the difference is one is 2 Channel Interface the other is 64 Channel Interface. Use the 2ch if you do not know the difference.

Soundflower 是一款开源软件，已经在 2014 年停止了功能维护，仅由原开发者进行一些新系统的适配工作，但作为一个免费开源的简易内录软件，至今仍不可替代。Soundflower 的功能非常简单，它提供了两个虚拟声卡（2ch 和 64ch），你只需要将你想要提供给其他程序的声音输出到其中一个声卡上，再将另一个程序的声音输入设置为这个声卡，就可以完成简单的音频路由了。

Soundflower 的开发停止几乎是种必然，因为 LoopBack 这一图形化工具的出现，维护这样一款上古时期的软件已经显得没有必要了。但是如果没有这个工具，在 macOS 上直播 Minecraft 几乎是不可能的。LoopBack 选择音源靠的是选择一个 .app 结尾的程序文件，对 Java 应用程序（比如 Minecraft）无能为力，当我尝试用这款软件直播玩 Minecraft 的时候，意识到了这个问题的严重性。而 Soundflowr 是对系统声卡输出的回放，不依赖于选择应用程序。

Loopback 选择一个虚拟声卡，然后在 Source 中选择一个 app 作为音频 source，source 连接一个 Output Channels，然后 Output Channels 连接一个 Monitors，Monitors 是监视器，这样可以在录音的同事监听录制的音频。但是 Soundflow 和 Loopback 不能一起使用，当使用 Loopback Monitors Source 捕获应用程序并使用 Monitors 监听时，Soundflow 的声卡就不在收到声音了。可能有解决方案，但是没有必要让二者一起工作。Loopback 可以免费录制 20 mins，对于大多数音乐音效已经够用了。

Loopback 新建的声卡 Audacity 可能不能立即检测到，重启 Audacity。

Soundflow 简明使用过程：

- 只需使用 2ch 声卡
- Audio MIDI Setup 中创建一个 Multi-Output Device，选中 Soundflow(2ch) 和一个系统输出声卡
- System Preference -> Sound 中，Output 选择 Multi-Output Device，Input 选择 Soundflow(2ch)
- Audacity 中，Input 选择 Soundflow(2ch)，Output 选择任何一个外放声卡即可
