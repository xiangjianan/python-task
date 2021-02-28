## Python练习-FTP文件系统

### 1.[功能描述]
1. 服务器
    * 支持多用户同时在线
    * 并发处理用户发来的请求指令
2. 客户端
    * 用户注册、登录（注册时设置磁盘空间大小）
    * 访问家目录，随意切换家目录下的任何目录
    * 创建、删除目录
    * 下载、上传文件（md5校验）
    * 删除文件

### 2.[开发环境]
1. 操作系统：macOS
2. 解释器版本：python3.9
3. IDE：Pycharm

### 3.[项目结构简介]
1. bin
    * sever.py
        > 服务器入口
    * client.py
        > 客户端入口
2. conf
    * setting.py
        > 用户可以配置最大并发数，默认并发用户为10
        > 用户可以配置端口号，默认8080
3. core
    * tools.py
        > 自定义文件处理功能
        > 自定义md5功能
4. db
    * client
        > 存储所有用户的家目录
    * client_usr
        > 存储所有pickle序列化的用户对象
5. README.md
    > 用户帮助文档
6. 流程图

### 4.[启动方式]
1. IDE：进入工程bin目录，先运行sever.py文件，再运行client.py文件
2. 终端：打开终端运行sever.py文件，新建终端再运行client.py文件

### 5.[登录信息]
1. 用户登录信息
    * 账号：alex
        > 密码：123456
    * 账号：小明
        > 密码：123
2. 自定义创建用户

### 6.[指令集]
1. 创建目录
    * mkdir 目录名
2. 删除目录
    * rmdir 目录名
3. 切换目录
    * cd 目录
    * cd ..
    * cd /
4. 遍历目录
    * ls
5. 上传文件
    * put 本地文件绝对路径
6. 下载文件
    * get 文件名（带后缀）
        > 输入指令，回车后，再输入文件下载到本地的绝对路径
7. 删除文件
    * remove 文件名
8. 退出客户端
    * exit

### 7.[运行效果]
1. 客户端界面
    * 注册与登录
        > ![8d4ccdf4f4a800cdfcfd7ebb304ca274](README.resources/C7B5F43C-2644-4D7C-A1B7-124D900B1AAD.png)
    * 多用户登录
        > ![7c43dad7ac10de06654aa5e571faea82](README.resources/C3560131-C59C-4BB8-8C63-864525C987B5.png)
    * 创建、删除及浏览目录
        > ![27792e67effa803e4b86cbe689c9e0ed](README.resources/9FED2AE4-D78D-42BF-B20F-C00832E7C038.png)
        > ![88f6d04236c29ea90e91006b28024ccd](README.resources/0E23C5C0-798D-432F-B99A-175B0F4B3C68.png)
        > ![a4c47c181fc0e5ecc1b4194ed3ca3146](README.resources/9EB456C4-09F7-4EBA-BFC6-5EA3F07F6E04.png)
    * 上传文件
        > ![5be6c7d19e7956bbcf504a5ac7a2430e](README.resources/D4DD9B6E-5737-452E-AF23-48FCDFE7CA00.png)
    * 下载文件
        > ![3953efcc7534ba99a2e392ed5ad9a21f](README.resources/0A8EDD26-0646-484F-9C61-A12BE4D8B013.png)
        > ![1d05a527fccd196ecfd47758d6514401](README.resources/AA2A3A5A-C992-48D1-A532-D17F437B42DA.png)
        > ![f8a82a6818af30adf74d0c7aff15394e](README.resources/B8E317C1-CFF5-4DD9-9C98-DB873BC53505.png)
    * 删除文件
        > ![7bf8ee792b530f2de1936196f633103e](README.resources/43C40EAB-89F2-4890-8624-EB9035964C8D.png)
2. 服务器界面
    ![afebb592a76619c30a4fba6c76e262b5](README.resources/25988B3F-94A1-4099-98B9-CF853B814573.png)
    
