import ctypes

_dll = ctypes.CDLL('libX11.so')

_XInitThreads = _dll.XInitThreads
_XInitThreads.argtypes = ()
_XInitThreads.restype = ctypes.c_int

class XlibError(SystemError):
  pass

def enable_threads():
  if _XInitThreads() > 0:
    return

  raise XlibError
