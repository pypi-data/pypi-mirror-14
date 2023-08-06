# cython: language_level=3
from cpython.exc cimport PyErr_CheckSignals


cpdef object progressBar(object pos,
                  off_t maxi,
                  bint reset=False,
                  bytes head=b'',
                  list delta=[],
                  list step=[1,0,0]):
                  
    cdef off_t    ipos
    cdef double percent 
    cdef int days,hour,minu,sec
    cdef bytes bar
    cdef off_t fraction
    cdef int freq,cycle,arrow
    cdef tm remain

    cdef clock_t d
    cdef clock_t elapsed
    cdef clock_t newtime 
    cdef clock_t more
    
    #                   0123456789
    cdef char* wheel=  '|/-\\'
    cdef char*  spaces='          ' \
                       '          ' \
                       '          ' \
                       '          ' \
                       '          '
                
    cdef char*  diese ='##########' \
                       '##########' \
                       '##########' \
                       '##########' \
                       '##########' 
                  
    if reset:
        del delta[:]
        step[0]=1
        step[1]=0
        step[2]=0
    if not delta:
        delta.append(clock())
        delta.append(clock())
        
    if maxi<=0:
        maxi=1
    assert maxi>0
    
    freq,cycle,arrow = step

    cycle+=1
    
    if cycle % freq == 0:
        cycle=1
        newtime = clock()
        try:
            d = newtime-delta[1]
        except OverflowError:
            d=0
            
        if d < 0.02 * CLOCKS_PER_SEC :
            freq*=2
        elif d > 0.4 * CLOCKS_PER_SEC and freq>1:
            freq/=2
            
        delta[1]=newtime
        try:
            elapsed = newtime-delta[0]
        except OverflowError:
            elapsed = 0
        
        if callable(pos):
            ipos=pos()
        else:
            ipos=pos
            
        percent = <double>ipos/<double>maxi
        more = <time_t>((<double>elapsed / percent * (1. - percent))/CLOCKS_PER_SEC)
        <void>gmtime_r(&more, &remain)
        days = remain.tm_yday 
        hour = remain.tm_hour
        minu  = remain.tm_min
        sec  = remain.tm_sec

        fraction=<int>(percent * 50.)
        arrow=(arrow+1) % 4
        diese[fraction]=0
        spaces[50 - fraction]=0
        
        if days:
            <void>fprintf(stderr,b'\r%s %5.1f %% |%s%c%s] remain : %d days %02d:%02d:%02d',
                            <char*>head,
                            percent*100,
                            diese,wheel[arrow],spaces,
                            days,hour,minu,sec)
        else:
            <void>fprintf(stderr,b'\r%s %5.1f %% |%s%c%s] remain : %02d:%02d:%02d',
                            <char*>head,
                            percent*100.,
                            diese,wheel[arrow],spaces,
                            hour,minu,sec)
            
        diese[fraction]=b'#'
        spaces[50 - fraction]=b' '
        
        # Added to check if signal (Ctrl-C) are send to the program
        PyErr_CheckSignals()

    else:
        cycle+=1

    step[0:3] = freq,cycle,arrow
