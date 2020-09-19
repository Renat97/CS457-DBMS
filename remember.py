import os
from shutil import rmtree

a = input();

subDir = a.split("CREATE TABLE ")[1]
        #parsing for passed
data = a.split("(",1)[1]
data = data[:-1];
print(data);


