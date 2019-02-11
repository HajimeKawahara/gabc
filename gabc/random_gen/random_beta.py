import time
import matplotlib.pyplot as plt
import math
import numpy as np
import pycuda.autoinit
import pycuda.driver as cuda
import pycuda.compiler
from pycuda.compiler import SourceModule

def gabcrm_module ():
    source_module = SourceModule("""
    #include <curand_kernel.h>
    #include "gengamma.h"


    extern "C"{
    
    __global__ void betagen(float* x, float alpha, float beta){
    unsigned long seed;
    unsigned long id;
    curandState s;
    float ga;
    float gb;

    seed=10;
    id = blockIdx.x;
    curand_init(seed, id, 0, &s);

    ga=gammaf(alpha,1.0, &s);
    gb=gammaf(beta,1.0, &s);
    x[id] = ga/(ga + gb);

    return;

    }

    }


    """,options=['-use_fast_math'],no_extern_c=True)

    return source_module

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.stats import beta as betafunc
    
    print("********************************************")
    print("Beta function Random Sampler using curand_kernel.h")
    print("g_a ~ Gamma[a], beta is generated by g_a/(g_a + g_b)")
    print("********************************************")

    alpha=1.2
    beta=1.3
    
    nw=1
    nt=100000
    nq=1
    nb = nw*nt*nq 
    sharedsize=0 #byte
    x=np.zeros(nb)
    x=x.astype(np.float32)
    dev_x = cuda.mem_alloc(x.nbytes)
    cuda.memcpy_htod(dev_x,x)

    source_module=gabcrm_module()
    pkernel=source_module.get_function("betagen")
    pkernel(dev_x,np.float32(alpha),np.float32(beta),block=(int(nw),1,1), grid=(int(nt),int(nq)),shared=sharedsize)
    cuda.memcpy_dtoh(x, dev_x)

    
    plt.hist(x,bins=30,density=True)
    xl = np.linspace(betafunc.ppf(0.001, alpha, beta),betafunc.ppf(0.999, alpha, beta), 100)
    plt.plot(xl, betafunc.pdf(xl, alpha, beta))

    plt.show()
