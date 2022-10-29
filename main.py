from entities import entities
from xlsx_to_txt import xlsx_to_txt  # thanks to Rahul for creating this

from random import randint, shuffle 
from termcolor import colored as coloured, cprint
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


    """
    subjects_with_2_periods = []
    # finds out which subjects need two periods
    for subject in subjects:
        if subject.multiple_periods:
            subjects_with_2_periods.append(subject.ID)

    # moves all subjects that need 2 periods to the front of the priority 
    for target_value in subjects_with_2_periods:
        subject_placement_priority.remove(target_value)
        subject_placement_priority.insert(0, target_value)
    """

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
            if i.ID == subject:   # if the name of the subject matches the name of the class

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


def create_random_timetable (timetable: list, students: list, teachers: list, subjects: list, rooms: list) -> list:
    """
    Creates a completely random timetable that may or may not work. 
    """
    LGcounter = 0 # this is the ID of the lessons created

    list_subjects = []
    for i in subjects:
        list_subjects.append(i.ID) # creates a list of subject IDs. e.g. sciY8

    students_subjects = []  # a list of tuples containing student subject pairs. e.g. (Rahul, physY12)
    for student in students:   
        for subject in student.subjects:  # iterates through each subject the student takes
            student_subject = (f'{student.forename} {student.surname}', subject)   # creates a student subject pair
            students_subjects.append(student_subject)   # appends the pair to a list

    teachers_subjects = [] # a list of tuples containing teacher subject pairs
    for teacher in teachers:
        for subject in teacher.subjects_they_can_teach: # iterates through each subject the teacher can teach
            teacher_subject = (f'{teacher.forename} {teacher.surname}', subject) # creates a teacher subject pair
            teachers_subjects.append(teacher_subject) # appedn the pair to a list

    while True:

        print('Picking random subject...')
        subject_ready = False
        while subject_ready is False:

            if students_subjects == []: # checks if all subject have been placed
                print('No subjects left to place! Random timetable complete!!!')
                return timetable  # returns the randomly generated timetable

            else:
                subject = subject[randint(0, len(subject)-1)] # picks a random subject out of the list: subjects

                subjects_left_to_place = []
                for i in student_subject: # for student subject pair in ...
                    subjects_left_to_place.append(i[1]) # append subject to list
                
                if subject in subjects_left_to_place: # if the subject is still not fully placed
                    subject_ready = True  # subject ready = True so while loop is ended

                
        print(f'Random subject picked : {subject.name}')

        teachers_for_LG = []

        print('Finding random teachers for subject...')
        for teacher in shuffle(teachers): # iterates through teachers in a random order
            print(f'Checking : {teacher.forename} {teacher.surname}')

            # checks if the LG already has enough teachers and if the teacher can teach that subject
            if len(teachers_for_LG) != subject.number_of_teachers and teacher.subjects_they_can_teach == subject.ID:
                teachers_for_LG.append(teacher)
                cprint(f'{teacher.forename} {teacher.surname} Successful added to lesson group!', 'green')
            else:
                print('Nope!')

        cprint(f'Teachers found : {teachers_for_LG}', 'green')

        students_for_LG = []

        print('Finding student for LG...')

        while len(students_for_LG) > subject.max_students: # whil;e the LG is not full
            poss_stud_pair = students_subjects[randint[0, len(students_subjects)-1]] #picks a random student subject pair
            print(f'Checking : {poss_stud_pair[0]}...')
            
            if poss_stud_pair[1] == subject.ID: # if the subject = the ID of the subject
                students_for_LG.append(poss_stud_pair[1])  # add student to teaching group
                cprint(f'{poss_stud_pair[0]} Succefully added to lesson group!', 'green')
                students_subjects.remove(poss_stud_pair)  # remove student subject pair from student subject pairs
            else:
                print('Nope!')

        cprint(f'Students found : {students_for_LG}', 'green')
            
                
                
        
    

    



def main () -> None:
    
    print('Starting...') # starting sequence: collects data from spreadsheet

    print('Converting spreadsheets to text...')
    xlsx_to_txt()
    print(coloured('Finished converting spreadsheets to text!', 'cyan'))

    print('Loading infomation from text...')  # converts text information to classes
    students = entities.student.load_students('students.txt')
    teachers = entities.teacher.load_teachers('teachers.txt')
    subjects = entities.subject.load_subjects('subjects.txt')
    rooms = entities.room.load_rooms('rooms.txt')
    print(coloured('All information loaded!', 'magenta'))

    print(coloured('Starting sequence finished!', 'cyan', 'on_magenta'))

    """
    print('Displaying all information...')
    for student in students:
        entities.student.display_info(student)
    for teacher in teachers:
        entities.teacher.display_info(teacher)
    for subject in subjects:
        entities.subject.display_info(subject)
    for room in rooms:
        entities.room.display_info(room)
    """

    students_in_subjects = count_students_in_subjects (students) # finds the number of students who take each subject
    print(f'Number of students in each subject: {students_in_subjects}')

    print(f"{coloured('Ideal num of teaching group and size', attrs = ['bold', 'underline'])} : {find_teaching_group_size(subjects, students_in_subjects)}")

    placement_priority = find_subject_placement_priority(students_in_subjects, subjects)  # atm this is based on subject popularity, this could lead to the program being less effient
    print(f'Subject placement priority [note: needs fixing to increase efficiency]: {placement_priority}')


    print('Creating blank timetable...')
    timetable = create_blank_timetable()  # creates a blank timetable
    cprint('Blank timetable created!')


if __name__ == '__main__':
    main ()