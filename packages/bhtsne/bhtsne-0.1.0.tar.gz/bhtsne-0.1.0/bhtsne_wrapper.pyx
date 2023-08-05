# distutils: language = c++
import numpy as np
cimport numpy as np
cimport cython

cdef extern from "tsne.h":
    cdef cppclass TSNE:
        TSNE()
        void run(double* X, int N, int D, double* Y, int no_dims, double perplexity, double theta, int rand_seed)


cdef class BHTSNE:
    cdef TSNE* tsne

    def __cinit__(self):
        self.tsne = new TSNE()

    def __dealloc__(self):
        del self.tsne

    @cython.boundscheck(False)
    @cython.wraparound(False)
    def run(self, X, N, D, d, perplexity, theta, rand_seed):
        cdef np.ndarray[np.float64_t, ndim=2, mode='c'] _X = np.ascontiguousarray(X)
        cdef np.ndarray[np.float64_t, ndim=2, mode='c'] Y = np.zeros((N, d), dtype=np.float64)
        self.tsne.run(&_X[0,0], N, D, &Y[0,0], d, perplexity, theta, rand_seed)
        return Y
