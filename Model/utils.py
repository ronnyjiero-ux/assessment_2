import random
import re
EMAIL_PATTERN = r"^[A-Za-z]+\.[A-Za-z]+@university\.com$"
PASSWORD_PATTERN = r"^[A-Z][A-Za-z]{4,}\d{3,}$"

def check_email(email):
    if re.match(EMAIL_PATTERN,email):
        return True
    else:
        return False

def check_password(password):
    if re.match(PASSWORD_PATTERN,password):
        return True
    else:
        return False    

def generatestudentid():
    number = random.randint(1,999999)
    return (f"{number:06d}")

def generatesclassid():
    number = random.randint(1,999)
    return (f"{number:03d}")

def shengchengfenshu():
    number = round(random.randint(0,100), 2)
    return number

def suanfen(mark):
    if mark >= 85:
        return "H"
    elif mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    else:
        return "F"

def pingjunfen(subjects):
    total = 0.0
    for i in subjects:
        total = total + i["mark"]
    average = total / len(subjects)
    return average

