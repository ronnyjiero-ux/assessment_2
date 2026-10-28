from Controller import student_system
from Controller import admin_system
def main():
    while 1:
        x = input('University System: (A)dmin, (S)tudent, or X to exit: ')

        if x == 'A':
            admin_system.handle_admin_system()
        elif x == 'S':
            student_system.handle_student_system()
        elif x == 'X':
            print('Thank You')
            break
        else:
            print('unknown input')
            pass 


        
if __name__ == "__main__":
    main()