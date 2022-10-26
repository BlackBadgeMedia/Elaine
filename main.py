from entities import entities


def main () -> None:

    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')


if __name__ == '__main__':
    main ()

