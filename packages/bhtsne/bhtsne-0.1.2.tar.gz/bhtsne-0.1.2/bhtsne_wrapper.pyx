# distutils: language = c++
import numpy as np
cimport numpy as np
cimport cython

cdef extern from "tsne.h":
    cdef cppclass TSNE:
        TSNE()
        void run(double* X, int N, int D, double* Y, int no_dims, double perplexity, double theta, int rand_seed, double* SX, int SN)

cdef class BHTSNE:
    cdef TSNE* tsne

    def __cinit__(self):
        self.tsne = new TSNE()

    def __dealloc__(self):
        del self.tsne

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def run(self, X, no_rows, no_cols, no_dims, perplexity, theta, rand_seed, seed_positions, seed_positions_no_cols):
        cdef np.ndarray[np.float64_t, ndim=2, mode='c'] _X = np.ascontiguousarray(X)
        cdef np.ndarray[np.float64_t, ndim=2, mode='c'] Y = np.zeros((no_rows, no_dims), dtype=np.float64)
        cdef np.ndarray[np.float64_t, ndim=2, mode='c'] SX
        if seed_positions_no_cols > 0:
          SX = np.ascontiguousarray(seed_positions)
        else:
          SX = np.zeros((no_rows, no_dims), dtype=np.float64)
        self.tsne.run(&_X[0,0], no_rows, no_cols, &Y[0,0], no_dims, perplexity, theta, rand_seed, &SX[0,0], seed_positions_no_cols)
        return Y
