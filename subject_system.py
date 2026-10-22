import random
from copy import deepcopy

import database
import utils

MAX_SUBJECT = 4

def handle_subject_system(student):
    while True:
        choice = input("\t\tStudent Course Menu (c/e/r/s/x): ").strip().lower()
        if choice == 'c':
            change_password(student)
        elif choice == 'e':
            enrol_subject(student)
        elif choice == 'r':
            remove_subject(student)
        elif choice == 's':
            show_subjects(student)
        elif choice == 'x':
            return
        else:
            print("\t\tInvalid option. Please enter c, e, r, s or x.")

def save_changes(student, update_student):
    try:
        students = database.load_students()

        for index,saved_student in enumerate(students):
            if saved_student["id"] == student.id:
                students[index] = update_student
                database.save_students(students)

                student.clear()
                student.update(update_student)
                return True

        print("\t\tStudent does not exist. Changes were not saved.")

    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"\t\tUnable to save changes: {error}")

    return False

def calculate_grade(mark):
    if mark >= 85:
        return "HD"
    elif mark >= 75:
        return "DN"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    return "F"

def calculate_average(subjects):
    if not subjects:
        return None

    return sum(subject["mark"] for subject in subjects) / len(subjects)

def change_password(student):
    print("\t\tUpdating Password")

    while True:
        new_password = input("\t\tNew password: ")

        if utils.yanzhengmima(new_password):
            break

        print(
            "\t\tIncorrect password format. "
            "Start with an uppercase letter, use at least "
            "5 letters, followed by at least 3 digits."
        )

    while True:
        confirm_password = input("\t\tConfirm password: ")

        if confirm_password == new_password:
            break

        print("\t\tPassword does not match - try again")

    update_student = deepcopy(student)
    update_student["password"] = new_password

    save_changes(student, update_student)

def generate_subject_id():
    students = database.load_students()

    used_ids = {
        str(subject["id"]).zfill(3)
        for saved_student in students
        for subject in saved_student.get("subjects", [])
    }

    available_ids = [
        f"{number:03d}"
        for number in range(1, 1000)
        if f"{number:03d}" not in used_ids
    ]

    if not available_ids:
        raise ValueError("No subject IDs are available.")

    return random.choice(available_ids)

def enrol_subject(student):
    subjects = student.get("subjects", [])

    if len(subjects) >= MAX_SUBJECT:
        print("\t\tStudents are allowed to enrol in 4 subjects only")
        return

    try:
        subject_id = generate_subject_id()
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"\t\tUnable to enrol: {error}")
        return

    mark = random.randint(25, 100)

    new_subject = {
        "id": subject_id,
        "mark": mark,
        "grade": calculate_grade(mark)
    }

    update_student = deepcopy(student)
    update_student.setdefault("subjects", []).append(new_subject)

    update_student["average_mark"] = calculate_average(
        update_student["subject"]
    )

    if save_changes(student, update_student):
        print(f"\t\tEnrolling in Subject-{subject_id}")
        print(
            f"\t\tYou are now enrolled in "
            f"{len(student['subjects'])} out of 4 subjects"
        )

def remove_subject(student):
    subjects = student.get("subjects", [])

    if not subjects:
        print("\t\tYou have no enrolled subjects")
        return

    subject_id = input("\t\tRemove subject by ID: ").strip()

    if (
        not subject_id.isascii()
        or not subject_id.isdigit()
        or not 1 <= len(subject_id) <= 3
        or not 1 <= int(subject_id) <= 999
    ):
        print("\t\tInvalid subject ID. Enter a number from 001 to 999.")
        return

    subject_id = subject_id.zfill(3)

    subject_index = None

    for index, subject in enumerate(subjects):
        if str(subject["id"]).zfill(3) == subject_id:
            subject_index = index
            break
    if subject_index is None:
        print(f"\t\tSubject-{subject_id} is not enrolled")
        return

    update_student = deepcopy(student)
    del update_student["subjects"][subject_index]

    update_student = deepcopy(student)
    del update_student["subjects"][subject_index]

    update_student["average_mark"] = calculate_average(
        update_student["subjects"]
    )

    if save_changes(student, update_student):
        print(f"\t\tDropping Subject-{subject_id}")
        print(
            f"\t\tYou are now enrolled in "
            f"{len(student['subjects'])} out of 4 subjects"
        )

def show_subjects(student):
    subjects = student.get("subjects", [])

    print(f"\t\tShowing {len(subjects)} subjects")

    for subject in subjects:
        subject_id = str(subject["id"]).zfill(3)
        mark = subject["mark"]
        grade = subject["grade"]

        print(
            f"\t\t[ Subject::{subject_id} "
            f"-- mark = {mark} -- grade = {grade} ]"
        )
