"""
main gamemodel module
"""
import numpy
from .starsystem import StarSystemModel, StarSystemNaturalObjectModel

class GameModel():
    def __init__(self):
        """init method"""
        pass
    
    def configure(self):
        """
        configure Model
        """
        pass
    
    def initialize(
        self,
        number_points=40,
        list_starnames=[],
        list_starsystemnames=[],
        szenario_path=None
    ):
        """
        initialize Model
        
        param szenario_path(String): path to a scenario file to be loaded
        param number_points(int): absolute number of points
        param list_starnames(List): list of names for stars
        param list_starsystemnames(List): list of names for objects in starsystems
        """
        self.starnames = list_starnames
        self.starsystemnames = list_starsystemnames
        if(szenario_path is None):
            self.initialize_universe_random(
                number_points=number_points
            )
        else:
            pass
    
    def initialize_universe_random(
        self,
        number_points=40
    ):
        """
        create new universe with randomly set star systems
        
        param number_points(int): absolute number of points
        """
        dict_cylinder_points = GameModel.create_cylinder_points(
            number_points=number_points
        )
        self.dict_starsystems = GameModel.create_starsystems(
            dict_points=dict_cylinder_points,
            list_starnames=self.starnames
        )
        self.populate_starsystems()
    
    def populate_starsystems(
        self,
        max_step_size=10000,
        min_stap_size=500,
        max_speed=0.5
    ):
        """
        creates objects in star systems
        
        param max_step_size(int): max distance between star objects
        param min_step_size(int): min distance between star objects
        """
        from random import Random
        
        _random = Random()
        _list_names = self.starsystemnames.copy()
        _array_number_planets = GameModel.get_number_planets_gaussian_distribution(
            size=len(self.dict_starsystems)
        )
        for system in self.dict_starsystems.values():
            _number_planets = _array_number_planets[0]
            _array_number_planets = numpy.delete(_array_number_planets,0,0)
            
            _ellipse_a = (numpy.random.random(_number_planets)*max_step_size).astype(numpy.int64)
            _ellipse_b = (numpy.random.random(_number_planets)*max_step_size).astype(numpy.int64)
            _ellipse_z = numpy.random.random(_number_planets) # default 0 <-> 1
            
            _var_a_before = 0
            _var_b_before = 0
            
            _list_objects = []
            for i in range(0,_number_planets):
                _index = _random.randrange(len(_list_names))
                _name = _list_names.pop(_index)
                
                _a = _ellipse_a[i] if _ellipse_a[i] > min_stap_size else min_stap_size + _ellipse_a[i]
                _b = _ellipse_b[i] if _ellipse_b[i] > min_stap_size else min_stap_size + _ellipse_b[i]
                _var_z = _ellipse_z[i]
                
                _var_a = _var_a_before + _a
                _var_b = _var_b_before + _b
                
                _speed = max_speed / _var_a
                
                _angle = _random.randrange(360)
                
                _list_objects.append(StarSystemNaturalObjectModel(
                    var_a = _var_a,
                    var_b = _var_b,
                    var_z = _var_z,
                    speed = _speed,
                    angle = _angle,
                    name = _name
                ))
                
                _var_a_before = _var_a
                _var_b_before = _var_b

            system.populate_starsystem(
                system_size=_number_planets,
                system_objects=_list_objects
            )
    
    @staticmethod
    def create_cylinder_points(
            number_points=40,
            vector_len=[100,100,100]
    ):
        """
        returns dictionary with randomly generates points
        arranged as cylinder
        
        param number_points(int): absolute number of points
        param vector_len([x(int),y(int),z(int)]): dimensions of cylinder
        """
        _gr = 1
        _a = numpy.random.rand(number_points) * (2 * numpy.pi)
        _z = numpy.random.rand(number_points)
        _r = _gr * numpy.sqrt(numpy.random.rand(number_points))
        _x, _y = _r * numpy.sin(_a), _r * numpy.cos(_a)

        x_int = (_x * vector_len[0] + vector_len[0]).astype(int)
        y_int = (_y * vector_len[1] + vector_len[1]).astype(int)
        z_int = (_z * vector_len[2] + vector_len[2]).astype(int)

        x_int.shape = (number_points, 1)
        y_int.shape = (number_points, 1)
        z_int.shape = (number_points, 1)

        _matrix = numpy.concatenate((x_int, y_int, z_int), axis=1)

        x_int.shape = (1, number_points)
        y_int.shape = (1, number_points)
        z_int.shape = (1, number_points)

        _return = {
            'x': x_int,
            'y': y_int,
            'z': z_int,
            'matrix': _matrix
        }

        return _return
    
    @staticmethod
    def create_starsystems(
        dict_points={},
        list_starnames=[]
    ):
        """
        creates list of starsystems from points_dict
        
        param dict_points({'x':([x1,x2,...,xn]),'y':([y1,y2,...,yn]),'z':([z1,z2,...,zn]),'matrix':[[x1,y1,z1],[x2,y2,z2],...,[xn,yn,zn]]})
        param list_starnames(List): list of names for stars
        """
        from random import Random

        _random = Random()
        _list_starnames = list_starnames.copy()
        _dict_starsystems = {}
        for point in dict_points['matrix']:
            _index = _random.randrange(len(_list_starnames))
            _star_name = _list_starnames.pop(_index)
            _dict_starsystems[_star_name] = StarSystemModel(
                position=point,
                name=_star_name
            )
        return _dict_starsystems
    
    @staticmethod
    def get_number_planets_gaussian_distribution(
        loc=6,
        scale=3,
        size=40,
        limits=(3,12)
    ):
        """
        return array gaussian distribution
        
        for loc, scale, size look at numpy documentation of
        numpy.random.normal()
        
        param limits(Tuple): all values smaller first entry or greater
        second entry will be set to loc value
        """
        array = numpy.random.normal(loc, scale, size).astype(numpy.int64)
        for i in range(0,size):
            value = array[i]
            if value < limits[0] or value > limits[1]:
                value = loc
            array[i] = value
        return array