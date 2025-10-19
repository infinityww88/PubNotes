# Accessing entity data

当你实现 ECS 系统时，迭代你的数据是你要执行的最常见的任务。

ECS 系统通常处理一个 entities 集合，从一个或多个 components 读取数据，执行一个计算，然后将结果写入到另一个 component。

迭代 entities 和 components 的最高效方式是在一个 parallelizable job，它按顺序处理 components。这个可以利用所有可用核心的处理能力，以及数据局部性来避免 CPU cache misses。



