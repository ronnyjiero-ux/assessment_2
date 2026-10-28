import random
import tkinter as tk
from copy import deepcopy
from pathlib import Path
from tkinter import ttk

from Model import database
from Controller import subject_system
from Model import utils




def authenticate_student(email, password):
    email = email.strip()
    password = password.strip()

    if not email or not password:
        raise ValueError("Email and password cannot be empty.")

    if not utils.check_email(email):
        raise ValueError("Incorrect email format.")

    if not utils.check_password(password):
        raise ValueError("Incorrect password format.")

    student = database.emailsearch(email)

    if student is None or student.get("password") != password:
        raise ValueError("Incorrect email or password.")

    return student


def enrol_student(student):
    subjects = student.get("subjects", [])

    if len(subjects) >= subject_system.MAX_SUBJECT:
        raise ValueError("Students can enrol in a maximum of four subjects.")

    subject_id = subject_system.generate_subject_id()
    mark = random.randint(25, 100)
    new_subject = {
        "id": subject_id,
        "mark": mark,
        "grade": subject_system.calculate_grade(mark)
    }

    update_student = deepcopy(student)
    update_student.setdefault("subjects", []).append(new_subject)
    update_student["average_mark"] = subject_system.calculate_average(
        update_student["subjects"]
    )

    if not subject_system.save_changes(student, update_student):
        raise RuntimeError("The subject could not be saved.")

    return new_subject


def centre_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = min(width, screen_width - 40)
    height = min(height, screen_height - 80)
    x_position = (screen_width - width) // 2
    y_position = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x_position}+{y_position}")


BACKGROUND = "#f3f5f9"
SURFACE = "#ffffff"
INK = "#17243b"
MUTED = "#5b687e"
ACCENT = "#315ed6"


def configure_window(window, title, width, height, minimum_width, minimum_height):
    window.title(f"GUIUniApp - {title}")
    window.configure(background=BACKGROUND)
    centre_window(window, width, height)
    window.minsize(
        min(minimum_width, window.winfo_screenwidth() - 40),
        min(minimum_height, window.winfo_screenheight() - 80)
    )


def header(parent, title, subtitle):
    frame = ttk.Frame(parent)
    frame.pack(fill="x", pady=(0, 22))
    ttk.Label(frame, text="GUIUniApp  /  STUDENT PORTAL", style="Eyebrow.TLabel").pack(anchor="w")
    ttk.Label(frame, text=title, style="Title.TLabel").pack(anchor="w", pady=(10, 6))
    label = ttk.Label(frame, text=subtitle, style="Muted.TLabel", wraplength=600)
    label.pack(fill="x")
    label.bind("<Configure>", lambda event: label.configure(wraplength=max(120, event.width)))


class ExceptionWindow(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        configure_window(self, "Please check", 460, 280, 400, 260)
        self.transient(parent)
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="PLEASE CHECK", style="Error.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Unable to continue", style="Heading.TLabel").pack(anchor="w", pady=(12, 12))
        label = ttk.Label(frame, text=message, justify="left", wraplength=400)
        label.pack(fill="x")
        label.bind("<Configure>", lambda event: label.configure(wraplength=max(100, event.width)))
        button = ttk.Button(frame, text="Got it", command=self.destroy, style="Primary.TButton")
        button.pack(side="bottom", anchor="e", pady=(18, 0))
        self.bind("<Return>", lambda event: self.destroy())
        self.bind("<Escape>", lambda event: self.destroy())
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_visibility()
        self.grab_set()
        button.focus_set()


class SubjectWindow(tk.Toplevel):
    def __init__(self, parent, student):
        super().__init__(parent)
        self.student = student
        configure_window(self, "My subjects", 740, 600, 580, 580)
        self.transient(parent)
        frame = ttk.Frame(self, padding=28)
        frame.pack(fill="both", expand=True)
        header(frame, "My subjects", f"{student['name']}  |  Student ID: {student['id']}")
        self.summary = ttk.Label(frame, style="Heading.TLabel")
        self.summary.pack(anchor="w", pady=(0, 16))
        card = ttk.Frame(frame, style="Card.TFrame", padding=16)
        card.pack(fill="both", expand=True)
        columns = ("id", "mark", "grade")
        self.table = ttk.Treeview(card, columns=columns, show="headings", height=4, selectmode="browse")
        for column, title in zip(columns, ("Subject ID", "Mark / 100", "Grade")):
            self.table.heading(column, text=title)
            self.table.column(column, width=150, minwidth=95, anchor="center")
        self.table.tag_configure("even", background="#f1f5fc")
        self.table.tag_configure("odd", background=SURFACE)
        self.table.pack(fill="both", expand=True)
        self.empty_text = ttk.Label(card, style="CardMuted.TLabel", text="No subjects yet. Enrol in a subject to see your results here.", wraplength=430)
        footer = ttk.Frame(frame)
        footer.pack(fill="x", pady=(20, 0))
        ttk.Label(footer, text="Grades: HD / DN / C / P / F", style="Muted.TLabel").pack(side="left")
        ttk.Button(footer, text="Back to enrolment", command=self.destroy).pack(side="right")
        self.bind("<Escape>", lambda event: self.destroy())
        self.refresh()

    def refresh(self):
        subjects = self.student.get("subjects", [])
        average_mark = subject_system.calculate_average(subjects)
        average_text = "--" if average_mark is None else f"{average_mark:.2f}"
        self.summary.configure(text=f"{len(subjects)} subjects enrolled    |    Average mark: {average_text}")
        for item in self.table.get_children():
            self.table.delete(item)
        for index, subject in enumerate(subjects):
            self.table.insert("", "end", values=(subject["id"], subject["mark"], subject["grade"]), tags=("even" if index % 2 == 0 else "odd",))
        if subjects:
            self.empty_text.pack_forget()
        else:
            self.empty_text.pack(fill="x", pady=(16, 4))


class EnrolmentWindow(tk.Toplevel):
    def __init__(self, app, student):
        super().__init__(app)
        self.app = app
        self.student = student
        self.subject_window = None
        configure_window(self, "Enrolment", 800, 700, 660, 680)
        self.protocol("WM_DELETE_WINDOW", self.logout)
        frame = ttk.Frame(self, padding=28)
        frame.pack(fill="both", expand=True)
        header(frame, "Your enrolment", f"Welcome, {student['name']}  |  Student ID: {student['id']}")
        stats = ttk.Frame(frame)
        stats.pack(fill="x", pady=(0, 20))
        for column in range(3):
            stats.columnconfigure(column, weight=1, uniform="stats")
        self.enrolled_text = tk.StringVar()
        self.remaining_text = tk.StringVar()
        self.average_text = tk.StringVar()
        for column, (title, variable) in enumerate((("ENROLLED", self.enrolled_text), ("AVAILABLE", self.remaining_text), ("AVERAGE MARK", self.average_text))):
            card = ttk.Frame(stats, style="Card.TFrame", padding=18)
            card.grid(row=0, column=column, sticky="nsew", padx=(0 if column == 0 else 8, 0))
            ttk.Label(card, text=title, style="CardMuted.TLabel").pack(anchor="w")
            ttk.Label(card, textvariable=variable, style="Metric.TLabel").pack(anchor="w", pady=(8, 0))
        card = ttk.Frame(frame, style="Card.TFrame", padding=24)
        card.pack(fill="both", expand=True)
        ttk.Label(card, text="Manage your subjects", style="CardHeading.TLabel").pack(anchor="w")
        ttk.Label(card, text=f"You can enrol in up to {subject_system.MAX_SUBJECT} subjects.", style="CardMuted.TLabel").pack(anchor="w", pady=(8, 18))
        self.count_text = tk.StringVar()
        ttk.Label(card, textvariable=self.count_text, style="Card.TLabel").pack(anchor="w")
        self.progress = ttk.Progressbar(card, maximum=subject_system.MAX_SUBJECT, style="Enrolment.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(10, 22))
        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x")
        actions.columnconfigure((0, 1), weight=1, uniform="actions")
        self.enrol_button = ttk.Button(actions, text="+  Enrol in a subject", command=self.enrol, style="Primary.TButton")
        self.enrol_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        ttk.Button(actions, text="View my subjects", command=self.show_subjects).grid(row=0, column=1, sticky="ew")
        self.status_text = tk.StringVar(value="Choose Enrol to add a subject to your record.")
        status = ttk.Label(card, textvariable=self.status_text, style="CardMuted.TLabel", wraplength=550)
        status.pack(fill="x", pady=(18, 0))
        status.bind("<Configure>", lambda event: status.configure(wraplength=max(150, event.width)))
        footer = ttk.Frame(frame)
        footer.pack(fill="x", pady=(20, 0))
        ttk.Label(footer, text="Changes are saved automatically.", style="Muted.TLabel").pack(side="left")
        ttk.Button(footer, text="Log out", command=self.logout).pack(side="right")
        self.refresh_count()

    def refresh_count(self):
        subject_count = len(self.student.get("subjects", []))
        self.count_text.set(
            f"Enrolled subjects: {subject_count} out of "
            f"{subject_system.MAX_SUBJECT}"
        )
        self.enrolled_text.set(f"{subject_count} / {subject_system.MAX_SUBJECT}")
        self.remaining_text.set(str(max(0, subject_system.MAX_SUBJECT - subject_count)))
        average = subject_system.calculate_average(self.student.get("subjects", []))
        self.average_text.set("--" if average is None else f"{average:.2f}")
        self.progress["value"] = subject_count
        self.enrol_button.configure(text="Enrolment limit reached" if subject_count >= subject_system.MAX_SUBJECT else "+  Enrol in a subject")

    def enrol(self):
        try:
            new_subject = enrol_student(self.student)
        except (OSError, ValueError, TypeError, KeyError, RuntimeError) as error:
            ExceptionWindow(self, str(error))
            return

        self.refresh_count()
        self.status_text.set(
            f"Subject-{new_subject['id']} enrolled successfully."
        )
        self.show_subjects()

    def show_subjects(self):
        if self.subject_window is not None and self.subject_window.winfo_exists():
            self.subject_window.refresh()
            self.subject_window.deiconify()
            self.subject_window.lift()
            self.subject_window.focus_set()
        else:
            self.subject_window = SubjectWindow(self, self.student)

    def logout(self):
        self.destroy()
        self.app.show_login()


class GUIUniApp(tk.Tk):
    def __init__(self):
        super().__init__()
        database.check_existingstudent()
        configure_window(self, "Student login", 900, 560, 760, 520)
        self.configure_style()
        self.build_login_window()

    def configure_style(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 11), foreground=INK, background=BACKGROUND)
        style.configure("TFrame", background=BACKGROUND)
        style.configure("Card.TFrame", background=SURFACE)
        style.configure("Hero.TFrame", background=INK)
        style.configure("TLabel", background=BACKGROUND)
        style.configure("Title.TLabel", font=("Segoe UI", 25, "bold"))
        style.configure("Heading.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("Muted.TLabel", foreground=MUTED)
        style.configure("Eyebrow.TLabel", foreground=ACCENT, font=("Segoe UI", 10, "bold"))
        style.configure("Error.TLabel", foreground="#a53438", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TLabel", background=SURFACE)
        style.configure("CardMuted.TLabel", background=SURFACE, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("CardHeading.TLabel", background=SURFACE, font=("Segoe UI", 17, "bold"))
        style.configure("Metric.TLabel", background=SURFACE, foreground=ACCENT, font=("Segoe UI", 27, "bold"))
        style.configure("Hero.TLabel", background=INK, foreground="#c4d2ec")
        style.configure("HeroTitle.TLabel", background=INK, foreground=SURFACE, font=("Segoe UI", 29, "bold"))
        style.configure("HeroBrand.TLabel", background=INK, foreground=SURFACE, font=("Segoe UI", 15, "bold"))
        style.configure("TButton", background=SURFACE, foreground=INK, padding=(16, 11), borderwidth=1, focusthickness=2, focuscolor=ACCENT)
        style.map("TButton", background=[("pressed", "#dce5f8"), ("active", "#eaf0fb")])
        style.configure("Primary.TButton", background=ACCENT, foreground=SURFACE, borderwidth=0, font=("Segoe UI", 11, "bold"), focuscolor=SURFACE)
        style.map("Primary.TButton", background=[("pressed", "#2445a1"), ("active", "#244fbe")], foreground=[("disabled", "#d5ddf2")])
        style.configure("TEntry", fieldbackground=SURFACE, foreground=INK, padding=10, bordercolor="#c7d0e0", lightcolor=SURFACE, darkcolor=SURFACE)
        style.map("TEntry", bordercolor=[("focus", ACCENT)])
        style.configure("Card.TCheckbutton", background=SURFACE, foreground=MUTED, font=("Segoe UI", 10))
        style.map("Card.TCheckbutton", background=[("active", SURFACE)])
        style.configure("Treeview", background=SURFACE, fieldbackground=SURFACE, rowheight=42, borderwidth=0)
        style.map("Treeview", background=[("selected", "#dce7ff")], foreground=[("selected", INK)])
        style.configure("Treeview.Heading", background="#e9eef8", foreground=INK, font=("Segoe UI", 10, "bold"), padding=12, relief="flat")
        style.configure("Enrolment.Horizontal.TProgressbar", background=ACCENT, troughcolor="#e9eef8", borderwidth=0, thickness=8)

    def build_login_window(self):
        outer = ttk.Frame(self, padding=24)
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=4, uniform="login")
        outer.columnconfigure(1, weight=5, uniform="login")
        outer.rowconfigure(0, weight=1)
        hero = ttk.Frame(outer, style="Hero.TFrame", padding=28)
        hero.grid(row=0, column=0, sticky="nsew")
        ttk.Label(hero, text="GUIUniApp", style="HeroBrand.TLabel").pack(anchor="w")
        hero_title = ttk.Label(hero, text="Your studies.\nOne place.", style="HeroTitle.TLabel", justify="left", wraplength=320)
        hero_title.pack(fill="x", pady=(60, 20))
        hero_title.bind("<Configure>", lambda event: hero_title.configure(wraplength=max(100, event.width)))
        intro = ttk.Label(hero, text="Enrol in subjects and keep track of your marks.", style="Hero.TLabel", wraplength=240)
        intro.pack(fill="x")
        intro.bind("<Configure>", lambda event: intro.configure(wraplength=max(100, event.width)))
        ttk.Label(hero, text="STUDENT PORTAL", style="Hero.TLabel").pack(side="bottom", anchor="w")
        frame = ttk.Frame(outer, style="Card.TFrame", padding=32)
        frame.grid(row=0, column=1, sticky="nsew")
        ttk.Label(frame, text="Welcome back", style="CardHeading.TLabel").pack(anchor="w", pady=(4, 8))
        ttk.Label(frame, text="Sign in with your registered account.", style="CardMuted.TLabel", wraplength=280).pack(anchor="w", pady=(0, 26))
        ttk.Label(frame, text="University email", style="Card.TLabel").pack(anchor="w")
        self.email_text = tk.StringVar()
        self.email_entry = ttk.Entry(
            frame,
            textvariable=self.email_text,
            width=24
        )
        self.email_entry.pack(fill="x", pady=(7, 16))
        ttk.Label(frame, text="Password", style="Card.TLabel").pack(anchor="w")
        self.password_text = tk.StringVar()
        self.password_entry = ttk.Entry(
            frame,
            textvariable=self.password_text,
            show="*",
            width=24
        )
        self.password_entry.pack(fill="x", pady=(7, 10))
        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame, text="Show password", variable=self.show_password, command=self.toggle_password, style="Card.TCheckbutton").pack(anchor="w", pady=(0, 20))
        ttk.Button(frame, text="Sign in", command=self.login, style="Primary.TButton").pack(fill="x")
        ttk.Label(frame, text="Use the main application to register first.", style="CardMuted.TLabel", wraplength=280).pack(anchor="w", pady=(20, 0))
        self.email_entry.focus_set()
        self.email_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        self.password_entry.configure(show="" if self.show_password.get() else "*")

    def login(self):
        try:
            student = authenticate_student(
                self.email_text.get(),
                self.password_text.get()
            )
        except (OSError, ValueError, TypeError, KeyError) as error:
            ExceptionWindow(self, str(error))
            return

        self.password_text.set("")
        self.withdraw()
        EnrolmentWindow(self, student)

    def show_login(self):
        self.password_text.set("")
        self.show_password.set(False)
        self.toggle_password()
        self.deiconify()
        self.lift()
        self.email_entry.focus_set()


def main():
    app = GUIUniApp()
    app.mainloop()


if __name__ == "__main__":
    main()
