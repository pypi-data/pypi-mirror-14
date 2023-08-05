# -*- coding: utf-8 -*-

def measuresecound(func):
	import functools
	import time
	@functools.wraps(func)
	def wrapper(*args,**kwargs):
		sttime = time.clock()
		res = func(*args,**kwargs)
		entime = time.clock()
		count = (entime - sttime)
		print count
		print 'Call %s %f second' % (func.__name__, count)
		return res
	return wrapper

if __name__ == "__main__":
    print u"Usage: decorator @measuretime"
