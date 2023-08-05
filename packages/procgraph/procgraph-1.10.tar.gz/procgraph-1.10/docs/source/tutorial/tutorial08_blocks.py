import numpy
from procgraph import simple_block

@simple_block
def choose(rgb, channel=0):
    v = rgb[:,:,channel]
    result = numpy.dstack((v,v,v))
    return result
