import os
from shutil import rmtree

a = input();

subDir = a.split("CREATE TABLE ")[1]
        #parsing for passed
subDir = subDir.split(" (")[0].lower()

print(subDir);


