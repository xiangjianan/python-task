import os

# 配置本地数据库路径
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIENT_PATH = os.path.join(path, 'db', 'client')
CLIENT_USR_PATH = os.path.join(path, 'db', 'client_usr')

# 配置服务器属性
IP_ADDR = ('127.0.0.1', 8080)
LISTEN_MAX = 5
POOL_MAX = 10

# 配置上传/下载延时
TIME_DELAY = 0.1
