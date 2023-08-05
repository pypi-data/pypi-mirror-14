


cdef extern from "dali/layers/Layers.h" nogil:
    cdef cppclass CLayer "Layer" [T]:
        int hidden_size
        int input_size
        CMat[T] W
        CMat[T] b

        vector[CMat[T]] parameters() const
        # constructors
        CLayer()
        CLayer(int input_size, int hidden_size)
        CLayer(const CLayer& other, bint copy_w, bint copy_dw)

        CMat[T] activate(CMat[T]) except +
        CLayer[T] shallow_copy() const

    cdef cppclass CRNN "RNN" [T] nogil:
        int input_size
        int hidden_size
        int output_size

        CMat[T] Wx
        CMat[T] Wh
        CMat[T] b

        CRNN()
        CRNN(int input_size, int hidden_size)
        CRNN(int input_size, int hidden_size, int output_size)
        CRNN(CRNN[T]&, bool, bool)
        CMat[T] activate(CMat[T] input_vector, CMat[T] prev_hidden) except +
        CRNN[T] shallow_copy() const
        vector[CMat[T]] parameters() const

    cdef cppclass CStackedInputLayer "StackedInputLayer" [T] nogil:
        vector[int] input_sizes() const
        int hidden_size
        vector[CMat[T]] matrices
        CMat[T] b

        vector[CMat[T]] parameters() const
        CStackedInputLayer()
        CStackedInputLayer(vector[int] input_sizes, int output_size)
        CStackedInputLayer(const CStackedInputLayer& other, bint copy_w, bint copy_dw)

        CMat[T] activate(const vector[CMat[T]]&) except +
        CMat[T] activate(CMat[T]) except +
        CMat[T] activate(CMat[T], const vector[CMat[T]]&) except +

        CStackedInputLayer[T] shallow_copy() const


cdef class Layer:
    cdef void* layerinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(Layer self):
            return np.PyArray_DescrFromType(self.dtypeinternal)



    property input_size:
        def __get__(Layer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLayer[float]*>((<Layer>(self)).layerinternal))[0].input_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLayer[double]*>((<Layer>(self)).layerinternal))[0].input_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property hidden_size:
        def __get__(Layer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLayer[float]*>((<Layer>(self)).layerinternal))[0].hidden_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLayer[double]*>((<Layer>(self)).layerinternal))[0].hidden_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")



    property W:
        def __get__(Layer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CLayer[float]*>((<Layer>(self)).layerinternal))[0].W)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CLayer[double]*>((<Layer>(self)).layerinternal))[0].W)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property b:
        def __get__(Layer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CLayer[float]*>((<Layer>(self)).layerinternal))[0].b)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CLayer[double]*>((<Layer>(self)).layerinternal))[0].b)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def name_parameters(self, prefix):
        self.W.name = prefix + ".W"
        self.b.name = prefix + ".b"

    def __cinit__(Layer self, int input_size, int hidden_size, dtype=np.float32):
        self.layerinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE


        self.dtypeinternal = np.dtype(dtype).num
        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.layerinternal = new CLayer[float](input_size, hidden_size)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.layerinternal = new CLayer[double](input_size, hidden_size)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(Layer self):
        self.free_internal()

    cdef free_internal(Layer self):
        cdef CLayer[float]* ptr_internal_float
        cdef CLayer[double]* ptr_internal_double

        if self.layerinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CLayer[float]*>((<Layer>(self)).layerinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CLayer[double]*>((<Layer>(self)).layerinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.layerinternal = NULL

    def activate(Layer self, Mat input_vector):
        assert self.dtypeinternal == input_vector.dtypeinternal, \
               "All arguments must be of the same type"
        cdef CMat[float] out_float
        cdef CMat[double] out_double


        if (self).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = (<CLayer[float]*>((<Layer>(self)).layerinternal))[0].activate((<CMat[float]*>((<Mat>(input_vector)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = (<CLayer[double]*>((<Layer>(self)).layerinternal))[0].activate((<CMat[double]*>((<Mat>(input_vector)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")



    def shallow_copy(Layer self):
        cdef Layer copy = Layer(0,0)
        copy.free_internal()
        if (self).dtypeinternal == np.NPY_FLOAT32:
            copy.layerinternal = new CLayer[float]((<CLayer[float]*>((<Layer>(self)).layerinternal))[0], False, True)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            copy.layerinternal = new CLayer[double]((<CLayer[double]*>((<Layer>(self)).layerinternal))[0], False, True)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return copy

    def parameters(Layer self):
        params = []
        cdef CMat[float]         param_float
        cdef vector[CMat[float]] param_vec_float
        cdef CMat[double]         param_double
        cdef vector[CMat[double]] param_vec_double

        if (self).dtypeinternal == np.NPY_FLOAT32:
            param_vec_float = (<CLayer[float]*>((<Layer>(self)).layerinternal))[0].parameters()
            for param_float in param_vec_float:
                params.append(WrapMat_float(param_float))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            param_vec_double = (<CLayer[double]*>((<Layer>(self)).layerinternal))[0].parameters()
            for param_double in param_vec_double:
                params.append(WrapMat_double(param_double))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return params

    def __setstate__(Layer self, state):
        for param, saved_param in zip(self.parameters(), state["parameters"]):
            param.w = saved_param.w
        self.dtypeinternal = state["dtype"].num

    def __getstate__(Layer self):
        return {
            "parameters" : self.parameters(),
            "dtype" : self.dtype
        }

    def __reduce__(Layer self):
        return (
            self.__class__,
            (
                self.input_size,
                self.hidden_size,
            ), self.__getstate__(),
        )

    def __str__(self):
        return "<Layer in=%d, hidden=%d>" % (self.input_size, self.hidden_size)

    def __repr__(Layer self):
        return str(self)

cdef void copy_name_layer_int(const CLayer[int]& internal, const CLayer[int]& output):
    copy_name_int(internal.W, output.W)
    copy_name_int(internal.b, output.b)
cdef void copy_name_layer_float(const CLayer[float]& internal, const CLayer[float]& output):
    copy_name_float(internal.W, output.W)
    copy_name_float(internal.b, output.b)
cdef void copy_name_layer_double(const CLayer[double]& internal, const CLayer[double]& output):
    copy_name_double(internal.W, output.W)
    copy_name_double(internal.b, output.b)


cdef inline Layer WrapLayer_int(const CLayer[int]& internal):
    cdef Layer output = Layer(0,0)
    output.free_internal()
    output.layerinternal = new CLayer[int](internal, False, False)
    output.dtypeinternal = np.NPY_INT32

    copy_name_layer_int(internal, (<CLayer[int]*>((<Layer>(output)).layerinternal))[0])

    return output
cdef inline Layer WrapLayer_float(const CLayer[float]& internal):
    cdef Layer output = Layer(0,0)
    output.free_internal()
    output.layerinternal = new CLayer[float](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT32

    copy_name_layer_float(internal, (<CLayer[float]*>((<Layer>(output)).layerinternal))[0])

    return output
cdef inline Layer WrapLayer_double(const CLayer[double]& internal):
    cdef Layer output = Layer(0,0)
    output.free_internal()
    output.layerinternal = new CLayer[double](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT64

    copy_name_layer_double(internal, (<CLayer[double]*>((<Layer>(output)).layerinternal))[0])

    return output



cdef class RNN:
    cdef void*        layerinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(RNN self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property input_size:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRNN[float]*>((<RNN>(self)).layerinternal))[0].input_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRNN[double]*>((<RNN>(self)).layerinternal))[0].input_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property hidden_size:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRNN[float]*>((<RNN>(self)).layerinternal))[0].hidden_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRNN[double]*>((<RNN>(self)).layerinternal))[0].hidden_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property output_size:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CRNN[float]*>((<RNN>(self)).layerinternal))[0].output_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CRNN[double]*>((<RNN>(self)).layerinternal))[0].output_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")



    property Wx:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CRNN[float]*>((<RNN>(self)).layerinternal))[0].Wx)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CRNN[double]*>((<RNN>(self)).layerinternal))[0].Wx)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property Wh:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CRNN[float]*>((<RNN>(self)).layerinternal))[0].Wh)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CRNN[double]*>((<RNN>(self)).layerinternal))[0].Wh)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property b:
        def __get__(RNN self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CRNN[float]*>((<RNN>(self)).layerinternal))[0].b)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CRNN[double]*>((<RNN>(self)).layerinternal))[0].b)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def name_parameters(self, prefix):
        self.Wx.name = prefix + ".Wx"
        self.Wh.name = prefix + ".Wh"
        self.b.name = prefix + ".b"


    def __cinit__(self, int input_size, int hidden_size, output_size = None, dtype=np.float32):
        self.layerinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE

        if output_size is None:
            output_size = hidden_size
        assert(input_size > -1 and hidden_size > -1 and output_size > -1), "Only positive dimensions may be used."
        cdef int out_size = output_size

        self.dtypeinternal = np.dtype(dtype).num

        if (<RNN>self).dtypeinternal == np.NPY_FLOAT32:
            self.layerinternal = new CRNN[float](input_size, hidden_size, out_size)
        elif (<RNN>self).dtypeinternal == np.NPY_FLOAT64:
            self.layerinternal = new CRNN[double](input_size, hidden_size, out_size)
        else:
            raise ValueError("Invalid dtype:" + str(<RNN>self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(RNN self):
        self.free_internal()

    cdef free_internal(RNN self):
        cdef CRNN[float]* ptr_internal_float
        cdef CRNN[double]* ptr_internal_double

        if self.layerinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CRNN[float]*>((<RNN>(self)).layerinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CRNN[double]*>((<RNN>(self)).layerinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.layerinternal = NULL



    def __setstate__(RNN self, state):
        for param, saved_param in zip(self.parameters(), state["parameters"]):
            param.w = saved_param.w
        self.dtypeinternal = state["dtype"].num


    def __getstate__(self):
        return {
            "parameters" : self.parameters(),
            "dtype" : self.dtype
        }

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.input_size,
                self.hidden_size,
                self.output_size
            ), self.__getstate__(),
        )


    def activate(RNN self, Mat input_vector,  Mat prev_hidden):
        assert self.dtypeinternal == input_vector.dtypeinternal and \
               self.dtypeinternal == prev_hidden.dtypeinternal, \
               "All arguments must be of the same type"
        cdef CMat[float] out_float
        cdef CMat[double] out_double


        if (self).dtypeinternal == np.NPY_FLOAT32:
            with nogil:
                out_float = (<CRNN[float]*>((<RNN>(self)).layerinternal))[0].activate((<CMat[float]*>((<Mat>(input_vector)).matinternal))[0], (<CMat[float]*>((<Mat>(prev_hidden)).matinternal))[0])
            return WrapMat_float(out_float)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            with nogil:
                out_double = (<CRNN[double]*>((<RNN>(self)).layerinternal))[0].activate((<CMat[double]*>((<Mat>(input_vector)).matinternal))[0], (<CMat[double]*>((<Mat>(prev_hidden)).matinternal))[0])
            return WrapMat_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")



    def shallow_copy(RNN self):
        cdef RNN copy = RNN(0,0)
        copy.free_internal()
        if (self).dtypeinternal == np.NPY_FLOAT32:
            copy.layerinternal = new CRNN[float]((<CRNN[float]*>((<RNN>(self)).layerinternal))[0], False, True)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            copy.layerinternal = new CRNN[double]((<CRNN[double]*>((<RNN>(self)).layerinternal))[0], False, True)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return copy

    def parameters(RNN self):
        params = []
        cdef CMat[float]         param_float
        cdef vector[CMat[float]] param_vec_float
        
        cdef CMat[double]         param_double
        cdef vector[CMat[double]] param_vec_double
        

        if (self).dtypeinternal == np.NPY_FLOAT32:
            param_vec_float = (<CRNN[float]*>((<RNN>(self)).layerinternal))[0].parameters()
            for param_float in param_vec_float:
                params.append(WrapMat_float(param_float))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            param_vec_double = (<CRNN[double]*>((<RNN>(self)).layerinternal))[0].parameters()
            for param_double in param_vec_double:
                params.append(WrapMat_double(param_double))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return params


    def __str__(self):
        return "<RNN in=%d, hidden=%d out=%d>" % (self.input_size, self.hidden_size, self.output_size)

    def __repr__(Layer self):
        return str(self)


cdef class StackedInputLayer:
    cdef void* layerinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(StackedInputLayer self):
            return np.PyArray_DescrFromType(self.dtypeinternal)


    property input_sizes:
        def __get__(StackedInputLayer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].input_sizes()
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].input_sizes()
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property hidden_size:
        def __get__(StackedInputLayer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].hidden_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].hidden_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property matrices:
        def __get__(StackedInputLayer self):
            cdef int i
            params = []
            if (self).dtypeinternal == np.NPY_FLOAT32:
                for i in range((<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].matrices.size()):
                    params.append(WrapMat_float((<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].matrices[i]))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                for i in range((<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].matrices.size()):
                    params.append(WrapMat_double((<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].matrices[i]))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            return params

    property b:
        def __get__(StackedInputLayer self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].b)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].b)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def name_parameters(self, prefix):
        for matidx, matrix in enumerate(self.matrices):
            matrix.name = prefix + ".matrices[%d]" % (matidx,)
        self.b.name = prefix + ".b"

    def __cinit__(StackedInputLayer self, list input_sizes, int hidden_size, dtype=np.float32):
        self.layerinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE

        self.dtypeinternal = np.dtype(dtype).num

        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.layerinternal = new CStackedInputLayer[float](<vector[int]>input_sizes, hidden_size)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.layerinternal = new CStackedInputLayer[double](<vector[int]>input_sizes, hidden_size)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(StackedInputLayer self):
        self.free_internal()

    cdef free_internal(StackedInputLayer self):
        cdef CStackedInputLayer[float]* ptr_internal_float
        cdef CStackedInputLayer[double]* ptr_internal_double

        if self.layerinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.layerinternal = NULL

    def __setstate__(StackedInputLayer self, state):
        for param, saved_param in zip(self.parameters(), state["parameters"]):
            param.w = saved_param.w
            self.dtypeinternal = state["dtype"].num

    def __getstate__(self):
        return {
            "parameters" : self.parameters(),
            "dtype" : self.dtype,
        }

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.input_sizes,
                self.hidden_size
            ), self.__getstate__(),
        )

    def activate(StackedInputLayer self, input_vectors):
        cdef vector[CMat[float]]  input_vec_float
        cdef CMat[float]          input_mat_float
        cdef CMat[float]          out_float
        cdef vector[CMat[double]]  input_vec_double
        cdef CMat[double]          input_mat_double
        cdef CMat[double]          out_double


        if type(input_vectors) is Mat:
            assert (<Mat>input_vectors).dtypeinternal == self.dtypeinternal, \
                    "input mat must be of the same type as StackedInputLayer"

            if (self).dtypeinternal == np.NPY_FLOAT32:
                input_mat_float = (<CMat[float]*>((<Mat>(input_vectors)).matinternal))[0]
                with nogil:
                    out_float = (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].activate(input_mat_float)
                return WrapMat_float(out_float)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                input_mat_double = (<CMat[double]*>((<Mat>(input_vectors)).matinternal))[0]
                with nogil:
                    out_double = (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].activate(input_mat_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        elif type(input_vectors) == list:
            for v in input_vectors:
                assert type(v) == Mat, "Matrices required for Stacked Input Layer"
                assert (<Mat>v).dtypeinternal == self.dtypeinternal, "All arguments must have the same type."


            if (self).dtypeinternal == np.NPY_FLOAT32:
                input_vec_float.clear()
                for inpt in input_vectors:
                    input_vec_float.push_back((<CMat[float]*>((<Mat>(inpt)).matinternal))[0])
                with nogil:
                    out_float = (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].activate(input_vec_float)
                return WrapMat_float(out_float)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                input_vec_double.clear()
                for inpt in input_vectors:
                    input_vec_double.push_back((<CMat[double]*>((<Mat>(inpt)).matinternal))[0])
                with nogil:
                    out_double = (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].activate(input_vec_double)
                return WrapMat_double(out_double)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        else:
            raise TypeError("activate takes a list of Mat or single Mat as input.")

    def shallow_copy(StackedInputLayer self):
        cdef StackedInputLayer copy = StackedInputLayer(0,0)
        copy.free_internal()
        if (self).dtypeinternal == np.NPY_FLOAT32:
            copy.layerinternal = new CStackedInputLayer[float]((<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0], False, True)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            copy.layerinternal = new CStackedInputLayer[double]((<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0], False, True)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return copy


    def parameters(StackedInputLayer self):
        params = []
        cdef CMat[float]         param_float
        cdef vector[CMat[float]] param_vec_float
        
        cdef CMat[double]         param_double
        cdef vector[CMat[double]] param_vec_double
        

        if (self).dtypeinternal == np.NPY_FLOAT32:
            param_vec_float = (<CStackedInputLayer[float]*>((<StackedInputLayer>(self)).layerinternal))[0].parameters()
            for param_float in param_vec_float:
                params.append(WrapMat_float(param_float))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            param_vec_double = (<CStackedInputLayer[double]*>((<StackedInputLayer>(self)).layerinternal))[0].parameters()
            for param_double in param_vec_double:
                params.append(WrapMat_double(param_double))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return params

    def __str__(self):
        return "<StackedInputLayer in=%s, out=%d>" % (str(self.input_sizes), self.hidden_size)

    def __repr__(StackedInputLayer self):
        return str(self)

cdef void copy_name_stackedlayer_int(const CStackedInputLayer[int]& internal, const CStackedInputLayer[int]& output):
    for i in range(internal.matrices.size()):
        copy_name_int(internal.matrices[i], output.matrices[i])
    copy_name_int(internal.b, output.b)
cdef void copy_name_stackedlayer_float(const CStackedInputLayer[float]& internal, const CStackedInputLayer[float]& output):
    for i in range(internal.matrices.size()):
        copy_name_float(internal.matrices[i], output.matrices[i])
    copy_name_float(internal.b, output.b)
cdef void copy_name_stackedlayer_double(const CStackedInputLayer[double]& internal, const CStackedInputLayer[double]& output):
    for i in range(internal.matrices.size()):
        copy_name_double(internal.matrices[i], output.matrices[i])
    copy_name_double(internal.b, output.b)



cdef inline StackedInputLayer WrapStackedLayer_int(const CStackedInputLayer[int]& internal):
    cdef StackedInputLayer output = StackedInputLayer([0],0)
    output.free_internal()
    output.layerinternal = new CStackedInputLayer[int](internal, False, False)
    output.dtypeinternal = np.NPY_INT32

    copy_name_stackedlayer_int(internal, (<CStackedInputLayer[int]*>((<StackedInputLayer>(output)).layerinternal))[0])

    return output
cdef inline StackedInputLayer WrapStackedLayer_float(const CStackedInputLayer[float]& internal):
    cdef StackedInputLayer output = StackedInputLayer([0],0)
    output.free_internal()
    output.layerinternal = new CStackedInputLayer[float](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT32

    copy_name_stackedlayer_float(internal, (<CStackedInputLayer[float]*>((<StackedInputLayer>(output)).layerinternal))[0])

    return output
cdef inline StackedInputLayer WrapStackedLayer_double(const CStackedInputLayer[double]& internal):
    cdef StackedInputLayer output = StackedInputLayer([0],0)
    output.free_internal()
    output.layerinternal = new CStackedInputLayer[double](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT64

    copy_name_stackedlayer_double(internal, (<CStackedInputLayer[double]*>((<StackedInputLayer>(output)).layerinternal))[0])

    return output

