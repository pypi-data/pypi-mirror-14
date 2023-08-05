

cdef extern from "dali/tensor/Solver.h" nogil:
    cdef cppclass CSGD "Solver::SGD" [T]:
        T clipval
        T smooth_eps
        T regc
        T step_size
        # default parameters look like overloaded
        # functions to cython:
        CSGD(T clipval, T smooth_eps, T regc)
        CSGD(T clipval, T regc)
        CSGD(T clipval)
        CSGD()
        CSGD(vector[CMat[T]]&, T clipval, T regc)
        void step(vector[CMat[T]]&)
        void step(vector[CMat[T]]&, T step_size)
        void reset_caches(vector[CMat[T]]&)

    cdef cppclass CAdaGrad "Solver::AdaGrad" [T]:
        T clipval
        T smooth_eps
        T regc
        T step_size
        CAdaGrad()
        CAdaGrad(T smooth_eps, T clipval, T regc)
        CAdaGrad(vector[CMat[T]]&, T smooth_eps, T clipval, T regc)
        void step(vector[CMat[T]]&) except +
        void step(vector[CMat[T]]&, T step_size) except +
        void reset_caches(vector[CMat[T]]&) except +
        void create_gradient_caches(vector[CMat[T]]&)

    cdef cppclass CRMSProp "Solver::RMSProp" [T]:
        T clipval
        T smooth_eps
        T regc
        T step_size
        T decay_rate
        CRMSProp()
        CRMSProp(T decay_rate, T smooth_eps, T clipval, T regc)
        CRMSProp(vector[CMat[T]]&, T decay_rate, T smooth_eps, T clipval, T regc)
        void step(vector[CMat[T]]&) except +
        void step(vector[CMat[T]]&, T step_size) except +
        void reset_caches(vector[CMat[T]]&) except +
        void create_gradient_caches(vector[CMat[T]]&)

    cdef cppclass CAdaDelta "Solver::AdaDelta" [T]:
        T clipval
        T smooth_eps
        T regc
        T rho
        CAdaDelta()
        CAdaDelta(T rho, T smooth_eps, T clipval, T regc)
        CAdaDelta(vector[CMat[T]]&, T rho, T smooth_eps, T clipval, T regc)
        void step(vector[CMat[T]]&) except +
        void reset_caches(vector[CMat[T]]&) except +
        void create_gradient_caches(vector[CMat[T]]&)

    cdef cppclass CAdam "Solver::Adam" [T]:
        T clipval
        T smooth_eps
        T regc
        T b1
        T b2
        unsigned long long epoch
        CAdam()
        CAdam(T b1, T b2, T smooth_eps, T clipval, T regc)
        CAdam(vector[CMat[T]]&, T b1, T b2, T smooth_eps, T clipval, T regc)
        void step(vector[CMat[T]]&) except +
        void step(vector[CMat[T]]&, T step_size) except +
        void reset_caches(vector[CMat[T]]&) except +
        void create_gradient_caches(vector[CMat[T]]&)

cdef class SGD:
    cdef void * solverinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(SGD self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property step_size:
        def __get__(SGD self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(SGD self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].step_size = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].step_size = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property clipval:
        def __get__(SGD self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].clipval
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].clipval
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(SGD self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].clipval = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].clipval = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property regc:
        def __get__(SGD self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].regc
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].regc
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(SGD self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].regc = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].regc = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property smooth_eps:
        def __get__(SGD self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].smooth_eps
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].smooth_eps
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(SGD self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].smooth_eps = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].smooth_eps = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(SGD self):
        cdef CSGD[float]* ptr_internal_float
        cdef CSGD[double]* ptr_internal_double

        if self.solverinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CSGD[float]*>((<SGD>(self)).solverinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CSGD[double]*>((<SGD>(self)).solverinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.solverinternal = NULL

    def __cinit__(SGD self, params = None, float clipval = 5.0, float regc = 0.0, float step_size = 0.01, dtype = None):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        self.dtypeinternal = np.NPY_NOTYPE
        # get the dtype from kwargs
        if dtype is not None:
            self.dtypeinternal = np.dtype(dtype).num
            ensure_fdtype(self.dtypeinternal)

        if params is not None and len(params) > 0:
            if len(params) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(params[0])).dtypeinternal
            for el in params:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                c_params_float = mats_to_vec_float(params)
                if c_params_float.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT32
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT32:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            elif common_dtype == np.NPY_FLOAT64:
                c_params_double = mats_to_vec_double(params)
                if c_params_double.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT64
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT64:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            else:
                raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")

        if self.dtypeinternal == np.NPY_NOTYPE:
            self.dtypeinternal = np.NPY_FLOAT32

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.solverinternal = new CSGD[float](
                c_params_float, clipval, regc)
            (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].step_size = step_size
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.solverinternal = new CSGD[double](
                c_params_double, clipval, regc)
            (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].step_size = step_size
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def reset_caches(SGD self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].reset_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].reset_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def step(SGD self, list params, step_size = None):
        cdef float cstep_size_float
        cdef vector[CMat[float]] c_params_float
        cdef double cstep_size_double
        cdef vector[CMat[double]] c_params_double


        if step_size is not None:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CSGD[float]*>((<SGD>(self)).solverinternal))[0].step(c_params_float, cstep_size_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CSGD[double]*>((<SGD>(self)).solverinternal))[0].step(c_params_double, cstep_size_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


cdef class AdaGrad:
    cdef void * solverinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(AdaGrad self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property step_size:
        def __get__(AdaGrad self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaGrad self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].step_size = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].step_size = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property clipval:
        def __get__(AdaGrad self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].clipval
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].clipval
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaGrad self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].clipval = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].clipval = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property regc:
        def __get__(AdaGrad self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].regc
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].regc
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaGrad self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].regc = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].regc = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property smooth_eps:
        def __get__(AdaGrad self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].smooth_eps
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].smooth_eps
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaGrad self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].smooth_eps = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].smooth_eps = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(AdaGrad self):
        cdef CAdaGrad[float]* ptr_internal_float
        cdef CAdaGrad[double]* ptr_internal_double

        if self.solverinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.solverinternal = NULL

    def __cinit__(AdaGrad self, params = None, float eps = 1e-6, float clipval = 5.0, float regc = 0.0, float step_size = 0.01, dtype = None):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        self.dtypeinternal = np.NPY_NOTYPE
        # get the dtype from kwargs
        if dtype is not None:
            self.dtypeinternal = np.dtype(dtype).num
            ensure_fdtype(self.dtypeinternal)

        if params is not None and len(params) > 0:
            if len(params) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(params[0])).dtypeinternal
            for el in params:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                c_params_float = mats_to_vec_float(params)
                if c_params_float.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT32
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT32:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            elif common_dtype == np.NPY_FLOAT64:
                c_params_double = mats_to_vec_double(params)
                if c_params_double.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT64
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT64:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            else:
                raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")

        if self.dtypeinternal == np.NPY_NOTYPE:
            self.dtypeinternal = np.NPY_FLOAT32

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.solverinternal = new CAdaGrad[float](
                c_params_float, eps, clipval, regc)
            (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].step_size = step_size
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.solverinternal = new CAdaGrad[double](
                c_params_double, eps, clipval, regc)
            (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].step_size = step_size
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def reset_caches(AdaGrad self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].reset_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].reset_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def create_gradient_caches(AdaGrad self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].create_gradient_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].create_gradient_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def step(AdaGrad self, list params, step_size = None):
        cdef float cstep_size_float
        cdef vector[CMat[float]] c_params_float
        cdef double cstep_size_double
        cdef vector[CMat[double]] c_params_double


        if step_size is not None:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[float]*>((<AdaGrad>(self)).solverinternal))[0].step(c_params_float, cstep_size_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaGrad[double]*>((<AdaGrad>(self)).solverinternal))[0].step(c_params_double, cstep_size_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")



cdef class RMSProp:
    cdef void * solverinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(RMSProp self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property step_size:
        def __get__(RMSProp self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(RMSProp self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].step_size = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].step_size = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property clipval:
        def __get__(RMSProp self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].clipval
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].clipval
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(RMSProp self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].clipval = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].clipval = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property regc:
        def __get__(RMSProp self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].regc
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].regc
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(RMSProp self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].regc = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].regc = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property smooth_eps:
        def __get__(RMSProp self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].smooth_eps
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].smooth_eps
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(RMSProp self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].smooth_eps = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].smooth_eps = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property decay_rate:
        def __get__(RMSProp self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].decay_rate
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].decay_rate
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(RMSProp self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].decay_rate = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].decay_rate = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(AdaGrad self):
        cdef CRMSProp[float]* ptr_internal_float
        cdef CRMSProp[double]* ptr_internal_double

        if self.solverinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.solverinternal = NULL

    def __cinit__(RMSProp self, params = None, float decay_rate = 0.999, float eps = 1e-6, float clipval = 5.0, float regc = 0.0, float step_size = 0.01, dtype = None):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        self.dtypeinternal = np.NPY_NOTYPE
        # get the dtype from kwargs
        if dtype is not None:
            self.dtypeinternal = np.dtype(dtype).num
            ensure_fdtype(self.dtypeinternal)

        if params is not None and len(params) > 0:
            if len(params) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(params[0])).dtypeinternal
            for el in params:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                c_params_float = mats_to_vec_float(params)
                if c_params_float.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT32
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT32:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            elif common_dtype == np.NPY_FLOAT64:
                c_params_double = mats_to_vec_double(params)
                if c_params_double.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT64
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT64:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            else:
                raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")

        if self.dtypeinternal == np.NPY_NOTYPE:
            self.dtypeinternal = np.NPY_FLOAT32

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.solverinternal = new CRMSProp[float](
                c_params_float, decay_rate, eps, clipval, regc)
            (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].step_size = step_size
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.solverinternal = new CRMSProp[double](
                c_params_double, decay_rate, eps, clipval, regc)
            (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].step_size = step_size
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def reset_caches(RMSProp self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].reset_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].reset_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def create_gradient_caches(RMSProp self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].create_gradient_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].create_gradient_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def step(RMSProp self, list params, step_size = None):
        cdef float cstep_size_float
        cdef vector[CMat[float]] c_params_float
        cdef double cstep_size_double
        cdef vector[CMat[double]] c_params_double


        if step_size is not None:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                cstep_size_float = (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].step_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                cstep_size_double = (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].step_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[float]*>((<RMSProp>(self)).solverinternal))[0].step(c_params_float, cstep_size_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CRMSProp[double]*>((<RMSProp>(self)).solverinternal))[0].step(c_params_double, cstep_size_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")



cdef class AdaDelta:
    cdef void * solverinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(AdaDelta self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property clipval:
        def __get__(AdaDelta self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].clipval
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].clipval
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaDelta self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].clipval = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].clipval = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property regc:
        def __get__(AdaDelta self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].regc
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].regc
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaDelta self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].regc = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].regc = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property smooth_eps:
        def __get__(AdaDelta self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].smooth_eps
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].smooth_eps
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaDelta self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].smooth_eps = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].smooth_eps = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property rho:
        def __get__(AdaDelta self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].rho
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].rho
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(AdaDelta self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].rho = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].rho = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(AdaDelta self):
        cdef CAdaDelta[float]* ptr_internal_float
        cdef CAdaDelta[double]* ptr_internal_double

        if self.solverinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.solverinternal = NULL

    def __cinit__(AdaDelta self, params = None, float rho = 0.95, float eps = 1e-4, float clipval = 5.0, float regc = 0.0, dtype = None):

        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        self.dtypeinternal = np.NPY_NOTYPE
        # get the dtype from kwargs
        if dtype is not None:
            self.dtypeinternal = np.dtype(dtype).num
            ensure_fdtype(self.dtypeinternal)

        if params is not None and len(params) > 0:
            if len(params) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(params[0])).dtypeinternal
            for el in params:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                c_params_float = mats_to_vec_float(params)
                if c_params_float.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT32
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT32:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            elif common_dtype == np.NPY_FLOAT64:
                c_params_double = mats_to_vec_double(params)
                if c_params_double.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT64
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT64:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            else:
                raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")

        if self.dtypeinternal == np.NPY_NOTYPE:
            self.dtypeinternal = np.NPY_FLOAT32

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.solverinternal = new CAdaDelta[float](
                c_params_float, rho, eps, clipval, regc)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.solverinternal = new CAdaDelta[double](
                c_params_double, rho, eps, clipval, regc)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def reset_caches(AdaDelta self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].reset_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].reset_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def create_gradient_caches(AdaDelta self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].create_gradient_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].create_gradient_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def step(AdaDelta self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[float]*>((<AdaDelta>(self)).solverinternal))[0].step(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdaDelta[double]*>((<AdaDelta>(self)).solverinternal))[0].step(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")



cdef class Adam:
    cdef void * solverinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(Adam self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property clipval:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].clipval
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].clipval
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].clipval = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].clipval = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property regc:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].regc
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].regc
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].regc = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].regc = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property smooth_eps:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].smooth_eps
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].smooth_eps
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].smooth_eps = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].smooth_eps = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property b1:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].b1
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].b1
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].b1 = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].b1 = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property b2:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].b2
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].b2
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, float val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].b2 = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].b2 = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property epoch:
        def __get__(Adam self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].epoch
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].epoch
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(Adam self, unsigned long long val):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].epoch = val
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].epoch = val
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(Adam self):
        cdef CAdam[float]* ptr_internal_float
        cdef CAdam[double]* ptr_internal_double

        if self.solverinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CAdam[float]*>((<Adam>(self)).solverinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CAdam[double]*>((<Adam>(self)).solverinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.solverinternal = NULL

    def __cinit__(Adam self, params = None, float b1 = 0.5, float b2 = 1e-6, float eps = 1e-4, float clipval = 5.0, float regc = 0.0, dtype = None):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        self.dtypeinternal = np.NPY_NOTYPE
        # get the dtype from kwargs
        if dtype is not None:
            self.dtypeinternal = np.dtype(dtype).num
            ensure_fdtype(self.dtypeinternal)

        if params is not None and len(params) > 0:
            if len(params) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(params[0])).dtypeinternal
            for el in params:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                c_params_float = mats_to_vec_float(params)
                if c_params_float.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT32
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT32:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            elif common_dtype == np.NPY_FLOAT64:
                c_params_double = mats_to_vec_double(params)
                if c_params_double.size() > 0:
                    if self.dtypeinternal == np.NPY_NOTYPE:
                        self.dtypeinternal = np.NPY_FLOAT64
                    else:
                        if self.dtypeinternal != np.NPY_FLOAT64:
                            raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            else:
                raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")

        if self.dtypeinternal == np.NPY_NOTYPE:
            self.dtypeinternal = np.NPY_FLOAT32

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.solverinternal = new CAdam[float](
                c_params_float, b1, b2, eps, clipval, regc)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.solverinternal = new CAdam[double](
                c_params_double, b1, b2, eps, clipval, regc)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def reset_caches(Adam self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].reset_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].reset_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def create_gradient_caches(Adam self, list params):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double

        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].create_gradient_caches(c_params_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].create_gradient_caches(c_params_double)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


    def step(Adam self, list params, float step_size = 0.0002):
        cdef vector[CMat[float]] c_params_float
        cdef vector[CMat[double]] c_params_double


        if len(params) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(params[0])).dtypeinternal
        for el in params:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_params_float = mats_to_vec_float(params)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[float]*>((<Adam>(self)).solverinternal))[0].step(c_params_float, step_size)
        elif common_dtype == np.NPY_FLOAT64:
            c_params_double = mats_to_vec_double(params)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for parameters: " + str(params[0].dtype) + ", when solver is " + str(self.dtype))
            with nogil:
                (<CAdam[double]*>((<Adam>(self)).solverinternal))[0].step(c_params_double, step_size)
        else:
            raise ValueError("Invalid dtype:" + str(params[0].dtype) + " (should be one of np.float32, np.float64)")


