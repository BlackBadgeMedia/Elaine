from entities import entities
from xlsx_to_txt import xlsx_to_txt  # thanks to Rahul for creating this

from termcolor import colored as coloured
from math import ceil

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


def find_teaching_group_size (subjects: list, students_in_subjects: dict) -> dict:
    """
    Find how many teaching groups are needed per subject and what the ideal group size for each teaching group would be. \n
    Returns a dictionary - {'subject name': ['num of groups', 'ideal num of students per group']} \n
    """

    teaching_group_sizes = {}

    for subject in students_in_subjects: # for subject in dict: students in subjects
        students_who_take_subject = students_in_subjects[subject]  # the num of students who take that subject

        for i in subjects:  # for subject[class] in subjects[list of classes] 
            if i.name == subject:   # if the name of the subject matches the name of the class

                # checks if the number of students who take the class is within min and max students
                if i.min_students <= students_who_take_subject and i.max_students >= students_who_take_subject: 
                    teaching_group_sizes[subject] = [1, students_who_take_subject]  # if true will set the numbers of teaching groups to 1 and the number of students who take that subject
                else:
                    num_of_groups = ceil(students_who_take_subject / i.max_students) # finds the number of groups if they have max students, rounds up
                    teaching_group_sizes[subject] = [num_of_groups, ceil(students_who_take_subject / num_of_groups)]
        
    return teaching_group_sizes
        

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


def place_subject (timetable: list, lesson, week: int, day: int, period: int) -> list:
    """
    Places a subject in the timetable. 
    """
    p = timetable[week][day][period]   # locations the period the lesson needs to be placed in
    p.append(lesson)

    timetable[week][day][period] = p # places period back into timetable

    return timetable



def main () -> None:
    
    print('Starting...')

    print('Converting spreadsheets to text...')
    xlsx_to_txt()
    print(coloured('Finished converting spreadsheets to text!', 'cyan'))

    print('Loading infomation from text...')
    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')
    rooms = entities.room.load_rooms('rooms.txt')
    print(coloured('All information loaded!', 'magenta'))

    print(coloured('Starting sequence finished!', 'cyan', 'on_magenta'))

    students_in_subjects = count_students_in_subjects (students)
    timetable = create_blank_timetable()

    for student in students:
        entities.student.display_info(student)
    for teacher in teachers:
        entities.teacher.display_info(teacher)
    for subject in subjects:
        entities.subject.display_info(subject)
    for room in rooms:
        entities.room.display_info(room)

    print(students_in_subjects)

    print(find_teaching_group_size(subjects, students_in_subjects))





if __name__ == '__main__':
    main ()