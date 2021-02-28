import pymysql

from conf import setting


class MySql:
    def __init__(self):
        """
        构造函数，建立数据库连接
        """
        self.conn = pymysql.connect(
            host=setting.HOST,
            port=setting.PORT,
            user=setting.USER,
            password=setting.PWD,
            db=setting.DB,
            charset=setting.CHAR_SET,
        )

    @staticmethod
    def show_answer(cmd, answer):
        """
        格式化打印
        :param cmd: mysql指令
        :param answer: 执行结果
        :return:
        """
        print(cmd)
        if answer:
            for i in answer:
                print('\t', i)
        else:
            print('\tNULL')

    def running(self):
        """
        运行函数
        :return:
        """
        # 获取游标
        cursor = self.conn.cursor()

        # 执行mysql语句
        for cmd in setting.CMD_DICT:
            cursor.execute(setting.CMD_DICT[cmd])
            answer = cursor.fetchall()
            self.show_answer(cmd, answer)
        self.conn.commit()

        # 关闭连接
        cursor.close()
        self.conn.close()


def run():
    """
    启动函数
    :return:
    """
    obj = MySql()
    obj.running()


if __name__ == '__main__':
    run()
