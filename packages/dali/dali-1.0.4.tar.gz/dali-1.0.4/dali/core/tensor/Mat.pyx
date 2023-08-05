

ctypedef unsigned int dim_t;
from cython.operator cimport dereference as deref
from libcpp11.stringstream cimport stringstream

from libc.stdlib cimport free

from cpython cimport PyObject, Py_INCREF
# Numpy must be initialized. When using numpy from C or Cython you must
# _always_ do that, or you will have segfaults
np.import_array()

cdef extern from "dali/tensor/Mat.h":
    cdef cppclass CMat "Mat" [T]:
        bint constant
        shared_ptr[string] name
        CMat()
        CMat(dim_t, dim_t)


        vector[dim_t] dims() const
        void npy_load(string fname)
        void npy_save(string fname, string mode)
        int id() const
        unsigned int number_of_elements() const
        dim_t dims(int idx)
        CMat[T] operator_plus   "operator+"(CMat[T] other) except +
        CMat[T] operator_plus   "operator+"(T other) except +
        CMat[T] operator_minus  "operator-"(CMat[T] other) except +
        CMat[T] operator_minus  "operator-"(T other) except +
        CMat[T] operator_times  "operator*"(CMat[T] other) except +
        CMat[T] operator_times  "operator*"(T other) except +
        CMat[T] operator_divide "operator/"(CMat[T] other) except +
        CMat[T] operator_divide "operator/"(T other) except +
        CMat[T] operator_pow    "operator^"(T other) except +
        CMat[T] operator_pow_mat"operator^"(CMat[T] other) except +

        CMat[T] sum()                  except +
        CMat[T] mean()                 except +
        CMat[T] L2_norm()              except +

        CMat[T] sigmoid()              except +
        CMat[T] tanh()                 except +
        CMat[T] elt_inv()                 except +
        CMat[T] relu()                 except +
        CMat[T] absolute_value "abs"() except +
        CMat[T] square()               except +
        CMat[T] exp()                  except +
        CMat[T] softplus()                  except +

        void clear_grad()
        void clear()
        void grad() except +
        void set_name(string& name)
        void print_stdout "print" ()
        void print_me "print" (stringstream& stream)
        CMat[T] dot(CMat[T] other) except+

        CMat(const CMat[T]&, bint, bint)

        TensorInternal[T]& w()
        TensorInternal[T]& dw()

cdef extern from "core/tensor/matrix_initializations.h":
    cdef cppclass matrix_initializations [T]:
        @staticmethod
        CMat[T]* uniform(T low, T high, int rows, int cols)
        @staticmethod
        CMat[T]* gaussian(T mean, T std, int rows, int cols)
        @staticmethod
        CMat[T]* eye(T diag, int width)
        @staticmethod
        CMat[T]* bernoulli(T prob, int rows, int cols)
        @staticmethod
        CMat[T]* bernoulli_normalized(T prob, int rows, int cols)
        @staticmethod
        CMat[T]* empty(int rows, int cols)
        @staticmethod
        CMat[T]* ones(int rows, int cols)
        @staticmethod
        CMat[T]* zeros(int rows, int cols)
        @staticmethod
        CMat[T]* from_pointer(T*, int row, int cols)
        @staticmethod
        CMat[T]* as_pointer(const CMat[T]&)

# forward declaring Matops


cdef extern from "core/math/memory_status.h":
    bint is_gpu_fresh[T](const CMat[T]& mat)
    bint is_cpu_fresh[T](const CMat[T]& mat)
    bint is_gpu_allocated[T](const CMat[T]& mat)
    bint is_cpu_allocated[T](const CMat[T]& mat)
    void to_gpu[T](const CMat[T]& mat) except +
    void to_cpu[T](const CMat[T]& mat)


from numpy.core.numerictypes import sctypeDict, sctype2char


cdef bint is_dtype_supported(np.NPY_TYPES type_id) nogil:
    return type_id == np.NPY_FLOAT32 or \
           type_id == np.NPY_FLOAT64 or \
           type_id == np.NPY_INT32


cdef class Mat:
    cdef void* matinternal
    # WRAPMAT function makes a shallow copy of mat,
    # which does not share superficial properties
    # (like name) with the new instance.
    cdef void* matinternal_parent

    cdef np.NPY_TYPES dtypeinternal
    cdef dict extra_state_internal

    property extra_state:
        def __get__(Mat self):
            return self.extra_state_internal
        def __set__(Mat self, dict value):
            self.extra_state_internal = value

    property dtype:
        def __get__(Mat self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    def __dealloc__(Mat self):
        self.free_internal()


    def memory_status(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return {
                'gpu_fresh' : is_gpu_fresh[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0]),
                'cpu_fresh' : is_cpu_fresh[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0]),
                'gpu_allocated' : is_gpu_allocated[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0]),
                'cpu_allocated' : is_cpu_allocated[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0]),
            }
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return {
                'gpu_fresh' : is_gpu_fresh[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0]),
                'cpu_fresh' : is_cpu_fresh[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0]),
                'gpu_allocated' : is_gpu_allocated[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0]),
                'cpu_allocated' : is_cpu_allocated[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0]),
            }
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return {
                'gpu_fresh' : is_gpu_fresh[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0]),
                'cpu_fresh' : is_cpu_fresh[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0]),
                'gpu_allocated' : is_gpu_allocated[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0]),
                'cpu_allocated' : is_cpu_allocated[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0]),
            }
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def to_gpu(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            to_gpu[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0])
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            to_gpu[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0])
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            to_gpu[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0])
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def to_cpu(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            to_cpu[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0])
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            to_cpu[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0])
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            to_cpu[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0])
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    cdef free_internal(Mat self):
        cdef CMat[int]* ptr_internal_int
        cdef CMat[float]* ptr_internal_float
        cdef CMat[double]* ptr_internal_double

        if self.matinternal != NULL:
            if (self).dtypeinternal == np.NPY_INT32:
                ptr_internal_int = (<CMat[int]*>((<Mat>(self)).matinternal))
                with nogil:
                    del ptr_internal_int
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CMat[float]*>((<Mat>(self)).matinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CMat[double]*>((<Mat>(self)).matinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            self.matinternal = NULL


    cdef void steal_numpy_memory(Mat self, np.ndarray py_array, bint steal):
        assert(py_array.ndim <= 2,
            "Only numpy arrays with dimensions 2 or lower can be borrowed")
        if is_dtype_supported(py_array.dtype.num):
            if self.dtypeinternal == np.NPY_NOTYPE:
                self.dtypeinternal = py_array.dtype.num
            else:
                if self.dtypeinternal != py_array.dtype.num:
                    py_array = py_array.astype(self.dtype)
        else:
            if self.dtypeinternal == np.NPY_NOTYPE:
                if np.issubdtype(py_array.dtype, np.float):
                    py_array = py_array.astype(np.float32)
                    self.dtypeinternal = py_array.dtype.num
                elif np.issubdtype(py_array.dtype, np.integer):
                    py_array = py_array.astype(np.int32)
                    self.dtypeinternal = py_array.dtype.num
                else:
                    raise ValueError("Invalid dtype: " + str(py_array.dtype) + " (should be int or float)")
            else:
                if self.dtypeinternal != py_array.dtype.num:
                    py_array = py_array.astype(self.dtype)

        cdef np.ndarray c_py_array
        cdef int n = py_array.shape[0]
        cdef int d = py_array.shape[1] if py_array.ndim > 1 else 1
        if steal:
            c_py_array = np.PyArray_GETCONTIGUOUS(py_array)
            if c_py_array.flags.owndata and c_py_array.flags.writeable:
                if (self).dtypeinternal == np.NPY_INT32:
                    self.free_internal()
                    self.matinternal = matrix_initializations[int].from_pointer(<int*> np.PyArray_DATA(c_py_array), n, d)
                elif (self).dtypeinternal == np.NPY_FLOAT32:
                    self.free_internal()
                    self.matinternal = matrix_initializations[float].from_pointer(<float*> np.PyArray_DATA(c_py_array), n, d)
                elif (self).dtypeinternal == np.NPY_FLOAT64:
                    self.free_internal()
                    self.matinternal = matrix_initializations[double].from_pointer(<double*> np.PyArray_DATA(c_py_array), n, d)
                else:
                    raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

                if (n * d) > 0:
                    np.PyArray_CLEARFLAGS(c_py_array, np.NPY_OWNDATA)
                return
        if (self).dtypeinternal == np.NPY_INT32:
            self.free_internal()
            self.matinternal = new CMat[int](n, d)
            self.w = py_array.reshape((n,d))
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            self.free_internal()
            self.matinternal = new CMat[float](n, d)
            self.w = py_array.reshape((n,d))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.free_internal()
            self.matinternal = new CMat[double](n, d)
            self.w = py_array.reshape((n,d))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def __cinit__(Mat self, *args, **kwargs):
        self.dtypeinternal = np.NPY_NOTYPE
        self.extra_state = {}
        if kwargs.get('dtype') is not None:
            self.dtypeinternal = np.dtype(kwargs['dtype']).num
            if not is_dtype_supported(self.dtypeinternal):
                raise ValueError("Invalid dtype: " + str(self.dtype) + " (should be one of int32, float32, float64)")
        else:
            self.dtypeinternal = np.NPY_FLOAT32

        if len(args) == 2 and type(args[0]) == int and type(args[1]) == int:
            n, d = args[0], args[1]
            assert(n > -1 and d > -1), "Only positive dimensions may be used."
            if (self).dtypeinternal == np.NPY_INT32:
                self.free_internal()
                self.matinternal = new CMat[int](n, d)
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                self.free_internal()
                self.matinternal = new CMat[float](n, d)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                self.free_internal()
                self.matinternal = new CMat[double](n, d)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        elif len(args) == 1 and type(args[0]) == np.ndarray:
            arr = args[0]
            if kwargs.get('dtype') is not None and arr.dtype != self.dtype:
                arr = arr.astype(self.dtype)
            self.steal_numpy_memory(arr, kwargs.get("borrow", False))
        elif len(args) == 1 and type(args[0]) == list:
            x = np.array(args[0])
            if len(x.shape) == 2:
                pass
            elif len(x.shape) == 1:
                x = x.reshape((1, x.shape[0]))
            elif len(x.shape) == 0:
                x = x.reshape((1,1))
            else:
                raise ValueError("Passed a list with higher than 2 dimensions to constructor.")

            self.steal_numpy_memory(x, True)
        else:
            raise ValueError("Passed " + str(args) + " to Mat constructor")

        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].set_name(kwargs.get('name', '').encode("utf-8"))
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].set_name(kwargs.get('name', '').encode("utf-8"))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].set_name(kwargs.get('name', '').encode("utf-8"))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


        constantness = kwargs.get('constant')
        if constantness is not None:
            self.constant = constantness

    def dims(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return tuple((<CMat[int]*>((<Mat>(self)).matinternal))[0].dims())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return tuple((<CMat[float]*>((<Mat>(self)).matinternal))[0].dims())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return tuple((<CMat[double]*>((<Mat>(self)).matinternal))[0].dims())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    property shape:
        def __get__(self):
            if (self).dtypeinternal == np.NPY_INT32:
                return tuple((<CMat[int]*>((<Mat>(self)).matinternal))[0].dims())
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                return tuple((<CMat[float]*>((<Mat>(self)).matinternal))[0].dims())
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return tuple((<CMat[double]*>((<Mat>(self)).matinternal))[0].dims())
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def npy_save(Mat self, str fname, str mode = "w"):
        cdef string fname_norm = normalize_s(fname)
        cdef string mode_norm = normalize_s(mode)
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].npy_save(fname_norm, mode_norm)
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].npy_save(fname_norm, mode_norm)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].npy_save(fname_norm, mode_norm)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def npy_load(Mat self, str fname):
        cdef string fname_norm = normalize_s(fname)
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].npy_load(fname_norm)
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].npy_load(fname_norm)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].npy_load(fname_norm)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def clear_grad(self):
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].clear_grad()
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].clear_grad()
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].clear_grad()
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def clear(self):
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].clear()
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].clear()
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].clear()
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def grad(self):
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].grad()
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].grad()
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].grad()
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def __array__(self, dtype=None):
        if dtype is None or dtype == self.dtype:
            return self.w
        else:
            return self.w.astype(dtype)


    def astype(Mat self, dtype):
        if self.dtype == dtype:
            return self
        else:
            return Mat(self.w, dtype=dtype)

    property w:
        def __get__(self):
            return self.get_value(False)

        def __set__(self, value):
            self.get_value(False)[:] = value

    property dw:
        def __get__(self):
            return self.get_grad_value(False)

        def __set__(self, value):
            self.get_grad_value(False)[:] = value

    property constant:
        def __get__(self):
            if (self).dtypeinternal == np.NPY_INT32:
                return (<CMat[int]*>((<Mat>(self)).matinternal))[0].constant
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CMat[float]*>((<Mat>(self)).matinternal))[0].constant
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CMat[double]*>((<Mat>(self)).matinternal))[0].constant
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        def __set__(self, bint constant):
            if (self).dtypeinternal == np.NPY_INT32:
                (<CMat[int]*>((<Mat>(self)).matinternal))[0].constant = constant
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                (<CMat[float]*>((<Mat>(self)).matinternal))[0].constant = constant
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CMat[double]*>((<Mat>(self)).matinternal))[0].constant = constant
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def get_value(self, copy=False):
        if copy:
            return np.array(self.get_value(False), copy=True)

        cdef np.ndarray ndarray
        cdef np.npy_intp shape[2]

        if (self).dtypeinternal == np.NPY_INT32:
            if (<CMat[int]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[int]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[int]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[int]*>((<Mat>(self)).matinternal))[0].w().data()
            )
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            if (<CMat[float]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[float]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[float]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[float]*>((<Mat>(self)).matinternal))[0].w().data()
            )
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            if (<CMat[double]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[double]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[double]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[double]*>((<Mat>(self)).matinternal))[0].w().data()
            )
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


        ndarray.base = <PyObject*> self
        Py_INCREF(self)

        return ndarray

    def clone(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int(CMat[int]((<CMat[int]*>((<Mat>(self)).matinternal))[0], True, True))
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float(CMat[float]((<CMat[float]*>((<Mat>(self)).matinternal))[0], True, True))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double(CMat[double]((<CMat[double]*>((<Mat>(self)).matinternal))[0], True, True))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def copy(Mat self, Mat other):
        MatOps.copy(self, other)

    def get_grad_value(Mat self, copy=False):
        if copy:
            return np.array(self.get_grad_value(False), copy=True)

        cdef np.ndarray ndarray
        cdef np.npy_intp shape[2]

        if (self).dtypeinternal == np.NPY_INT32:
            if (<CMat[int]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[int]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[int]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[int]*>((<Mat>(self)).matinternal))[0].dw().data()
            )
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            if (<CMat[float]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[float]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[float]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[float]*>((<Mat>(self)).matinternal))[0].dw().data()
            )
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            if (<CMat[double]*>((<Mat>(self)).matinternal))[0].number_of_elements() == 0:
                return np.zeros((0,0), dtype = self.dtype)
            shape[0] = <np.npy_intp> (<CMat[double]*>((<Mat>(self)).matinternal))[0].dims(0)
            shape[1] = <np.npy_intp> (<CMat[double]*>((<Mat>(self)).matinternal))[0].dims(1)
            ndarray = np.PyArray_SimpleNewFromData(
                2,
                shape,
                self.dtypeinternal,
                (<CMat[double]*>((<Mat>(self)).matinternal))[0].dw().data()
            )
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


        ndarray.base = <PyObject*> self
        Py_INCREF(self)

        return ndarray

    property name:
        def __get__(self):
            cdef string name
            if (self).dtypeinternal == np.NPY_INT32:
                if (<CMat[int]*>((<Mat>(self)).matinternal))[0].name != NULL:
                    name = deref((<CMat[int]*>((<Mat>(self)).matinternal))[0].name)
                    return name.decode("utf-8")
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                if (<CMat[float]*>((<Mat>(self)).matinternal))[0].name != NULL:
                    name = deref((<CMat[float]*>((<Mat>(self)).matinternal))[0].name)
                    return name.decode("utf-8")
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                if (<CMat[double]*>((<Mat>(self)).matinternal))[0].name != NULL:
                    name = deref((<CMat[double]*>((<Mat>(self)).matinternal))[0].name)
                    return name.decode("utf-8")
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            return None

        def __set__(self, str newname):
            if (self).dtypeinternal == np.NPY_INT32:
                (<CMat[int]*>((<Mat>(self)).matinternal))[0].set_name(newname.encode("utf-8"))
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                (<CMat[float]*>((<Mat>(self)).matinternal))[0].set_name(newname.encode("utf-8"))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CMat[double]*>((<Mat>(self)).matinternal))[0].set_name(newname.encode("utf-8"))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def __str__(Mat self):
        name_str = ', name=%s' % (self.name.__repr__(),) if self.name is not None else ''
        dtype_str = ', dtype=%s' % (self.dtype.__repr__(),) if self.dtype != np.float32 else ''

        extra = dtype_str + name_str
        n, d = self.shape
        return "dali.Mat(%d, %d%s)" % (n, d, extra)

    def __repr__(Mat self):
        cdef stringstream ss
        if (self).dtypeinternal == np.NPY_INT32:
            (<CMat[int]*>((<Mat>(self)).matinternal))[0].print_me(ss)
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            (<CMat[float]*>((<Mat>(self)).matinternal))[0].print_me(ss)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CMat[double]*>((<Mat>(self)).matinternal))[0].print_me(ss)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        return ss.to_string().decode("utf-8")

    def T(Mat self):
        return MatOps.transpose(self)

    def reshape(Mat self, unsigned int rows, unsigned int cols):
        return MatOps.reshape(self, rows, cols)

    def __add__(self, other):
        if type(self) is Mat:
            if type(other) is Mat:
                if (<Mat>self).dtypeinternal != (<Mat>other).dtypeinternal:
                   raise ValueError("All arguments must be of the same type")
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_plus( (<CMat[int]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_plus( (<CMat[float]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_plus( (<CMat[double]*>((<Mat>(other)).matinternal))[0] ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            elif type(other) is float or type(other) is int:
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_plus( (<int>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_plus( (<float>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_plus( (<double>other) ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            else:
                raise TypeError("Mat can only be added to float, int, or Mat.")
        else:
            return other.__add__(self)

    def __sub__(self, other):
        if type(self) is Mat:
            if type(other) is Mat:
                if (<Mat>self).dtypeinternal != (<Mat>other).dtypeinternal:
                   raise ValueError("All arguments must be of the same type")
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_minus( (<CMat[int]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_minus( (<CMat[float]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_minus( (<CMat[double]*>((<Mat>(other)).matinternal))[0] ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            elif type(other) is float or type(other) is int:
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_minus( (<int>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_minus( (<float>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_minus( (<double>other) ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            else:
                raise TypeError("Mat can only be added to float, int, or Mat.")
        else:
            return other._rsub(self)

    def _rsub(Mat self, other):
        if type(other) is Mat:
            if (<Mat>self).dtypeinternal != (<Mat>other).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (<Mat>self).dtypeinternal == np.NPY_INT32:
                return WrapMat_int((<CMat[int]*>((<Mat>(other)).matinternal))[0].operator_minus( (<CMat[int]*>((<Mat>(self)).matinternal))[0] ))
            elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CMat[float]*>((<Mat>(other)).matinternal))[0].operator_minus( (<CMat[float]*>((<Mat>(self)).matinternal))[0] ))
            elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CMat[double]*>((<Mat>(other)).matinternal))[0].operator_minus( (<CMat[double]*>((<Mat>(self)).matinternal))[0] ))
            else:
                raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        elif type(other) is float or type(other) is int:
            return MatOps.sub_broadcast_reversed(self, other)
        else:
            raise TypeError("Mat can only subtract from a float, int, or Mat.")

    def __pow__(Mat self, other, modulo):
        if type(other) is Mat:
            if (self).dtypeinternal != (<Mat>other).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (self).dtypeinternal == np.NPY_INT32:
                return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_pow_mat( (<CMat[int]*>((<Mat>(other)).matinternal))[0] ))
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_pow_mat( (<CMat[float]*>((<Mat>(other)).matinternal))[0] ))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_pow_mat( (<CMat[double]*>((<Mat>(other)).matinternal))[0] ))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        elif type(other) is float or type(other) is int:
            if (<Mat>self).dtypeinternal == np.NPY_INT32:
                return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_pow( (<int>other) ))
            elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_pow( (<float>other) ))
            elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_pow( (<double>other) ))
            else:
                raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        else:
            raise TypeError("Mat can only be added to float, int, or Mat.")

    def __mul__(self, other):
        if type(self) is Mat:
            if type(other) is Mat:
                if (<Mat>self).dtypeinternal != (<Mat>other).dtypeinternal:
                   raise ValueError("All arguments must be of the same type")
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_times( (<CMat[int]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_times( (<CMat[float]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_times( (<CMat[double]*>((<Mat>(other)).matinternal))[0] ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            elif type(other) is float or type(other) is int:
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_times( (<int>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_times( (<float>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_times( (<double>other) ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            else:
                raise TypeError("Mat can only be added to float, int, or Mat.")
        else:
            return other.__mul__(self)

    def __truediv__(self, other):
        if type(self) is Mat:
            if type(other) is Mat:
                if (<Mat>self).dtypeinternal != (<Mat>other).dtypeinternal:
                   raise ValueError("All arguments must be of the same type")
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_divide( (<CMat[int]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_divide( (<CMat[float]*>((<Mat>(other)).matinternal))[0] ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_divide( (<CMat[double]*>((<Mat>(other)).matinternal))[0] ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            elif type(other) is float or type(other) is int:
                if (<Mat>self).dtypeinternal == np.NPY_INT32:
                    return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].operator_divide( (<int>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT32:
                    return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].operator_divide( (<float>other) ))
                elif (<Mat>self).dtypeinternal == np.NPY_FLOAT64:
                    return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].operator_divide( (<double>other) ))
                else:
                    raise ValueError("Invalid dtype:" + str(<Mat>self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

            else:
                raise TypeError("Mat can only be added to float, int, or Mat.")
        else:
            return self * other.elt_inv()

    def __getitem__(Mat self, index):
        if type(index) == Mat:
            return MatOps.rows_pluck(self, index)
        else:
            return MatOps.row_pluck(self, <int>index)

    def __setstate__(self, state):
        self.free_internal()
        self.dtypeinternal = np.NPY_NOTYPE
        self.steal_numpy_memory(state["w"], True)
        self.constant = state["cst"]
        self.extra_state = state.get("extra_state")
        if "n" in state:
            self.name = state["n"]

    def __getstate__(self):
        state = {
            "w" : self.w,
            "cst":self.constant
        }
        if self.name is not None:
            state["n"] = self.name
        if self.extra_state is not None:
            state["extra_state"] = self.extra_state
        return state

    def __reduce__(self):
        return (
            self.__class__,
            (
                0, 0
            ), self.__getstate__(),
        )

    def log(Mat self):
        return MatOps.log(self)

    def dot(Mat self, Mat other):
        if (self).dtypeinternal != (<Mat>other).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].dot((<CMat[int]*>((<Mat>(other)).matinternal))[0]))
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].dot((<CMat[float]*>((<Mat>(other)).matinternal))[0]))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].dot((<CMat[double]*>((<Mat>(other)).matinternal))[0]))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")



    def sum(Mat self, axis=None):
        return MatOps.sum(self, axis)
    def L2_norm(Mat self, axis=None):
        return MatOps.L2_norm(self, axis)
    def mean(Mat self, axis=None):
        return MatOps.mean(self, axis)
    def __sum__(Mat self):
        return self.sum()

    def __abs__(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].absolute_value())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].absolute_value())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].absolute_value())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    def sigmoid(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].sigmoid())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].sigmoid())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].sigmoid())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def tanh(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].tanh())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].tanh())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].tanh())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def relu(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].relu())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].relu())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].relu())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def square(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].square())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].square())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].square())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def exp(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].exp())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].exp())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].exp())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def softplus(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].softplus())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].softplus())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].softplus())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    def elt_inv(Mat self):
        if (self).dtypeinternal == np.NPY_INT32:
            return WrapMat_int((<CMat[int]*>((<Mat>(self)).matinternal))[0].elt_inv())
        elif (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float((<CMat[float]*>((<Mat>(self)).matinternal))[0].elt_inv())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double((<CMat[double]*>((<Mat>(self)).matinternal))[0].elt_inv())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def eye(rows, diag = 1, dtype=None):
        cdef Mat output = Mat(0, 0, dtype=dtype)
        if (output).dtypeinternal == np.NPY_INT32:
            output.free_internal()
            output.matinternal = matrix_initializations[int].eye(diag, rows)
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            output.free_internal()
            output.matinternal = matrix_initializations[float].eye(diag, rows)
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            output.free_internal()
            output.matinternal = matrix_initializations[double].eye(diag, rows)
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        return output

    @staticmethod
    def empty(shape, dtype=None):
        cdef Mat output = Mat(0, 0, dtype=dtype)
        output.free_internal()

        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[int].empty(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[int].empty(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[float].empty(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[float].empty(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[double].empty(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[double].empty(shape, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise TypeError("shape must be of type int, list, or tuple.")
        return output

    @staticmethod
    def ones(shape, dtype=None, constant = None):
        cdef Mat output = Mat(0, 0, dtype=dtype)
        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[int].ones(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[int].ones(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[float].ones(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[float].ones(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[double].ones(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[double].ones(shape, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise TypeError("shape must be of type int, list, or tuple.")
        if constant is not None:
            output.constant = constant
        return output

    @staticmethod
    def zeros(shape, dtype=None, constant=None):
        cdef Mat output = Mat(0, 0, dtype=dtype)
        output.free_internal()

        cdef bint error = False
        if (output).dtypeinternal == np.NPY_INT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[int].zeros(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[int].zeros(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT32:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[float].zeros(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[float].zeros(shape, 1)
            else:
                error = True
        elif (output).dtypeinternal == np.NPY_FLOAT64:
            if (type(shape) == list or type(shape) == tuple) and len(shape) == 2:
                output.matinternal = matrix_initializations[double].zeros(shape[0], shape[1])
            elif type(shape) == int:
                output.matinternal = matrix_initializations[double].zeros(shape, 1)
            else:
                error = True
        else:
            raise ValueError("Invalid dtype:" + str(output.dtype) + " (should be one of np.int32, np.float32, np.float64)")

        if error:
            raise TypeError("shape must be of type int, list, or tuple.")

        if constant is not None:
            output.constant = constant

        return output


cdef inline vector[CMat[int]] mats_to_vec_int(list mats):
    "Converts a list of mats to a vector[CMat[int]]"
    cdef vector[CMat[int]] mats_vec
    mats_vec.reserve(len(mats))
    for mat in mats:
        mats_vec.push_back((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
    return mats_vec
cdef inline vector[CMat[float]] mats_to_vec_float(list mats):
    "Converts a list of mats to a vector[CMat[float]]"
    cdef vector[CMat[float]] mats_vec
    mats_vec.reserve(len(mats))
    for mat in mats:
        mats_vec.push_back((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
    return mats_vec
cdef inline vector[CMat[double]] mats_to_vec_double(list mats):
    "Converts a list of mats to a vector[CMat[double]]"
    cdef vector[CMat[double]] mats_vec
    mats_vec.reserve(len(mats))
    for mat in mats:
        mats_vec.push_back((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
    return mats_vec


cdef inline Mat WrapMat_int(const CMat[int]& internal):
    if internal.name == NULL:
        (<CMat[int]&>internal).set_name('')
    cdef Mat output = Mat(0,0)
    output.free_internal()
    output.matinternal = matrix_initializations[int].as_pointer(internal)
    output.dtypeinternal = np.NPY_INT32
    (<CMat[int]*>((<Mat>(output)).matinternal))[0].name = internal.name
    return output
cdef inline Mat WrapMat_float(const CMat[float]& internal):
    if internal.name == NULL:
        (<CMat[float]&>internal).set_name('')
    cdef Mat output = Mat(0,0)
    output.free_internal()
    output.matinternal = matrix_initializations[float].as_pointer(internal)
    output.dtypeinternal = np.NPY_FLOAT32
    (<CMat[float]*>((<Mat>(output)).matinternal))[0].name = internal.name
    return output
cdef inline Mat WrapMat_double(const CMat[double]& internal):
    if internal.name == NULL:
        (<CMat[double]&>internal).set_name('')
    cdef Mat output = Mat(0,0)
    output.free_internal()
    output.matinternal = matrix_initializations[double].as_pointer(internal)
    output.dtypeinternal = np.NPY_FLOAT64
    (<CMat[double]*>((<Mat>(output)).matinternal))[0].name = internal.name
    return output

