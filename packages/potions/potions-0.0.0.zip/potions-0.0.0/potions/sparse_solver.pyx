# cython: boundscheck=False
# cython: cdivision=True
# cython: wraparound=True

from libc.math cimport sqrt
from cython.parallel cimport prange
from cython cimport view
from libcpp.vector cimport vector

import numpy as np
import scipy.linalg
from test.test_os import groups
cimport numpy as np

cdef class SparseSolver:

    cdef np.ndarray rows, cols, jacobian

    cpdef np.ndarray[double, ndim=1] compute_residuals(self, np.ndarray[double, ndim=1] x):
        # The idea is that this could be the only function for the user to implement
        # and to calculate automatic jacobian
        print"computing base residual"        
        return np.zeros(len(x))
    
    cpdef tuple compute_pattern(self, np.ndarray[double, ndim=1] x0):
        cdef int i, j, I
        cdef double[:] f0, f1
        cdef double xi, eps
        cdef list rows, cols
        
        eps = 1.0e-6
        I = x0.shape[0]
        rows = []
        cols = []
        
        f0 = self.compute_residuals(x0)
        for i in range(I):
            xi = x0[i]
            x0[i] = x0[i] + eps
            f1 = self.compute_residuals(x0)
            x0[i] = xi
            for j in range(I): # assuming n = m (variables and functions)
                if f1[j] == f0[j]:
                    continue
                print j,i, 'is a thing'
                rows.append(j)
                cols.append(i) 
        self.rows = np.array(rows, dtype=np.int)
        return (np.array(rows, dtype=np.int),np.array(cols, dtype=np.int))
    
    cpdef list find_groups(self, int[:] rows, int[:] cols):
        # store 2 things: group_column [[0,2],[]] and group non-zero elemets index (corresponding to
        # rows and cols [[0,1,3,5], [...]] with the last it's easy to find the row (f), with row[0]
        # for example, to get the value and 0 will be the data[0] of the jacobian.
        cdef int i, j, r,
        cdef int I, J
        cdef list groups
        cdef int last_col
        
        I = cols.shape[0]
        print cols[I-1]
        
        
        groups = []
        last_col = cols[0]
        groups.append([0])
        for i in range(1,I):
            if cols[i] != last_col:
                last_col = cols[i]
                groups.append([])
            groups[-1].append(i)
        print groups
        
        I = len(groups)
        for i in range(I):
            J = len(groups[i])
            for j in range(J):
                r = groups[i][j]
                print rows[r],
            print ''
            
#         cdef np.ndarray[np.boo, ndim=1] is_merged = np.zeros(I)
        cdef list group_i
        cdef list group_j
        cdef np.uint8_t [:] is_merged= np.zeros(I, dtype=np.uint8)
        
        for i in range(1,I):
            for j in range(0,i):
                if i == j:
                    continue
                print 'trying to merge colum ', i, 'in column ', j
                if is_merged[j]:
                    print j, 'already merged'
                    continue
                group_i = groups[i]
                group_j = groups[j]
                should_merge = True
                for ii in range(len(group_i)):
                    if not should_merge:
                        break
                    print 'row ii', rows[group_i[ii]]
                    for jj in range(len(group_j)):
                        print 'row jj', rows[group_j[jj]]
                        if rows[group_i[ii]] == rows[group_j[jj]]:
                            should_merge = False
                            break;
                if should_merge:
                    print 'should merge'
                    is_merged[i] = 1
                    group_j.extend(group_i)
#                     group_i.clear()
                    break
        print groups
        
        cdef list result = []
        for i in range(I):
            print i, 'merged',  is_merged[i]
            if not is_merged[i]:
                result.append(np.array(groups[i], dtype=np.int))
        print result
        return result
    
        
    cdef do_stuff(self, int[:] x):
        cdef int i, I
        
        I = x.shape[0]
        with nogil:
            for i in range(I):
                x[i]=x[i]+1
        print np.asarray(x)
            