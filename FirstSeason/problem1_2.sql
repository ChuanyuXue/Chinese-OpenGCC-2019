/*任务描述
编写合适的 SQL 语句在限制时间内（20s）查询出1-10000之间的哪一个数字不存在于test1表中

输出结果字段命名为a

表结构说明
test1表字段说明如下：

字段名	类型	描述
a1	int	a1列，非空
a2	int	a2列，非空
a3	int	a3列，非空
a4	int	a4列，非空
a5	int	a5列，非空
a6	int	a6列，非空
a7	int	a7列，非空
a8	int	a8列，非空
该表总共三十多万行，表中的每个值为1-10000中的某个数，其中第一行数据如下:



测试说明
你只需在右侧编辑窗口编写查询 SQL 语句即可，其余平台会自动完成。

注意：当右侧结果窗口出现如下错误时，再次点击测评即可。*/

select 50005000 - sum(a1) as a from (select distinct test1.a1 from test1
union  select distinct test1.a2 from test1
union  select distinct test1.a3 from test1
union  select distinct test1.a4 from test1
union  select distinct test1.a5 from test1
union  select distinct test1.a6 from test1
union  select distinct test1.a7 from test1
union  select distinct test1.a8 from test1) a;

