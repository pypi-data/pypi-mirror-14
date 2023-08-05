#/usr/bin/env python
#author: lgpang
#email: lgpang@qq.com
#createTime: So 15 Nov 2015 16:43:45 CET

from cffi import FFI

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

ffi.set_source('_gubser', open('kernel_gubser_visc.h', 'r').read())

if __name__=='__main__':
    ffi.compile()

