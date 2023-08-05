import time
import pout

def mgen(start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    pout.h()
    yield "hello world"
    pout.v("done with request")
    time.sleep(5)





def application(env, start_response):
    for body in mgen(start_response):
        yield body

