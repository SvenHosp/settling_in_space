"""
starsystem module
"""

class StarSystemModel():
    """
    model class for star systems
    """
    
    def __init__(
        self,
        position=[0,0,0],
        name=''
    ):
        """
        init method
        
        param position([x(int),y(int),z(int)]): list of x,y,z coordinates
        param name(String): name of star system
        """
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.position = position
        self.name = name
        pass
    
    def create_from_dict(self):
        """
        method to create starsystem from dict
        """
        pass

class StarSystenNaturalObjectModel():
    """
    model for star system objects like planets, moon or
    meteorits
    """
    
    def __init__(self):
        """
        init method
        """
        pass
    
    