import os
import time
import hashlib
from conf.setting import TIME_DELAY


class FileMixIn:
    """
    自定义文件处理功能
    方法：获取文件头、获取文件大小、下载文件、上传文件
    """

    def get_header(self, file_flag, file, file_name):
        """
        根据文件信息创建文件头
        :param file_flag: 断点续传标志位
        :param file: 文件绝对路径
        :param file_name: 文件名
        :return: 文件头header
        """
        header = [
            file_name,
            os.path.getsize(file),
            file_flag,
            self.get_md5(file),
        ]
        return header

    @staticmethod
    def get_file_size(file_path):
        """
        获取文件夹内所有文件总大小
        :param file_path: 文件夹绝对路径
        :return: 文件夹总大小
        """
        size = 0
        for root, dirs, files in os.walk(file_path):
            for f in files:
                size += os.path.getsize(os.path.join(root, f))
        return size

    @staticmethod
    def print_bar(size_per, file_size):
        """
        打印进度条
        :param size_per: 文件已上传/下载的大小
        :param file_size: 文件总大小
        :return:
        """
        per = int(size_per / file_size * 50)
        per_ = '█' * per
        print('\r[%-50s]%s%%' % (per_, per * 2), end='')

    def get_file(self, conn, file, file_size, file_flag, file_md5):
        """
        下载文件，并对下载后的文件进行md5校验
        :param conn: socket对象
        :param file: 文件下载到本地的绝对路径
        :param file_size: 文件大小
        :param file_flag: 断点续传标志位
        :param file_md5: 文件md5值
        :return:
        """
        size_per = file_flag
        with open(file, 'ab') as f:
            if size_per == file_size:
                inp = 'n'
                print('\033[32m文件已经存在，且文件完整\033[0m')
            elif 0 < size_per < file_size:
                inp = input('\033[31m文件存在但不完整，是否断点续传(y/n):\033[0m')
            elif size_per == 0:
                inp = 'y'
            # 下载文件
            while size_per < file_size:
                res = conn.recv(2048)
                size_per += len(res)
                time.sleep(TIME_DELAY)
                if inp == 'y':
                    f.write(res)
                    # 打印进度条
                    self.print_bar(size_per, file_size)
        # 文件md5校验
        if inp == 'y':
            self.check_md5(file_md5, file)

    def put_file(self, conn, file, file_flag):
        """
        上传文件，并打印进度条
        :param conn: socket对象
        :param file: 上传文件所在的本地绝对路径
        :param file_flag: 断点续传标志位
        :return:
        """
        file_size = os.path.getsize(file)
        size_per = file_flag
        # 上传文件
        with open(file, 'rb')as f:
            f.seek(file_flag)
            while True:
                msg = f.read(2048)
                if not msg:
                    break
                time.sleep(TIME_DELAY)
                conn.send(msg)
                size_per += len(msg)
                # 打印进度条
                self.print_bar(size_per, file_size)
        print('\033[32m发送文件成功\033[0m')


class Md5MixIn:
    """
    自定义md5功能
    方法：获取文件md5值、校验文件md5值
    """

    @staticmethod
    def get_md5(file):
        """
        获取文件md5值
        :param file: 文件绝对路径
        :return: 文件md5值
        """
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                msg = f.read(2048)
                if not msg:
                    break
                md5.update(msg)
        return md5.hexdigest()

    @staticmethod
    def check_md5(file_md5, file):
        """
        校验文件md5值
        :param file_md5: 文件md5值
        :param file: 文件绝对路径
        :return:
        """
        md5 = hashlib.md5()
        with open(file, 'rb') as f:
            while True:
                msg = f.read(2048)
                if not msg:
                    break
                md5.update(msg)
        if md5.hexdigest() == file_md5:
            print('\033[32m(md5校验正确)\033[0m')
        else:
            print('\033[31m(md5校验文件无效)\033[0m')
