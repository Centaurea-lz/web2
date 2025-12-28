import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app

# 创建app并获取数据库配置
app = create_app()
# 获取真实的数据库文件路径
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
# 解析SQLite路径（sqlite:///xxx.db → 提取xxx.db的绝对路径）
if db_uri.startswith('sqlite:///'):
    # 相对路径转绝对路径
    db_relative_path = db_uri.replace('sqlite:///', '')
    db_abs_path = os.path.abspath(db_relative_path)
    print(f"✅ Flask项目实际使用的数据库文件路径：")
    print(f"   {db_abs_path}")
    # 检查文件是否存在
    if os.path.exists(db_abs_path):
        file_size = os.path.getsize(db_abs_path) / 1024  # 转KB
        print(f"✅ 文件存在，大小：{file_size:.2f} KB")
    else:
        print(f"❌ 文件不存在！")
else:
    print(f"❌ 不是SQLite数据库：{db_uri}")
