from entities import entities

def count_students_in_subjects (students) -> dict:
    """
    Works out how many people take each subject. \n
    This is to workout which subjects are most popular to speed up \n
    lesson placement in the timetable.
    """
    num_of_students_in_subjects = {}

    for student in students:
        subjects = student.subjects

        for subject in subjects:
            if subject in num_of_students_in_subjects:
                num_of_students_in_subjects[subject] += 1
            else:
                num_of_students_in_subjects[subject] = 1

    return num_of_students_in_subjects
            

def main () -> None:
    print('Starting...')
    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')
    rooms = entities.room.load_rooms('rooms.txt')

    print(count_students_in_subjects(students))


if __name__ == '__main__':
    main ()

