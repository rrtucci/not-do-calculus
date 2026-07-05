from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))
from itertools import product
from NDC_BnetMaker import *
from NDC_AdjBnetMaker import *

class NDC_Searcher:
    """
    Attributes
    ----------
    bnet_maker: NDC_BnetMaker
    """

    def __init__(self, bnet_maker):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        """
        self.bnet_maker = bnet_maker


    def conduct_search(self, verbose):
        """
        verbose: bool

        Returns
        -------
        None

        """
        num_hidden_nns = len(self.bnet_maker.hidden_nns)
        nns = self.bnet_maker.nns
        for subs in product(nns, repeat=num_hidden_nns):
            subs = list(subs)
            adj_candy = AdjCandidate(self.bnet_maker, subs)
            if not adj_candy.valid_sub:
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
                      f" is a VALID substitution")
            else:
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
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
        bnet_maker = NDC_BnetMaker(dot_file="dot_atlas/back-door.dot",
                                    hidden_nns=[])
        if draw:
            bnet_maker.draw(jupyter=False)
        searcher = NDC_Searcher(bnet_maker)
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
        bnet_maker = NDC_BnetMaker(dot_file="dot_atlas/front-door.dot",
                                    hidden_nns=["h"])
        if draw:
            bnet_maker.draw(jupyter=False)
        searcher = NDC_Searcher(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    # main_backdoor(True, True)
    main_frontdoor(True, True)