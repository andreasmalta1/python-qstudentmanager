import datetime
import os
from typing import List
import jsonpickle


class Student:
    STUDENT_LIST: List = []

    def __init__(self, name: str, surname:str, email: str, dob: datetime.date):
        self.name: str = name
        self.surname: str = surname
        self.email: str = email
        self.dob: datetime.date = dob
        Student.STUDENT_LIST.append(self)

    @staticmethod
    def save_to_file () -> None:
        json_object = jsonpickle.encode(Student.STUDENT_LIST, unpicklable=False)
        with open("students.json", "w") as outfile:
            outfile.write(json_object)

    @staticmethod
    def load_from_file() -> None:
        Student.STUDENT_LIST.clear()

        if not os.path.isfile("students.json") or not os.path.getsize("students.json") > 0:
            return

        with open("students.json") as infile:
            json_object = infile.read()
            dictionary = jsonpickle.decode(json_object)
            for item in dictionary:
                Student(item["name"],
                        item["surname"],
                        item["email"],
                        datetime.datetime.strptime(item["dob"], "%Y-%m-%d").date())
