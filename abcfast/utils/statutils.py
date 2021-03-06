import numpy as np

def getptwo(n):
    i=0
    while n > 2**i:
        i=i+1
    return 2**(i-1)

def checkpower2(n):
    logn=np.log2(n)
    if logn - int(logn) > 0.0:
        return True

def genalias_init(parrs):
    parr=np.array(parrs, np.float32)
    parr = parr/np.sum(parr)

    Ui = np.ndarray(len(parrs), np.float32)
    Ki= np.zeros(len(parrs), dtype=np.int32)
    Li= np.zeros(len(parrs), dtype=np.int32)

    il, ir = 0, 0
    pairs = list(zip(parr, range(len(parrs))))
    pairs.sort()
    for parr, i in pairs:
        p = parr * len(parrs)
        while p > 1 and ir < len(Ui):
            Ki[ir] = i
            p -= 1.0 - Ui[ir]
            ir += 1
        Ui[il] = p
        Li[il] = i
        il += 1
    for i in range(ir, len(parrs)):
        Ki[i] = 0

    Ui=Ui.astype(np.float32)
    Li=Li.astype(np.int32)
    Ki=Ki.astype(np.int32)
        
    return Ki,Li,Ui
