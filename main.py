from entities import entities

def count_students_in_subjects (students: list) -> dict:
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
            
def find_subject_placement_priority (num_of_students_in_subjects: dict, subjects: list) -> list:
    """
    Finds out which subjects the program should place in the timetable first. \n
    This is to speed up the algortith. \n
    Returns a list with the order in which the program should place subjects. 
    """
    subject_placement_priority = []

    return subject_placement_priority

def main () -> None:
    print('Starting...')
    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')
    rooms = entities.room.load_rooms('rooms.txt')

    print(count_students_in_subjects(students))


if __name__ == '__main__':
    main ()

