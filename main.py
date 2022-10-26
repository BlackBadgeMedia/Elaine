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


def find_subject_placement_priority (num_of_students_in_subjects: dict, subjects: tuple) -> list:
    """
    Finds out which subjects the program should place in the timetable first. \n
    This is to speed up the algortithm. \n
    Returns a list with the order in which the program should place subjects. 
    """
    subject_placement_priority = []

    # places subject priority based on frequency
    for i in dict(sorted(num_of_students_in_subjects.items(), key = lambda x:x[1], reverse = True)):
        subject_placement_priority.append(i)

    subjects_with_2_periods = []
    # finds out which subjects need two periods
    for subject in subjects:
        if subject.multiple_periods:
            subjects_with_2_periods.append(subject.ID)

    # moves all subjects that need 2 periods to the front of the priority 
    for target_value in subjects_with_2_periods:
        subject_placement_priority.remove(target_value)
        subject_placement_priority.insert(0, target_value)

    return subject_placement_priority

def create_blank_timetable () -> list:
    blank_timetable = [
        [ # week 1
            [ #MON
                [], [], [], [], [], # p1, p2, p3, p4, p5,
            ],
            [ #TUE
                [], [], [], [], [],   
            ],
            [ #WED
                [], [], [], [], [], 
            ],
            [ #THU
                [], [], [], [], [],  
            ],
            [ #FRI
                [], [], [], [], [],
            ],
        ],
        [ # week 2
            [ #MON
                [], [], [], [], [],
            ],
            [ #TUE
                [], [], [], [], [],
            ],
            [ #WED
                [], [], [], [], [],                
            ],
            [ #THU
                [], [], [], [], [],                
            ],
            [ #FRI
                [], [], [], [], [],
            ],
        ],
    ]

    return blank_timetable

def main () -> None:
    print('Starting...')
    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')
    rooms = entities.room.load_rooms('rooms.txt')
    print('All information loaded.')



if __name__ == '__main__':
    main ()

