#import numpy as np
#import ctypes as ct
#
#clib = ct.CDLL('./test.so')
#a = [1.0, 2.0, 3.0]
#clib.test_python((ct.c_float*len(a))(*a), ct.c_int(len(a)))


import numpy as np
import numpy as np
import ctypes as ct

clib = ct.CDLL('./test.so')
a = np.array([1,2,3], dtype=np.float32, copy=True)
clib.test_python.restype = ct.c_float
clib_result = clib.test_python(a.ctypes.data_as(ct.POINTER(ct.c_float)), a.shape[0])
print clib_result
