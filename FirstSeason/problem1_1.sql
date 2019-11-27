/* 本关任务：某店铺网站的数据库系统中现有四张表记录着用户信息及其消费情况，由于运维人员的疏忽，会员表中部分数据丢失了，现在请你将丢失的数据进行恢复。

会员表中数据统计注意点：

丢失数据可能是整条记录或只丢失积分

现会员表中还存有部分数据，但积分可能不准确

会员积分只对会员消费有效（消费1元为1个积分）

会员积分 = 所有消费记录 - 退货记录

只要为本店会员则在会员表中都会有记录，若无消费积分为0

会员表的数据顺序按card_id升序显示

表结构说明
用户表user：

字段名	类型	说明	约束
name	varchar	用户名	主键
age	int	年龄	非空
sex	varchar	性别	非空
ismember	int	是否为会员（0表示不是，1表示是）	默认为0
card_id	int	卡号	非空
会员表member：

字段名	类型	说明	约束
card_id	int	卡号	主键
creadits	int	积分	非空
销售表sales：

字段名	类型	说明	约束
name	varchar	用户名	非空
expense_money	int	消费金额	非空
退货表back：

字段名	类型	说明	约束
card_id	int	卡号	主键
return_money	int	退款金额	非空
测试说明
请在右侧编辑器中编写 SQL ，完成任务后平台将会查询你更新后的会员表数据进行评测。*/

TRUNCATE TABLE member;

CREATE TABLE temp1 AS SELECT name as card_id, SUM(expense_money) as sum_expense_money  FROM sales GROUP BY name;

INSERT INTO member (card_id,creadits) SELECT user.card_id, IFNULL((sum_expense_money  - IFNULL(return_money,0)), 0) as creadits FROM user LEFT OUTER JOIN back ON (user.card_id = back.card_id) LEFT OUTER JOIN temp1 ON (user.name = temp1.card_id) WHERE user.ismember = 1;

DROP TABLE temp1;