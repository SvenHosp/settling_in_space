__version__ = '0.0.1'

from .plantuml_magics import Plantuml

def load_ipython_extension(ipython):
    ipython.register_magics(Plantuml)

load_ipython_extension(get_ipython())