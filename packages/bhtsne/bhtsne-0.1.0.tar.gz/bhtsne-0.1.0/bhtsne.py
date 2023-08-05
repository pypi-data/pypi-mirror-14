
from bhtsne_wrapper import BHTSNE

def tsne(data, dimensions=2, perplexity=30.0, theta=0.5, rand_seed=-1):
    tsne = BHTSNE()
    Y = tsne.run(data, data.shape[0], data.shape[1], dimensions, perplexity, theta, rand_seed)
    return Y
