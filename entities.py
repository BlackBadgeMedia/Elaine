from termcolor import colored as coloured

class entities ():
    """
    Contains building blocks for entities. 
    """
    
    class student ():
        """
        Holds information about individual students.
        """
        def __init__ (self, ID: str, surname: str, forename: str, subjects: tuple) -> None:
            self.ID = ID
            self.surname = surname
            self.forename = forename
            self.subjects = subjects # these are the subjects the student has chosen to take e.g. chemY13

        def load_students (input_file: str) -> tuple:
            """
            Collects information about students from a specified file.\n
            It then converts that data to objects then stores them in a list.
            """

            print('Loading students...')

            students = []

            with open(input_file, 'r') as file: # opens input file note: there is no data cleansing so input data must be clean
                lines = file.read().split('\n')  # splits input file into individual lines

            for line in lines: 
                info = line.split(' | ')  # splits the line into sections based on ' | '
                students.append(
                    entities.student(
                        ID = info[0],
                        surname = info[1],
                        forename = info[2],
                        subjects = tuple(info[3].split(', ')),  # splits the last section into a list and then a tuple because a student can have multiple subjects
                    )
                )

            print(f"{coloured('Loading Complete!', 'green', attrs = ['bold'])}")

            return tuple(students) 

        def display_info (*args) -> None:
            """
            Displays the information of one or more students at a time.
            """

            for i in args:
                print('-------------------------------')
                print(f'ID: {coloured(i.ID, "magenta", attrs = ["bold"])}')
                print(f'Surname: {coloured(i.surname, "magenta", attrs = ["bold"])}')
                print(f'Forename: {coloured(i.forename, "magenta", attrs = ["bold"])}')
                print(f'Subjects: {coloured(i.subjects, "magenta", attrs = ["bold"])}')
                print('-------------------------------')



    class teacher ():
        """
        Holds information about individual teachers.
        """
        def __init__ (self, ID: str, surname: str, forename: str, subjects_they_can_teach: tuple, working_periods: tuple) -> None:
            self.ID = ID
            self.surname = surname
            self.forename = forename
            self.subjects_they_can_teach = subjects_they_can_teach # these are the subjects the teacher can teach e.g. mathY10set2a
            self.working_periods = working_periods  # these are the periods the teachers are working e.g. cycle1TUESp5

        def load_teachers (input_file: str) -> tuple:
            """
            Collects information about teachers from a specified file.\n
            It then converts that data to objects then stores them in a list.
            """

            print('Loading teachers...')

            teachers = []

            with open(input_file, 'r') as file: 
                lines = file.read().split('\n')

            for line in lines:
                info = line.split(' | ')

                teachers.append(
                    entities.teacher(
                        ID = info[0],
                        surname = info[1],
                        forename = info[2],
                        subjects_they_can_teach = tuple(info[3].split(', ')),
                        working_periods = tuple(info[4].split(', ')),
                    )
                )

            print(f"{coloured('Loading Complete!', 'green', attrs=['bold'])}")

            return tuple(teachers)

        def display_info (*args) -> None:
            """
            Displays the information about one or more teachers.
            """
            for i in args:
                print('-------------------------------')
                print(f'ID: {coloured(i.ID, "cyan", attrs = ["bold"])}')
                print(f'Surname: {coloured(i.surname, "cyan", attrs = ["bold"])}')
                print(f'Forename: {coloured(i.forename, "cyan", attrs = ["bold"])}')
                print(f'Subjects they can teach: {coloured(i.subjects_they_can_teach, "cyan", attrs = ["bold"])}')
                print(f'Working periods: {coloured(i.working_periods, "cyan", attrs = ["bold"])}')
                print('-------------------------------')



    class subject ():
        """
        Holds information about individual subjects. e.g. physY9
        """
        def __init__ (self, ID: str, name: str, possible_teaching_periods: tuple, possible_rooms: tuple, how_many_teaching_periods: int, min_students: int, max_students: int, number_of_teachers: int, multiple_periods: bool = False) -> None:
            self.ID = ID 
            self.name = name
            self.possible_teaching_periods = possible_teaching_periods  # what times of the day can a subject be taught e.g. [YP1, GP5]
            self.possible_rooms = possible_rooms # these are the rooms in which a subject can be taught e.g. [H1.2, H2.4]
            self.multiple_periods = multiple_periods # does the lesson need 1 or 2 periods to teach. For example 6th form chemistry takes up 2 periods.
            self.min_students = min_students # the mininum number of student required for this subject
            self.max_students = max_students # the maximum number of students needed for this subject
            self.number_of_teachers = number_of_teachers
            self.how_many_teaching_periods = how_many_teaching_periods # the number of teaching periods the subject requires per cycle

        def load_subjects (input_file: str) -> tuple:
            """
            Collects information about different subjects from the specified file.
            """

            print('Loading subjects...')

            subjects = []

            with open(input_file, 'r') as file:
                lines = file.read().split('\n')

            for line in lines:
                info = line.split(' | ')

                subjects.append(
                    entities.subject(
                        ID = info[0],
                        name = info[1],
                        possible_teaching_periods = tuple(info[2].split(', ')),
                        possible_rooms = tuple(info[3].split(', ')),
                        how_many_teaching_periods = int(info[4]),
                        min_students = int(info[5]),
                        max_students = int(info[6]),
                        number_of_teachers = int(info[7]),
                        multiple_periods = bool(info[8]),
                    )
                )
            
            print(coloured('Loading Complete!', 'green', attrs = ['bold']))

            return tuple(subjects)
    class room ():
        """
        Holds information about rooms.
        """
        def __init__(self, ID: str, name: str, max_capacity: int) -> None:
            self.ID = ID
            self.name = name
            self.max_capacity = max_capacity # the maximum number of students that can be taught in this room

    class lesson ():
        """
        This is the building block for every timetable. \n
        Holds information about the teacher, the rooms, the teaching periods and the students.
        """
        def __init__(self, ID: str, name: str, teachers: list, periods_and_rooms: list, students: list, subjectID: str) -> None:
            self.ID = ID
            self.name = name
            self.teachers = teachers
            self.periods_and_rooms = periods_and_rooms
            self.students = students
            self.subjectID = subjectID