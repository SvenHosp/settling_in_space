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
    
    def populate_starsystem(
        self,
        system_size=0,
        system_objects=[]
    ):
        """
        method to populate the starsystem
        
        param system_size(int): size of starsystem
        param system_objects(List): list of StarSystenNaturalObjectModel
        """
        self.system_size = system_size
        self.system_objects = system_objects
        
    def move_natural_objects_through_system(self):
        """
        moves all natural objects in star system
        """
        for obj in self.system_objects:
            obj.move_object_through_starsystem()
    
    def create_from_dict(self):
        """
        method to create starsystem from dict
        """
        pass

class StarSystemNaturalObjectModel():
    """
    model for star system objects like planets, moon or
    meteorits
    """
    
    def __init__(
        self,
        speed=1,
        var_a=1,
        var_b=1,
        var_z=0,
        angle=1,
        name=''
    ):
        """
        init method
        
        param speed(int): speed of StarSystemObject
        param var_a(int): ellipse parameter
        param var_b(int): ellipse parameter
        param var_z(int): ellipse parameter
        param angle(float): ellipse parameter
        param name(String): name of object
        """
        self.speed = speed
        self.var_a = var_a
        self.var_b = var_b
        self.var_z = var_z
        self.angle = angle
        self.x = 0
        self.y = 0
        self.z = 0
        self.position = [0,0,0]
        self.move_object_through_starsystem(init=True)
        
        self.name = name
    
    def move_object_through_starsystem(
        self,
        init=False
    ):
        """
        moves object through the starsystem
        
        param init(boolean): if it is an init move then angle
        should not be incremented
        """
        import numpy
        
        if not init:
            self.angle = (self.angle + self.speed) % 360
        self.x = self.var_a * numpy.cos(self.angle)
        self.y = self.var_b * numpy.sin(self.angle)
        self.z = self.var_z * numpy.sin(self.angle)
        self.position = [self.x, self.y, self.z]
    
    
    