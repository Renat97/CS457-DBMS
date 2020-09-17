import os
from shutil import rmtree

a = input();

dir = a.split('CREATE DATABASE');

print(dir);

if os.path.exists(dir):
    print('already exists');
