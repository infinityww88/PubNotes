# Logical Operators

## Compare

给出两个值A和B，比较它们之间的大小和相等关系，结果可以通过True/False输入端口取正或取反

## Compare With Range

比较一个值是否在一个range中

## Debug Swith

选择一个输入端口，输入它的值。只对选择的端口生成源代码，hard swtich

MaxAmount：最大switch选项数量（2～8）

Current：当前选择的输出端口

## If

给出两个值A和B，更具它们的大小关系输出A>B，A==B，A<B三个输入端口中的对应值

## Static（TODO）

创建和使用shader关键字#if, #elif, #endif指示符。

连接到True输入端口的值将被用于在#if指示符中，False被用于#else中。如果Type指定多个关键字，为每个关键字生成一个#elif输入端口

## Template Multi-Pass Switch（TODO）

Multi-Pass模板switch节点根据当前分析的sub-shader/pass在编译时转发正确的输入端口值。即在编译时，为每个pass输入端口生成一个pass，并把对应pass的输入传递给它

## Toggle Switch Node

根据toggle value内部属性切换输入。切换值可以之后通过material进行修改（与hard swtich相反，hard switch不能通过material修改，而是在编译时就必须选好使用哪个分支，然后生成对应的代码，舍弃剩余的哪些分支的代码生成）
