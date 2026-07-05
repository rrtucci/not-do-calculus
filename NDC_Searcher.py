from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))
from itertools import product
from NDC_BnetMaker import *
from NDC_AdjBnetMaker import *
from NDC_Tester import *

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
        self.adj_bnet_maker = None

    @staticmethod
    def get_nn_to_parents(arrows, nns):
        # nn = node name
        nn_to_parents = {nn: [] for nn in nns}
        for arrow in arrows:
            pa, child = arrow
            nn_to_parents[child].append(pa)
        return nn_to_parents

    @staticmethod
    def substitution_is_valid(nn_to_parents, nn_to_sub):
        valid = True
        for nn, parents in nn_to_parents.items():
            sub_parents = [nn_to_sub[nn] for nn in parents]
            # print("czvb, nn, parents, sub_parents", nn, parents, sub_parents)
            if len(sub_parents) != len(set(sub_parents)):
                valid = False
                break
        # print("xxcv", "valid", valid)
        # print()
        return valid


    def conduct_search(self, verbose):
        """
        verbose: bool

        Returns
        -------
        None

        """
        hidden_nns = self.bnet_maker.hidden_nns
        num_hidden_nns = len(hidden_nns)
        non_hidden_nns = [x for x in self.bnet_maker.nns if x not in
                          hidden_nns]

        for subs in product(non_hidden_nns, repeat=num_hidden_nns):
            subs = list(subs)

            nn_to_parents = NDC_Searcher.get_nn_to_parents(
                self.bnet_maker.arrows, self.bnet_maker.nns)
            nn_to_sub = NDC_AdjBnetMaker.get_nn_to_sub(
                self.bnet_maker.nns,
                self.bnet_maker.hidden_nns,
                subs
            )

            valid_subs =NDC_Searcher.substitution_is_valid(
                nn_to_parents, nn_to_sub)
            if valid_subs:
                print("===================")
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
                      f" is a VALID substitution")
                self.adj_bnet_maker = NDC_AdjBnetMaker(self.bnet_maker,
                                             subs)
                tester = NDC_Tester(self.adj_bnet_maker)
                tester.print_adj_report(False, False)
            else:
                if verbose:
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


    # main_backdoor(False, False)
    main_frontdoor(False, False)