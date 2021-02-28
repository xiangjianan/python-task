import pickle
import os
import time
from conf.setting import DATA_DIR
from core import admin
from core import student
from core import teacher


class DataBase:
    """
    数据库类
    方法：pickle序列化、pickle反序列化、字符串方法
    """
    dir_name = None
    name = None

    def save(self):
        """
        pickle序列化，将对象self保存到本地数据库
        :return:
        """
        with open(DATA_DIR[self.dir_name] + self.name, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def get_obj(cls, name):
        """
        pickle反序列化，从本地数据库加载数据
        :param name: 文件名
        :return: cls类的实例对象
        """
        try:
            with open(DATA_DIR[cls.dir_name] + name, 'rb')as f:
                return pickle.load(f)
        except FileNotFoundError as e:
            exit('404')

    def __str__(self):
        """
        字符串方法
        :return: self对象的name属性
        """
        return self.name


class School(DataBase):
    """
    学校类 --> 继承数据库类
    字段：学校名
    方法：创建学校、创建班级、创建课程、创建老师
    """
    dir_name = 'school'

    def __init__(self, name):
        self.name = name

    @classmethod
    def create_school(cls):
        """
        创建学校
        :return: School的实例对象
        """
        name = input('输入学校名：')
        print(f'\033[32m成功创建校区：{name}\033[0m')
        return cls(name)

    @classmethod
    def create_class(cls):
        """
        创建班级
        :return: ClassTeam的实例对象
        """
        name = input('输入班级名称：')
        school = input('关联学校：')
        print(f'\033[32m成功创建班级：{name}\033[0m')
        return ClassTeam(name, school)

    @classmethod
    def create_lesson(cls):
        """
        创建课程
        :return: Lesson的实例对象
        """
        name = input('输入课程名称：')
        period = input('输入课程周期：')
        price = input('输入课程价格：')
        print(f'\033[32m成功创建课程：{name}\033[0m')
        return Lesson(name, period, price)

    @classmethod
    def create_teacher(cls):
        """
        创建老师
        :return: Teacher的实例对象
        """
        name = input('输入姓名：')
        school = input('关联学校：')
        class_team = input('关联班级：')
        pwd = input('创建密码：')
        obj_teacher = Teacher(name, school, pwd)
        # 老师关联班级
        obj_teacher.class_team = class_team
        # 班级关联老师
        obj_class = ClassTeam.get_obj(class_team)
        if not hasattr(obj_class, 'teacher_list'):
            obj_class.teacher_list = []
        obj_class.teacher_list.append(name)
        obj_class.save()
        print(f'\033[32m成功创建老师：{name}\033[0m')
        return obj_teacher


class ClassTeam(DataBase):
    """
    班级类 --> 继承数据库类
    字段：班级名、关联的学校
    方法：展示所有班级
    """
    dir_name = 'class'

    def __init__(self, name, school):
        self.name = name
        self.school = school

    @classmethod
    def show_class(cls):
        """
        展示所有班级
        :return:
        """
        os.system(f'ls {DATA_DIR["class"]}')


class Lesson(DataBase):
    """
    课程类 --> 继承数据库类
    字段：课程名、课程周期、课程价格
    方法：None
    """
    dir_name = 'lesson'

    def __init__(self, name, period, price):
        self.name = name
        self.period = int(period)
        self.price = int(price)


class Teacher(DataBase):
    """
    老师类 --> 继承数据库类
    字段：姓名、所属学校、密码
    方法：上课、显示学生列表、管理成绩、检查密码
    """
    __salary = 0
    __password = None
    dir_name = 'teacher'

    def __init__(self, name, school, pwd):
        self.name = name
        self.school = school
        self.__password = pwd

    def class_begin(self):
        """
        上课，计算课时，并增加老师收入
        :return:
        """
        self.__salary += 100
        lesson_name = input('选择课程：')
        obj_lesson = Lesson.get_obj(lesson_name)
        obj_lesson.period -= 1
        print(f'\033[32m{self.name}老师开始教{obj_lesson}课程...\033[0m')
        time.sleep(1)
        print(f'\033[32m上课结束\n{self.name}老师工资加100元，当前工资{self.__salary}元\n'
              f'{obj_lesson}课程剩余课时：{obj_lesson.period}课时\033[0m')
        time.sleep(1)
        self.save()
        obj_lesson.save()

    def show_students(self):
        """
        展示班级所有学生
        :return: bool
        """
        ClassTeam.show_class()
        class_team = input('选择班级：')
        obj_class = ClassTeam.get_obj(class_team)
        # 判断当前老师是否有权限查看班级
        if self.name in getattr(obj_class, 'teacher_list', None):
            if hasattr(obj_class, 'student_list'):
                for i in obj_class.student_list:
                    obj_stu = Student.get_obj(i)
                    print(f'\033[32m姓名：{i}，成绩：{obj_stu.score}\033[0m')
                    return True
            else:
                print(f'\033[31m当前班级暂无学生\033[0m')
                return False
        else:
            print(f'\033[31m只能查看自己班级的学生\033[0m')
            return False

    def change_score(self):
        """
        管理学生成绩
        :return:
        """
        if self.show_students():
            name = input('输入学生姓名：')
            obj_student = Student.get_obj(name)
            obj_student.score = input('输入分数：')
            print(f'\033[32m打分成功\n学生：{obj_student}\n分数：{obj_student.score}\033[0m')
            obj_student.save()

    def check_pwd(self, pwd):
        """
        检查密码
        :param pwd: 用户输入的密码
        :return: bool
        """
        if pwd == self.__password:
            return True


class Student(DataBase):
    """
    学生类 --> 继承数据库类
    字段：姓名、所属学校、密码
    方法：报名课程、显示成绩、保存数据、加载数据、检查密码
    """
    score = 0
    __password = None
    class_team = None
    dir_name = 'student'

    def __init__(self, name, school, pwd):
        self.name = name
        self.school = school
        self.__password = pwd

    @classmethod
    def create_student(cls):
        """
        注册学生账号
        :return: Student的实例对象
        """
        name = input('输入姓名：')
        school = input('输入学校名：')
        pwd = input('输入密码：')
        obj_stu = Student(name, school, pwd)
        print(f'\033[32m注册成功\033[0m')
        return obj_stu

    def show_score(self):
        """
        查看成绩
        :return:
        """
        print(f'\033[32m所在班级：{self.class_team}\n当前分数：{self.score}分\033[0m')

    def buy_lesson(self):
        """
        购买课程
        :return:
        """
        ClassTeam.show_class()
        class_team = input('选择班级：')
        # 学生关联班级
        self.class_team = class_team
        # 班级关联学生
        obj_class = ClassTeam.get_obj(class_team)
        if not hasattr(obj_class, 'student_list'):
            obj_class.student_list = []
        obj_class.student_list.append(self.name)
        obj_class.save()
        self.save()
        print(f'\033[32m报名成功，恭喜加入{class_team}\033[0m')

    def check_pwd(self, pwd):
        """
        检查密码
        :param pwd: 用户输入的密码
        :return: bool
        """
        if pwd == self.__password:
            return True


def get_cmd(inp_dict):
    """
    展示菜单，并接受用户输入
    :param inp_dict: 菜单字典
    :return: 用户输入值
    """
    print(''.center(50, '-'))
    for i in inp_dict:
        print(i, inp_dict[i][0])
    return input('>>>:')


def running():
    """
    主程序入口，提供管理员、老师和学生三个操作界面
    :return:
    """
    inp_dict = {
        '1': ['管理员界面', admin],
        '2': ['老师界面', teacher],
        '3': ['学生界面', student],
    }
    while True:
        inp = get_cmd(inp_dict)
        if inp.lower() == 'q':
            break
        if inp in inp_dict:
            inp_dict[inp][1].run()


if __name__ == '__main__':
    running()
