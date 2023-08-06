#/usr/bin/env python
#author: lgpang
#email: lgpang@qq.com
#createTime: So 15 Nov 2015 16:43:45 CET

'''http://arxiv.org/pdf/nucl-th/9504018.pdf Eq.53'''

from cffi import FFI

src = '''
#define cs2 (1.0f/3.0f)

inline float __pressure(float t, float z, float p0) {
    float coff = p0;
    float cs = sqrt(cs2);

    float result;
    if ( z >= -t && z <= -cs*t ) {
        result = coff;
    } else if ( (z >= -cs*t) && (z <= t) ) {
        result = coff*pow((1-cs)/(1+cs)*(t-z)/(t+z), (1+cs2)/(2*cs));
    } else {
        result = 0.0f;
    }

    return result;
}


inline float initial_pressure(float z, float pressure_left, float pressure_right) {
    if ( z <= 0.0f ) {
        return pressure_left;
    } else {
        return pressure_right;
    }
}


inline float pressure(float t, float z, float pressure_left, float pressure_right) {
    if ( z <= -t ) {
        return pressure_left;
    } else if (z >= t ) {
        return pressure_right;
    } else {
        // float p0 = initial_pressure(z, pressure_left, pressure_right);
        float p0 = pressure_left;
        return __pressure(t, z, p0);
    }
}
'''

ffi = FFI()

ffi.cdef('''
        inline float initial_pressure(float z, float pressure_left, float pressure_right);
        inline float pressure(float t, float z, float pressure_left, float pressure_right);
        ''')

ffi.set_source('_riemann', src)

if __name__ == '__main__':
    ffi.compile()

