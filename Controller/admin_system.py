from Model import database
from Model import utils


def calculate_average(subjects):
    if not subjects:
        return None
    return utils.pingjunfen(subjects)


def calculate_grade(mark):
    if mark >= 85:
        return "HD"
    elif mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    return "F"


def display_student(student):
    average_mark = calculate_average(student["subjects"])
    if average_mark is None:
        result = "No subjects / No grade"
    else:
        grade = calculate_grade(average_mark)
        result = f"Average: {average_mark:.2f} / Grade: {grade}"

    print(
        f"{student['id']} | {student['name']} | "
        f"{student['email']} | {result}"
    )


def show_all_students():
    students = database.load_students()
    if not students:
        print("No students found.")
        return

    print("\nAll students:")
    for student in students:
        display_student(student)


def group_students():
    students = database.load_students()
    if not students:
        print("No students found.")
        return

    groups = {"HD": [], "DN": [], "C": [], "P": [], "F": []}
    ungraded = []

    for student in students:
        average_mark = calculate_average(student["subjects"])
        if average_mark is None:
            ungraded.append(student)
        else:
            grade = calculate_grade(average_mark)
            groups[grade].append(student)

    for grade in groups:
        print(f"\nGrade {grade}:")
        if not groups[grade]:
            print("No students in this group.")
        for student in groups[grade]:
            display_student(student)

    if ungraded:
        print("\nNo grade (no subjects):")
        for student in ungraded:
            display_student(student)


def partition_students():
    students = database.load_students()
    if not students:
        print("No students found.")
        return

    passed = []
    failed = []
    ungraded = []

    for student in students:
        average_mark = calculate_average(student["subjects"])
        if average_mark is None:
            ungraded.append(student)
        elif average_mark >= 50:
            passed.append(student)
        else:
            failed.append(student)

    print("\nPASS:")
    if not passed:
        print("No students in this group.")
    for student in passed:
        display_student(student)

    print("\nFAIL:")
    if not failed:
        print("No students in this group.")
    for student in failed:
        display_student(student)

    if ungraded:
        print("\nNo result (no subjects):")
        for student in ungraded:
            display_student(student)


def remove_student():
    student_id = input("Student ID to remove: ").strip()

    if (
        len(student_id) != 6
        or not student_id.isascii()
        or not student_id.isdigit()
    ):
        print("Please enter a 6-digit student ID.")
        return

    students = database.load_students()
    remaining_students = []
    removed_student = None

    for student in students:
        if student["id"] == student_id:
            removed_student = student
        else:
            remaining_students.append(student)

    if removed_student is None:
        print("Student not found.")
        return

    database.save_students(remaining_students)
    print(f"Removed student {student_id}: {removed_student['name']}")


def clear_database():
    choice = input("Clear all students? (y/n): ").strip().lower()
    if choice == "y":
        database.clear_students()
        print("All students cleared.")
    else:
        print("Clear cancelled.")


def handle_admin_system():
    database.check_existingstudent()
    print("Admin System")
    print("s: show | g: group | p: pass/fail")
    print("r: remove | c: clear | x: exit")

    while True:
        choice = input("\nAdmin System (c/g/p/r/s/x): ").strip().lower()
        if choice == "c":
            clear_database()
        elif choice == "g":
            group_students()
        elif choice == "p":
            partition_students()
        elif choice == "r":
            remove_student()
        elif choice == "s":
            show_all_students()
        elif choice == "x":
            print("Exit Admin System.")
            return
        else:
            print("Unknown option. Please enter c, g, p, r, s, or x.")


if __name__ == "__main__":
    handle_admin_system()
