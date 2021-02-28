# coding: utf-8
from socket import *
import struct
import os
import sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import setting
from core.tools import FileMixIn, Md5MixIn


class ClientUsr(FileMixIn, Md5MixIn):
    """
    客户端类 ==混入==> 文件处理功能、md5功能
    字段：用户id、用户密码、用户空间大小、服务器地址
    方法：客户端启动、用户注册、用户登录、用户指令处理
    """

    def __init__(self, usr_id, usr_pwd, usr_size, ip_addr):
        """
        构造函数
        :param usr_id: 用户id
        :param usr_pwd: 用户密码
        :param usr_size: 用户存储空间大小
        :param ip_addr: 用户连接服务器的地址
        """
        self.id = usr_id
        self.pwd = usr_pwd
        self.ip_addr = ip_addr
        self.usr_size = usr_size

    @classmethod
    def client_run(cls):
        """
        客户端启动函数
        :return:
        """
        inp_dict = {
            '1、注册': 'create_usr',
            '2、登录': 'login',
            '3、退出': 'exit_client',
        }
        while True:
            obj = None
            # 打印客户端界面
            print(''.center(50, '-'))
            for key in inp_dict:
                print(key)
            # 处理用户输入指令
            inp = input('>>>:')
            for key in inp_dict:
                if inp in key:
                    obj = getattr(cls, inp_dict[key])()
            # 如果用户登录成功，则进入用户家目录，进行文件相关操作
            if obj:
                obj.client_cmd()

    @classmethod
    def create_usr(cls):
        """
        用户注册
        :return:
        """
        while True:
            usr_id = input('usr id:').strip()
            if os.path.isfile(os.path.join(setting.CLIENT_USR_PATH, usr_id)):
                print('\033[31m账号已被注册\033[0m')
                continue
            usr_pwd = input('password:').strip()
            usr_size = input('输入存储空间（MB）：')
            # 为用户创建家目录
            os.mkdir(os.path.join(setting.CLIENT_PATH, usr_id))
            # 将用户对象保存到本地
            cls(usr_id, usr_pwd, usr_size, setting.IP_ADDR).save()
            break

    @classmethod
    def login(cls):
        """
        用户登录
        :return: 用户对象
        """
        usr_id = input('usr id:').strip()
        usr_pwd = input('password:').strip()
        usr = cls.get_obj_by_id(usr_id)
        if usr_pwd == usr.pwd:
            print('\033[32m登录成功\033[0m')
            return cls(usr_id, usr_pwd, usr.usr_size, setting.IP_ADDR)
        else:
            print('\033[31m密码错误\033[0m')

    @staticmethod
    def get_obj_by_id(usr_id):
        """
        通过用户id获取用户对象
        :param usr_id: 用户id
        :return: 用户对象
        """
        file_path = os.path.join(setting.CLIENT_USR_PATH, usr_id)
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError as e:
            exit('账号不存在')

    def client_cmd(self):
        """
        用户指令处理函数
        指令包括：exit、get、put、ls、mkdir、rmdir、remove、cd
        :return:
        """
        cmd_list = [  # 非文件操作指令
            'ls',
            'mkdir',
            'rmdir',
            'remove',
            'cd'
        ]
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(self.ip_addr)
        while True:
            print(''.center(50, '-'))
            cmd = input('请输入指令:')
            if not cmd:
                continue
            # 退出客户端
            if cmd == 'exit':
                break

            # 下载指令，从服务器下载文件到本地
            elif cmd.startswith('get'):
                file_name = cmd.strip().split()[1]
                path_dl = input('输入文件保存路径：')
                # 断点续传标识位
                file_flag = 0
                if os.path.isfile(os.path.join(path_dl, file_name)):
                    file_flag = os.path.getsize(os.path.join(path_dl, file_name))
                # 1、发送get指令 --> 服务器
                client.send(' '.join([self.id, self.usr_size, cmd, str(file_flag)]).encode('utf-8'))
                # 2、接收帧头长度 <-- 服务器
                head = client.recv(4)
                len_head = struct.unpack('i', head)
                # 3、接收帧头 <-- 服务器
                header = eval(client.recv(len_head[0]))
                # 读取帧头数据信息
                file_name, file_size, file_flag, file_md5 = header
                # 文件下载到本地的绝对路径
                file = os.path.join(path_dl, file_name)
                # 4、开始接收文件 <-- 服务器
                self.get_file(client, file, file_size, file_flag, file_md5)

            # 上传指令，从本地上传文件到服务器
            elif cmd.startswith('put'):
                *_, file = cmd.strip().split()
                file_path, file_name = os.path.split(file)
                # 1、发送put指令 --> 服务器
                client.send(' '.join([self.id, self.usr_size, cmd]).encode('utf-8'))
                # 2、接收断点续传标识位 <-- 服务器
                file_flag_len = client.recv(4)
                file_flag = struct.unpack('i', file_flag_len)[0]
                # 创建帧头
                header = self.get_header(file_flag, file, file_name)
                # 3、发送帧头长度 --> 服务器
                len_head = struct.pack('i', len(str(header)))
                client.send(len_head)
                # 4、发送帧头 --> 服务器
                client.send(str(header).encode('utf-8'))
                # 5、开始发送文件 --> 服务器
                self.put_file(client, file, file_flag)

            # 非文件操作指令：ls、mkdir、rmdir、remove、cd
            elif cmd.strip().split()[0] in cmd_list:
                client.send(' '.join([self.id, self.usr_size, cmd]).encode('utf-8'))
                msg = client.recv(2048)
                print(f'{msg.decode("utf8")}')

        client.close()

    @classmethod
    def exit_client(cls):
        """
        用户退出客户端界面
        :return:
        """
        exit('\033[32m谢谢使用\033[0m')

    def save(self):
        """
        保存用户对象到本地
        :return:
        """
        file_path = os.path.join(setting.CLIENT_USR_PATH, self.id)
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    def __str__(self):
        """
        字符串方法
        :return: 用户id
        """
        return self.id


if __name__ == '__main__':
    ClientUsr.client_run()
