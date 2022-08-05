#!/usr/bin/env python3

from sys import executable

import subprocess
import os
from sys import platform
from typing import Optional


def is_linux() -> bool:
    return platform == "linux" or platform == "linux2"

def is_osx() -> bool:
    return platform == "darwin"

def is_win() -> bool:
    return platform == "win32"

def is_call_failed(
    ret_code: int,
    message: str='',
    failed_exit_code: Optional[int]=1
) -> Optional[bool]:
    if ret_code == 0:
        return False
    print(message)
    if failed_exit_code:
        exit(failed_exit_code)
    return True

# create virtual environment
if not os.path.exists('.venv'):
    print('Creating virtual environment...')
    is_call_failed(
        subprocess.call([executable, '-m', 'venv', '.venv']),
        message='Unable to create virtual environment!',
        failed_exit_code=1
    )
    print('Virtual environment created!\n')
else:
    print('Virtual environment detected!\n')

if is_linux() or is_osx():
    pipe = subprocess.Popen("source .venv/bin/activate", shell=True, executable="/bin/bash")
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)
elif is_win():
    is_call_failed(
        subprocess.check_call('.venv\\Scripts\\activate'),
        'Error: Unable to enter the virtual environment!',
        1
    )
else:
    print('Unknown operating system! Exiting setup...')
    exit(1)

print('Installing required libraries...\n')
print(subprocess.check_output(
    'pip install -r requirements-dev.txt'.split(),
    universal_newlines=True)
)
print(subprocess.check_output(
    'pip install -r requirements.txt'.split(),
    universal_newlines=True)
)

print('Setup complete! You can now enter your virtual environemnt `.venv` and start developing!')
