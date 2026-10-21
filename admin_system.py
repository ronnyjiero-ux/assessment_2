import database
import utils
# These import imply that you may need to use some of the functions from these three files. For the specific names, please refer to readme.py.


def handle_admin_system():
    while 1:
        x = input('Admin System (c/g/p/r/s/x): ')
        if x == 'c':
            database.clear_students()
## This will invoke a deletion function in database.py, deleting all the contents of student.data.
        elif x == 'g':
            group_students()
        elif x == "p":
            partition_students()
        elif x == "r":
            remove_student()
        elif x == "s":
            show_all_students()
        elif x == "x":
            return


