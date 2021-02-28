import os

# 设置本地数据库路径
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = {
    'school': f'{path}/db/school/',
    'class': f'{path}/db/class/',
    'teacher': f'{path}/db/teacher/',
    'student': f'{path}/db/student/',
    'lesson': f'{path}/db/lesson/',
}
