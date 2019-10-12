#  启动入口
from application import app, manager
from jobs.Launcher import runJob
from flask_script import Server
import www

# Web server
manager.add_command("runserver", Server(host='0.0.0.0',
                                        port=app.config['SERVER_PORT'],
                                        use_debugger=True,
                                        use_reloader=True))
#job entrance
manager.add_command('runjob', runJob())

def main():
    manager.run()

if __name__ == '__main__':

    try:
        import sys
        sys.exit(main())

    except Exception as e:
        import traceback
        # 打印所有错误
        traceback.print_exc()
