# coding: utf-8

import os
import sys

# 配置环境变量
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import main
from core.main import Teacher
from core.main import School
from core.main import Student

# 运行主函数
main.running()
