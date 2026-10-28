import json
import os
DATA_FILE = "students.data"
def check_existingstudent():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)


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


def save_students(students):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

def clear_students():
    save_students([])

def emailsearch(email):
    students = load_students()
    for i in students:
        if i['email'] == email:
            return i
    return None

def is_xueshengcunzai(email):
    return emailsearch(email) is not None


def idzhaoren(student_id):
    students = load_students()
    for i in students:
        if i['id'] == student_id:
            return i
    return None

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




