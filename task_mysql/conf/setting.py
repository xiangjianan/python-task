# 数据库连接配置
HOST = '0.0.0.0'  # 本机IP
PORT = 3306
USER = '******'  # mysql数据库账号
PWD = '******'  # mysql数据库密码
DB = 'db_school'  # 数据库名称
CHAR_SET = 'utf8'

# MySQL指令
CMD_DICT = {
    '1、自行创建测试数据':
        'show tables',
    '2、查看学生总人数':
        'select count(sid) from student',
    '3、查询“生物”课程和“物理”课程成绩都及格的学生id和姓名':
        '''
        select sid,sname from student where sid in 
            (
                select student_id from score
                where score >= 60 and  # 过滤掉不及格的记录、非生物和物理的记录
                    (
                        course_id = (select cid from course where cname="生物") or
                        course_id = (select cid from course where cname="物理")
                    )
                group by student_id  # 以学生id分组，如果学生的课程数为2，即两门课程都及格
                having count(course_id) = 2
            )
        ''',
    '4.1、查询每个年级的班级数':
        '''
        select gname,count(cid) from class_grade 
        left join class  # 连表：年级 + 班级
        on class_grade.gid = class.grade_id
        group by gname
        ''',
    '4.2、取出班级数最多的前三个年级':
        '''
        select gname,count(cid) from class_grade 
        left join class  # 连表：年级 + 班级
        on class_grade.gid = class.grade_id
        group by gname
        order by count(cid) desc
        limit 3
        ''',
    '5.1、查询平均成绩最高的学生的id和姓名以及平均成绩':
        '''
        select s1.sid,s1.sname,s2.avg_score from student as s1 
        inner join  # 连表：学生 + 成绩
            (
                select student_id,avg(score) as avg_score from score 
                group by student_id
            ) as s2 
        on s1.sid = s2.student_id
        order by avg_score desc 
        limit 1
        ''',
    '5.2、查询平均成绩最低的学生的id和姓名以及平均成绩':
        '''
        select s1.sid,s1.sname,s2.avg_score from student as s1 
        inner join  # 连表：学生 + 成绩
            (
                select student_id,avg(score) as avg_score from score 
                where score is not NULL
                group by student_id
            ) as s2 
        on s1.sid = s2.student_id
        order by avg_score 
        limit 1
        ''',
    '6、查询每个年级的学生人数':
        '''
        select gname,count(cid) from class_grade as t1
        left join  # 连表：年级 + 班级 + 学生
            (
                select * from class  # 连表：班级 + 学生
                right join student
                on class.cid = student.class_id
            ) as t2
        on t1.gid = t2.grade_id 
        group by gname
        ''',
    '7、查询每位学生的学号，姓名，选课数，平均成绩':
        '''
        select student.sid,sname,count(course_id),avg(score) from student 
        left join score # 连表：学生 + 成绩
        on student.sid = score.student_id
        where score is not NULL
        group by student.sid
        ''',
    '8.1、查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名及分数':
        '''
        select sname,cname,score from 
            (
                select student.sid,sname,course_id,score from student
                inner join score  # 连表：学生 + 成绩
                on student.sid = score.student_id
            ) as t1
        inner join course as t2  # 连表：学生 + 成绩 + 课程
        on t1.course_id = t2.cid 
        where sid = 2
        order by score desc 
        limit 1
        ''',
    '8.2、查询学生编号为“2”的学生的姓名、该学生成绩最低的课程名及分数':
        '''
        select sname,cname,score from 
            (
                select student.sid,sname,course_id,score from student
                inner join score  # 连表：学生 + 成绩
                on student.sid = score.student_id
            ) as t1
        inner join course as t2  # 连表：学生 + 成绩 + 课程
        on t1.course_id = t2.cid 
        where sid = 2 and score is not NULL
        order by score 
        limit 1
        ''',
    '9、查询姓“李”的老师的个数和所带班级数':
        '''
        select count(t1.tid),count(cid) from teacher as t1 
        inner join teach2cls as t2  # 连表：老师 + 班级任职表
        on t1.tid = t2.tid 
        where tname like "李%"
        ''',
    '10、查询班级数小于5的年级id和年级名':
        '''
        select gid,gname from class
        inner join class_grade  # 连表：班级 + 年级
        on class.grade_id = class_grade.gid 
        group by gid
        having count(cid) < 5
        ''',
    '11、查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)':
        '''
        select cid,caption,gname,
            (  # 新增字段，根据gid大小选择年级级别
                case when gid between 1 and 2 then '低年级' 
                when gid between 3 and 4 then '中年级' 
                when gid between 5 and 6 then '高年级' else NULL end
            ) as 年级级别
        from class inner join class_grade  # 连表：班级 + 年级
        on class.grade_id = class_grade.gid
        group by cid
        ''',
    '12、查询学过“张三”老师2门课以上的同学的学号、姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from 
                    (
                        select * from teacher 
                        inner join course  # 连表：老师 + 课程
                        on teacher.tid = course.teacher_id
                    ) as t1
                inner join score  # 连表：老师 + 课程 + 成绩
                on t1.cid = score.course_id 
                where tname = "张三" 
                group by student_id 
                having count(tname) > 2
            )
        ''',
    '13、查询教授课程超过2门的老师的id和姓名':
        '''
        select tid,tname from teacher where tid in
            (
                select teacher_id from course 
                group by teacher_id 
                having count(cid) > 2
            )
        ''',
    '14、查询学过编号“1”课程和编号“2”课程的同学的学号、姓名':
        '''
        select sid,sname from student 
        where sid in 
            (
                select student_id from score where 
                    student_id in (select student_id from score where course_id = 1) and
                    student_id in (select student_id from score where course_id = 2)
            )
        ''',
    '15、查询没有带过高年级的老师id和姓名':
        '''
        select * from teacher where tid not in
            (
                select tid from teach2cls left join class  # 连表：班级任职表 + 班级
                on teach2cls.cid = class.cid
                where grade_id between 5 and 6
            )
        ''',
    '16、查询学过“张三”老师所教的所有课的同学的学号、姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from 
                    (
                        select * from teacher 
                        inner join course   # 连表：老师 + 课程
                        on teacher.tid = course.teacher_id
                    ) as t1
                inner join score  # 连表：老师 + 课程 + 成绩
                on t1.cid = score.course_id 
                where tname = "张三" 
                group by student_id 
                having count(tname) = 
                    (  # 张三老师所教课程总数
                        select count(cid) from course 
                        where teacher_id = 
                            (
                                select tid from teacher
                                where tname = "张三"
                            )
                    )
            )
        ''',
    '17、查询带过超过2个班级的老师的id和姓名':
        '''
        select tid,tname from teacher where tid in
            (
                select tid from teach2cls 
                group by tid
                having count(cid) > 2
            )
        ''',
    '18、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名':
        '''
        select sid,sname from student where sid in
            (
                select score_1.student_id from 
                    (  # 课程1成绩表
                        select student_id,score as s1 from score
                        where course_id = 1
                    )as score_1 
                inner join  # 连表：课程1成绩表 + 课程2成绩表
                    (  # 课程2成绩表
                        select student_id,score as s2 from score
                        where course_id = 2
                    )as score_2
                on score_1.student_id = score_2.student_id
                where s2 < s1  # 筛选：课程2成绩 < 课程1成绩
            )
        ''',
    '19、查询所带班级数最多的老师id和姓名':
        '''
        select tid,tname from teacher where tid in
            (
                select tid from teach2cls
                group by tid
                order by count(cid) desc
            )
        limit 1
        ''',
    '20、查询有课程成绩小于60分的同学的学号、姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score
                where score is not NULL
                group by student_id 
                having min(score) < 60  # 按学生分组后，最低成绩<60分，即符合条件
            )
        ''',
    '21、查询没有学全所有课的同学的学号、姓名':
        '''
        select sid,sname from student where sid in
            (
                select sid from score
                group by sid 
                having count(course_id) <
                    (
                        select count(cid) from course
                    )
            )''',
    '22、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score where course_id in
                    (  # 学号1同学的所有课程
                        select course_id from score where student_id = 1
                    )
                group by student_id
            )
        ''',
    '23、查询至少学过学号为“1”同学所选课程中任意一门课的其他同学学号和姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score where course_id in
                    (  # 1号同学的所有课程
                        select course_id from score where student_id = 1
                    )
                group by student_id
            )
        and sid != 1  # 不包括1号同学自己
        ''',
    '24、查询和“2”号同学学习的课程完全相同的其他同学的学号和姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score where course_id in
                    (  # 2号同学的所有课程
                        select course_id from score where student_id = 2
                    )
                group by student_id
                having count(course_id) = 
                    (  # 2号同学课程总数
                        select count(course_id) from score where student_id = 2
                        group by student_id
                    )
            )
        and sid != 2
        ''',
    '25、删除学习“张三”老师课的score表记录':
        '''
        delete from score where course_id in
            (
                select cid from course where teacher_id = 
                    (
                        select tid from teacher where tname = "张三"
                    )
            )
        ''',
    '26.1、向score表中插入一些记录，这些记录要求符合以下条件:1没有上过编号“2”课程的同学学号':
        '''
        insert into score(student_id,course_id,score) 
            select sid,2,80 from student 
            where sid not in  # 没有上过编号“2”课程的同学学号
                (
                    select student_id from score where course_id = 2
                )
        ''',
    '26.2、插入“2”号课 程的平均成绩':
        '''
        update score set 课程2平均成绩 = 
            (  # 通过中间表select进行赋值，否则会报错
                select avg_score from
                    (  # 得到课程2平均分
                        select avg(score) as avg_score from score
                        where course_id = 2 and score is not NULL
                        group by course_id
                    ) avg
            )
        where course_id = 2
        ''',
    '27、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示: 学生ID,语文, 数学,英语,课程数和平均分':
        '''
        select student_id as 学生ID,
            # 新增字段 语文，内容为当前学生的语文成绩
            (select score from score where student_id = 学生ID and course_id= 
                (select cid from course where cname = '语文')) as 语文,
            # 新增字段 数学，内容为当前学生的数学成绩
            (select score from score where student_id = 学生ID and course_id= 
                (select cid from course where cname = '数学')) as 数学,
            # 新增字段 英语，内容为当前学生的英语成绩
            (select score from score where student_id = 学生ID and course_id= 
                (select cid from course where cname = '英语')) as 英语,
            count(course_id) as 课程数,avg(score) as 平均分
        from score 
        group by student_id
        order by avg(score)
    ''',
    '28、查询各科成绩最高和最低的分:以如下形式显示:课程ID，最高分，最低分':
        '''
        select course_id as 课程ID,max(score) as 最高分,min(score) as 最低分 from score 
        where score is not NULL
        group by course_id
        ''',
    '29.1、按各科平均成绩从低到高':
        '''
        select cname,avg(score) from course left join score
        on course.cid = score.course_id
        where score is not NULL
        group by cname
        order by avg(score)
        ''',
    '29.2、及格率的百分数从高到低顺序':
        '''
        select t1.course_id,jige/zong from
            (  # 课程及格成绩
                select course_id,count(score) as jige from score where score > 60
                group by course_id
            )as t1
        inner join
            (  # 课程所有成绩
                select course_id,count(score) as zong from score
                group by course_id
            )as t2
        on t1.course_id = t2.course_id
        order by jige/zong desc
        ''',
    '30、课程平均分从高到低显示(显示任课老师)':
        '''
        select cname,avg(score),tname from teacher 
        inner join  # 连表：成绩 + 课程 + 老师
            (
                select course_id,cname,teacher_id,score from score
                inner join course  # 连表：成绩 + 课程
                on score.course_id = course.cid
                where score is not NULL
            ) as t1
        on teacher.tid = t1.teacher_id
        group by course_id
        order by avg(score) desc
        ''',
    '31、查询各科成绩前三名的记录(不考虑成绩并列情况)':
        '''
        select * from score s1 where exists
            (  # 对成绩表筛选：过滤掉成绩不是前三的记录
                select NULL from score 
                where score >= s1.score and course_id = s1.course_id  # 筛选出所有比s1.score大的成绩
                group by course_id  
                having count(score) <= 3 or avg(score) = s1.score  # 筛选出的成绩个数不大于3，即该成绩为前三；或特殊情况，前n名同学成绩相同
            )  
        order by course_id,score desc
        ''',
    '32、查询每门课程被选修的学生数':
        '''
        select cname,count(student_id) from course left join score
        on course.cid = score.course_id
        group by cname
        ''',
    '33、查询选修了2门以上课程的全部学生的学号和姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score
                group by student_id 
                having count(course_id) > 2
            )
        ''',
    '34、查询男生、女生的人数，按倒序排列':
        '''
        select gender,count(sid) from student
        group by gender
        order by count(sid) desc
        ''',
    '35、查询姓“张”的学生名单':
        '''
        select * from student
        where sname like "张%"
        ''',
    '36、查询同名同姓学生名单，并统计同名人数':
        '''
        select sname,count(sname) from student
        group by sname
        having count(sname) > 1
        ''',
    '37、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列':
        '''
        select cid,avg(score) from
            (
                select * from course 
                left join score  # 连表：课程 + 成绩
                on course.cid = score.course_id
                where score is not NULL 
            )as t1
        group by cid
        order by avg(score),cid desc
        ''',
    '38、查询课程名称为“数学”，且分数低于60的学生姓名和分数':
        '''
        select sid,sname from student where sid in
            (   
                select student_id from course 
                inner join score  # 连表：课程 + 成绩
                on course.cid = score.course_id
                where cname = "数学" and score < 60
            )
        ''',
    '39、查询课程编号为“3”且课程成绩在80分以上的学生的学号和姓名':
        '''
        select sid,sname from student where sid in
            (
                select student_id from score where 
                course_id = 3 and score > 80
            )
        ''',
    '40、求选修了课程的学生人数':
        '''
        select count(student_id) from
            (
                select student_id from score
                group by student_id
            )as t1
        ''',
    '41.1、查询选修“王五”老师所授课程的学生中，成绩最高的学生姓名及其成绩':
        '''
        select sname,score from student inner join
            (
                select student_id,score from course 
                inner join score  # 连表：课程 + 成绩
                on course.cid = score.course_id
                where teacher_id = 
                    (
                        select tid from teacher where tname = "王五"
                    )
            )as t1
        on student.sid = t1.student_id
        order by score desc
        limit 1
        ''',
    '41.2、查询选修“王五”老师所授课程的学生中，成绩最低的学生姓名及其成绩':
        '''
        select sname,score from student inner join
            (
                select student_id,score from course 
                inner join score  # 连表：课程 + 成绩
                on course.cid = score.course_id
                where teacher_id = 
                    (
                        select tid from teacher where tname = "王五"
                    )
            )as t1
        on student.sid = t1.student_id
        order by score 
        limit 1
        ''',
    '42、查询各个课程及相应的选修人数':
        '''
        select cname,count(student_id) from course 
        left join score  # 连表：课程 + 成绩
        on course.cid = score.course_id
        group by cname
        ''',
    '43、查询不同课程但成绩相同的学生的学号、课程号、学生成绩':
        '''
        select student.sid,course_id,score from student 
        inner join  # 连表：学生 + 成绩
            (
                select * from score s1 where exists
                    (  # 找到成绩相同且学号相同的记录
                        select student_id from score
                        where score = s1.score and student_id = s1.student_id
                        group by student_id
                        having count(score) > 1  # 如果相同成绩数>1，即符合条件
                    )
                order by course_id
            )as s2
        on student.sid = s2.student_id
        ''',
    '44、查询每门课程成绩最好的前两名学生id和姓名':
        '''
        select course_id,student.sid,student.sname,score from student 
        inner join  # 连表：学生 + 成绩
            (  
                select * from score s1 where exists
                    (  # 对成绩表筛选：过滤掉成绩不是前二的记录
                        select NULL from score 
                        where score >= s1.score and course_id = s1.course_id  # 筛选出所有比s1.score大的成绩
                        group by course_id  
                        having count(score) <= 2 or avg(score) = s1.score  # 筛选出的成绩个数不大于2，即该成绩为前二；或特殊情况，前n名同学成绩相同
                    )  
            ) as s2
        on student.sid = s2.student_id
        order by course_id,score desc
        ''',
    '45、检索至少选修两门课程的学生学号':
        '''
        select student_id from score 
        group by student_id
        having count(sid) > 2
        ''',
    '46、查询没有学生选修的课程的课程号和课程名':
        '''
        select cid,cname from course 
        left join score  # 连表：课程 + 成绩
        on course.cid = score.course_id
        group by cid
        having count(sid) = 0
        ''',
    '47、查询没带过任何班级的老师id和姓名':
        '''
        select teacher.tid,teacher.tname from teacher 
        left join teach2cls  # 连表：老师 + 班级任职表
        on teacher.tid = teach2cls.tid
        group by teacher.tid
        having count(cid) = 0
        ''',
    '48、查询有两门以上课程超过80分的学生id及其平均成绩':
        '''
        select sid,avg_score from student 
        inner join  # 连表：学生 + 成绩
            (
                select student_id,avg(score) as avg_score from score 
                where score > 80
                group by student_id
                having count(score) > 2
            ) as t1
        on student.sid = t1.student_id
        ''',
    '49、检索“3”课程分数小于60，按分数降序排列的同学学号':
        '''
        select student_id from score
        where course_id = 3 and score < 60
        order by score desc
        ''',
    '50、删除编号为“2”的同学的“1”课程的成绩':
        '''
        delete from score where student_id = 2 and course_id = 1
        ''',
    '51、查询同时选修了物理课和生物课的学生id和姓名':
        '''
        select sid,sname from student where sid in 
            (
                select student_id from score
                where   # 过滤掉非生物和物理的记录
                    (
                        course_id = (select cid from course where cname="生物") or
                        course_id = (select cid from course where cname="物理")
                    )
                group by student_id  # 以学生id分组，如果学生的课程数为2，即两名课程同时选修
                having count(course_id) = 2
            )
        ''',
}
