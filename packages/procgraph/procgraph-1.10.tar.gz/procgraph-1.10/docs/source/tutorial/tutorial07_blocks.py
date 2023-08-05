from procgraph import simple_block

@simple_block
def green_channel(rgb):
    green = rgb[:,:,1]
    rgb[:,:,0] = green
    rgb[:,:,2] = green
    return rgb    