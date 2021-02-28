# coding: utf-8
from socket import *
import struct
import os
import sys
import subprocess
from threading import Thread
from queue import Queue

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import setting
from core.tools import FileMixIn, Md5MixIn


class TCPSever(FileMixIn, Md5MixIn):
    """
    服务器类 ==混入==> 文件处理功能、md5功能
    字段：服务器socket对象、服务器地址
    方法：服务器运行函数
    """

    def __init__(self, ip_addr):
        """
        构造函数
        :param ip_addr: 服务器地址
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.ip_addr = ip_addr

    def run(self):
        """
        服务器运行主函数
        :return:
        """
        self.socket.bind(self.ip_addr)
        self.socket.listen(setting.LISTEN_MAX)
        print('服务器已启动')
        # 使用队列queue模块，实现线程池
        q = Queue(setting.POOL_MAX)
        while True:
            conn, addr = self.socket.accept()
            print(f'\033[32m已连接{addr}\033[0m')
            t = Thread(target=self.sever_cmd, args=(conn, addr, q))
            # 线程开始前，队列内新增一个标志，队列满则阻塞
            q.put(1)
            t.start()

    def sever_cmd(self, conn, addr, q):
        """
        指令处理函数
        :param conn: 套接字对象
        :param addr: 连接地址
        :param q: Queue队列
        :return:
        """
        flag = 1
        path_current = None
        while True:
            try:
                # 1、接收指令数据 <-- 客户端
                res = conn.recv(1024).decode('utf8')
                usr_id, usr_size, cmd, *_ = res.strip().split()
                print('客户端指令：', res)
                # linux客户端断开连接，跳出循环
                if not res:
                    break
                # 用户家目录
                path_root = os.path.join(setting.CLIENT_PATH, usr_id)
                # 用户当前目录，初始化为家目录
                if flag:
                    path_current = path_root
                    flag = 0

                # 下载指令，从服务器下载文件到本地
                if cmd == 'get':
                    # 文件名、断点续传标识位、文件绝对路径
                    *_, file_name, file_flag = res.strip().split()
                    file = os.path.join(path_current, file_name)
                    # 创建帧头
                    header = self.get_header(int(file_flag), file, file_name)
                    # 2、发送帧头长度 --> 客户端
                    len_head = struct.pack('i', len(str(header)))
                    conn.send(len_head)
                    # 3、发送帧头 --> 客户端
                    conn.send(str(header).encode('utf-8'))
                    # 4、开始发送文件 --> 客户端
                    self.put_file(conn, file, int(file_flag))

                # 上传指令，从本地上传文件到服务器
                elif cmd == 'put':
                    # 文件绝对路径、文件所在目录，文件名
                    *_, file = res.strip().split()
                    file_path, file_name = os.path.split(file)
                    # 断点续传标志位
                    file_flag = 0
                    if os.path.isfile(os.path.join(path_current, file_name)):
                        file_flag = os.path.getsize(os.path.join(path_current, file_name))
                    # 2、发送断点续传标志 --> 客户端
                    file_flag_len = struct.pack('i', file_flag)
                    conn.send(file_flag_len)
                    # 3、接收帧头长度 <-- 客户端
                    head = conn.recv(4)
                    len_head = struct.unpack('i', head)
                    # 4、接收帧头 <-- 客户端
                    header = eval(conn.recv(len_head[0]))
                    # 得到帧头数据信息
                    file_name, file_size, file_flag, file_md5 = header
                    # 存储路径
                    file = os.path.join(path_current, file_name)
                    # 5、开始接收文件 <-- 客户端
                    self.get_file(conn, file, file_size, file_flag, file_md5)

                # 遍历目录指令
                elif cmd == 'ls':
                    obj = subprocess.Popen(' '.join(['ls', path_current]), shell=True,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    path_show = path_current.replace(setting.CLIENT_PATH, '')
                    path_show = f'\033[32m当前目录{path_show}\033[0m\n'.encode('utf8')
                    stdout = obj.stdout.read()
                    stderr = obj.stderr.read()
                    conn.send(path_show + stdout + stderr)

                # 创建目录指令
                elif cmd == 'mkdir':
                    *_, dir_name = res.strip().split()
                    os.mkdir(os.path.join(path_current, dir_name))
                    conn.send(f'\033[32m创建目录{dir_name}成功\033[0m'.encode('utf8'))

                # 删除文件指令
                elif cmd == 'remove':
                    *_, file_name = res.strip().split()
                    file_rm = os.path.join(path_current, file_name)
                    if os.path.isfile(file_rm):
                        os.remove(os.path.join(path_current, file_name))
                        conn.send(f'\033[32m删除文件{file_name}成功\033[0m'.encode('utf8'))
                    else:
                        conn.send(f'\033[31m文件{file_name}不存在\033[0m'.encode('utf8'))

                #  删除目录指令
                elif cmd == 'rmdir':
                    *_, dir_name = res.strip().split()
                    path_rm = os.path.join(path_current, dir_name)
                    if os.path.isdir(path_rm):
                        try:
                            os.rmdir(path_rm)
                            conn.send(f'\033[32m删除目录{dir_name}成功\033[0m'.encode('utf8'))
                        except OSError as e:
                            conn.send(f'\033[31m只允许删除单层目录\033[0m'.encode('utf8'))
                    else:
                        conn.send(f'\033[31m目录{dir_name}不存在\033[0m'.encode('utf8'))

                # 切换目录指令
                elif cmd == 'cd':
                    *_, dir_name = res.strip().split()
                    if dir_name == '/':
                        path_current = path_root
                        conn.send(f'\033[32m进入根目录成功\033[0m'.encode('utf8'))
                    elif dir_name.startswith('..'):
                        if path_current == path_root:
                            conn.send(f'\033[31m已经是根目录\033[0m'.encode('utf8'))
                        else:
                            path_current, *_ = os.path.split(path_current)
                            conn.send(f'\033[32m返回上级目录成功\033[0m'.encode('utf8'))
                    elif os.path.isdir(os.path.join(path_current, dir_name)):
                        path_current = os.path.join(path_current, dir_name)
                        conn.send(f'\033[32m进入目录{dir_name}成功\033[0m'.encode('utf8'))
                    else:
                        conn.send(f'\033[31m目录{dir_name}不存在\033[0m'.encode('utf8'))

            # windows客户端断开连接，跳出循环
            except Exception:
                break
        conn.close()
        print(f'\033[31m已断开{addr}\033[0m')
        # 线程结束后，从队列取出一个标志
        q.get()


if __name__ == '__main__':
    sever = TCPSever(setting.IP_ADDR)
    sever.run()
