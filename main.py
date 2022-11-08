from entities import entities
from xlsx_to_txt import xlsx_to_txt  # thanks to Rahul for creating this

from random import randint, shuffle 
import random
from termcolor import colored as coloured, cprint
from math import ceil

# Settings ------------------------------------------------- # 
printALLinfo = True    # this prints all information at every step of the program, useful for debugging but is otherwise very messy
printSOMEinfo = True   # this prints the data about finished groups, so still a lot but is tidier that printALLinfo
printGUIonly = False   # this enables the GUI in the terminal, printALLinfo and printSOMEinfo must both be false for this to work
# ---------------------------------------------------------- # 

def cprintIF (text: str, colour: str, on_colour: str, attrs: list,  Print: bool) -> None:
    """
    Only prints if Print == True. \n
    This is useful for debugging and print settings.
    """

    if Print: return cprint(text, colour, on_colour, attrs,)
  
    
def convert_nums_to_loc (week: int, day: int, period: int) -> str:
    """
    Converts the list indexes in a timetable to a string that humans can understand.
    For example convert_nums_to_loc(0,0,0) = w1MONp1
    """

    weeks = {
        0: 'w1',
        1: 'w2',
    }

    days = {
        0: 'MON',
        1: 'TUE',
        2: 'WED',
        3: 'THU',
        4: 'FRI',
    }

    periods = {
        0: 'p1',
        1: 'p2',
        2: 'p3',
        3: 'p4',
        4: 'p5',
    }

    return f'{weeks[week]}{days[day]}{periods[period]}'


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

    list_subjects = []
    for i in subjects:
        list_subjects.append(i.ID) # creates a list of subject IDs. e.g. sciY8

    students_subjects = []  # a list of tuples containing student subject pairs. e.g. (Rahul, physY12)
    for student in students:   
        for subject in student.subjects:  # iterates through each subject the student takes
            student_subject = (f'{student.forename} {student.surname}', subject)   # creates a student subject pair
            students_subjects.append(student_subject)   # appends the pair to a list

    '''
    teachers_subjects = [] # a list of tuples containing teacher subject pairs
    for teacher in teachers:
        for subject in teacher.subjects_they_can_teach: # iterates through each subject the teacher can teach
            teacher_subject = (f'{teacher.forename} {teacher.surname}', subject) # creates a teacher subject pair
            teachers_subjects.append(teacher_subject) # appedn the pair to a list
    '''

    LGcounter = 0 # this is the ID of the lessons created
    while True:

        print('Picking random subject...')
        subject_ready = False
        while subject_ready is False:
            
            if students_subjects == []: # checks if all subject have been placed
                print('No subjects left to place! Random timetable complete!!!')
                return timetable  # returns the randomly generated timetable

            else:
                subject = subjects[randint(0, len(subjects)-1)] # picks a random subject out of the list: subjects

                subjects_left_to_place = []
                for i in students_subjects: # for student subject pair in ...
                    subjects_left_to_place.append(i[1]) # append subject to list
                
                if subject.ID in subjects_left_to_place: # if the subject is still not fully placed
                    subject_ready = True  # subject ready = True so while loop is ended
                    print(f'{subject.ID} chosen!')
                else:
                    print('Nope!')

        LGcounter += 1
                
        print(f'Random subject picked : {subject.name}')

        teachers_for_LG = []

        print('Finding random teachers for subject...')
        def rand ():
            return randint(0,10) / 10
        for teacher in set(teachers): # iterates through teachers in a random order
            print(f'Checking : {teacher.forename} {teacher.surname}')

            # checks if the LG already has enough teachers and if the teacher can teach that subject
            if len(teachers_for_LG) != subject.number_of_teachers and subject.ID in teacher.subjects_they_can_teach:
                teachers_for_LG.append(teacher)
                cprint(f'{teacher.forename} {teacher.surname} successfully added to lesson group!', 'green')
            else:
                print('Nope!')

        cprint(f'Teachers found : {teachers_for_LG}', 'green')

        students_for_LG = []

        print('Finding student for LG...')

        no_students_left = False
        while len(students_for_LG) < subject.max_students and no_students_left == False: # whille the LG is not full and there are students left to place
            try:
                poss_stud_pair = students_subjects[randint(0, len(students_subjects)-1)] #picks a random student subject pair
            except ValueError:
                break

            print(f'Checking : {poss_stud_pair[0]}...')
            
            if poss_stud_pair[1] == subject.ID: # if the subject = the ID of the subject
                students_for_LG.append(poss_stud_pair[0])  # add student to teaching group
                cprint(f'{poss_stud_pair[0]} Succefully added to lesson group!', 'green')
                students_subjects.remove(poss_stud_pair)  # remove student subject pair from student subject pairs
            else:
                print('Nope!')

                p_left = []  # pupils left
                for i in students_subjects: # for student subject pair in students subjects pairs
                    p_left.append(i[1]) # append subjetc

                if subject.ID not in p_left:  # if no people left to place in subject
                    no_students_left = True # end while loop


        cprint(f'Students found : {students_for_LG}', 'green')

        print('LG created!!!')

        num_of_p_for_LG = int(subject.how_many_teaching_periods) # the number of periods the subject needs

        print(f'{subject.name} needs {num_of_p_for_LG} periods.')
        print('Placing lessons for LG...')

        subjects_pos_placed = [] # a list of the positions a subject has been placed
        LG_pos = [] # the positions and rooms of the subject in the timetable
        while num_of_p_for_LG != 0:
            p = subject.possible_teaching_periods[randint(0, len(subject.possible_teaching_periods)-1)]

            room = subject.possible_rooms[randint(0, len(subject.possible_rooms)-1)]
            print(f'Checking {p} {room}')

            if p not in subjects_pos_placed:
                LG_pos.append((p, room))
                cprint(f'{subject.ID} placed {room} at {p}!', 'magenta')
                num_of_p_for_LG -= 1 # one less leson to place
            else:
                print('Nope!')

        lesson = entities.lesson(   # creating the lesson object
                ID = f'LG{LGcounter}',
                name = subject.name,
                teachers = teachers_for_LG,
                periods_and_rooms = LG_pos,
                students = students_for_LG,
                subjectID = subject.ID,
                )
        cprint('Lesson created!', 'green', attrs = ['bold'])
        entities.lesson.display_info(lesson)

        print('Placing lessons in timetable...')

        days = {
            'MON': 0,
            'TUE': 1,
            'WED': 2,
            'THU': 3,
            'FRI': 4
            }
        for i in LG_pos:
            p = i[0]
            room = i[1]
            place_subject(
                timetable,
                lesson,
                week = (int(p[1])-1),
                day = days[p[2:5]],
                period = (int(p[6])-1),
            )
            print(f'{subject.ID} placed {room} at {p} in timetable!')


def check_timetable (timetable: list, students: tuple, teachers: tuple, subjects: tuple, rooms:tuple) -> bool:
    """
    Checks to see if a timetable works. 
    """
    for x, week in enumerate(timetable):  # for week in timetable

        for y, day in enumerate(week):    # for day in week
            # find lessons that happen this day
            lessons_this_day = []
            for period in day:
                for lesson in period:
                    lessons_this_day.append(lesson.ID)
            
            print(f'Lessons this day : {lessons_this_day}')
            
            # checks if lessons happen more than once in a day [except for lessons that need two consecutive periods]
            print('Checking if lessons do not occur twice in one day...')
            subjects_that_need_two_periods = []
            for subject in subjects:
                if subject.multiple_periods:
                    subjects_that_need_two_periods.append(subject.ID)

            lessons_that_need_two_periods = []
            for lesson in period:
                if lesson.subjectID in subjects_that_need_two_periods:
                    lessons_that_need_two_periods.append(lesson.ID)  

            lesson_counter = {}
            for lesson in lessons_this_day:
                if lesson_counter[lesson] == 1: lesson_counter[lesson] += 1      
                else: lesson_counter[lesson] = 1
            print(lesson_counter)

            for lesson in lesson_counter:
                if lesson_counter[lesson] > 2:
                    cprint('Timetable failed!', 'red')
                    return False
                elif lesson_counter[lesson] > 1 and lesson not in lessons_that_need_two_periods:
                    cprint('Timetable failed!', 'red')
                    return False



            for z, period in enumerate(day):   # for period in day
                # find the lessons that happen this period
                lessons_this_period = []
                for i, lesson in enumerate(period):
                    lessons_this_period.append(lesson)


                    
                    for subject in subjects: # for subject in subjects
                        if subject.ID == lesson.subjectID:  # if subject ID of object == subjectID of lesson
                            
                            # checks if double period subjects are accounted for 
                            if subject.multiple_periods:   # if the subject needs two consecutive periods
                                if z == 2:   # if the period is 3 return false. bc if the subject needs two consecutive periods it can't be p3
                                    cprint('Timetable failed', 'red')
                                    return False 
                            
                            elif lesson.ID not in day[z + 1]: # if the lesson group is not taught in the next period return false
                                cprint('Timetable failed!', 'red')
                                return False

                            # checks if a lesson has more than its max capacity
                            if len(lesson.students) > subject.max_students:
                                cprint('Timetable failed!', 'red')
                                return False

                            #checks if the subject has less than its min capacity
                            elif len(lesson.students) < subject.min_students:
                                cprint('Timetable failed!', 'red')
                                return False


                            # checks if the room the lesson is overfilled and if a subject can be teached in a room
                            for i, v in lesson.periodsandrooms:  # for period, room in periods and rooms
                                for room in rooms:  # for room object in room objects
                                    if room.ID == v:  # if the room ID equals the room the lesson is in
                                        if len(lesson.students) > room.max_capacity:  # checks if the room is overfilled
                                            cprint('Timetable failed!', 'red')
                                            return False

                                # checks if a lesson can be taught in a specific room
                                if v not in subject.possible_rooms:
                                        cprint('Timetable failed!', 'red')
                                        return False                                    
                        

                            # checks if lessons are not on the same day
                            


                            


                    
def display_lessongroup_timetable (timetable: list, lesson_group) -> None:
    """
    Prints the timetable of a lesson group. \n
    This is easier for a human to understand.
    """

    w1MONp1 = ''
    w1MONp2 = ''
    w1MONp3 = ''
    w1MONp4 = ''
    w1MONp5 = ''

    w2MONp1 = ''
    w2MONp2 = ''
    w2MONp3 = ''
    w2MONp4 = ''
    w2MONp5 = ''

    w1TUEp1 = ''
    w1TUEp2 = ''
    w1TUEp3 = ''
    w1TUEp4 = ''
    w1TUEp5 = ''

    w2TUEp1 = ''
    w2TUEp2 = ''
    w2TUEp3 = ''
    w2TUEp4 = ''
    w2TUEp5 = ''

    w1WEDp1 = ''
    w1WEDp2 = ''
    w1WEDp3 = ''
    w1WEDp4 = ''
    w1WEDp5 = ''

    w2TUEp1 = ''
    w2TUEp2 = ''
    w2TUEp3 = ''
    w2TUEp4 = ''
    w2TUEp5 = ''

    outL0 = f"|------------GREEN------------|-----------YELLOW------------|"
    outL1 = f"| MON | TUE | WED | THU | FRI | MON | TUE | WED | THU | FRI |"
    outL2 = f"|{w1MONp1}|{w1MONp2}|{w1MONp3}|{w1MONp4}|{w1MONp5}|{w2MONp1}|{w2MONp2}|{w2MONp3}|{w2MONp4}|{w2MONp5}|"
    outL3 = f"|{w1TUEp1}|{w1TUEp2}|{w1TUEp3}|{w1TUEp4}|{w1TUEp5}|{w2TUEp1}|{w2TUEp2}|{w2TUEp3}|{w2TUEp4}|{w2TUEp5}|"
    outL4 = f""
    outL5 = f""


                    




                    


        


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

    print(create_random_timetable(timetable, list(students), list(teachers), list(subjects), list(rooms)))

    # prints out the entire timetable
    for week in timetable:
        for day in week:
            for period in day:
                for i in period:
                    entities.lesson.display_info(i)


if __name__ == '__main__':
    main ()