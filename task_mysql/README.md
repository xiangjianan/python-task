## Python练习-pymysql指令练习

### 1.[功能描述]
1. 连接远程数据库（个人电脑）
2. 自定义MySQL指令，对远程数据库执行操作

### 2.[开发环境]
1. 操作系统：macOS
2. 解释器版本：python3.9
3. IDE：Pycharm

### 3.[项目结构简介]
1. bin
    * run.py
        > 程序入口
2. conf
    * setting.py
        > 配置数据库连接参数
        > 编辑MySQL指令
3. core
    * mysql.py
        > 执行MySQL指令
4. README.md
    > 用户帮助文档

### 4.[启动方式]
0. 启动前先设置MySQL登录信息
    * 修改`conf/setting.py`数据库参数
1. IDE：进入工程bin目录，运行run.py
2. 终端：进入工程bin目录，执行`python3 run.py`


### 6.[运行效果]
![fba25a164424ae6d9293603fe42e5f4b](README.resources/4DCF985D-9C5C-417E-A0E9-E8E2BD89B505.png)
![3c3d400c37bd97b23249968f2e13dfca](README.resources/E1494665-17B4-4360-AA0F-B58A5F4FE804.png)
![624ce5d2bd295c9bb29fefc26a87ead5](README.resources/6D2B6193-B4F7-4DA8-9C46-06321AA3E6A1.png)
![4ff954840c2958b8c32f070bf62401a0](README.resources/605A5757-744A-481A-A68E-C3F8FF1E4792.png)
![9571d57372f5f232d3fb150bb118e86b](README.resources/9B5F5E55-E6A2-4B55-AE86-862D8E7B1FBB.png)
![747a1374953afdb295f287efd13b2899](README.resources/32129814-A9AB-4BD1-A50B-74DD10CF8947.png)
![6cf138f8577c4f766111549ec9441f79](README.resources/9EF5912A-D34B-49BD-81F0-492D29BDFA64.png)
![51ab6a7b0cf5ccd2a337da0bace312d3](README.resources/84C0A3FF-0E73-4E91-A293-2ED523D36A91.png)
![a45a59fb547f7d4a951688996892b8b9](README.resources/9D3D911C-BFF8-45DA-AB98-7C8D35A6B6EC.png)
