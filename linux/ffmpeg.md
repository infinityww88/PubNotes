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
