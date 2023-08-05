
import numpy as np
from bhtsne_wrapper import BHTSNE

def tsne(data, dimensions=2, perplexity=30.0, theta=0.5, rand_seed=-1, seed_positions=np.array([])):
    tsne = BHTSNE()
    seed_positions_no_cols = seed_positions.shape[0]
    Y = tsne.run(data, data.shape[0], data.shape[1], dimensions, perplexity, theta, rand_seed, seed_positions, seed_positions_no_cols)
    return Y
