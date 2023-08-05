import numpy as np
import scipy.linalg
cimport numpy as np
from libc.math cimport sqrt
from cython.parallel cimport prange


cdef class Solver:
    '''Netwon non-linear solver
    (todo with line-search and Marquadt modification)
    '''
    
    cdef np.ndarray x    
    cdef int w
    cdef int[:] indices
    cdef int[:] ind_ptr
    
    property x:
        def __get__(self):
            return self.x
    
    cpdef set_initial_solution(self, np.ndarray[double, ndim=1] x):        
        self.x = x
        
    cpdef np.ndarray[double, ndim=1] compute_residuals(self, np.ndarray[double, ndim=1] x):
        # The idea is that this could be the only function for the user to implement
        # and to calculate automatic jacobian
        print"computing base residual"        
        return np.zeros(len(x))
    
    cdef double scalar_res(self, np.ndarray[double, ndim=1] res):
        return np.dot(res,res)
    
    cpdef np.ndarray[double, ndim=1] solve(self, np.ndarray[double, ndim=1] x):        
        cdef int i,count
        cdef double eps
        cdef int num_variables
        cdef double r
        cdef np.ndarray[double, ndim=1] x1, f0, f1, s
        cdef np.ndarray[double, ndim=2] J
        cdef tuple LU        
        
        num_variables = len(x)
        J = np.zeros((num_variables, num_variables))
        eps = 1e-6
        count = 0
        
        self.x = x
        f0 = self.compute_residuals(self.x)
        r = self.scalar_res(f0)

        while r > 1.0e-6:
            # Jacobian update
            for i in range(num_variables):
                x1 = np.copy(self.x)
                x1[i] += eps
                f1 = self.compute_residuals(x1)
                J[:,i] = (f1 - f0) / eps
            # inv version
            # s = - np.dot(f0, np.linalg.inv(J)) #this is bad
            s = -np.linalg.solve(J, f0)

            x1 = self.x + s
            f1 = self.compute_residuals(x1)

            while self.scalar_res(f1) > r:    
                print 'back<<<'
                s = 0.5 * s
                x1 = self.x + s
                f1 = self.compute_residuals(x1)

            self.x = np.copy(x1)
            f0 = self.compute_residuals(self.x)
            r = self.scalar_res(f0)
            # print '>>>>>>>>>>>>>>>>>>>>>>>>>>> residual[%d]'%count, r
            count += 1
#         print 'jacobian calls', count
        return self.x    
    
#=Extensions ====================================================================================== 
    
cdef class CythonExtendedSolver(Solver):
    cpdef np.ndarray[double, ndim=1] compute_residuals(self, np.ndarray[double, ndim=1] x):   
        print("computing CythonExtendedSolver residual")
        return x    
    
    # The thing is: Optiomization of h(X) is the same as root finding. But the
    # 'nonlinear functions' f(X) are actually dh(X)/dX. The jacobian will be the 
    # hessian. So compute residual in root finding => return the values of
    # f(X). And in optimizatio the values of dh(X)/dX which we want to be 0.0
    
cdef class CythonContinuitySolver(Solver):
    
    cpdef np.ndarray[double, ndim=1] compute_residuals(self, np.ndarray[double, ndim=1] x):        
        cdef int size = len(x)
        cdef np.ndarray[double, ndim=1] mass = np.zeros(size)
        cdef int i
        
        mass[0] = 100.0 - x[0]**2
        for i in range(1,size):
            mass[i] = -x[i]**2 + x[i-1]**2
        return mass

class OptimizationSolver(Solver):
    # optimize h(x) = x0^2 + x1^2
    def compute_residuals(self, x):
        # analitically write the functions or
        # retur numeric_gradient(h)
        return x 
        
        