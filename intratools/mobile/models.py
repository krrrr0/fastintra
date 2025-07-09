class Student():
    def __init__(self, number, name, school_class=None, school_grade=None, username=None, sex=None, birthcode=None) -> None:
        self.number = number
        self.name = name
        self.school_class = school_class
        self.school_grade = school_grade
        self.username = username
        self.sex = sex
        self.birthcode = birthcode

        return

class ClassReservation():
    def __init__(self, purpose, created, status, title, classroom, noise, time, user, index=0) -> None:
        self.purpose = purpose
        self.created = created
        self.status = status
        self.title = title
        self.classroom = classroom
        self.noise = noise
        self.time = time
        self.user = user
        self.index = index

        return