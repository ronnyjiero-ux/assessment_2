import database
import utils
import subject_system
import utils
import database
import admin_system
DATA_FILE = "students.data"

class Student:
    def __init__(self, student_id: str, name: str, email: str, password: str, subjects=None):
        self.id = str(student_id)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": self.subjects
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            student_id=data.get("id", ""),
            name=data.get("name", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
            subjects=data.get("subjects", [])
        )

class StudentController:
    def __init__(self):
     database.is_cunzai()

    def prompt_credentials(self) -> tuple[str, str]:
        while True:
            email = input("\tEmail: ").strip()
            password = input("\tPassword: ").strip()
#calls function from utils. It's for checking password and email format
            if utils.yanzhengyouxiang(email) and utils.yanzhengmima(password):
                print("\temail and  password formats acceptable")
                return email, password
            else:
                print("\tIncorrect email or password format")
#generate 6 digit student ID
    def generate_unique_id(self) -> str:
        existing_students = database.load_students()
        existing_ids = {s.get("id") for s in existing_students if isinstance(s, dict)}

        while True:
            new_id = utils.shengchengxueshengid()
            if new_id not in existing_ids:
                return new_id
#creating an account
    def register_student(self):
        print("\tStudent Sign Up")
        email, password = self.prompt_credentials()

        existing_students = database.youxiangzhaoren(email)
        if existing_students:
            student_name = existing_students.get("name", "")
            print(f"\tStudent {student_name} already exist")
            return

        name = input("\tName: ").strip()
        student_id = self.generate_unique_id()

        new_student = Student(student_id, name, email, password)
        database.tianjia(new_student.to_dict())
        print(f"\tEnrolling Student {name}")
#sign in
    def login_student(self) -> Student | None:
        print("\tStudent Sign In")
        email, password = self.prompt_credentials()

        student_record = database.youxiangzhaoren(email)

        if not student_record or student_record.get("password") != password:
            print("\tStudent does not exist")
            return None

        return Student.from_dict(student_record)
#This is for menu input
    def run(self):
        while True:
            choice = input("\tStudent System (l/r/x): ").strip().lower()

            if choice in ("l", "1"):
                student = self.login_student()
                if student is not None:
                    try:
                        subject_system.handle_subject_enrolment(student.to_dict())
                    except AttributeError:
                        print("\t\tStudent Course Menu (c/e/r/s/x): (pending subject_system implementation)")
            elif choice == "r":
                self.register_student()
            elif choice == "x":
             break

def handle_student_system():
    controller = StudentController()
    controller.run()


if __name__ == "__main__":
    handle_student_system()