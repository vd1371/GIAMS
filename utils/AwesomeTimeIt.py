import time

def timeit(method):
    '''This function is written to be used as dcorator
    Example of usage can be found in the below'''

    def timed(*args, **kw):
        ts = time.time()
        print (f'---- {method.__name__} is about to start ----')
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print (f'---- {method.__name__} is done in {te-ts:.3f} seconds ----')
        return result
    return timed


if __name__ == '__main__':

	# This is how to use timeIt as decorator
	@timeIt
	def testTimeIt(n = 1000):
		sum = 0
		for i in range(n):
			sum += i
		print (f"This test function sumed numbers from 0 to {n}")

	testTimeIt(2000)

	''' results in consloe:

	---- testTimeIt is about to start ----
	This test function sumed numbers from 0 to 2000
	---- testTimeIt is done in 0.001 seconds ----
	
	'''
