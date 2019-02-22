    extern "C"{

      __global__ void compute_weight(float* wnew, float* wprev, float* xnew, float* xprev, float* invcov){
    int nthread = blockDim.x;
    int npart = gridDim.x;
    float rnthread = float(nthread);
    float rnpart = float(npart);
    int ipart;

    /* prev:=t-1, new:=t in TVZ12 */ 
    /* iblock := i in TVZ12 */
    int iblock = blockIdx.x;

    /* ithread := j in TVZ12 */
    int ithread = threadIdx.x;
    float qf;
    
    for (int l=0; l<npart/nthread; l++){

      ipart = l*nthread+ithread;
      /* computing qf (Gaussian transition kernel) */
      qf=0.0;
      for (int m=0; m<NMODEL; m++){
	for (int k=0; k<NMODEL; k++){
	  /* [NMODEL*ipart + m] - xnew[NMODEL*iblock + m] */
	  /* xprev: ipart,imodel => NMODEL*ipart + imodel  */
	  /* xnew: iblock,imodel => NMODEL*iblock + imodel  */
	  /* imodel = m,k  */
	  /* here, computing an element of a quadratic form x_m x_k A_mk */
	  /* A_mk := m*NMODEL + k = k*NMODEL + m because inverse covariance matrix is a symmetric matrix */

	  qf += (xprev[NMODEL*ipart + m] - xnew[NMODEL*iblock + m])*(xprev[NMODEL*ipart + k] - xnew[NMODEL*iblock + k])/invcov[m*NMODEL + k];
	  
	}
      }
      qf = exp(-0.5*qf);
      /* thread cooperating computation of a denominater */        
      cache[ipart] = wprev[ipart]*qf;

    }
    __syncthreads();

    int i = npart/2;
    while(i !=0) {

    for (int m=0; m<npart/nthread; m++){

    ipart = m*nthread+ithread;
    if (ipart < i){
    cache[ipart] += cache[ipart + i];
    }
    __syncthreads();
    i /= 2;

    }
    }

    __syncthreads();
    /* ===================================================== */

    if (ithread==0){
    /* computing weight */
    wnew[iblock] = cache[0];

    return;

    }else{

    return;

    }


    }


    }
