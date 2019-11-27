/*任务描述
统计每个学生合格科目数量与不合格科目数量并按学生姓名排序（升序），取统计结果中第100000条到100010条数据。

最后展示的列及其列名为：学生姓名（studentName）、合格科目数量（qualifiedQuantity）、不合格科目数量（unqualifiedQuantity）

注意：科目成绩大于等于科目平均分判为合格 ，反之为不合格。

数据说明
course 课程表

字段名	类型	描述
course_id	int	主键
course_name	varchar	课程名称
student 学生表

字段名	类型	描述
student_id	int	主键
student_name	varchar	学生姓名
studentcourse  学生成绩表

字段名	类型	描述
studentcourse_id	int	主键
student_id	int	学生id
course_id	int	课程id
score	int	分数
测试说明
在右侧编辑器中完成 SQL 编写后点击评测，平台将运行你的 SQL 代码进行查询，且每次评测都会恢复为源初始数据。

注意：本关评测限时16s，若出现超时请对自己的sql进行优化。

所罗门王：一句责备话入聪明人心，强如责打愚昧人一百下，败坏之先，人心骄傲，尊荣之前，必有谦卑。
*/

set @a := 75.5027,
@b := 75.5280,
@c := 75.5886,
@d := 75.6015,
@e := 75.5269,
@f := 75.5183,
@g := 75.4652,
@h := 75.3546,
@i := 75.4426,
@j := 75.4448;

select student_name as studentName, temp3.kk as qualifiedQuantity, temp3.rr as unqualifiedQuantity from student join(
select student_id, sum(temp1.x) as kk, (10-sum(temp1.x)) rr from (
    select student_id, if(
        (course_id = 1 and score > @a) or
        (course_id = 2 and score > @b) or
        (course_id = 3 and score > @c) or
        (course_id = 4 and score > @d) or
        (course_id = 5 and score > @e) or
        (course_id = 6 and score > @f) or
        (course_id = 7 and score > @g) or
        (course_id = 8 and score > @h) or
        (course_id = 9 and score > @i) or
        (course_id = 10 and score > @j), 1, 0) as x from studentcourse) temp1 group by
        student_id) temp3 on student.student_id = temp3.student_id order by student_name
        limit 100000, 10;