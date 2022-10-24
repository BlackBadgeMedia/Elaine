
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
        def __init__ (self, ID: str, name: str, possible_teaching_periods: tuple, possible_rooms: tuple, multiple_periods: bool = False) -> None:
            self.ID = ID 
            self.name = name
            self.possible_teaching_periods = possible_teaching_periods  # what times of the day can a subject be taught e.g. [YP1, GP5]
            self.possible_rooms = possible_rooms # these are the rooms in which a subject can be taught e.g. [H1.2, H2.4]
            self.multiple_periods = multiple_periods # does the lesson need 1 or 2 periods to teach. For example 6th form chemistry takes up 2 periods.
            

def main ():
    pass


if __name__ == '__main__':
    main ()

