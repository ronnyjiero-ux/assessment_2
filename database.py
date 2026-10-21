import json
import os
DATA_FILE = "students.data"
def is_cunzai():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
#检查文件是否存在否则创建(老子就是要用中文写注释不服敲死我)

def load_students():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            students = json.load(f)
            if not isinstance(students, list):
                print('The returned result is not a list.')
                return []
            return students
        except json.JSONDecodeError:
            print('The returned result is not a JSON.')
            return []
#读取并检查, 一般我懒得做try检查...做个保险吧 省的怕他们写奇怪的东西进来.

def save_students(students):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)
#保存, 统一只有末尾带s的专用于代表读取进来的文件

def clear_students():
    save_students([])
#全删

##下面是查询函数:
def youxiangzhaoren(email):
    students = load_students()
    for i in students:
        if i['email'] == email:
            return i
    return None

def is_xueshengcunzai(email):
    return youxiangzhaoren(email) is not None
#纯确定是否存在, 可能不用这一段

def idzhaoren(student_id):
    students = load_students()
    for i in students:
        if i['id'] == student_id:
            return i
    return None
##查询部分到此为止

def tianjia(student):
    students = load_students()
    students.append(student)
    save_students(students)

def gengxin(updata_student):
    students = load_students()
    for i in range(len(students)):
        if students[i]['id'] == updata_student['id']:
            students[i] = updata_student
            break
    save_students(students)

def shanchu(student_id):
    student = load_students()
    save_studentsdexuesheng = []
    for i in student:
        if i['id'] != student_id:
            save_studentsdexuesheng.append(student)
    save_students(save_studentsdexuesheng)
#一加一改一删




