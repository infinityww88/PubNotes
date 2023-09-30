# ffmpeg

## 检验视频完整性

```text
ffmpeg -v error -i filename.mkv -map 0:1 -f null -

find . -name "*.mkv" -o -name "*.mp4" -exec sh -c "ffmpeg -v error -i {} -map 0:1 -f null - 2>{}.log"
```

如果输出 log 文件不为空，说明视频文件出现错误。完整的文件没有输出。

## 获取视频截图

```text
ffmpeg -ss 00:00:05 -i v0.mp4 sample.jpg -vframes 1 -an -vcodec mjpeg
ffmpeg -ss 00:00:05 -i v0.mp4 sample.png -vframes 1 -an -vcodec mjpeg
```

-ss 参数放在第一个位置。

-vframes 表示只输出一帧。

连续截取多帧：

```text
ffmpeg -ss 100 -t 600 -r 0.2 -i v0.mp4 -f image2 -y %03d.jpg
ffmpeg -ss 100 -t 600 -r 0.2 -i v0.mp4 -f image2 -vframes 5 -y %03d.jpg
```

-r 截取帧率，每秒多少帧，0.2 表示5秒一帧。

-t 使用的视频长度，乘以 -r 参数得到最终截取的帧的数量。

参数都放在 -i 前面。

## 缩放视频

假设原始视频尺寸是 1080p（即 1920×1080 px，16:9），使用下面命令可以缩小到 480p：

```sh
ffmpeg -i a.mov -vf scale=853:480 -acodec aac -vcodec h264 out.mp4
```

各个参数的含义：

- -i a.mov 指定待处理视频的文件名
- -vf scale=853:480 vf 参数用于指定视频滤镜，其中 scale 表示缩放，后面的数字表示缩放至 853×480 px，其中的 853px 是计算而得，因为原始视频的宽高比为 16:9，所以为了让目标视频的高度为 480px，则宽度 = 480 x 9 / 16 = 853
- -acodec aac 指定音频使用 aac 编码。注：因为 ffmpeg 的内置 aac 编码目前（写这篇文章时）还是试验阶段，故会提示添加参数 “-strict -2” 才能继续，尽管添加即可。又或者使用外部的 libfaac（需要重新编译 ffmpeg）。
- -vcodec h264 指定视频使用 h264 编码。注：目前手机一般视频拍摄的格式（封装格式、文件格式）为 mov 或者 mp4，这两者的音频编码都是 aac，视频都是 h264。
- out.mp4 指定输出文件名

上面的参数 scale=853:480 当中的宽度和高度实际应用场景中通常只需指定一个，比如指定高度为 480 或者 720，至于宽度则可以传入 “-1” 表示由原始视频的宽高比自动计算而得。即参数可以写为：scale=-1:480，当然也可以 scale=480:-1

## 裁剪视频

有时可能只需要视频的正中一块，而两头的内容不需要，这时可以对视频进行裁剪（crop），比如有一个竖向的视频 1080 x 1920，如果指向保留中间 1080×1080 部分，可以使用下面的命令：

```sh
ffmpeg -i a.mov -strict -2 -vf crop=1080:1080:0:420 out.mp4
```

其中的 crop=1080:1080:0:420 才裁剪参数，具体含义是 crop=width:height:x:y，其中 width 和 height 表示裁剪后的尺寸，x:y 表示裁剪区域的左上角坐标。比如当前这个示例，我们只需要保留竖向视频的中间部分，所以 x 不用偏移，故传入0，而 y 则需要向下偏移：(1920 – 1080) / 2 = 420
视频缩放和裁剪是可以同时进行的，如下命令则为将视频缩小至 853×480，然后裁剪保留横向中间部分：

```sh
ffmpeg -i IMG_4940.MOV -strict -2 -vf scale=853:480,crop=480:480:186:0 out.mp4
```

## 剪辑视频

如果有一段很长的视频只需保留其中的一段，可以使用下面命令对视频进行剪辑。

```sh
ffmpeg -i a.mov -ss 00:00:21 -t 00:00:10 -acodec aac -vcodec h264 -strict -2 out.mp4
```

其中 -ss 00:00:21 表示开始剪辑的位置（时间点），-t 00:00:10 表示剪辑的长度，即 10 秒钟。

当然一段视频是可以在一个命令里同时进行剪辑、缩放、裁剪的，只需把相关的参数合在一起即可。
