
# I have divided the task into four parts. I will be responsible for the infrastructure setup, and you just need to select and fill in one.py file.
# Please choose one for each person:
'''
1. student_system.py (responsible for registration and login)
2. subject_system.py (course selection, course withdrawal, password modification, etc.)
3. admin_system (administrator functions)
'''
# Regarding gui_app, it is an additional challenge. We will discuss it after completing the main functions.


# The existing interfaces are as follows. You can directly call these existing functions:

'''
def load_students: read the student.data file and return a list of dictionaries. If the file does not exist, it will be created.
def save_students: save the data back to student.data
def clear_students: clear the contents of students.data
def yanzhengyouxiang: verify whether the input email is legal
def yanzhengmima: verify whether the input password is legal
def shengchengxueshengid: generate a 6-digit random student ID
def shengchengkemu: generate a 3-digit random course ID
def suanfen: after receiving a score, it will return the specific level of this score (such as HD or DN)
def pingjunfen: calculate the average score
'''

(In my code, when reading data from a file, the name 'students' is uniformly used. Of course, you can use any name you prefer, but using the same name helps ensure consistency and avoids potential issues.)

[Important note:]
## When you complete a function in the code, you should add the function name and specific function description to the above table. This will help other team members call your function.

## The team members responsible for student_system and admin_system, please note: Considering that some team members are not good at writing code, I have built a function for you to start your code. They should help you understand what needs to be done.