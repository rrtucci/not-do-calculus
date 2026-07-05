from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))
from itertools import product
from NDC_BnetSample import *
from NDC_AdjBnetSample import *

class NDC_Searcher:
    """
    Attributes
    ----------
    bnet_sample: NDC_BnetSample
    """

    def __init__(self, bnet_sample):
        """

        Parameters
        ----------
        bnet_sample: NDC_BnetSample
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
            subs = list(subs)
            adj_candy = AdjCandidate(self.bnet_sample, subs)
            if not adj_candy.valid_sub:
                print(f"{self.bnet_sample.hidden_nns}>{subs}"
                      f" is a VALID substitution")
            else:
                print(f"{self.bnet_sample.hidden_nns}>{subs}"
                      f" is a INVALID substitution")


if __name__ == "__main__":
    def main_backdoor(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = NDC_BnetSample(dot_file="dot_atlas/back-door.dot",
                                     hidden_nns=[])
        if draw:
            bnet_sample.draw(jupyter=False)
        searcher = NDC_Searcher(bnet_sample)
        searcher.conduct_search(verbose=verbose)


    def main_frontdoor(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = NDC_BnetSample(dot_file="dot_atlas/front-door.dot",
                                     hidden_nns=["h"])
        if draw:
            bnet_sample.draw(jupyter=False)
        searcher = NDC_Searcher(bnet_sample)
        searcher.conduct_search(verbose=verbose)


    # main_backdoor(True, True)
    main_frontdoor(True, True)