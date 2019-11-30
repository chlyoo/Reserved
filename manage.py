#!/usr/bin/env python
import os
from app import create_app
from app.models import User, Role # 20191112
from flask_script import Manager, Shell, Server

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
	return dict(app=app, User=User, Role=Role) # 20191112

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))

if __name__ == '__main__':
	manager.run()
