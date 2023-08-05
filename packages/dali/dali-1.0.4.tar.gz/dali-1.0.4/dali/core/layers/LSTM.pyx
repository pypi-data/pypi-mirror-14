

from cython.operator cimport dereference as deref

cdef extern from "dali/layers/LSTM.h":
    cdef cppclass CLSTMState "LSTMState" [T] nogil:
        CMat[T] memory
        CMat[T] hidden
        CLSTMState()
        CLSTMState(CMat[T] memory, CMat[T] hidden)
        @staticmethod
        vector[CMat[T]] hiddens(const vector[CMat[T]]&)
        @staticmethod
        vector[CMat[T]] memories(const vector[CMat[T]]&)

    cdef cppclass CLSTM "LSTM" [T] nogil:
        int hidden_size
        int num_children
        vector[int] input_sizes
        CMat[T] Wco
        vector[CMat[T]] Wcells_to_inputs
        vector[CMat[T]] Wcells_to_forgets
        CStackedInputLayer[T] input_layer
        vector[CStackedInputLayer[T]] forget_layers
        CStackedInputLayer[T] output_layer
        CStackedInputLayer[T] cell_layer

        bint memory_feeds_gates
        bint backprop_through_gates
        CLSTM()
        CLSTM(int input_size, int hidden_size, bint memory_feeds_gates)
        CLSTM(int input_size, int hidden_size, int num_children, bint memory_feeds_gates)
        CLSTM(vector[int] input_sizes, int hidden_size, int num_children, bint memory_feeds_gates)
        CLSTM(const CLSTM& other, bint copy_w, bint copy_dw)
        vector[CMat[T]] parameters() const
        @staticmethod
        vector[CLSTMState[T]] initial_states(const vector[int]& hidden_sizes)
        CLSTMState[T] initial_states() const

        CLSTMState[T] activate(CMat[T] input_vector, CLSTMState[T] previous_state)  except +
        CLSTMState[T] activate_children "activate"(CMat[T] input_vector, vector[CLSTMState[T]] previous_children_states)  except +
        CLSTMState[T] activate_many_inputs "activate"(vector[CMat[T]] input_vectors, vector[CLSTMState[T]] previous_children_states) except +
        CLSTMState[T] activate_shortcut "activate"(CMat[T] input_vector, CMat[T] shortcut_vector, CLSTMState[T] previous_children_state) except +
        CLSTM[T] shallow_copy() const
        CLSTMState[T] activate_sequence(CLSTMState[T], const vector[CMat[T]]& input_vectors) except +

    cdef cppclass CStackedLSTM "StackedLSTM" [T] nogil:
        vector[CLSTM[T]] cells
        bint shortcut
        bint memory_feeds_gates
        vector[CLSTMState[T]] activate(vector[CLSTMState[T]] previous_state, CMat[T] inpt, T drop_prob) except +
        vector[CLSTMState[T]] activate(vector[CLSTMState[T]] previous_state, vector[CMat[T]] inpt, T drop_prob) except +
        vector[CMat[T]] parameters() const
        CStackedLSTM();
        CStackedLSTM(const CStackedLSTM& other, bint copy_w, bint copy_dw)
        CStackedLSTM(const int& input_size, const vector[int]& hidden_sizes, bint shortcut, bint memory_feeds_gates)
        CStackedLSTM(const vector[int]& input_size, const vector[int]& hidden_sizes, bint shortcut, bint memory_feeds_gates)
        vector[CLSTMState[T]] initial_states() const
        CStackedLSTM[T] shallow_copy() const



cdef class LSTMState:
    cdef void* lstmstateinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(LSTMState self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    def __cinit__(self, memory=None, hidden=None, dtype=None):
        self.lstmstateinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE

        if dtype is None and memory is not None:
            dtype = memory.dtype
        elif dtype is None and hidden is not None:
            dtype = hidden.dtype

        self.dtypeinternal = np.dtype(dtype).num
        if (self).dtypeinternal == np.NPY_FLOAT32:
            self.lstmstateinternal = new CLSTMState[float]()
            if memory is not None:
                assert type(memory) == Mat
                if self.dtypeinternal != (<Mat>memory).dtypeinternal:
                    raise ValueError("Dtype disagreement")
                (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].memory = (<CMat[float]*>((<Mat>(memory)).matinternal))[0]
            if hidden is not None:
                assert type(hidden) == Mat
                if self.dtypeinternal != (<Mat>hidden).dtypeinternal:
                    raise ValueError("Dtype disagreement")
                (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden = (<CMat[float]*>((<Mat>(hidden)).matinternal))[0]
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            self.lstmstateinternal = new CLSTMState[double]()
            if memory is not None:
                assert type(memory) == Mat
                if self.dtypeinternal != (<Mat>memory).dtypeinternal:
                    raise ValueError("Dtype disagreement")
                (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].memory = (<CMat[double]*>((<Mat>(memory)).matinternal))[0]
            if hidden is not None:
                assert type(hidden) == Mat
                if self.dtypeinternal != (<Mat>hidden).dtypeinternal:
                    raise ValueError("Dtype disagreement")
                (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden = (<CMat[double]*>((<Mat>(hidden)).matinternal))[0]
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(LSTMState self):
        self.free_internal()

    cdef free_internal(LSTMState self):
        cdef CLSTMState[float]* ptr_internal_float
        cdef CLSTMState[double]* ptr_internal_double

        if self.lstmstateinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.lstmstateinternal = NULL


    property memory:
        def __get__(LSTMState self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                if (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].memory.number_of_elements() == 0:
                    return None
                return WrapMat_float((<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].memory)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                if (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].memory.number_of_elements() == 0:
                    return None
                return WrapMat_double((<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].memory)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        def __set__(LSTMState self, Mat value):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                assert self.dtypeinternal == value.dtypeinternal,             "memory must have the same dtype as LSTMState"
                (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].memory = (<CMat[float]*>((<Mat>(value)).matinternal))[0]
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                assert self.dtypeinternal == value.dtypeinternal,             "memory must have the same dtype as LSTMState"
                (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].memory = (<CMat[double]*>((<Mat>(value)).matinternal))[0]
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

    property hidden:
        def __get__(LSTMState self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                if (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden.number_of_elements() == 0:
                    return None
                return WrapMat_float((<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                if (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden.number_of_elements() == 0:
                    return None
                return WrapMat_double((<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        def __set__(LSTMState self, Mat value):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                assert self.dtypeinternal == value.dtypeinternal,             "hidden must have the same dtype as LSTMState"
                (<CLSTMState[float]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden = (<CMat[float]*>((<Mat>(value)).matinternal))[0]
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                assert self.dtypeinternal == value.dtypeinternal,             "hidden must have the same dtype as LSTMState"
                (<CLSTMState[double]*>((<LSTMState>(self)).lstmstateinternal))[0].hidden = (<CMat[double]*>((<Mat>(value)).matinternal))[0]
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __setstate__(LSTMState self, state):
        self.memory        = state["memory"]
        self.hidden        = state["hidden"]
        self.dtypeinternal = state["dtype"]

    def __getstate__(self):
        return {
            "memory" : self.memory,
            "hidden" : self.hidden,
            "dtype"  : self.dtypeinternal,
        }

    def __reduce__(self):
        return (
            self.__class__,
            (), self.__getstate__(),
        )


cdef inline LSTMState WrapLSTMState_int(const CLSTMState[int]& internal):
    cdef LSTMState output = LSTMState(dtype=np.int32)

    (<CLSTMState[int]*>((<LSTMState>(output)).lstmstateinternal))[0].memory = internal.memory
    (<CLSTMState[int]*>((<LSTMState>(output)).lstmstateinternal))[0].hidden = internal.hidden

    return output
cdef inline LSTMState WrapLSTMState_float(const CLSTMState[float]& internal):
    cdef LSTMState output = LSTMState(dtype=np.float32)

    (<CLSTMState[float]*>((<LSTMState>(output)).lstmstateinternal))[0].memory = internal.memory
    (<CLSTMState[float]*>((<LSTMState>(output)).lstmstateinternal))[0].hidden = internal.hidden

    return output
cdef inline LSTMState WrapLSTMState_double(const CLSTMState[double]& internal):
    cdef LSTMState output = LSTMState(dtype=np.float64)

    (<CLSTMState[double]*>((<LSTMState>(output)).lstmstateinternal))[0].memory = internal.memory
    (<CLSTMState[double]*>((<LSTMState>(output)).lstmstateinternal))[0].hidden = internal.hidden

    return output


cdef inline list WrapLSTMStates_int(const vector[CLSTMState[int]]& internal):
    cdef CLSTMState[int] state
    res = []

    cdef vector[CLSTMState[int]].const_iterator it = internal.const_begin()

    while it != internal.const_end():
        res.append(WrapLSTMState_int(deref(it)))
        it += 1

    return res
cdef inline list WrapLSTMStates_float(const vector[CLSTMState[float]]& internal):
    cdef CLSTMState[float] state
    res = []

    cdef vector[CLSTMState[float]].const_iterator it = internal.const_begin()

    while it != internal.const_end():
        res.append(WrapLSTMState_float(deref(it)))
        it += 1

    return res
cdef inline list WrapLSTMStates_double(const vector[CLSTMState[double]]& internal):
    cdef CLSTMState[double] state
    res = []

    cdef vector[CLSTMState[double]].const_iterator it = internal.const_begin()

    while it != internal.const_end():
        res.append(WrapLSTMState_double(deref(it)))
        it += 1

    return res



cdef inline vector[CLSTMState[int]] lstm_states_to_vec_int(list lstmstates):
    "Converts a list of mats to a vector[CMat[int]]"
    cdef vector[CLSTMState[int]] lstmstates_vec
    lstmstates_vec.reserve(len(lstmstates))
    for lstmstate in lstmstates:
        lstmstates_vec.push_back((<CLSTMState[int]*>((<LSTMState>(lstmstate)).lstmstateinternal))[0])
    return lstmstates_vec
cdef inline vector[CLSTMState[float]] lstm_states_to_vec_float(list lstmstates):
    "Converts a list of mats to a vector[CMat[float]]"
    cdef vector[CLSTMState[float]] lstmstates_vec
    lstmstates_vec.reserve(len(lstmstates))
    for lstmstate in lstmstates:
        lstmstates_vec.push_back((<CLSTMState[float]*>((<LSTMState>(lstmstate)).lstmstateinternal))[0])
    return lstmstates_vec
cdef inline vector[CLSTMState[double]] lstm_states_to_vec_double(list lstmstates):
    "Converts a list of mats to a vector[CMat[double]]"
    cdef vector[CLSTMState[double]] lstmstates_vec
    lstmstates_vec.reserve(len(lstmstates))
    for lstmstate in lstmstates:
        lstmstates_vec.push_back((<CLSTMState[double]*>((<LSTMState>(lstmstate)).lstmstateinternal))[0])
    return lstmstates_vec


cdef class LSTM:
    cdef void* layerinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(LSTM self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property Wco:
        def __get__(LSTM self):
            if not self.memory_feeds_gates:
                raise AttributeError("LSTM without memory_feeds_gates does not have Wco")
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapMat_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].Wco)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapMat_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].Wco)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property Wcells_to_inputs:
        def __get__(LSTM self):
            if not self.memory_feeds_gates:
                raise AttributeError("LSTM without memory_feeds_gates does not have Wcells_to_inputs")

            cdef int i
            cdef vector[CMat[float]] mats_float
            cdef vector[CMat[double]] mats_double


            params = []
            if (self).dtypeinternal == np.NPY_FLOAT32:
                for i in range((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_inputs.size()):
                    params.append(WrapMat_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_inputs[i]))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                for i in range((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_inputs.size()):
                    params.append(WrapMat_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_inputs[i]))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            return params
    property Wcells_to_forgets:
        def __get__(LSTM self):
            if not self.memory_feeds_gates:
                raise AttributeError("LSTM without memory_feeds_gates does not have Wcells_to_forgets")

            cdef int i
            cdef vector[CMat[float]] mats_float
            cdef vector[CMat[double]] mats_double


            params = []
            if (self).dtypeinternal == np.NPY_FLOAT32:
                for i in range((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_forgets.size()):
                    params.append(WrapMat_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_forgets[i]))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                for i in range((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_forgets.size()):
                    params.append(WrapMat_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].Wcells_to_forgets[i]))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            return params

    property input_layer:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapStackedLayer_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].input_layer)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapStackedLayer_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].input_layer)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property output_layer:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapStackedLayer_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].output_layer)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapStackedLayer_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].output_layer)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property cell_layer:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return WrapStackedLayer_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].cell_layer)
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return WrapStackedLayer_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].cell_layer)
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property forget_layer:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                assert (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].forget_layers.size() == 1
                return WrapStackedLayer_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].forget_layers[0])
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                assert (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].forget_layers.size() == 1
                return WrapStackedLayer_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].forget_layers[0])
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property forget_layers:
        def __get__(LSTM self):
            cdef CStackedInputLayer[float] layer_float
            cdef vector[CStackedInputLayer[float]] layers_float
            cdef CStackedInputLayer[double] layer_double
            cdef vector[CStackedInputLayer[double]] layers_double


            layers = []

            if (self).dtypeinternal == np.NPY_FLOAT32:
                for i in range((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].forget_layers.size()):
                    layers.append(WrapStackedLayer_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].forget_layers[i]))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                for i in range((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].forget_layers.size()):
                    layers.append(WrapStackedLayer_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].forget_layers[i]))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            return layers

    property input_size:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                assert len((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].input_sizes) == 1
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].input_sizes[0]
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                assert len((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].input_sizes) == 1
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].input_sizes[0]
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property input_sizes:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].input_sizes
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].input_sizes
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property hidden_size:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].hidden_size
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].hidden_size
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property num_children:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].num_children
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].num_children
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property memory_feeds_gates:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].memory_feeds_gates
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].memory_feeds_gates
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    property backprop_through_gates:
        def __get__(LSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].backprop_through_gates
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].backprop_through_gates
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")



    def name_parameters(self, prefix):
        self.input_layer.name_parameters(prefix + ".input_layer")
        self.cell_layer.name_parameters(prefix + ".cell_layer")
        self.output_layer.name_parameters(prefix + ".output_layer")
        if len(self.forget_layers) == 1:
            self.forget_layer.name_parameters(prefix + ".forget_layer")
        else:
            for forget_idx, forget_layer in enumerate(self.forget_layers):
                forget_layer.name_parameters(prefix + ".forget_layer[%d]" % (forget_idx,))

        if self.memory_feeds_gates:
            for param_idx, param in enumerate(self.Wcells_to_inputs):
                param.name = prefix + ".Wcells_to_inputs[%d]" % (param_idx,)

            for param_idx, param in enumerate(self.Wcells_to_forgets):
                param.name = prefix + ".WCells_to_forgets[%d]" % (param_idx,)
            self.Wco.name = prefix + ".Wco"

    def __cinit__(LSTM self, input_sizes, hidden_size, num_children=1, memory_feeds_gates=False, dtype=np.float32):
        self.layerinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE

        self.dtypeinternal = np.dtype(dtype).num

        if (self).dtypeinternal == np.NPY_FLOAT32:
            if type(input_sizes) == list:
                self.layerinternal = new CLSTM[float](<vector[int]> input_sizes, <int> hidden_size, <int> num_children, <bint> memory_feeds_gates)
            elif type(input_sizes) == int:
                self.layerinternal = new CLSTM[float](<int> input_sizes, <int> hidden_size, <int> num_children, <bint> memory_feeds_gates)
            else:
                raise ValueError("LSTM input_sizes must be a list or int, not " + type(input_sizes))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            if type(input_sizes) == list:
                self.layerinternal = new CLSTM[double](<vector[int]> input_sizes, <int> hidden_size, <int> num_children, <bint> memory_feeds_gates)
            elif type(input_sizes) == int:
                self.layerinternal = new CLSTM[double](<int> input_sizes, <int> hidden_size, <int> num_children, <bint> memory_feeds_gates)
            else:
                raise ValueError("LSTM input_sizes must be a list or int, not " + type(input_sizes))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(StackedInputLayer self):
        self.free_internal()

    cdef free_internal(LSTM self):
        cdef CLSTM[float]* ptr_internal_float
        cdef CLSTM[double]* ptr_internal_double

        if self.layerinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CLSTM[float]*>((<LSTM>(self)).layerinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CLSTM[double]*>((<LSTM>(self)).layerinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.layerinternal = NULL

    def __call__(LSTM self, *args, **kwargs):
        return self.activate(*args, **kwargs)

    def activate(LSTM self, inpt, previous_states):
        cdef vector[CMat[float]]       inpt_vector_float
        cdef vector[CLSTMState[float]] previous_states_vector_float
        cdef CLSTMState[float] out_float
        cdef vector[CMat[double]]       inpt_vector_double
        cdef vector[CLSTMState[double]] previous_states_vector_double
        cdef CLSTMState[double] out_double

        if type(inpt) != list:
            inpt = [inpt]

        for inpt_el in inpt:
            assert type(inpt_el) == Mat, "LSTM accepts only tensors as input."
            assert (<Mat>inpt_el).dtypeinternal == self.dtypeinternal, \
                    "LSTM received input with different dtype."

        if type(previous_states) != list:
            previous_states = [previous_states]

        for previous_state in previous_states:
            assert type(previous_state) == LSTMState, "LSTM accepts only LSTMState as state."
            assert (<LSTMState>previous_state).dtypeinternal == self.dtypeinternal, \
                    "LSTM received state with different dtype."
        if (self).dtypeinternal == np.NPY_FLOAT32:
            inpt_vector_float = mats_to_vec_float(inpt)
            previous_states_vector_float = lstm_states_to_vec_float(previous_states)
        
            with nogil:
                out_float = (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].activate_many_inputs(inpt_vector_float, previous_states_vector_float)
        
            return WrapLSTMState_float(out_float)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            inpt_vector_double = mats_to_vec_double(inpt)
            previous_states_vector_double = lstm_states_to_vec_double(previous_states)
        
            with nogil:
                out_double = (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].activate_many_inputs(inpt_vector_double, previous_states_vector_double)
        
            return WrapLSTMState_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")




    def activate_sequence(LSTM self, list input_sequence, initial_state = None):
        if self.num_children != 1:
            raise NotImplementedError("Activate sequence is only available for single children LSTMs")

        cdef vector[CMat[float]] c_input_sequence_float
        cdef CLSTMState[float] out_float
        cdef vector[CMat[double]] c_input_sequence_double
        cdef CLSTMState[double] out_double


        if initial_state is None:
            initial_state = self.initial_states()

        if type(initial_state) is not LSTMState:
            raise ValueError("initial_state must be a LSTMState")

        if len(input_sequence) == 0:
            raise ValueError('list cannot be empty')
        common_dtype = (<Mat>(input_sequence[0])).dtypeinternal
        for el in input_sequence:
            if (<Mat>el).dtypeinternal != common_dtype:
                common_dtype = -1
                break
        if common_dtype == -1:
            raise ValueError("All the arguments must be of the same type")
        if common_dtype == np.NPY_FLOAT32:
            c_input_sequence_float = mats_to_vec_float(input_sequence)
            if self.dtypeinternal != np.NPY_FLOAT32:
                raise ValueError("Invalid dtype for input_sequence: " + str(input_sequence[0].dtype) + ", when LSTM is " + str(self.dtype))
            if (<LSTMState>initial_state).dtypeinternal != self.dtypeinternal:
                raise ValueError("Invalid dtype for initial_state: " + str(initial_state.dtype) + ", when LSTM is " + str(self.dtype))
            with nogil:
                out_float = (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].activate_sequence((<CLSTMState[float]*>((<LSTMState>(initial_state)).lstmstateinternal))[0], c_input_sequence_float)
            return WrapLSTMState_float(out_float)
        elif common_dtype == np.NPY_FLOAT64:
            c_input_sequence_double = mats_to_vec_double(input_sequence)
            if self.dtypeinternal != np.NPY_FLOAT64:
                raise ValueError("Invalid dtype for input_sequence: " + str(input_sequence[0].dtype) + ", when LSTM is " + str(self.dtype))
            if (<LSTMState>initial_state).dtypeinternal != self.dtypeinternal:
                raise ValueError("Invalid dtype for initial_state: " + str(initial_state.dtype) + ", when LSTM is " + str(self.dtype))
            with nogil:
                out_double = (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].activate_sequence((<CLSTMState[double]*>((<LSTMState>(initial_state)).lstmstateinternal))[0], c_input_sequence_double)
            return WrapLSTMState_double(out_double)
        else:
            raise ValueError("Invalid dtype:" + str(input_sequence[0].dtype) + " (should be one of np.float32, np.float64)")



    def initial_states(LSTM self):
        if (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapLSTMState_float((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].initial_states())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapLSTMState_double((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].initial_states())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def shallow_copy(LSTM self):
        cdef LSTM copy = LSTM(0,0)
        copy.free_internal()
        if (self).dtypeinternal == np.NPY_FLOAT32:
            copy.layerinternal = new CLSTM[float]((<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0], False, False)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            copy.layerinternal = new CLSTM[double]((<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0], False, False)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return copy

    def parameters(LSTM self):
        params = []
        cdef CMat[float]         param_float
        cdef vector[CMat[float]] param_vec_float
        
        cdef CMat[double]         param_double
        cdef vector[CMat[double]] param_vec_double
        

        if (self).dtypeinternal == np.NPY_FLOAT32:
            param_vec_float = (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].parameters()
            for param_float in param_vec_float:
                params.append(WrapMat_float(param_float))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            param_vec_double = (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].parameters()
            for param_double in param_vec_double:
                params.append(WrapMat_double(param_double))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return params

    def __setstate__(LSTM self, state):
        for param, saved_param in zip(self.parameters(), state["parameters"]):
            param.w = saved_param.w
        self.dtypeinternal          = state["dtype"]
        if (self).dtypeinternal == np.NPY_FLOAT32:
            (<CLSTM[float]*>((<LSTM>(self)).layerinternal))[0].backprop_through_gates = state["backprop_through_gates"]
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            (<CLSTM[double]*>((<LSTM>(self)).layerinternal))[0].backprop_through_gates = state["backprop_through_gates"]
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __getstate__(self):
        return {
            "parameters" : self.parameters(),
            "backprop_through_gates" : self.backprop_through_gates,
            "dtype" : self.dtypeinternal
        }

    def __reduce__(self):
        return (
            self.__class__,
            (
                self.input_sizes,
                self.hidden_size,
                self.num_children,
                self.memory_feeds_gates
            ), self.__getstate__(),
        )

    def __str__(LSTM self):
        child_string = '' if self.num_children == 1 else ', num_children=%d' % (self.num_children,)
        return "<LSTM inputs=%s, hidden_size=%d%s>" % (self.input_sizes, self.hidden_size, child_string)

    def __repr__(LSTM self):
        return str(self)

cdef void copy_name_lstm_int(const CLSTM[int]& internal, const CLSTM[int]& output):
    cdef int i

    copy_name_int(internal.Wco, output.Wco)

    for i in range(internal.Wcells_to_inputs.size()):
        copy_name_int(internal.Wcells_to_inputs[i], output.Wcells_to_inputs[i])

    for i in range(internal.Wcells_to_forgets.size()):
        copy_name_int(internal.Wcells_to_forgets[i], output.Wcells_to_forgets[i])

    for i in range(internal.forget_layers.size()):
        copy_name_stackedlayer_int(internal.forget_layers[i], output.forget_layers[i])

    copy_name_stackedlayer_int(internal.input_layer, output.input_layer)
    copy_name_stackedlayer_int(internal.output_layer, output.output_layer)
    copy_name_stackedlayer_int(internal.cell_layer, output.cell_layer)
cdef void copy_name_lstm_float(const CLSTM[float]& internal, const CLSTM[float]& output):
    cdef int i

    copy_name_float(internal.Wco, output.Wco)

    for i in range(internal.Wcells_to_inputs.size()):
        copy_name_float(internal.Wcells_to_inputs[i], output.Wcells_to_inputs[i])

    for i in range(internal.Wcells_to_forgets.size()):
        copy_name_float(internal.Wcells_to_forgets[i], output.Wcells_to_forgets[i])

    for i in range(internal.forget_layers.size()):
        copy_name_stackedlayer_float(internal.forget_layers[i], output.forget_layers[i])

    copy_name_stackedlayer_float(internal.input_layer, output.input_layer)
    copy_name_stackedlayer_float(internal.output_layer, output.output_layer)
    copy_name_stackedlayer_float(internal.cell_layer, output.cell_layer)
cdef void copy_name_lstm_double(const CLSTM[double]& internal, const CLSTM[double]& output):
    cdef int i

    copy_name_double(internal.Wco, output.Wco)

    for i in range(internal.Wcells_to_inputs.size()):
        copy_name_double(internal.Wcells_to_inputs[i], output.Wcells_to_inputs[i])

    for i in range(internal.Wcells_to_forgets.size()):
        copy_name_double(internal.Wcells_to_forgets[i], output.Wcells_to_forgets[i])

    for i in range(internal.forget_layers.size()):
        copy_name_stackedlayer_double(internal.forget_layers[i], output.forget_layers[i])

    copy_name_stackedlayer_double(internal.input_layer, output.input_layer)
    copy_name_stackedlayer_double(internal.output_layer, output.output_layer)
    copy_name_stackedlayer_double(internal.cell_layer, output.cell_layer)


cdef inline LSTM WrapLSTM_int(const CLSTM[int]& internal):
    cdef LSTM output = LSTM(0,0)
    cdef vector[CMat[int]] params_internal
    cdef vector[CMat[int]] params_output
    output.free_internal()
    output.layerinternal = new CLSTM[int](internal, False, False)
    output.dtypeinternal = np.NPY_INT32

    copy_name_lstm_int(internal, (<CLSTM[int]*>((<LSTM>(output)).layerinternal))[0])

    return output
cdef inline LSTM WrapLSTM_float(const CLSTM[float]& internal):
    cdef LSTM output = LSTM(0,0)
    cdef vector[CMat[float]] params_internal
    cdef vector[CMat[float]] params_output
    output.free_internal()
    output.layerinternal = new CLSTM[float](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT32

    copy_name_lstm_float(internal, (<CLSTM[float]*>((<LSTM>(output)).layerinternal))[0])

    return output
cdef inline LSTM WrapLSTM_double(const CLSTM[double]& internal):
    cdef LSTM output = LSTM(0,0)
    cdef vector[CMat[double]] params_internal
    cdef vector[CMat[double]] params_output
    output.free_internal()
    output.layerinternal = new CLSTM[double](internal, False, False)
    output.dtypeinternal = np.NPY_FLOAT64

    copy_name_lstm_double(internal, (<CLSTM[double]*>((<LSTM>(output)).layerinternal))[0])

    return output




cdef class StackedLSTM:
    cdef void* layerinternal
    cdef np.NPY_TYPES dtypeinternal

    property dtype:
        def __get__(StackedLSTM self):
            return np.PyArray_DescrFromType(self.dtypeinternal)

    property shortcut:
        def __get__(StackedLSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].shortcut
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].shortcut
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(self, bint param_value):
            if (self).dtypeinternal == np.NPY_INT32:
                (<CStackedLSTM[int]*>((<StackedLSTM>(self)).layerinternal))[0].shortcut = param_value
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].shortcut = param_value
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].shortcut = param_value
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")

    property memory_feeds_gates:
        def __get__(StackedLSTM self):
            if (self).dtypeinternal == np.NPY_FLOAT32:
                return (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].memory_feeds_gates
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                return (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].memory_feeds_gates
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


        def __set__(self, bint param_value):
            if (self).dtypeinternal == np.NPY_INT32:
                (<CStackedLSTM[int]*>((<StackedLSTM>(self)).layerinternal))[0].memory_feeds_gates = param_value
            elif (self).dtypeinternal == np.NPY_FLOAT32:
                (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].memory_feeds_gates = param_value
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].memory_feeds_gates = param_value
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.int32, np.float32, np.float64)")


    property cells:
        def __get__(StackedLSTM self):
            cdef CLSTM[float] lstm_float
            cdef vector[CLSTM[float]] lstms_float
            cdef CLSTM[double] lstm_double
            cdef vector[CLSTM[double]] lstms_double

            ret = []
            if (self).dtypeinternal == np.NPY_FLOAT32:
                for i in range((<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].cells.size()):
                    ret.append(WrapLSTM_float((<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].cells[i]))
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                for i in range((<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].cells.size()):
                    ret.append(WrapLSTM_double((<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].cells[i]))
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            return ret
        def __set__(StackedLSTM self, list cells):
            cdef vector[CLSTM[float]] newcells_float
            cdef vector[CLSTM[double]] newcells_double


            if len(cells) == 0:
                raise ValueError('list cannot be empty')
            common_dtype = (<LSTM>(cells[0])).dtypeinternal
            for el in cells:
                if (<LSTM>el).dtypeinternal != common_dtype:
                    common_dtype = -1
                    break
            if common_dtype == -1:
                raise ValueError("All the arguments must be of the same type")
            if common_dtype == np.NPY_FLOAT32:
                if np.NPY_FLOAT32 != self.dtypeinternal:
                    raise ValueError("LSTM has different dtype than StackedLSTM")
                for cell in cells:
                    newcells_float.push_back((<CLSTM[float]*>((<LSTM>(cell)).layerinternal))[0])
                (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].cells = newcells_float
            elif common_dtype == np.NPY_FLOAT64:
                if np.NPY_FLOAT64 != self.dtypeinternal:
                    raise ValueError("LSTM has different dtype than StackedLSTM")
                for cell in cells:
                    newcells_double.push_back((<CLSTM[double]*>((<LSTM>(cell)).layerinternal))[0])
                (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].cells = newcells_double
            else:
                raise ValueError("Invalid dtype:" + str(cells[0].dtype) + " (should be one of np.float32, np.float64)")


    def name_parameters(self, prefix):
        for cell_idx, cell in enumerate(self.cells):
            cell.name_parameters(prefix + ".cells[%d]" % (cell_idx,))

    def __cinit__(self, input_sizes, hidden_sizes, shortcut=False, memory_feeds_gates=False, dtype=np.float32):

        self.layerinternal = NULL
        self.dtypeinternal = np.NPY_NOTYPE

        ensure_fdtype(np.dtype(dtype).num)
        self.dtypeinternal = np.dtype(dtype).num

        if (self).dtypeinternal == np.NPY_FLOAT32:
            if type(input_sizes) == list:
                self.layerinternal = new CStackedLSTM[float](<vector[int]> input_sizes, <vector[int]> hidden_sizes, <bint> shortcut, <bint> memory_feeds_gates)
            elif type(input_sizes) == int:
                self.layerinternal = new CStackedLSTM[float](<int> input_sizes, <vector[int]> hidden_sizes, <bint> shortcut, <bint> memory_feeds_gates)
            else:
                raise ValueError("list of int required for input_sizes for StackedLSTM constructor not " + type(input_sizes))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            if type(input_sizes) == list:
                self.layerinternal = new CStackedLSTM[double](<vector[int]> input_sizes, <vector[int]> hidden_sizes, <bint> shortcut, <bint> memory_feeds_gates)
            elif type(input_sizes) == int:
                self.layerinternal = new CStackedLSTM[double](<int> input_sizes, <vector[int]> hidden_sizes, <bint> shortcut, <bint> memory_feeds_gates)
            else:
                raise ValueError("list of int required for input_sizes for StackedLSTM constructor not " + type(input_sizes))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __dealloc__(StackedLSTM self):
        self.free_internal()

    cdef free_internal(StackedLSTM self):
        cdef CStackedLSTM[float]* ptr_internal_float
        cdef CStackedLSTM[double]* ptr_internal_double

        if self.layerinternal != NULL:
            if (self).dtypeinternal == np.NPY_FLOAT32:
                ptr_internal_float = (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))
                with nogil:
                    del ptr_internal_float
            elif (self).dtypeinternal == np.NPY_FLOAT64:
                ptr_internal_double = (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))
                with nogil:
                    del ptr_internal_double
            else:
                raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

            self.layerinternal = NULL

    def __call__(StackedLSTM self, *args, **kwargs):
        return self.activate(*args, **kwargs)

    def activate(StackedLSTM self, inputs, hiddens, drop_prob = 0.0):
        cdef vector[CMat[float]]       inputs_vector_float
        cdef vector[CLSTMState[float]] hiddens_vector_float
        cdef vector[CMat[double]]       inputs_vector_double
        cdef vector[CLSTMState[double]] hiddens_vector_double


        for hidden in hiddens:
            assert type(hidden) == LSTMState, "LSTM accepts only LSTMState as state."
            assert (<LSTMState>hidden).dtypeinternal == self.dtypeinternal, \
                    "LSTM received state with different dtype."

        if (self).dtypeinternal == np.NPY_FLOAT32:
            hiddens_vector_float = lstm_states_to_vec_float(hiddens)
            if type(inputs) == list:
                for inpt_el in inputs:
                    assert type(inpt_el) == Mat, "StackedLSTM accepts only tensors as input."
                    assert (<Mat>inpt_el).dtypeinternal == self.dtypeinternal,                     "StackedLSTM received input with different dtype."
        
                inputs_vector_float = mats_to_vec_float(inputs)
                return WrapLSTMStates_float(
                    (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].activate(hiddens_vector_float, inputs_vector_float, <float> drop_prob)
                )
            elif type(inputs) == Mat:
                assert (<Mat>inputs).dtypeinternal == self.dtypeinternal,                 "StackedLSTM received input with different dtype."
                return WrapLSTMStates_float(
                    (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].activate(hiddens_vector_float, (<CMat[float]*>((<Mat>(inputs)).matinternal))[0], <float> drop_prob)
                )
            else:
                raise Exception("list or Mat expected for StackedLSTM activate not " + type(inputs))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            hiddens_vector_double = lstm_states_to_vec_double(hiddens)
            if type(inputs) == list:
                for inpt_el in inputs:
                    assert type(inpt_el) == Mat, "StackedLSTM accepts only tensors as input."
                    assert (<Mat>inpt_el).dtypeinternal == self.dtypeinternal,                     "StackedLSTM received input with different dtype."
        
                inputs_vector_double = mats_to_vec_double(inputs)
                return WrapLSTMStates_double(
                    (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].activate(hiddens_vector_double, inputs_vector_double, <double> drop_prob)
                )
            elif type(inputs) == Mat:
                assert (<Mat>inputs).dtypeinternal == self.dtypeinternal,                 "StackedLSTM received input with different dtype."
                return WrapLSTMStates_double(
                    (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].activate(hiddens_vector_double, (<CMat[double]*>((<Mat>(inputs)).matinternal))[0], <double> drop_prob)
                )
            else:
                raise Exception("list or Mat expected for StackedLSTM activate not " + type(inputs))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def shallow_copy(StackedLSTM self):
        cdef StackedLSTM copy = LSTM(0,0)
        copy.free_internal()
        if (self).dtypeinternal == np.NPY_FLOAT32:
            copy.layerinternal = new CStackedLSTM[float]((<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0], False, False)
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            copy.layerinternal = new CStackedLSTM[double]((<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0], False, False)
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return copy

    def parameters(StackedLSTM self):
        params = []
        cdef CMat[float]         param_float
        cdef vector[CMat[float]] param_vec_float
        
        cdef CMat[double]         param_double
        cdef vector[CMat[double]] param_vec_double
        

        if (self).dtypeinternal == np.NPY_FLOAT32:
            param_vec_float = (<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].parameters()
            for param_float in param_vec_float:
                params.append(WrapMat_float(param_float))
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            param_vec_double = (<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].parameters()
            for param_double in param_vec_double:
                params.append(WrapMat_double(param_double))
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")

        return params

    def initial_states(StackedLSTM self):
        if (self).dtypeinternal == np.NPY_FLOAT32:
            return WrapLSTMStates_float((<CStackedLSTM[float]*>((<StackedLSTM>(self)).layerinternal))[0].initial_states())
        elif (self).dtypeinternal == np.NPY_FLOAT64:
            return WrapLSTMStates_double((<CStackedLSTM[double]*>((<StackedLSTM>(self)).layerinternal))[0].initial_states())
        else:
            raise ValueError("Invalid dtype:" + str(self.dtype) + " (should be one of np.float32, np.float64)")


    def __setstate__(LSTM self, state):
        self.cells              = state["cells"]
        self.dtypeinternal      = state["dtype"]
        self.shortcut           = state["shortcut"]
        self.memory_feeds_gates = state["memory_feeds_gates"]

    def __getstate__(self):
        return {
            "cells"              : self.cells,
            "dtype"              : self.dtypeinternal,
            "shortcut"           : self.shortcut,
            "memory_feeds_gates" : self.memory_feeds_gates,
        }

    def __reduce__(self):
        return (
            self.__class__,
            (
                [],
                [],
                False,
                False
            ), self.__getstate__(),
        )

    def __str__(StackedLSTM self):
        return "<StackedLSTM cells=%r>" % (self.cells)

    def __repr__(StackedLSTM self):
        return str(self)
