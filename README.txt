System Requirements

Programming Language: Python 3.x (Built and tested on Python 3.14).

Additional Libraries: No external pip packages are required. The application relies entirely on Python's standard library (json, os, random, re, copy, pathlib).

GUI Requirement: The graphical interface uses tkinter.

Note for macOS users: If you are using a package manager like MacPorts or Homebrew, ensure the underlying Tcl/Tk GUI libraries are installed for your specific Python version (e.g., sudo port install py314-tkinter or brew install python-tk@3.14). Alternatively, use the official macOS installer from python.org, which bundles Tkinter by default.

How to Run the Application

The application has two separate entry points depending on the interface you wish to use. Ensure your terminal is in the root directory of the project before running these commands.

1. Command Line Interface (CLI)
The CLI provides access to both the Admin System and the Student System.

python3 main.py


2. Graphical User Interface (GUI)
The GUI provides a visual student portal for secure login, enrolment, and grade tracking.

python3 run_gui.py


Project Structure

The codebase is organized into standard MVC folders to separate data, logic, and visuals:

/Model: Contains database.py and utils.py. Handles data storage, retrieval, regex validation, and grade calculations.

/Controller: Contains admin_system.py, student_system.py, and subject_system.py. Processes user input, routing, and executes business logic.

/Views: Contains gui_app.py. Manages the Tkinter visual layout, components, and user interface.

students.data: The local JSON storage file generated in the root directory to persist user credentials, subject IDs, and marks.