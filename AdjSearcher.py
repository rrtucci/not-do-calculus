from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))
from itertools import product
from BnetSample import *
from AdjCandidate import *

class AdjSearcher:
    """
    Attributes
    ----------
    bnet_sample: BnetSample
    """

    def __init__(self, bnet_sample):
        """

        Parameters
        ----------
        bnet_sample: BnetSample
        """
        self.bnet_sample = bnet_sample


    def conduct_search(self, verbose):
        """
        verbose: bool

        Returns
        -------
        None

        """
        num_hidden_nns = len(self.bnet_sample.hidden_nns)
        nns = self.bnet_sample.nns
        for subs in product(nns, repeat=num_hidden_nns):
            adj_candy = AdjCandidate(self.bnet_sample, subs)
            if not adj_candy.valid_sub:
                continue






if __name__ == "__main__":
