# Sqlite3 FTS5

普通 FTS5 表可以和一般的数据表一样 Update 和 Delete，只有特殊的 FTS5 表（external content table，contentless table，contentless-delete table）的 delete 需要特殊处理。

Andoird 内置的 sqlite3 从 API 24（Andoird 7， 2016）开始默认支持 fts5.

FTS5 是 SQLite virtual table 模块，为数据库应用程序提供全文索引功能。

全文索引允许高效地在大量的文档集合中搜索包含一个或多个要搜索条目的子集，就像 Google 一样。

创建虚拟表：

```sql
create virtual table email USING fts5(sender, title, body);
```

不能为列条件类型、约束、或 primary key，因为列总是文本的，添加它们是一个错误。

创建之后可以用 insert，update 或 delete 填充或删除信息，就像其他表一样。

就像其他没有 primary key 的表一样，FTS5 表有一个默认的 rowid integer primary key 列。

但是可以为列和表提供各种选项，可以用来修改 FTS5 表从 document 和 query 中 extract terms 的方式（分词器），创建额外的索引加速前缀查询，或者创建一个引用其他表为其做全文索引的 FTS 表等等。

全文查询方法：

- select * from email where email MATCH '表达式'
- select * from email where email = '表达式'
- select * from email('表达式')

以上三种方法等价。

全文索引默认在 table 的所有 columns 上查找。可以使用 column filter 限制只在指定 colums 做全文查询。

默认全文查询是大小写不敏感的。

默认返回结果的顺序是任意的，通过 order by rank 按相关性排序。

可以自定义 C 函数扩展 FTS5 模块。

## 全文搜索语法 query

Insert 到 FTS5 的文档（各个列）和执行的 query 表达式被分词器打断解析成一个一个的 token，以及由这些 token 组成的复杂表达式。

```bnf
<phrase> := string[*]
<phrase> := <phrase> + <phrase>
<neargroup>  := NEAR(<phrase> <phrase> .. [, N])
<query>  := [ [-] <columns> :] [^] <phrase>
<query>  := [ [-] <columns> :] [^] <neargroup>
<query>  := [ [-] <columns> :] [^] <query>
<query>  := <query> AND <query>
<query>  := <query> OR  <query>
<query>  := <query> NOT <query>
<columns>  := column_name
<columns>  := {column_name1 column_name2 ... }
```

### FTS5 strings(string\[*\])

FTS 表达式中，string 可以以两种方式指定：

- 将字符包含在 "" 之中
- FTS5 bareword（裸单词）（AND, OR, NOT 除外，大小写敏感）。bardword 是以下字符的连续序列：

  - 非 ASCII 范围的字符（> 127 的 unicode code）
  - 26 个小写字母和 26 个大写英文字母
  - 10 个数字字母
  - 下划线

  这些字符组成的 bareword 可以不用包含在 "" 中

### FTS5 Phrases

最小的 token 是没有任何分隔符号的单词（ascii 的 word，或 unicode > 127 的字符）。

Phrase 是由 word（string） 和 phrase 组成的有序 token 序列，中间不能有其他的 token，而且它们作为一个原子单位在文档中查询。例如 "alpha beta gamma" 是有三个 token 组成的 phrase，它匹配的文档必须有至少一次 "alpha" "beta" "gamma" 作为连续序列的出现，且中间不能有任何其他 token，但是中间的分隔（空白）可以是任意的。但是如果使用 '"alpha" "beta" "gamma"' 查询，它的意思是匹配的文档必须 alpha beta gamma 都出现至少一次，但是不要求它们是连续的。空白分隔的 phrases 默认是 AND 操作，即 '"alpha" AND "beta" AND "gamma"'，它是 3 个 phrase（由 AND 连接），而 '"alpha beta gamma"' 是一个 phrase。

query 中的 string 被分词器 tokenizer 提取 extract 为一个或多个 token/term 组成的列表。

FTS 的查询有 phrases 组成。phrase 是基本单位。一个 word 本身也是一个 phrase。

一个 phrase 是一个或多个 token 的有序列表，中间不能有其他 token，它在全文查询中作为一个原子单元。

由 phrase 组成更大的 phrase 由三种方法：

- 将 token 包含在 "" 中，用空白分隔，例如 '"alpha beta gamma"'
- 用 + 连接多个 phrase，例如 'alpha + beta + gamma'
- 用 . 连接多个 phrase，例如 'alpha.beta.gamma'

这些方法是等价的，而且可以混合使用，例如 '"alpha beta" + gamma'。

### FTS5 Prefix Query

如果一个 FTS expression 中的 string 后面跟着一个 *，则这个 string 提取的最后一个 token 被标记为 prefix token。一个 prefix token 匹配任何以它为前缀的 document token。

例如，

```plain
MATCH '"alpha beta gam"*'
MATCH 'alpha + beta + gam*'
```

匹配任何连续出现 alpha 和 beta token，而且后面紧跟着一个以 gam 为前缀的 toekn 的 文档。

注意 * 必须在 "" 外面，才被解释为特殊字符，否则将作为普通的 token 的一部分。

```plain
MATCH '"alpha beta gam*"'
```

不能匹配上面的文档，因为 * 成为 token 的一部分。

### FTS5 Initial Token Query

如果一个 ^ 出现在一个不是 NEAR group 的 phrase 前面，则这个 phrase 只匹配某个 column 以这个 phrase 开头的 document。

^ 可以和 column filter 一起使用，指定匹配某个 column。

^ 不可以出现在 phrase 中间。

```plain
MATCH '^alpha'              匹配某个 column 以 "alpha" 开头的文档
MATCH '^alpha + beta'       匹配某个 column 以 "alpha beta" 开头的文档
MATCH '^"alpha beta"'       同上
MATCH 'a: ^alpha'           匹配列 a 以 "alpha" 开头的文档
MATCH 'NRAR(^alpha, beta)'  语法错误，^ 后面的 phrase 不能是 NEAR group 的一部分
MATCH '"^alpha beta"        无效，^ 在 "" 里面，被作为 token，而不是特殊字符
```

### FTS5 NEAR Query

两个或多个 phrase 可以放在一个 NEAR group 中查询。NEAR 是大小写敏感的，near 会导致语法错误，必须用大写。

```plain
MATCH NEAR(空白分隔的短语列表 [, 可选的距离 N])
```

N 可选，默认 = 10.

它匹配的文档：

- 每个 phrase 至少出现一次
- 第一个短语结尾和最后一个短语开头之间的 token 数必须小于等于 N

### FTS5 column filter

默认全文索引是在 table 中的每个 column 上执行的，任何一个 column 匹配都返回整个文档，这也是为什么 MATCH 左边指定的是 table name。

Column fitlers 可以限定只在指定的一个或多个列上匹配。

```plain
MATCH 'column: 查询表达式'
MATCH '"column": 查询表达式' 
MATCH '{column0, column1, ...}: 查询表达式' 
```

列指定前面还可以加一个 - 表示在这些列之外的其他列上匹配。

```plain
MATCH '- column: 查询表达式'
MATCH '- {column0, column1, ...}: 查询表达式' 
```

除了在表达式中指定 column filter，对于单个列的 filter 还可以直接把 column 写在 MATCH 左边。

### FTS5 boolean operators

查询表达式本质就是过滤的断言，将这个表达式应用在 document 上求值为 true，则这个 document 匹配。因此这些 bool 断言可以通过 bool 操作符组合成更复杂的过滤断言，就像编程语言的 if 语句一样。

```plain
<query1> NOT <query2>   文档必须满足 query1 且不满足 query2
<query1> AND <query2>   文档必须同时满足 query1 和 query2
<query1> OR  <query2>   文档只需满足 query1 或 query2 中的一个
```

优先级按顺序是 NOT，AND，OR。可以用括号组合优先级。

NOT AND OR 都是大小写敏感的。FTS5 关键字之所以大小写敏感是因为它处理的是文本，能尽量避免干扰文本就尽量避免。

此外空白分隔的表达式默认就是由 AND 连接的 bool 表达式，但是它的优先级比 NOT 更高，就像用括号括起来的 AND 表达式。

'alpha OR beta gamma' 等价于 'alpha OR (beta AND GAMMA)'。

但是隐式 AND 从不插入括号表达式的前后，'(alpha OR beta) gamma' 和 'alpha (beta gamma)' 都是语法错误。

## 创建 FTS5 表

create virtual table tbl using fts5 (...) 括号中每个参数或者是一个 column 声明，或者是一个配置选项。

列名不可以使用 rowid 或 rank，它们是 FTS5 每个表内置的列。

列名后面可以指定选项，当前唯一的选项是 UNINDECED，它表示不为这个列创建 FT 索引，这个列不可以用在查询表达式中，但是可以伴随查询结果返回，在 select 中。

配置选项有一组 key=value 构成，例如：

```sql
create virtual table tbl using fts5(sender, title, body, tokenize = 'porter ascii')
```

当前支持的配置选项：

- tokenize，配置分词器
- prefix，为 FTS5 table 添加 prefix 前缀
- content，使 FTS5 table 成为 external content 或 contentless 的表
- content_rawid，为 external content 表指定 rowid 列
- columnsize，用来配置 FTS5 表的每个 value 的 tokens 数量是否分开存储
- detail，用于优化 FTS index 的磁盘空间

### 前缀索引

默认，FTS5 维护一个 index 表，记录文档集合中每个 token 的位置。这意味着查询完整的 token 很快，因为它和整个 token 比较，但是查询一个前缀 token（string*）则很慢，因为它需要一个 range scan。例如，查询 prefix token "abc*" 需要一个大于等于 "abc" 而小于等于 "abd" 的所有 toekns 的 range scan。

普通的 text 没有前缀索引，而是完全的字符串比较。要使用前缀索引只能用 FTS 表。Mysql 可以为字符串列创建前缀索引。

Prefix 索引是一个单独的 index，它记录特定字符长度的前缀 token 的所有实例的位置，来加快前缀 token 的查询。这与完整 token 的倒排索引是一样的，只是这次，token 不是完整 token 了，而只是一个前缀。

对与完整 token，倒排索引记录的是：

```plain
timestamp -> [doc0, pos0] [doc0, pos1] [doc1, pos0]
timeline-> [doc1, pos0] [doc2, pos0]
```

对于前缀 token time*，倒排索引记录的是：

```plain
time* -> [doc0, pos0] [doc0, pos1] [doc1, pos0], [doc1, pos0] [doc2, pos0]
```

优化前缀 abc* 的查询需要一个 3 字符的前缀索引。

前缀索引需要指定一个字符长度。

```sql
create virtual table ft USING fts5(a, b, prefix='2, 3');
create virtual table ft USING fts5(a, b, prefix=2, prefix=3);
```

### 配置分词器

```sql
create virtual table ft USING fts5(x, tokenize = 'porter ascii');
```

FTS5 内置了 3 个分词器：

- unicode61，默认
- ascii，将所有 >127 的字符视为 token 字符
- porter，实现 porter stemming 算法

#### unicode61

将所有 unicode 字符分类，或者为 separator 字符，或者为 token 字符。默认所有空白和标点都视为分隔符，所有其他字符都视为 token 字符。

每个连续的 token 字符序列被视为一个 token。token 是大小写不敏感的。默认 Latin 字母的音调符号被移除，但可以配置飞机否移除。

分词器参数可以显式设置哪些字符应视为 token 字符，哪些字符应视为 separator 字符。

#### ascii

类似 unicode61，除了：

- 所有 >127 的非 ASCII 字符都视为 token 字符
- 大小写 fold 只应用到 ASCII 字母，只有 A-a 这样的才视为相同字母
- 不支持移除音调符号

#### porter

porter 是一个包装的分词器，它基于一个底层的分词器（unicode61 或 ascii），在底层分词器的结果上再次进行 transform，将具有相同词干的 token 使用共同的词干代替，这样 create 和 creation 都被使用相同的 token，它们被 creat 代替。注意，分词同时应用到 document 建立索引和 query 的解析 token。因此在 query 中 create 或 creation 也被解析为 creat，然后匹配 document 索引中的 creat（create 或 creation）。

#### trigram 分词器

Trigram 分词器扩展 FTS5 来支持一般的子串查询，而不是使用通常的 token 匹配。当使用 trigram 分词器时，一个 query 或 phrase token 可以匹配 document 中的任何字符序列，而不仅是完整 token。用法与其他分词器一样，只是创建表时，指定 trigram 分词器，返回的结果匹配的不仅仅是完整 token，还有以 query phrase 为子串的任何文档。

可以指定是否大小写敏感，还支持 GLOB 和 LIKE 模式匹配。如果指定大小写敏感，则仅支持 GLOB 模式匹配。

```sql
select * from tbl where col LIKE '%XXX%';
select * from tbl where col GLOB '*XXX.'
```

少于 3 个字符的子串不匹配任何 row。

## External Content 和 Contentless Tables

FTS5 是虚拟表，不是真是的 sql 表格。它只是以 sql 语法提供 api 接口。

FTS5 本质是一个倒排索引，记录一个 token 出现在哪些 doc 中，以及出现的位置。每插入一个文档，分词器将它解析为一系列 token，然后在索引中创建或更新每个 token 的索引值。倒排索引只需要 token 和到 doc 的指针。不需要 doc 本身。

但是通常我们查询完文档，还想将文档内容提取出来，因此必须在另外的地方存储文档，倒排索引中 token 的索引值就指向那里的文档位置。

默认地，当一个 row（doc）插入到一个 FTS 表中，除了创建倒排索引，FTS5 还保存这些 doc。当全文查询请求这些 columsn 时，就从保存的 doc 中取出并返回。

content 选项可以告诉 FTS5 不必保存这些 docs，只创建索引就好，因为这些文档通常巨大，可以放在其他地方保存。例如将文档作为外部文件，每次将将文档内容插入虚拟表时，FTS 仅为文档创建索引，而不保存文档内容。虚拟表中可以包含一个 UNINDEXED 的列，记录文件路径。这样 FTS 表可以最小，仅包含倒排索引，和对应的文件路径。全文查询时只能返回匹配的文档的路径，但这就足够了，后面程序可以自己去读取文档文件的内容。这就是 contentless table 的用途所在。

普通 FTS5 表则会在 db 内部保存 docs 的内容，这样就可以直接在 sql 语句中返回文档内容，不需要在外部查询，但这会显著增大 db 大小。可用于 doc 内部不是很大的场景。

有两种方式使用 content 选项：

- 设置它为空字符串，来创建一个 contentless FTS5 table。索引正常创建，查询正常工作，但是仅能返回 rowid 和 rank 列，不能返回任何 column 内容，因为 FTS5 就没有存储 column 的内容。
- 设置它为一个 database object 的名字（table，virtual table，view）。这成为 external content table。和上面说的保存文件路径的 contentless table 类似，这种 FTS5 table 的每个 row 保存引用的 database object 的 row 的 rowid。然后通过 rowid 就可以到 external database object 中查询对应的内容。在 external content table 上全文查询返回 columns（select）时，FTS5 通过 rowid 去引用的 table 取出内容并返回。但是用户需要负责外部表的内容和 FTS5 虚拟表（索引）的内容保持一致，否则行为不可预测。一种方式是在引用的 table 上创建触发器，更新它自动更新 FTS5 虚拟表。

### Contentless tables

```sql
create virtual table tbl USING fts5(a, b, c, content='');
```

Contentless 表不支持 Update 或 Delete 语句，以及没有提供非空 rowid 的 Insert 语句。还不支持 Replace 冲突处理。Replace 和 Insert Or Replace 语句被当做普通的 Insert 语句。

因为删除全文索引的更新、删除很复杂，涉及很多 B-Tree 操作以及很多优化措施。因此对 contentless 表，FTS5 提供特殊的 delete 命令来删除文档，而且不支持 Update，Update 需要先 delete 原来的索引，然后重新插入更新的 doc。

### Contentless-Delete tables

Contentless-delete table 通过将 content 选项设置为空字符串，以及设置 contentless_delete=1 来创建。

```sql
create virtual table f1 USING fts5(a, b, c, content="", contentless_delete=1)
```

Contentless-delete table 和 contentless-delete table 的不同之处是：

- Contentless-delete table 支持 DELETE 和 INSERT OR REPLACE INTO 语句
- Contentless-delete table 支持 Update 语句，但必须为 FTS5 表的所有 columns 提供新的 values
- Contentless-delete table 不支持 FTS5 delete 命令

除非为了向后兼容，新的 code 应该使用 contentless-delete 表，而不是 contentless 表。

### External Content tables

External Content FTS5 表通过将 content 设置为同一个数据库的 table、virutal table、view（即 content table）的名字来创建。

任何时候 FTS5 需要 column values 时，它查询 content table（引用的表），使用它绑定的 rowid：

```sql
select <content_rowid>, <cols> from <content_table> where <content_rowid> = ?
```

通常 content_rowid 就是 rowid。如果创建表时使用 content_rowid 选项设置了 content_table 的 row id 的名字，则使用那个名字。cols 就是逗号分隔的 FTS5 的列名。

因为 FTS5 需要用同样的名字去查询 content table，因此 FTS5 表的列名就是 content table 的列名。另外，普通的 FTS5 表具有自增的 rowid，因为 FTS5 自己创建了一个内部的 table 保存 docs 内容，那个 rowid 就是这个私有表的 rowid。对于 external content 表，content table 不是 FTS5 自己维护的，而是外部系统维护的，因此相应的 rowid 需要用户自己保持与 content table 一致。External content 表没有自己维护的自增 rowid，需要用户自己维持与 content table 的 rowid 一致。对于 columns 也是一样。

总之，external content FTS5 表的 rowid 和 columns 就是 content 表的映射、连接，FTS5 只是为 columns 的内容建立索引，需要用户自己维护两个表的一致。

```sql
create table tbl(a, b, c, d integer primary key);
create vitual table tbl USING fts5(a, c, content=tbl, content_rowid=d);
```

保持 content table 和 FTS5 表一致的一种方式是使用触发器：

```sql
create table tbl(a integer primary key, b, c);
create virtual table fts_idx using fts5(b, c, content='tbl', content_rowid='a');

create trigger tbl_ai after insert on tbl begin
  insert into fts_idx(rowid, b, c) values (new.a, new.b, new.c);
end

create trigger tbl_ad after delete on tbl begin
  insert into fts_idx(fts_idx, rowid, b, c) values ('delete', old.a, old.b, old.c);
end

create trigger tbl_au after delete on tbl begin
  insert into fts_idx(fts_idx, rowid, b, c) values ('delete', old.a, old.b, old.c);
  insert into fts_idx(rowid, b, c) values (new.a, new.b, new.c);
end
```

但是注意新建的 trigger 不会将现有的 row 插入虚拟表。

可以用 rebuild 命令丢弃虚拟表中的索引，基于 content table 中完全重建索引。

在很多方法 external content table 就像 contentless table，不支持 delete，必须用 fts5 的 delete 命令来删除 row。因为 external content table 很可能就是基于 contentless 实现的一个高级功能而已，用来引用另一个 table，给它见索引，这是很常见的功能，因此 sqlite 就直接提供它了。

用户需要负责确保 FTS5 external content table 和 content table 保持一致。

External content table 只用来给 content table 创建索引，不会自动与 content table 保持一致，需要用户手动 insert，update，delete。

### Columnsize 选项

FTS5 通常在 db 中维护一个特殊的 table，存储每个 column value 的 token 数量。这个 table 被 xColumnSize API 函数使用，后者被 bm25 ranking 函数（以及其他自定义 rank 函数）使用。

可以开启或关闭这个功能。

### Detail 选项

控制倒排索引记录哪些内容，用以优化索引占用的磁盘空间。记录的内容更少，占用的磁盘空间越小。但是既然现在存储空间完全不是问题。既然使用 sqlite，要存储的内容肯定也少不了，至少是 Gb 级别的。而且为什么使用 FTS5，就是为了快速查询，而为了快速查询，建立额外的辅助索引文件是必须付出的代价。尤其是如果后端服务器使用 sqlite 做数据，存储更不是问题了。

## 辅助函数

辅助函数就像 sql 的标量函数一样，可以用在 select、order by 等子句中。

内置 3 个辅助函数：

- bm25 相关性排序，默认参数等价 rank 列的值
- highlight
- snippet 提取包含指定数量搜索 token 的文档片段，并高亮 query 的 token

```sql
select * from fts where fts MATCH ? order by bm25(fts);
select * from fts where fts MATCH ? order by rank;
```

### 相关性排序

每个虚拟表都有一个 rank 列，默认它的值就是无参数的 bm25()。如果当前查询不是一个全文查询，rank 总是 null。

可以指定一次查询使用的 bm25 算法的参数。

## 特殊 insert 命令

FTS5 通过 insert 语句提供了一些 API：

```sql
insert into ft(ft, rank) values ("automerge", 8);
```

- merge，automerge, crisismerge，delete-merge，optimize 涉及内部合并 b-tree
- delete 标记删除，在合适时机正式移除 b-tree
- delete-all 删除所有索引
- integrity-check，检查索引与 content table 的一致性，不一致 insert 命令返回 SQLITE_CORRUPT_VTAB 错误
- rank 设置 rank 列使用的默认 bm25 的参数
- rebuild 命令，完全丢弃当前索引，基于虚拟表或引用表的内容重建索引
- secure-delete 内存安全性，防内存攻击

使用 delete 命令删除一个 row 时，必须提供与当前索引建立时的全部列完全一样的文档内容，否则就会导致索引与内容不一致。因为建立索引时就是使用一个特定文档提取出的 tokens 来建立的，并且指向这个文档，要删除时，必须找到完全一样的 tokens，而唯一的方式就是提供完全一样的文档，由分词器再重新分词一次，提供完全一样的 tokens。

delete 和 delete-all 对 contentless table 和 external content table 是唯一能删除索引的方法，它们不支持 Delete sql 语句。
