from core import main
import hashlib


def login():
    """
    学生登录认证
    :return: 学生对象
    """
    while True:
        name = input("输入管理员账号：")
        pwd = input("输入管理员密码：")
        pwd_sha1 = hashlib.sha1()
        pwd_sha1.update(pwd.encode("utf-8"))
        if name == 'admin' and pwd_sha1.hexdigest() == 'd033e22ae348aeb5660fc2140aec35850c4da997':
            print(f'\033[32m登录成功\033[0m')
            break


def run():
    """
    管理员操作界面
    :return:
    """
    login()
    inp_dict = {
        '1': ['创建学校', 'create_school'],
        '2': ['创建班级', 'create_class'],
        '3': ['创建老师', 'create_teacher'],
        '4': ['创建课程', 'create_lesson'],
    }
    while True:
        inp = main.get_cmd(inp_dict)
        if inp.lower() == 'q':
            break
        if inp in inp_dict:
            obj = getattr(main.School, inp_dict[inp][1], None)()
            obj.save()


if __name__ == '__main__':
    run()
