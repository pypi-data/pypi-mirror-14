import numpy
from procgraph import simple_block, BadConfig

@simple_block
def choose(rgb, channel=0):
    ''' Chooses a channel from an rgb image and replicates it 
        over the other two.

        Raises an error if ``channel`` is invalid.
    
        :param rgb: Input image.
        :param channel: Which channel to choose.        
        :return: processed: The processed image.
    '''
    if not channel in [0,1,2]:
        raise BadConfig('Invalid channel specified.', config='channel')
    
    v = rgb[:,:,channel]
    return numpy.dstack((v,v,v))
