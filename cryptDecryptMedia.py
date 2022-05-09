
import os
import sys
import hashlib

files = os.listdir()
random_string = "/thee/"

def hide(file):
    with open(file, "rb") as f:
        content = f.read()
    with open(file, "wb") as f:
        f.write(content.replace("A".encode(), random_string.encode()))

def unhide(file):
    with open(file, "rb") as f:
        content = f.read()
    with open(file, "wb") as f:
        f.write(content.replace(random_string.encode(), "A".encode()))


password_ = input("<> ")
# print(password_)
if not hashlib.sha256(password_.encode()).hexdigest() == '058abbc695d381e1c59aa13b088338fbfb4133fbeeb92f312e51c7f08860409b': #abp
    # print(hashlib.sha256(password_.encode()).hexdigest)
    sys.exit(1)
    
choice = input("<e/d>").lower()

for file in files:    
    if not (file.endswith('.ini') or file.endswith('.py')):
        if choice == "d":
            unhide(file)
        else:
            hide(file)

