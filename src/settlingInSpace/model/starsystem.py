"""
starsystem module
"""
import numpy

class StarSystemModel():
    """
    model class for star systems
    """
    
    def __init__(
        self,
        position=None,
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
        list_system_objects=[]
    ):
        """
        method to populate the starsystem
        
        param system_size(int): size of starsystem
        param list_system_objects(List): list of StarSystenNaturalObjectModel
        """
        self.system_size = system_size
        self.list_system_objects = list_system_objects
        
    def move_natural_objects_through_system(self):
        """
        moves all natural objects in star system
        """
        for obj in self.list_system_objects:
            obj.move_object_around()
    
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
        name='',
        moving_reference=None,
        list_satellite_objects=[]
    ):
        """
        init method
        
        param speed(int): speed of StarSystemObject
        param var_a(int): ellipse parameter
        param var_b(int): ellipse parameter
        param var_z(int): ellipse parameter
        param angle(float): ellipse parameter
        param name(String): name of object
        param moving_reference(StarSystemModel or StarSystemNaturalObjectModel): reference to move around
        param list_satellite_objects(list of StarSystemNaturalObjectModel): list of natural satellite objects
        """
        self.speed = speed
        self.var_a = var_a
        self.var_b = var_b
        self.var_z = var_z
        self.angle = angle
        self.position = numpy.array([0, 0, 0])
        
        self.name = name
        
        self.moving_reference = moving_reference
        
        self.list_satellite_objects = list_satellite_objects
        
        self.move_object_around()
    
    def move_object_around(
        self,
        init=False
    ):
        """
        moves object through the starsystem
        
        param init(boolean): if it is an init move then angle
        should not be incremented
        """
        self.angle = (self.angle + self.speed) % 360
        
        _x = self.var_a * numpy.cos(self.angle)
        _y = self.var_b * numpy.sin(self.angle)
        _z = self.var_z * numpy.sin(self.angle)
        
        _position = numpy.array([_x, _y, _z])
        
        self.position = _position if not isinstance(self.moving_reference, StarSystemNaturalObjectModel) else _position + self.moving_reference.position
        
        for satellite in self.list_satellite_objects:
            satellite.move_object_around()
    
    
    