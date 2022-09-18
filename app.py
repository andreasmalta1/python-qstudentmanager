import sys
import re
from PyQt5 import uic
from PyQt5.Qt import QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QHeaderView, QMessageBox
from Student import Student


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("studentmanager.ui", self)
        self.build_ui()
        self._error_message = ""

    def build_ui(self):
        self.ui.btn_add.clicked.connect(self.add_student)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_delete.clicked.connect(self.delete_student)

        self.ui.tbl_students.setColumnCount(4)
        self.ui.tbl_students.setHorizontalHeaderLabels(("Name", "Surname", "Email", "DOB"))
        self.ui.tbl_students.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_students()

    def load_students(self) -> None:
        for i in reversed(range(self.ui.tbl_students.rowCount())):
            self.ui.tbl_students.removeRow(i)

        Student.load_from_file()
        r = 0
        for s in Student.STUDENT_LIST:
            self.ui.tbl_students.insertRow(r)
            self.ui.tbl_students.setItem(r, 0, QTableWidgetItem(s.name))
            self.ui.tbl_students.setItem(r, 1, QTableWidgetItem(s.surname))
            self.ui.tbl_students.setItem(r, 2, QTableWidgetItem(s.email))
            self.ui.tbl_students.setItem(r, 3, QTableWidgetItem(s.dob.strftime("%d/%m/%Y")))
            r += 1

    def is_valid_input(self) -> bool:
        is_valid = True
        if not self.ui.txt_name.text():
            self._error_message += "Student Name is missing.\n"
            is_valid = False
        if not self.ui.txt_surname.text():
            self._error_message += "Student Surname is missing.\n"
            is_valid = False
        if not self.ui.txt_email.text():
            self._error_message += "Student Email is missing.\n"
            is_valid = False
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.ui.txt_email.text()):
            self._error_message += "Email address is invalid"
            is_valid = False

        return is_valid

    def add_student(self) -> None:

        if not self.is_valid_input():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(self._error_message)
            msg.setWindowTitle("Error in Entry")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            self._error_message = ""
            return

        name = self.ui.txt_name.text()
        surname = self.ui.txt_surname.text()
        email = self.ui.txt_email.text()
        dob = self.ui.cal_dob.selectedDate().toPyDate()
        Student(name, surname, email, dob)
        Student.save_to_file()
        self.clear_form()
        self.load_students()

    def clear_form(self) -> None:
        self.ui.txt_name.clear()
        self.ui.txt_surname.clear()
        self.ui.txt_email.clear()
        self.ui.cal_dob.setSelectedDate(QDate.currentDate())

    def delete_student(self) -> None:
        rows = sorted(set(index.row() for index in
                          self.ui.tbl_students.selectedIndexes()))

        if len(rows) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please select a student to delete")
            msg.setWindowTitle("No Student Selected")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        ask = QMessageBox()
        ask.setIcon(QMessageBox.Question)
        ask.setText("Are you sure you want to delete this student")
        ask.setWindowTitle("Really delete student")
        ask.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ask.activateWindow()
        user_choice = ask.exec_()

        if user_choice == QMessageBox.No:
            return

        for row in rows:
            Student.STUDENT_LIST.pop(row)

        Student.save_to_file()
        self.load_students()


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
