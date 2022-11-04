import os

from app import create_app
from cli import init_cli

# 获取应用配置&创建应用
app = create_app(os.getenv('APP_CONFIG', 'default'))

# 初始化命令行

init_cli(app)
# shell工具
# from shell import init_shell
# init_shell(app)


if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=False)

__version__ = 'v0.9'
