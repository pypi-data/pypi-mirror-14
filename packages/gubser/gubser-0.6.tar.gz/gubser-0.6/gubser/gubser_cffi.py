#/usr/bin/env python
#author: lgpang
#email: lgpang@qq.com
#createTime: So 15 Nov 2015 16:43:45 CET

from cffi import FFI

src = '''
//#pragma OPENCL EXTENSION cl_khr_fp64 : enable
inline float eps(float x, float y, float tau, float L0, float lam1){
    return  pow(1 + (1.0/4.0)*pow(-pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2)/(pow(L0, 2)*pow(tau, 2)), -1.33333333333333 + 1.0/lam1)/pow(tau, 4) ;
}


inline float ut(float x, float y, float tau, float L0){
    return  pow(-4*pow(tau, 2)*(pow(x, 2) + pow(y, 2))/pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2) + 1, -1.0/2.0) ;
}


inline float ux(float x, float y, float tau, float L0){
    return  2*tau*x/(sqrt(-4*pow(tau, 2)*(pow(x, 2) + pow(y, 2))/pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2) + 1)*(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2))) ;
}


inline float uy(float x, float y, float tau, float L0){
    return  2*tau*y/(sqrt(-4*pow(tau, 2)*(pow(x, 2) + pow(y, 2))/pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2) + 1)*(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2))) ;
}


inline float pitt(float x, float y, float tau, float L0, float lam1){
    return  -4*pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(pow(x, 2) + pow(y, 2))*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(lam1*pow(tau, 2)*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}


inline float pitx(float x, float y, float tau, float L0, float lam1){
    return  -2*x*pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))*(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2))/(lam1*pow(tau, 3)*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}


inline float pity(float x, float y, float tau, float L0, float lam1){
    return  -2*y*pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))*(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2))/(lam1*pow(tau, 3)*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}


inline float pixx(float x, float y, float tau, float L0, float lam1){
    // avoid the  NAN problem when x=0, y=0
    if ( fabs(x) < 1.0E-6 ) x = 1.0E-6;
    if ( fabs(y) < 1.0E-6 ) y = 1.0E-6;
    return  -pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))*(pow(x, 2)*pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2) + pow(y, 2)*(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2)))/(lam1*pow(tau, 4)*(pow(x, 2) + pow(y, 2))*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}


inline float pixy(float x, float y, float tau, float L0, float lam1){
    // avoid the  NAN problem when x=0, y=0
    if ( fabs(x) < 1.0E-6 ) x = 1.0E-6;
    if ( fabs(y) < 1.0E-6 ) y = 1.0E-6;
    return  x*y*pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))*(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2) - pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(lam1*pow(tau, 4)*(pow(x, 2) + pow(y, 2))*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}


inline float piyy(float x, float y, float tau, float L0, float lam1){
    // avoid the  NAN problem when x=0, y=0
    if ( fabs(x) < 1.0E-6 ) x = 1.0E-6;
    if ( fabs(y) < 1.0E-6 ) y = 1.0E-6;
    return  -pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))*(pow(x, 2)*(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2)) + pow(y, 2)*pow(pow(L0, 2) + pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(lam1*pow(tau, 4)*(pow(x, 2) + pow(y, 2))*pow(4*pow(L0, 2)*(pow(x, 2) + pow(y, 2)) + pow(pow(L0, 2) + pow(tau, 2) - pow(x, 2) - pow(y, 2), 2), 2)) ;
}

/* pizz = pi^{\eta\eta} */
inline float pizz(float x, float y, float tau, float L0, float lam1){
    return  2*pow((0.25)*(4*pow(L0, 2)*pow(tau, 2) + pow(pow(L0, 2) - pow(tau, 2) + pow(x, 2) + pow(y, 2), 2))/(pow(L0, 2)*pow(tau, 2)), (-1.33333333333333*lam1 + 1)/lam1)/(lam1*pow(tau, 6)) ;
}
'''



ffi = FFI()

ffi.cdef('''
    inline float eps(float x, float y, float tau, float L0, float lam);
    inline float ut(float x, float y, float tau, float L0);
    inline float ux(float x, float y, float tau, float L0);
    inline float uy(float x, float y, float tau, float L0);
    inline float pitt(float x, float y, float tau, float L0, float lam1);
    inline float pitx(float x, float y, float tau, float L0, float lam1);
    inline float pity(float x, float y, float tau, float L0, float lam1);
    inline float pixx(float x, float y, float tau, float L0, float lam1);
    inline float pixy(float x, float y, float tau, float L0, float lam1);
    inline float piyy(float x, float y, float tau, float L0, float lam1);
    inline float pizz(float x, float y, float tau, float L0, float lam1);
    ''')

ffi.set_source('_gubser', src)

if __name__=='__main__':
    ffi.compile()

