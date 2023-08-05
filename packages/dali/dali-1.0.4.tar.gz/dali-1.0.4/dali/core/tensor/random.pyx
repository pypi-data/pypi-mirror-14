

cdef extern from "core/tensor/matrix_initializations.h" nogil:
    cdef cppclass matrix_initializations [T]:
        @staticmethod
        CMat[T] uniform(T low, T high, int rows, int cols)
        @staticmethod
        CMat[T] gaussian(T mean, T std, int rows, int cols)
        @staticmethod
        CMat[T] eye(T diag, int width)
        @staticmethod
        CMat[T] bernoulli(T prob, int rows, int cols)
        @staticmethod
        CMat[T] bernoulli_normalized(T prob, int rows, int cols)
        @staticmethod
        CMat[T] empty(int rows, int cols)


class random:
    @staticmethod
    def uniform(low = 0, high = 1, size=None, dtype=None):
        cdef Mat output = Mat(0,0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[int].uniform(low, high, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[int].uniform(low, high, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[float].uniform(low, high, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[float].uniform(low, high, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[double].uniform(low, high, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[double].uniform(low, high, size, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise ValueError("size must be of type int, tuple, or list")
        return output

    @staticmethod
    def normal(loc=0, scale=1, size=None, dtype=None):
        cdef Mat output = Mat(0,0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[int].gaussian(loc, scale, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[int].gaussian(loc, scale, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[float].gaussian(loc, scale, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[float].gaussian(loc, scale, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[double].gaussian(loc, scale, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[double].gaussian(loc, scale, size, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise ValueError("size must be of type int, tuple, or list")
        return output

    @staticmethod
    def standard_normal(size=None, dtype=None):
        cdef Mat output = Mat(0,0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[int].gaussian(0, 1, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[int].gaussian(0, 1, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[float].gaussian(0, 1, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[float].gaussian(0, 1, size, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[double].gaussian(0, 1, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[double].gaussian(0, 1, size, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise ValueError("size must be of type int, tuple, or list")
        return output

    @staticmethod
    def bernoulli(prob, size=None, dtype=None):
        cdef Mat output = Mat(0,0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[int].bernoulli(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[int].bernoulli(prob, size, 1)
            else:
                    error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[float].bernoulli(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[float].bernoulli(prob, size, 1)
            else:
                    error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[double].bernoulli(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[double].bernoulli(prob, size, 1)
            else:
                    error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise ValueError("size must be of type int, tuple, or list")
        return output

    @staticmethod
    def bernoulli_normalized(prob, size=None, dtype=None):
        cdef Mat output = Mat(0,0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[int].bernoulli_normalized(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[int].bernoulli_normalized(prob, size, 1)
            else:
                    error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[float].bernoulli_normalized(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[float].bernoulli_normalized(prob, size, 1)
            else:
                    error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if type(size) == list or type(size) == tuple and len(size) == 2:
                output.matinternal = matrix_initializations[double].bernoulli_normalized(prob, size[0], size[1])
            elif type(size) == int:
                output.matinternal = matrix_initializations[double].bernoulli_normalized(prob, size, 1)
            else:
                    error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise ValueError("size must be of type int, tuple, or list")
        return output
