"""
main gamemodel module
"""
import numpy

class GameModel():
    def __init__(self):
        """init method"""
        pass
    
    def initialize(self, szenario_path=None):
        """
        initialize Model
        
        param szenario_path(String): path to a scenario file to be loaded
        """
        if(szenario_path is None):
            self.initialize_universe_random()
        else:
            pass
    
    def initialize_universe_random(self):
        """
        create new universe with randomly set star systems
        """
        dict_cylinder_points = GameModel.create_cylinder_points()
        pass
    
    @staticmethod
    def create_cylinder_points(
            number_points=40,
            vector_len=[100,100,100]
    ):
        """
        returns dictionary with randomly generates points
        arranged as cylinder    
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

