# Process

在 C# 中以子进程执行一个命令行命令。

- FileName：指定要运行的程序的文件名，对于命令行命令，可执行文件是 cmd.exe
- Arguments：传递给可执行文件的命令行参数。要执行命令行命令，需要传递 /c 参数，它只是将后面的命令传递给 cmd.exe 来执行
- CreateNoWindow：子进程不产生新窗口，完全在后台运行
- RedirectStandardOutput/RedirectStandardError：将子进程（命令行命令）的文本输出重定向到 StandardOutput Stream 和 StandardError Stream。这样可以在父进程中通过这两个 Stream 读取子进程的输出
- UseShellExecute：这个 shell 不是 Linux 系统 shell，对于 Windows，shell 是 Explorer 中打开任意文件的那个 shell
- process.StandardOutput.ReadToEnd() 读取完整的输出文本
- process.WaitForExit() 同步子进程的结束，在父进程阻塞等待子进程的完结

```C#
System.Diagnostics.Process process = new System.Diagnostics.Process();
process.StartInfo.FileName = "cmd.exe";
process.StartInfo.Arguments = $"/c {cmd}";
process.StartInfo.CreateNoWindow = true;
process.StartInfo.RedirectStandardError = true;
process.StartInfo.RedirectStandardOutput = true;

process.Start();

string output = process.StandardOutput.ReadToEnd();

if (!string.IsNullOrEmpty(output)) {
    Debug.Log(output);
}

var error = process.StandardError.ReadToEnd();

if (!string.IsNullOrEmpty(error)) {
    Debug.LogError(error);
}
process.WaitForExit();
if (process.ExitCode != 0) {
    throw new Exception($"Run Command Failed with exit code: {process.ExitCode}");
}
```

## RedirectStandardOutput Property

子进程的文本输出是否写入 StandardOutput stream。

当 Process 向 Standard stream 写入 text，文本一般显示在 console 中。将 RedirectStandardOutput 设置为 true，可以将输出重定向到 StandardOutput Stream，这样可以在父进程接收子进程的输出。

如果要设置 RedirectStandardOutput 为 true，必须将 UseShellExecute 设置为 false。否则从 StandardOutput 读取将会抛出异常。

重定向的 StandardOutput stream 可以同步或异步读取。诸如 Read，ReadLin，和 ReadToEnd 等方法在子进程的 output stream 上同步读取。

作为对比，BeginOutputReadLine 在 StandardOutput stream 上开始一个异步读取操作。这个方法立即返回，并使用一个 event handle 异步接收 Stream 的文本。

异步读取输出的程序应该调用 WaitForExit 方法来确保 output buffer 被 flushed。

同步读取操作在读取 StandardOutput stream 的父进程和向 stream 写入的子进程之间创建一个依赖。这个依赖可能导致死锁条件。当调用者从子进程的 redirected stream 读取时，它依赖子进程。当子进程写入足够的数据来填充它的 redirected stream 时，它依赖于父进程。子进程等待下一个 write 操作，直到 parent 从填充满的 full stream 读取走数据，或者关闭这个 stream。死锁条件导致父进程和子进程彼此等等，谁都无法进行下去。

你需要协调父进程和子进程的依赖来避免死锁。

在 p.WaitForExit 之前调用 p.StandardOutput.ReadToEnd 可以避免死锁条件，否则可能会导致死锁，因为子进程已经将 redirected stream 填满，父进程因为先 WaitForExit 而无法从 redirect stream 读取走数据，子进程也无法继续向 redirect stream 写入数据，产生死锁。

因此必须先 ReadToEnd，从 redirect stream 将数据读取走，防止阻塞 child 向 redirect stream 写入数据。最后 WaitForExit。

从同时从 Standard Output 和 Standard Error streams 读取时，也会有类似的问题。因为同时同步读取 output 和 error 必然要先读取一个后读取一个。如果父进程同步等待读取一个 stream（例如 output），而子进程却等等写入另一个 stream，两个条件都不满足，相互等等，产生死锁。可以通过在 StandardError stream 上执行异步读取，在 StandardOutput stream 上执行同步读取来避免死锁；或者创建两个线程分别同步读取两个 stream。

