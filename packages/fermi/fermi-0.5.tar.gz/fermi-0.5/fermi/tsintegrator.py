try:
    import cython
    from .src.intcore import Tsintegrator
    from .src.intcore import Tsintegrator1D
    from .src.intcore import Tsintegrator2D
except:
    from .src.intcore_py import Tsintegrator
    from .src.intcore_py import Tsintegrator1D
    from .src.intcore_py import Tsintegrator2D