# -*- coding: utf-8 -*-
import os
import sys
from jinja2 import Environment, FileSystemLoader

# py_path нужен, чтобы systemd запускал скрипт из виртуального окружения
# watcher_path нужен, чтобы systemd знал, что запускать
# workdir_path нужен, чтобы не нарушать логику обращения к файлам по относительному пути

vals = {
    'py_path': sys.executable,
    'watcher_path': os.path.abspath('../watcher/watcher.py'),
    'workdir_path': os.path.abspath('../watcher'),
    'user': 'watcher',
    'group':'watcher',
}


file_loader = FileSystemLoader('')
env = Environment(loader=file_loader)

template = env.get_template('template.txt')

output = template.render(vals)

with open('watcher.service', 'w') as f:
    f.write(output)

print('python path is ' + vals['py_path'])
print('watcher.py path is ' + vals['watcher_path'])
print('workdir path is ' + vals['workdir_path'])
print('user is ' + vals['user'])
print('group is ' + vals['group'])
