# 表达式

## Primaries

### Calls

调用一个callable对象

Python语法比Javascript更严格，函数参数是严格匹配的，而Javascript则是宽松的，不指定就是undefined，多余参数被忽略，而Python不指定参数或有多余参数会抛出TypeError

如果有关键字arguments出现，它们首先被转换为位置参数。首先为所有formal parameters创建一个未填充的slots list。如果有N个positional arguments，它们被放置在前N个slots中。接着对于每个关键字argument，关键字用来确定参数对应的slots（第一个和关键字相同的formal parameter名字对应的slots）。如果slot以及填充了，抛出TypeError异常。否则，这个arguemnt将填充这个slot。如果所有的argument都被被处理了，还没有被填充的slot被填充以函数定义的默认参数（默认参数在函数定义时被执行求值一次，如果默认参数是list或dict，它们可被多次函数调用共享）。如果还有没有填充的slot，则TypeError异常将被发出。否则填充好的slot list将作为调用的argument

CPython实现细节

    built-in函数的位置参数可能没有名字，尽管在文档中它们被命名，因此它们不能以关键字方式传递

    如果有比formal paramter slots更多的位置参数，TypeError将raised，除非有一个使用*identifier语法的formal parameter。这种情况下，这个formal parameter接收一个包含所有多余的位置arguments的tuple（或者empty tuple如果没有多余的位置参数）

    如果关键字参数不对应任何formal paramter名字，则抛出TypeError异常，除非有一个使用**identifier语法的formal paramter。这种情况下，这个formal paramter接收一个包含所有多余关键字arguments的dict（或者empty dict如果没有多余的关键字参数）

    Call接收任何数量arguments的*和**unpacking，位置argument可以跟在*unpacking后面，关键字参数可以跟在**unpacking后面

argument list无论是单个传递还是unpacking传递，最终分为两组，第一组为位置参数，第二组为关键字参数。位置参数必须在关键字参数之前。位置参数用于传递必须参数，关键字参数用于调整可选项

parameter list分为两组，第一组为位置-关键字参数，第二组为关键字-only参数。位置-关键字参数和关键字-only参数通过\*或者\*identifier分割。\*或者\*identifier只能是位置参数的最后一个，因为它后面的参数只能通过关键字传递。关键字参数是位置无关的，因此\*\*identifier只能是最后一个参数

parameter list定义参数可以怎样传递，argument list为参数实际怎样传递

每个函数定义只能有一个*parameter, **parameter，否则编译器不知道每个parameter应该接收多少argument

通常的函数参数列表定义

    def func(pp0, pp1, *pp2, kp0, kp1, **kp2)
    pp0，pp1即可以通过位置传递，也可以通过关键字传递
    kp0, kp1只能通过关键字传递
    pp0，pp1，kp0，kp1都可以定义默认参数
