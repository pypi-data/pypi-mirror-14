


cdef extern from "dali/tensor/MatOps.h" nogil:
    cdef cppclass CMatOps "MatOps" [T]:
        ### OTHER ###
        @staticmethod
        CMat[T] fill(CMat[T] to_fill, T filler)

        @staticmethod
        CMat[T] consider_constant(CMat[T])

        @staticmethod
        bint equals(CMat[T], CMat[T])

        @staticmethod
        bint allclose(CMat[T], CMat[T], double tol)

        @staticmethod
        bint grad_allclose(CMat[T], CMat[T], double tol)

        @staticmethod
        bint is_nan(CMat[T])

        @staticmethod
        bint is_grad_nan(CMat[T])

        @staticmethod
        vector[int] argsort(CMat[T])

        @staticmethod
        vector[size_t] argsort(const vector[CMat[T]]&) except +

        @staticmethod
        int argmax(const CMat[T]&) except +

        @staticmethod
        int argmin(const CMat[T]&) except +

        @staticmethod
        vector[int] argmax_axis "argmax" (const CMat[T]&, int dimension)

        @staticmethod
        vector[int] argmin_axis "argmin" (const CMat[T]&, int dimension)

        @staticmethod
        int argmax_slice(const CMat[T]&, int lower, int upper)  except +

        @staticmethod
        int argmin_slice(const CMat[T]&, int lower, int upper)  except +

        @staticmethod
        void copy(CMat[T]* dest, const CMat[T]& source)  except +

        @staticmethod
        void copy_grad(CMat[T]* dest, const CMat[T]& source)  except +

        ### REDUCERS ###
        @staticmethod
        CMat[T] grad_norm(CMat[T])
        @staticmethod
        CMat[T] grad_norm_rowwise(CMat[T])
        @staticmethod
        CMat[T] grad_norm_colwise(CMat[T])

        @staticmethod
        CMat[T] L2_norm(CMat[T])

        @staticmethod
        CMat[T] L2_norm_rowwise(CMat[T]) except +

        @staticmethod
        CMat[T] L2_norm_colwise(CMat[T]) except +

        @staticmethod
        CMat[T] sum(CMat[T]) except +

        @staticmethod
        CMat[T] sum_rowwise(CMat[T]) except +

        @staticmethod
        CMat[T] sum_colwise(CMat[T]) except +

        @staticmethod
        CMat[T] mean(CMat[T]) except +

        @staticmethod
        CMat[T] mean_rowwise(CMat[T]) except +

        @staticmethod
        CMat[T] mean_colwise(CMat[T]) except +

        @staticmethod
        CMat[T] max(CMat[T]) except +

        @staticmethod
        CMat[T] max_rowwise(CMat[T]) except +

        @staticmethod
        CMat[T] max_colwise(CMat[T]) except +


        @staticmethod
        CMat[T] min(CMat[T]) except +

        @staticmethod
        CMat[T] min_rowwise(CMat[T]) except +

        @staticmethod
        CMat[T] min_colwise(CMat[T]) except +

        ### RESHAPING ###

        @staticmethod
        CMat[T] hstack(CMat[T], CMat[T])  except +

        @staticmethod
        CMat[T] hstack_vec "hstack" (const vector[CMat[T]]&)  except +

        @staticmethod
        CMat[T] vstack(CMat[T], CMat[T])  except +

        @staticmethod
        CMat[T] vstack_vec "vstack"(const vector[CMat[T]]&)  except +

        @staticmethod
        CMat[T] broadcast_row_vector(CMat[T] input, int num_rows) except +

        @staticmethod
        CMat[T] broadcast_col_vector(CMat[T] input, int num_cols) except +

        @staticmethod
        CMat[T] transpose(CMat[T])

        @staticmethod
        CMat[T] rows_pluck(CMat[T], CMat[int])  except +

        @staticmethod
        CMat[T] reshape(CMat[T], int, int)  except +

        @staticmethod
        CMat[T] row_pluck(CMat[T], int)  except +

        @staticmethod
        CMat[T] col_pluck(CMat[T], int)  except +

        @staticmethod
        void resize(CMat[T]& mat, unsigned int rows, unsigned int cols)  except +

        ### SOLVER_UPDATES ###
        @staticmethod
        void clip_and_regularize(CMat[T] param, T clipval, T regc)

        @staticmethod
        void regularize(CMat[T] param, T regc)

        @staticmethod
        void normalize(CMat[T] param, T norm_threshold)

        @staticmethod
        void sgd_update(CMat[T] param, T step_size) except +

        @staticmethod
        void adagrad_update(CMat[T] param, CMat[T]& cache, T step_size, T smooth_eps) except +

        @staticmethod
        void rmsprop_update(CMat[T] param, CMat[T]& cache, T decay_rate, T step_size, T smooth_eps) except +

        @staticmethod
        void rmsprop_momentum_update(CMat[T] param, CMat[T]& n_cache, CMat[T]& g_cache, CMat[T]& momentum_cache, T decay_rate, T momentum, T step_size, T smooth_eps) except +

        @staticmethod
        void adadelta_update(CMat[T] param, CMat[T]& gsum, CMat[T]& xsum, T rho, T smooth_eps) except +

        @staticmethod
        void adam_update(CMat[T] param, CMat[T]& m, CMat[T]& v, T b1, T b2, T smooth_eps, T step_size, unsigned long long epoch) except +

        ### ELEMWISE ###
        @staticmethod
        CMat[T] add(CMat[T], T)

        @staticmethod
        CMat[T] sub_broadcast_reversed(CMat[T], T)

        @staticmethod
        CMat[T] eltmul(CMat[T], T)

        @staticmethod
        CMat[T] eltmul_mat "eltmul" (CMat[T], CMat[T]) except+

        @staticmethod
        CMat[T] eltmul_mat "eltmul" (CMat[T], CMat[T]) except+

        @staticmethod
        CMat[T] eltmul_broadcast_colwise(CMat[T], CMat[T]) except +

        @staticmethod
        CMat[T] eltmul_broadcast_rowwise(CMat[T], CMat[T]) except +

        @staticmethod
        CMat[T] eltdivide(CMat[T], T)

        @staticmethod
        CMat[T] eltmax(CMat[T], T)

        @staticmethod
        CMat[T] square(CMat[T])

        @staticmethod
        CMat[T] log(CMat[T])

        @staticmethod
        CMat[T] exp(CMat[T])

        @staticmethod
        CMat[T] sigmoid(CMat[T])

        @staticmethod
        CMat[T] steep_sigmoid(CMat[T], T aggressiveness)

        @staticmethod
        CMat[T] tanh(CMat[T])

        @staticmethod
        CMat[T] relu(CMat[T])

        @staticmethod
        CMat[T] abs(CMat[T])

        @staticmethod
        CMat[T] pow(CMat[T], T power)

        @staticmethod
        CMat[T] sqrt(CMat[T])

        @staticmethod
        CMat[T] elt_inv(CMat[T])

        ### DROPOUT ###

        @staticmethod
        CMat[T] dropout(CMat[T], T drop_prob)

        @staticmethod
        CMat[T] dropout_normalized(CMat[T], T drop_prob)

        @staticmethod
        CMat[T] fast_dropout(CMat[T])

        @staticmethod
        vector[CMat[T]] dropout(const vector[CMat[T]]&, T drop_prob)

        @staticmethod
        vector[CMat[T]] dropout_normalized(const vector[CMat[T]]&, T drop_prob)

        @staticmethod
        vector[CMat[T]] fast_dropout(const vector[CMat[T]]&)

        ### COST ###

        @staticmethod
        CMat[T] binary_cross_entropy(CMat[T], T target) except +

        @staticmethod
        CMat[T] binary_cross_entropy_mat "binary_cross_entropy"(CMat[T], CMat[T] target) except +

        @staticmethod
        CMat[T] sigmoid_binary_cross_entropy(CMat[T], T target) except +

        @staticmethod
        CMat[T] sigmoid_binary_cross_entropy_mat "sigmoid_binary_cross_entropy"(CMat[T], CMat[T] target) except +

        @staticmethod
        CMat[T] softmax_colwise(CMat[T], T temperature) except +

        @staticmethod
        CMat[T] softmax_rowwise(CMat[T], T temperature) except +

        @staticmethod
        CMat[T] softmax_no_grad_colwise(CMat[T], T temperature) except +

        @staticmethod
        CMat[T] softmax_no_grad_rowwise(CMat[T], T temperature) except +

        @staticmethod
        CMat[T] margin_loss_colwise(CMat[T], unsigned int answer_idx, T margin) except +

        @staticmethod
        CMat[T] margin_loss_rowwise(CMat[T], unsigned int answer_idx, T margin) except +


        @staticmethod
        CMat[T] SCE_rowwise_int "softmax_cross_entropy_rowwise"(CMat[T], unsigned int answer_idx) except +

        @staticmethod
        CMat[T] SCE_rowwise_mat "softmax_cross_entropy_rowwise"(CMat[T], CMat[int] targets) except +

        @staticmethod
        CMat[T] SCE_colwise_int "softmax_cross_entropy_colwise"(CMat[T], unsigned int answer_idx) except +

        @staticmethod
        CMat[T] SCE_colwise_mat "softmax_cross_entropy_colwise"(CMat[T], CMat[int] targets) except +

        @staticmethod
        CMat[T] CE_colwise_int "cross_entropy_colwise"(CMat[T], unsigned int answer_idx) except +

        @staticmethod
        CMat[T] CE_rowwise_int "cross_entropy_rowwise"(CMat[T], unsigned int answer_idx) except +

        @staticmethod
        CMat[T] CE_colwise_mat "cross_entropy_colwise"(CMat[T], CMat[int] targets) except +

        @staticmethod
        CMat[T] CE_rowwise_mat "cross_entropy_rowwise"(CMat[T], CMat[int] targets) except +

        @staticmethod
        CMat[T] CE_eltwise     "cross_entropy"(CMat[T], CMat[T] targets) except +

        @staticmethod
        CMat[T] CE_rowwise_mat "cross_entropy_rowwise"(CMat[T], CMat[int] targets) except +


        @staticmethod
        vector[CMat[T]] softmax_vector "softmax"(vector[CMat[T]], T temperature) except +

        @staticmethod
        CMat[T] CE_Mat "cross_entropy"(CMat[T], CMat[T]) except +

        ### CONVOLUTION ###
        @staticmethod
        CMat[T] circular_convolution(CMat[T], CMat[T])  except +

cdef class MatOps:
    @staticmethod
    def fill(Mat mat, filler):
        cdef int filler_int
        cdef CMat[int] out_int
        cdef float filler_float
        cdef CMat[float] out_float
        cdef double filler_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            filler_int = filler
            with nogil:
                out_int = CMatOps[int].fill((<CMat[int]*>((<Mat>(mat)).matinternal))[0], filler_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            filler_float = filler
            with nogil:
                out_float = CMatOps[float].fill((<CMat[float]*>((<Mat>(mat)).matinternal))[0], filler_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            filler_double = filler
            with nogil:
                out_double = CMatOps[double].fill((<CMat[double]*>((<Mat>(mat)).matinternal))[0], filler_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")



    @staticmethod
    def consider_constant(Mat mat):
        if (mat).dtypeinternal == np.NPY_INT32:
            return WrapMat_int(CMatOps[int].consider_constant((<CMat[int]*>((<Mat>(mat)).matinternal))[0]))
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            return WrapMat_float(CMatOps[float].consider_constant((<CMat[float]*>((<Mat>(mat)).matinternal))[0]))
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            return WrapMat_double(CMatOps[double].consider_constant((<CMat[double]*>((<Mat>(mat)).matinternal))[0]))
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def equals(Mat a, Mat b):
        cdef bint out
        if (a).dtypeinternal != (b).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (a).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].equals((<CMat[int]*>((<Mat>(a)).matinternal))[0], (<CMat[int]*>((<Mat>(b)).matinternal))[0])
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].equals((<CMat[float]*>((<Mat>(a)).matinternal))[0], (<CMat[float]*>((<Mat>(b)).matinternal))[0])
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].equals((<CMat[double]*>((<Mat>(a)).matinternal))[0], (<CMat[double]*>((<Mat>(b)).matinternal))[0])
            return out
        else:
            raise ValueError("Invalid dtype:" + str(a.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def allclose(Mat a, Mat b, float tol = 1e-6):
        cdef bint out

        if (a).dtypeinternal != (b).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (a).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].allclose((<CMat[int]*>((<Mat>(a)).matinternal))[0], (<CMat[int]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].allclose((<CMat[float]*>((<Mat>(a)).matinternal))[0], (<CMat[float]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].allclose((<CMat[double]*>((<Mat>(a)).matinternal))[0], (<CMat[double]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        else:
            raise ValueError("Invalid dtype:" + str(a.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def is_nan(Mat mat):
        cdef bint out

        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].is_nan((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].is_nan((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return out
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def is_grad_nan(Mat mat):
        cdef bint out

        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].is_grad_nan((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].is_grad_nan((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return out
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def grad_allclose(Mat a, Mat b, float tol = 1e-6):
        cdef bint out
        if (a).dtypeinternal != (b).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (a).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].grad_allclose((<CMat[int]*>((<Mat>(a)).matinternal))[0], (<CMat[int]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].grad_allclose((<CMat[float]*>((<Mat>(a)).matinternal))[0], (<CMat[float]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        elif (a).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].grad_allclose((<CMat[double]*>((<Mat>(a)).matinternal))[0], (<CMat[double]*>((<Mat>(b)).matinternal))[0], tol)
            return out
        else:
            raise ValueError("Invalid dtype:" + str(a.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def argsort(Mat mat):
        cdef vector[int] out
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].argsort((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].argsort((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].argsort((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return out
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def argmax(Mat mat, axis=None):
        cdef int         out_int
        cdef vector[int] out_vector
        cdef int axis_int
        if (mat).dtypeinternal == np.NPY_INT32:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[int].argmax_axis((<CMat[int]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[int].argmax((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[float].argmax_axis((<CMat[float]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[float].argmax((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[double].argmax_axis((<CMat[double]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[double].argmax((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def argmin(Mat mat, axis=None):
        cdef int         out_int
        cdef vector[int] out_vector
        cdef int axis_int
        if (mat).dtypeinternal == np.NPY_INT32:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[int].argmin_axis((<CMat[int]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[int].argmin((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[float].argmin_axis((<CMat[float]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[float].argmin((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            if axis is not None:
                axis_int = axis
                with nogil:
                    out_vector = CMatOps[double].argmin_axis((<CMat[double]*>((<Mat>(mat)).matinternal))[0], axis_int)
                return out_vector
            else:
                with nogil:
                    out_int = CMatOps[double].argmin((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                return out_int
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def argmax_slice(Mat mat, int lower, int upper):
        cdef int out
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].argmax_slice((<CMat[int]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].argmax_slice((<CMat[float]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].argmax_slice((<CMat[double]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def argmin_slice(Mat mat, int lower, int upper):
        cdef int out
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out = CMatOps[int].argmin_slice((<CMat[int]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out = CMatOps[float].argmin_slice((<CMat[float]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out = CMatOps[double].argmin_slice((<CMat[double]*>((<Mat>(mat)).matinternal))[0], lower, upper)
            return out
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")



    @staticmethod
    def copy(Mat destination, Mat source):
        if (destination).dtypeinternal != (source).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (destination).dtypeinternal == np.NPY_INT32:
            with nogil:
                CMatOps[int].copy((<CMat[int]*>((<Mat>(destination)).matinternal)), (<CMat[int]*>((<Mat>(source)).matinternal))[0])
        elif (destination).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].copy((<CMat[float]*>((<Mat>(destination)).matinternal)), (<CMat[float]*>((<Mat>(source)).matinternal))[0])
        elif (destination).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].copy((<CMat[double]*>((<Mat>(destination)).matinternal)), (<CMat[double]*>((<Mat>(source)).matinternal))[0])
        else:
            raise ValueError("Invalid dtype:" + str(destination.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def copy_grad(Mat destination, Mat source):
        if (destination).dtypeinternal != (source).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (destination).dtypeinternal == np.NPY_INT32:
            with nogil:
                CMatOps[int].copy_grad((<CMat[int]*>((<Mat>(destination)).matinternal)), (<CMat[int]*>((<Mat>(source)).matinternal))[0])
        elif (destination).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].copy_grad((<CMat[float]*>((<Mat>(destination)).matinternal)), (<CMat[float]*>((<Mat>(source)).matinternal))[0])
        elif (destination).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].copy_grad((<CMat[double]*>((<Mat>(destination)).matinternal)), (<CMat[double]*>((<Mat>(source)).matinternal))[0])
        else:
            raise ValueError("Invalid dtype:" + str(destination.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    # ### REDUCERS ###
    @staticmethod
    def sum(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].sum((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].sum_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].sum_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].sum((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].sum_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].sum_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].sum((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].sum_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].sum_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def L2_norm(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].L2_norm((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].L2_norm_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].L2_norm_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].L2_norm((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].L2_norm_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].L2_norm_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].L2_norm((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].L2_norm_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].L2_norm_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def mean(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].mean((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].mean_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].mean_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].mean((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].mean_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].mean_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].mean((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].mean_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].mean_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def grad_norm(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].grad_norm((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].grad_norm_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].grad_norm_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].grad_norm((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].grad_norm_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].grad_norm_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].grad_norm((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].grad_norm_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].grad_norm_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def min(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].min((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].min_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].min_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].min((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].min_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].min_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].min((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].min_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].min_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def max(Mat mat, axis=None):
        cdef bint error = False
        cdef int true_axis
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis is None:
            true_axis = -1
        else:
            true_axis = axis
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if true_axis == -1:
                    out_int = CMatOps[int].max((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_int = CMatOps[int].max_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_int = CMatOps[int].max_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if true_axis == -1:
                    out_float = CMatOps[float].max((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_float = CMatOps[float].max_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_float = CMatOps[float].max_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if true_axis == -1:
                    out_double = CMatOps[double].max((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 0:
                    out_double = CMatOps[double].max_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                elif true_axis == 1:
                    out_double = CMatOps[double].max_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
                else:
                    error = True
            if error:
                assert False
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    ### RESHAPING ###

    @staticmethod
    def resize(Mat mat,  unsigned int rows, unsigned int cols):
        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                CMatOps[int].resize((<CMat[int]*>((<Mat>(mat)).matinternal))[0], rows, cols)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].resize((<CMat[float]*>((<Mat>(mat)).matinternal))[0], rows, cols)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].resize((<CMat[double]*>((<Mat>(mat)).matinternal))[0], rows, cols)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")



    @staticmethod
    def hstack(arg1, arg2=None):
        cdef vector[CMat[int]] input_matrices_int
        cdef CMat[int] out_int
        cdef vector[CMat[float]] input_matrices_float
        cdef CMat[float] out_float
        cdef vector[CMat[double]] input_matrices_double
        cdef CMat[double] out_double

        cdef Mat left
        cdef Mat right
        cdef common_dtype
        if arg2 is None:
            if len(arg1) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(arg1[0])).dtypeinternal
            for el in arg1:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_INT32:
                input_matrices_int = mats_to_vec_int(arg1)
                with nogil:
                    out_int = CMatOps[int].hstack_vec(input_matrices_int)
                return WrapMat_int(out_int)
            elif common_dtype == np.NPY_FLOAT32:
                input_matrices_float = mats_to_vec_float(arg1)
                with nogil:
                    out_float = CMatOps[float].hstack_vec(input_matrices_float)
                return WrapMat_float(out_float)
            elif common_dtype == np.NPY_FLOAT64:
                input_matrices_double = mats_to_vec_double(arg1)
                with nogil:
                    out_double = CMatOps[double].hstack_vec(input_matrices_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(arg1[0].dtype) + " (should be one of np.int32, np.float32, np.float64)")

        else:
            left  = <Mat> arg1
            right = <Mat> arg2
            if (left).dtypeinternal != (right).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (left).dtypeinternal == np.NPY_INT32:
                with nogil:
                    out_int = CMatOps[int].hstack((<CMat[int]*>((<Mat>(left)).matinternal))[0], (<CMat[int]*>((<Mat>(right)).matinternal))[0])
                return WrapMat_int(out_int)
            elif (left).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    out_float = CMatOps[float].hstack((<CMat[float]*>((<Mat>(left)).matinternal))[0], (<CMat[float]*>((<Mat>(right)).matinternal))[0])
                return WrapMat_float(out_float)
            elif (left).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    out_double = CMatOps[double].hstack((<CMat[double]*>((<Mat>(left)).matinternal))[0], (<CMat[double]*>((<Mat>(right)).matinternal))[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(left.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def vstack(arg1, arg2=None):
        cdef vector[CMat[int]] input_matrices_int
        cdef CMat[int] out_int
        cdef vector[CMat[float]] input_matrices_float
        cdef CMat[float] out_float
        cdef vector[CMat[double]] input_matrices_double
        cdef CMat[double] out_double

        cdef Mat top
        cdef Mat bottom
        cdef common_dtype
        if arg2 is None:
            if len(arg1) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<Mat>(arg1[0])).dtypeinternal
            for el in arg1:
                if (<Mat>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_INT32:
                input_matrices_int = mats_to_vec_int(arg1)
                with nogil:
                    out_int = CMatOps[int].vstack_vec(input_matrices_int)
                return WrapMat_int(out_int)
            elif common_dtype == np.NPY_FLOAT32:
                input_matrices_float = mats_to_vec_float(arg1)
                with nogil:
                    out_float = CMatOps[float].vstack_vec(input_matrices_float)
                return WrapMat_float(out_float)
            elif common_dtype == np.NPY_FLOAT64:
                input_matrices_double = mats_to_vec_double(arg1)
                with nogil:
                    out_double = CMatOps[double].vstack_vec(input_matrices_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(arg1[0].dtype) + " (should be one of np.int32, np.float32, np.float64)")

        else:
            top    = <Mat> arg1
            bottom = <Mat> arg2
            if (top).dtypeinternal != (bottom).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (top).dtypeinternal == np.NPY_INT32:
                with nogil:
                    out_int = CMatOps[int].vstack((<CMat[int]*>((<Mat>(top)).matinternal))[0], (<CMat[int]*>((<Mat>(bottom)).matinternal))[0])
                return WrapMat_int(out_int)
            elif (top).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    out_float = CMatOps[float].vstack((<CMat[float]*>((<Mat>(top)).matinternal))[0], (<CMat[float]*>((<Mat>(bottom)).matinternal))[0])
                return WrapMat_float(out_float)
            elif (top).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    out_double = CMatOps[double].vstack((<CMat[double]*>((<Mat>(top)).matinternal))[0], (<CMat[double]*>((<Mat>(bottom)).matinternal))[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(top.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def row_pluck(Mat mat, int idx):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].row_pluck((<CMat[int]*>((<Mat>(mat)).matinternal))[0], idx)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].row_pluck((<CMat[float]*>((<Mat>(mat)).matinternal))[0], idx)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].row_pluck((<CMat[double]*>((<Mat>(mat)).matinternal))[0], idx)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def reshape(Mat mat, unsigned int rows, unsigned int cols):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].reshape((<CMat[int]*>((<Mat>(mat)).matinternal))[0], rows, cols)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].reshape((<CMat[float]*>((<Mat>(mat)).matinternal))[0], rows, cols)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].reshape((<CMat[double]*>((<Mat>(mat)).matinternal))[0], rows, cols)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def rows_pluck(Mat mat, Mat idx):
        cdef CMat[int]* idx_mat
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double


        assert idx.dtypeinternal == np.NPY_INT32, \
                "Only integer tensors can be used for indexing"
        idx_mat = <CMat[int]*> idx.matinternal

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].rows_pluck((<CMat[int]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].rows_pluck((<CMat[float]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].rows_pluck((<CMat[double]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def transpose(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double


        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].transpose((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].transpose((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].transpose((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    # ### UPDATES ###
    @staticmethod
    def clip_and_regularize(Mat mat, float clipval = 5.0, float regc = 1e-6):
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].clip_and_regularize((<CMat[float]*>((<Mat>(mat)).matinternal))[0], clipval, regc)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].clip_and_regularize((<CMat[double]*>((<Mat>(mat)).matinternal))[0], clipval, regc)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def regularize(Mat mat, float regc = 1e-6):
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].regularize((<CMat[float]*>((<Mat>(mat)).matinternal))[0], regc)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].regularize((<CMat[double]*>((<Mat>(mat)).matinternal))[0], regc)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def normalize(Mat mat, float norm_threshold = 5.0):
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].normalize((<CMat[float]*>((<Mat>(mat)).matinternal))[0], norm_threshold)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].normalize((<CMat[double]*>((<Mat>(mat)).matinternal))[0], norm_threshold)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def sgd_update(Mat param, float step_size):
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].sgd_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], step_size)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].sgd_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], step_size)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def adagrad_update(Mat param, Mat cache, float step_size, float smooth_eps):
        if (param).dtypeinternal != (cache).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].adagrad_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], (<CMat[float]*>((<Mat>(cache)).matinternal))[0], step_size, smooth_eps)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].adagrad_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], (<CMat[double]*>((<Mat>(cache)).matinternal))[0], step_size, smooth_eps)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def rmsprop_update(Mat param, Mat cache, float decay_rate, float step_size, float smooth_eps):
        if (param).dtypeinternal != (cache).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].rmsprop_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], (<CMat[float]*>((<Mat>(cache)).matinternal))[0], decay_rate, step_size, smooth_eps)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].rmsprop_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], (<CMat[double]*>((<Mat>(cache)).matinternal))[0], decay_rate, step_size, smooth_eps)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def rmsprop_momentum_update(Mat param,
                                Mat n_cache,
                                Mat g_cache,
                                Mat momentum_cache,
                                float decay_rate,
                                float momentum,
                                float step_size,
                                float smooth_eps):
        if (param).dtypeinternal != (n_cache).dtypeinternal or (n_cache).dtypeinternal != (g_cache).dtypeinternal or (g_cache).dtypeinternal != (momentum_cache).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].rmsprop_momentum_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], (<CMat[float]*>((<Mat>(n_cache)).matinternal))[0], (<CMat[float]*>((<Mat>(g_cache)).matinternal))[0], (<CMat[float]*>((<Mat>(momentum_cache)).matinternal))[0],
                                                          decay_rate, momentum, step_size, smooth_eps)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].rmsprop_momentum_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], (<CMat[double]*>((<Mat>(n_cache)).matinternal))[0], (<CMat[double]*>((<Mat>(g_cache)).matinternal))[0], (<CMat[double]*>((<Mat>(momentum_cache)).matinternal))[0],
                                                          decay_rate, momentum, step_size, smooth_eps)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def adadelta_update(Mat param, Mat gsum, Mat xsum, float rho, float smooth_eps):
        if (param).dtypeinternal != (gsum).dtypeinternal or (gsum).dtypeinternal != (xsum).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].adadelta_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], (<CMat[float]*>((<Mat>(gsum)).matinternal))[0], (<CMat[float]*>((<Mat>(xsum)).matinternal))[0], rho, smooth_eps)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].adadelta_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], (<CMat[double]*>((<Mat>(gsum)).matinternal))[0], (<CMat[double]*>((<Mat>(xsum)).matinternal))[0], rho, smooth_eps)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def adam_update(Mat param, Mat m, Mat v, float b1, float b2, float smooth_eps, float step_size, int epoch):
        if (param).dtypeinternal != (m).dtypeinternal or (m).dtypeinternal != (v).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (param).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                CMatOps[float].adam_update((<CMat[float]*>((<Mat>(param)).matinternal))[0], (<CMat[float]*>((<Mat>(m)).matinternal))[0], (<CMat[float]*>((<Mat>(v)).matinternal))[0], b1, b2, smooth_eps, step_size, epoch)
        elif (param).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                CMatOps[double].adam_update((<CMat[double]*>((<Mat>(param)).matinternal))[0], (<CMat[double]*>((<Mat>(m)).matinternal))[0], (<CMat[double]*>((<Mat>(v)).matinternal))[0], b1, b2, smooth_eps, step_size, epoch)
        else:
            raise ValueError("Invalid dtype:" + str(param.dtype) + " (should be one of np.float32, np.float64)")


    ### ELEMWISE ###

    @staticmethod
    def add(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].add((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].add((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].add((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def sub_broadcast_reversed(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].sub_broadcast_reversed((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].sub_broadcast_reversed((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].sub_broadcast_reversed((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def eltdivide(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].eltdivide((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].eltdivide((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].eltdivide((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def eltmax(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].eltmax((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].eltmax((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].eltmax((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def dropout(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].dropout((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].dropout((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].dropout((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def dropout_normalized(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].dropout_normalized((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].dropout_normalized((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].dropout_normalized((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def pow(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].pow((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].pow((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].pow((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")




    @staticmethod
    def sigmoid_binary_cross_entropy(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if type(val) == Mat:
            if (mat).dtypeinternal != (<Mat>val).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    out_float = CMatOps[float].sigmoid_binary_cross_entropy_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(val)).matinternal))[0])
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    out_double = CMatOps[double].sigmoid_binary_cross_entropy_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(val)).matinternal))[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                val_float = val
                with nogil:
                    out_float = CMatOps[float].sigmoid_binary_cross_entropy((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                val_double = val
                with nogil:
                    out_double = CMatOps[double].sigmoid_binary_cross_entropy((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")

    @staticmethod
    def binary_cross_entropy(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if type(val) == Mat:
            if (mat).dtypeinternal != (<Mat>val).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    out_float = CMatOps[float].binary_cross_entropy_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(val)).matinternal))[0])
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    out_double = CMatOps[double].binary_cross_entropy_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(val)).matinternal))[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                val_float = val
                with nogil:
                    out_float = CMatOps[float].binary_cross_entropy((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                val_double = val
                with nogil:
                    out_double = CMatOps[double].binary_cross_entropy((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def square(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].square((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].square((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].square((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def log(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].log((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].log((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].log((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def exp(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].exp((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].exp((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].exp((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def sigmoid(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].sigmoid((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].sigmoid((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].sigmoid((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def tanh(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].tanh((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].tanh((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].tanh((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def relu(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].relu((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].relu((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].relu((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def abs(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].abs((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].abs((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].abs((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def sqrt(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].sqrt((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].sqrt((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].sqrt((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def elt_inv(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].elt_inv((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].elt_inv((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].elt_inv((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    @staticmethod
    def fast_dropout(Mat mat):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                out_int = CMatOps[int].fast_dropout((<CMat[int]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].fast_dropout((<CMat[float]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].fast_dropout((<CMat[double]*>((<Mat>(mat)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def _eltmul_mat(Mat mat, Mat other, bint broadcast=True, int axis=1):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal != (other).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (mat).dtypeinternal == np.NPY_INT32:
            if broadcast:
                if axis != 1 and axis != 0:
                    raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
            with nogil:
                if broadcast:
                    if axis == 1:
                        out_int = CMatOps[int].eltmul_broadcast_rowwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>((<Mat>(other)).matinternal))[0])
                    elif axis == 0:
                        out_int = CMatOps[int].eltmul_broadcast_colwise((<CMat[int]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>((<Mat>(other)).matinternal))[0])
                else:
                    out_int = CMatOps[int].eltmul_mat((<CMat[int]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>((<Mat>(other)).matinternal))[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            if broadcast:
                if axis != 1 and axis != 0:
                    raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
            with nogil:
                if broadcast:
                    if axis == 1:
                        out_float = CMatOps[float].eltmul_broadcast_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(other)).matinternal))[0])
                    elif axis == 0:
                        out_float = CMatOps[float].eltmul_broadcast_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(other)).matinternal))[0])
                else:
                    out_float = CMatOps[float].eltmul_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(other)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            if broadcast:
                if axis != 1 and axis != 0:
                    raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
            with nogil:
                if broadcast:
                    if axis == 1:
                        out_double = CMatOps[double].eltmul_broadcast_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(other)).matinternal))[0])
                    elif axis == 0:
                        out_double = CMatOps[double].eltmul_broadcast_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(other)).matinternal))[0])
                else:
                    out_double = CMatOps[double].eltmul_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(other)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def _eltmul_val(Mat mat, val):
        cdef int val_int
        cdef CMat[int] out_int
        cdef float val_float
        cdef CMat[float] out_float
        cdef double val_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            val_int = val
            with nogil:
                out_int = CMatOps[int].eltmul((<CMat[int]*>((<Mat>(mat)).matinternal))[0], val_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            val_float = val
            with nogil:
                out_float = CMatOps[float].eltmul((<CMat[float]*>((<Mat>(mat)).matinternal))[0], val_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            val_double = val
            with nogil:
                out_double = CMatOps[double].eltmul((<CMat[double]*>((<Mat>(mat)).matinternal))[0], val_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def eltmul(Mat mat, other, bint broadcast=True, int axis=1):
        if type(other) == Mat:
            return MatOps._eltmul_mat(mat, other, broadcast, axis)
        else:
            return MatOps._eltmul_val(mat, other)

    @staticmethod
    def dropout(Mat mat, drop_prob, normalized=True):
        cdef int drop_prob_int
        cdef CMat[int] out_int
        cdef float drop_prob_float
        cdef CMat[float] out_float
        cdef double drop_prob_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            drop_prob_int = drop_prob
            if normalized:
                with nogil:
                    out_int = CMatOps[int].dropout_normalized((<CMat[int]*>((<Mat>(mat)).matinternal))[0], drop_prob_int)
                return WrapMat_int(out_int)
            else:
                with nogil:
                    out_int = CMatOps[int].dropout((<CMat[int]*>((<Mat>(mat)).matinternal))[0], drop_prob_int)
                return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            drop_prob_float = drop_prob
            if normalized:
                with nogil:
                    out_float = CMatOps[float].dropout_normalized((<CMat[float]*>((<Mat>(mat)).matinternal))[0], drop_prob_float)
                return WrapMat_float(out_float)
            else:
                with nogil:
                    out_float = CMatOps[float].dropout((<CMat[float]*>((<Mat>(mat)).matinternal))[0], drop_prob_float)
                return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            drop_prob_double = drop_prob
            if normalized:
                with nogil:
                    out_double = CMatOps[double].dropout_normalized((<CMat[double]*>((<Mat>(mat)).matinternal))[0], drop_prob_double)
                return WrapMat_double(out_double)
            else:
                with nogil:
                    out_double = CMatOps[double].dropout((<CMat[double]*>((<Mat>(mat)).matinternal))[0], drop_prob_double)
                return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")



    @staticmethod
    def steep_sigmoid(Mat mat, aggressiveness =  3.75):
        cdef int aggressiveness_int
        cdef CMat[int] out_int
        cdef float aggressiveness_float
        cdef CMat[float] out_float
        cdef double aggressiveness_double
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_INT32:
            aggressiveness_int = aggressiveness
            with nogil:
                out_int = CMatOps[int].steep_sigmoid((<CMat[int]*>((<Mat>(mat)).matinternal))[0], aggressiveness_int)
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            aggressiveness_float = aggressiveness
            with nogil:
                out_float = CMatOps[float].steep_sigmoid((<CMat[float]*>((<Mat>(mat)).matinternal))[0], aggressiveness_float)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            aggressiveness_double = aggressiveness
            with nogil:
                out_double = CMatOps[double].steep_sigmoid((<CMat[double]*>((<Mat>(mat)).matinternal))[0], aggressiveness_double)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    @staticmethod
    def _softmax_cross_entropy_int(Mat mat, int answer_idx, int axis=1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].SCE_colwise_int((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx)
                elif axis == 1:
                    out_float = CMatOps[float].SCE_rowwise_int((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx)
        
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].SCE_colwise_int((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx)
                elif axis == 1:
                    out_double = CMatOps[double].SCE_rowwise_int((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx)
        
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")


    @staticmethod
    def _softmax_cross_entropy_mat(Mat mat, Mat idx, int axis=1):
        cdef CMat[int]* idx_mat
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double


        if idx.dtypeinternal != np.NPY_INT32:
            raise ValueError("Only integer tensors can be used for indexing")
        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")

        idx_mat = <CMat[int]*> idx.matinternal

        if (mat).dtypeinternal == np.NPY_INT32:
            with nogil:
                if axis == 0:
                    out_int = CMatOps[int].SCE_colwise_mat((<CMat[int]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
                elif axis == 1:
                    out_int = CMatOps[int].SCE_rowwise_mat((<CMat[int]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_int(out_int)
        elif (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].SCE_colwise_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
                elif axis == 1:
                    out_float = CMatOps[float].SCE_rowwise_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].SCE_colwise_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
                elif axis == 1:
                    out_double = CMatOps[double].SCE_rowwise_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], idx_mat[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.int32, np.float32, np.float64)")




    @staticmethod
    def cross_entropy(Mat mat, index, int axis=1):
        if type(index) == Mat:
            return MatOps._cross_entropy_mat(mat, <Mat>index, axis)
        elif type(index) == int:
            return MatOps._cross_entropy_int(mat, <int>index, axis)
        else:
            raise AttributeError("Cross entropy takes integer of Tensor of integers as argument.")

    @staticmethod
    def _cross_entropy_mat(Mat mat, Mat index, int axis=1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if index.dtypeinternal == np.NPY_INT32:
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    if axis == 0:
                        out_float = CMatOps[float].CE_colwise_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>(<Mat>index).matinternal)[0])
                    elif axis == 1:
                        out_float = CMatOps[float].CE_rowwise_mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>(<Mat>index).matinternal)[0])
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    if axis == 0:
                        out_double = CMatOps[double].CE_colwise_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>(<Mat>index).matinternal)[0])
                    elif axis == 1:
                        out_double = CMatOps[double].CE_rowwise_mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[int]*>(<Mat>index).matinternal)[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")

        else:
            if (mat).dtypeinternal != (index).dtypeinternal:
               raise ValueError("All arguments must be of the same type")
            if (mat).dtypeinternal == np.NPY_FLOAT32:
                with nogil:
                    out_float = CMatOps[float].CE_Mat((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(index)).matinternal))[0])
                return WrapMat_float(out_float)
            elif (mat).dtypeinternal == np.NPY_FLOAT64:
                with nogil:
                    out_double = CMatOps[double].CE_Mat((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(index)).matinternal))[0])
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def _cross_entropy_int(Mat mat, int answer_idx, int axis=1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].CE_colwise_int((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx)
                elif axis == 1:
                    out_float = CMatOps[float].CE_rowwise_int((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx)
        
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].CE_colwise_int((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx)
                elif axis == 1:
                    out_double = CMatOps[double].CE_rowwise_int((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx)
        
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def softmax_cross_entropy(Mat mat, index, int axis=1):
        if type(index) == Mat:
            return MatOps._softmax_cross_entropy_mat(mat, <Mat>index, axis)
        elif type(index) == int:
            return MatOps._softmax_cross_entropy_int(mat, <int>index, axis)
        else:
            raise AttributeError("Softmax cross entropy takes integer of Tensor of integers as argument.")

    @staticmethod
    def margin_loss(Mat mat, int answer_idx, int axis = 1, float margin = 0.1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].margin_loss_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx, margin)
                elif axis == 1:
                    out_float = CMatOps[float].margin_loss_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], answer_idx, margin)
        
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].margin_loss_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx, margin)
                elif axis == 1:
                    out_double = CMatOps[double].margin_loss_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], answer_idx, margin)
        
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")





    @staticmethod
    def softmax(Mat mat, float temperature = 1.0, int axis = 1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].softmax_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], temperature)
                elif axis == 1:
                    out_float = CMatOps[float].softmax_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], temperature)
        
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].softmax_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], temperature)
                elif axis == 1:
                    out_double = CMatOps[double].softmax_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], temperature)
        
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def softmax_no_grad(Mat mat, float temperature = 1.0, int axis = 1):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if axis != 0 and axis != 1:
            raise ValueError("axis must be 0 (columnwise) or 1 (rowwise)")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].softmax_no_grad_colwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], temperature)
                elif axis == 1:
                    out_float = CMatOps[float].softmax_no_grad_rowwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], temperature)
        
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].softmax_no_grad_colwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], temperature)
                elif axis == 1:
                    out_double = CMatOps[double].softmax_no_grad_rowwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], temperature)
        
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def softmax_list(list mats, float temperature=1.0):
        cdef vector[CMat[float]] input_matrices_float
        cdef vector[CMat[float]] out_list_float
        cdef CMat[float]         out_mat_float
        cdef vector[CMat[double]] input_matrices_double
        cdef vector[CMat[double]] out_list_double
        cdef CMat[double]         out_mat_double

        cdef common_dtype

        if len(mats) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(mats[0])).dtypeinternal
        for el in mats:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            input_matrices_float = mats_to_vec_float(mats)
            with nogil:
                out_list_float = CMatOps[float].softmax_vector(input_matrices_float, temperature)
            out_py_list = []
            for out_mat_float in out_list_float:
                out_py_list.append(WrapMat_float(out_mat_float))
            return out_py_list
        elif common_dtype == np.NPY_FLOAT64:
            input_matrices_double = mats_to_vec_double(mats)
            with nogil:
                out_list_double = CMatOps[double].softmax_vector(input_matrices_double, temperature)
            out_py_list = []
            for out_mat_double in out_list_double:
                out_py_list.append(WrapMat_double(out_mat_double))
            return out_py_list
        else:
            raise ValueError("Invalid dtype:" + str(mats[0].dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def cross_entropy_elementwise(Mat mat, Mat target):
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal != (target).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].CE_eltwise((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(target)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].CE_eltwise((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(target)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def circular_convolution(Mat mat, Mat shift):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal != (shift).dtypeinternal:
           raise ValueError("All arguments must be of the same type")
        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = CMatOps[float].circular_convolution((<CMat[float]*>((<Mat>(mat)).matinternal))[0], (<CMat[float]*>((<Mat>(shift)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = CMatOps[double].circular_convolution((<CMat[double]*>((<Mat>(mat)).matinternal))[0], (<CMat[double]*>((<Mat>(shift)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")



    @staticmethod
    def broadcast(Mat mat, int axis, int num_replicas):
        cdef CMat[int] out_int
        cdef CMat[float] out_float
        cdef CMat[double] out_double

        if (mat).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                if axis == 0:
                    out_float = CMatOps[float].broadcast_row_vector((<CMat[float]*>((<Mat>(mat)).matinternal))[0], num_replicas)
                elif axis == 1:
                    out_float = CMatOps[float].broadcast_col_vector((<CMat[float]*>((<Mat>(mat)).matinternal))[0], num_replicas)
            return WrapMat_float(out_float)
        elif (mat).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                if axis == 0:
                    out_double = CMatOps[double].broadcast_row_vector((<CMat[double]*>((<Mat>(mat)).matinternal))[0], num_replicas)
                elif axis == 1:
                    out_double = CMatOps[double].broadcast_col_vector((<CMat[double]*>((<Mat>(mat)).matinternal))[0], num_replicas)
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(mat.dtype) + " (should be one of np.float32, np.float64)")

