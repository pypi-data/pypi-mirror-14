from spine.skeleton.skeleton cimport Skeleton


cdef class Timeline(object):

    cpdef apply(Timeline self, Skeleton skeleton,
                float last_time, float time, list fired_events, float alpha)