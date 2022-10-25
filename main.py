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

    class subject ():
        """
        Holds information about individual subjects. e.g. physY9
        """
        def __init__ (self, ID: str, name: str, possible_teaching_periods: tuple, possible_rooms: tuple, how_many_teaching_periods: int, min_students: str, max_students: int, multiple_periods: bool = False) -> None:
            self.ID = ID 
            self.name = name
            self.possible_teaching_periods = possible_teaching_periods  # what times of the day can a subject be taught e.g. [YP1, GP5]
            self.possible_rooms = possible_rooms # these are the rooms in which a subject can be taught e.g. [H1.2, H2.4]
            self.multiple_periods = multiple_periods # does the lesson need 1 or 2 periods to teach. For example 6th form chemistry takes up 2 periods.
            self.min_students = min_students # the mininum number of student required for this subject
            self.max_students = max_students # the maximum number of students needed for this subject
            self.how_many_teaching_periods = how_many_teaching_periods # the number of teaching periods the subject requires per cycle

    class room ():
        """
        Holds information about rooms.
        """
        def __init__(self, ID: str, name: str, max_capacity: int) -> None:
            self.ID = ID
            self.name = name
            self.max_capacity = max_capacity # the maximum number of students that can be taught in this room

            

def main ():
    pass


if __name__ == '__main__':
    main ()

