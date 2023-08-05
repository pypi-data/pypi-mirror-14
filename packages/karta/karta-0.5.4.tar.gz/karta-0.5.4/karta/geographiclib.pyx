
typedef double real

cdef extern from "Geodesic.hpp" namespace "GeographicLib":
    cdef cppclass Geodesic:
        Geodesic(real, real) except +
        real GenDirect(real, real, real, bool, real, unsigned, real*, real*,
                       real*, real*, real*, real*, real*, real*)
        real GenInverse(real, real, real, real, unsigned, real*, real*, real*,
                        real*, real*, real*, real*)

cdef class PyGeodesic:
    cdef Geodesic *thisptr

    def __cinit__(self, real a, real f):
        self.thisptr = new Geodesic(a, f)

    def __dealloc__(self):
        del self.thisptr

    def GenDirect(real lat1, real lon1, real azi1, bool arcmode, real s12_a12, unsigned outmask):
        # real &lat2, real &lon2, real &azi2, real &s12, real &m12, real &M12, real &M21, real &S12):
        cdef real lat2, lon2, azi2, s12, m12, M12, M21, S12
        self.thisptr.GenDirect(lat1, lon1, azi1, arcmode, s12_a12, outmask,
                &lat2, &lon2, &azi2, &s12, &m12, &M12, &M21, &S12)
        return lat2, lon2, azi2

    def GenInverse(real lat1, real lon1, real lat2, real lon2, unsigned outmask):
        # real &s12, real &azi1, real &azi2, real &m12, real &M12, real &M21, real &S12):
        cdef real s12, azi1, azi2, m12, M12, M21, S12
        self.thisptr.GenInverse(lat1, lon1, lat2, lon2, outmask, &s12, &azi1, &azi2, &m12, &M12, &M21, &S12)
        return s12, azi1, azi2
