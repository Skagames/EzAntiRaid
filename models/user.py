"""
This model is a representation of a person, who is in multiple servers OR
it is a representation of a member, who is a user IN a server
"""

# imports


# user class
class user():
    """
    Attributes:
    - uid: the id the user has
    - flags: integer representing the user flags
        - 1 << 0: user is verified human
        - 1 << 1: user is marked as spammer
        - 1 << 2: user has been banned by auto-raid before
        - 1 << 3: user should always be banned by default

    Methods:
    - __save: saves the user to the database
    - __load: loads the user from the database
    - __quicksave: saves the user to the database and loads it again

    - add_flag: adds a flag
    - remove_flag: removes a flag
    - fetch_flags: fetches the list of flags the user has

    """
    def __init__(self, **kwargs) -> None:
        """
        
        """
        pass


# member class
class member(user):
    """
    This class is a child class of the user, it serves as a possibility to make
    serverside decisions such as kick and ban
    """
    def __init__(self, **kwargs) -> None:
        """
        
        """
        super().__init__(**kwargs)