
"generic code timer tool"
import sys
import time

#~ print(time.time())
if sys.version_info[0] >= 3 and sys.version_info[1] >= 3:
	timer = time.perf_counter
	# or process_time
else:		#python 2
	timer = time.clock if sys.platform[:3] == 'win' else time.time


def test(reps, func, *args):        # or best of N? see Learning Python
    
    start = time.clock()            # current CPU time in float seconds
    for i in range(reps):           # call function reps times
        func(*args)                 # discard any return value
    
    total = time.clock() - start
    average = total / reps
    return total, average    # stop time - start time

def total(reps, func, *pargs, **kargs):
	"""
	Total time to run func() reps times.
	Returns (total time, last result)
	"""
	repslist = list(range(reps))
	start = timer()
	for i in repslist:
		ret = func(*pargs, **kargs)
	elapsed = timer() - start
	return (elapsed, ret)
def bestof(reps, func, *pargs, **kargs):
	"""
	Quickest func() among reps runs.
	Returns (best time, last result)
	"""
	best = 2 ** 32
	for i in range(reps):
		start = timer()
		ret = func(*pargs, **kargs)
		elapsed = timer() - start
		if elapsed < best: best = elapsed
	return (best, ret)
	# Hoist out, equalize 2.x, 3.x
	# Or perf_counter/other in 3.3+
	# 136 years seems large enough
	# range usage not timed here
	# Or call total() with reps=1
	# Or add to list and take min()
def bestoftotal(reps1, reps2, func, *pargs, **kargs):
	"""
	Best of totals:
	(best of reps1 runs of (total of reps2 runs of func))
	"""
	return bestof(reps1, total, reps2, func, *pargs, **kargs)

#~ print(test(100,print,['what']))
