from itertools import product
from NDC_BnetMaker import *
from NDC_Searcher import *
from NDC_Search2Tester import *
from NDC_global_funs import bnet_has_x_parent_that_is_hidden


class NDC_Searcher2(NDC_Searcher):
    """
    This class is a subclass of the abstract class NDC_Searcher. Its purpose
    is to test the validity of each adjustment in a set of plausible ones.

    The adjustment considered here is of the form

    P(y|do(x)) = \frac{1}{\sum_y numer} \sum_{u, v} P(x,y|u, v) P(u)P(v)

    where we are assuming there are two hidden nodes h1 and h2 which are
    replaced by u and v, respectively


    Attributes
    ----------
    bnet_maker: NDC_BnetMaker
    """

    def __init__(self, bnet_maker):
        """
        Constructor

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        """
        NDC_Searcher.__init__(self, bnet_maker)

    def conduct_search(self, verbose):
        """
        This method overrides its namesake abstract method. See description
        of this method in docstring for NDC_Searcher.conduct_search()

        Returns
        -------
        None

        """
        if not bnet_has_x_parent_that_is_hidden(self.bnet_maker.arrows,
                                                self.bnet_maker.hidden_nns):
            subs = []
            print("===================")
            print("No substitution is necessary.")
            tester = NDC_Search2Tester(self.bnet_maker, subs)
            tester.print_adj_report(False)
            return
        hidden_nns = self.bnet_maker.hidden_nns
        num_hidden_nns = len(hidden_nns)
        non_hidden_xy_nns = [nn for nn in self.bnet_maker.nns if nn not in
                             hidden_nns + ["x", "y"]]

        for subs in product(non_hidden_xy_nns, repeat=num_hidden_nns):
            subs = list(subs)
            plausible_subs = self.substitution_is_plausible(subs)
            if plausible_subs:
                print("===================")
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
                      f" is a PLAUSIBLE substitution")
                tester = NDC_Search2Tester(self.bnet_maker, subs)
                tester.print_adj_report(False)
            else:
                if verbose:
                    print("===================")
                    print(f"{self.bnet_maker.hidden_nns}>{subs}"
                          f" is a NON-PLAUSIBLE substitution")

    def substitution_is_plausible(self, subs):
        """
        This method overrides its namesake abstract method. It returns True
        iff subs is a plausible substitution.

        Parameters
        ----------
        subs: list[str]

        Returns
        -------
        bool

        """
        return len(subs) == len(set(subs))


if __name__ == "__main__":
    def main_backdoor(verbose):
        """
        Parameters
        ----------
        verbose: bool

        Returns
        -------
        None

        """
        dot_file = "dot_atlas/back-door.dot"
        nns, arrows = DotTool.read_dot_file(dot_file)
        bnet_maker = NDC_BnetMaker(nns,
                                   arrows,
                                   hidden_nns=[])
        searcher = NDC_Searcher2(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    def main_frontdoor(verbose):
        """
        Parameters
        ----------
        verbose: bool

        Returns
        -------
        None

        """
        dot_file = "dot_atlas/front-door.dot"
        nns, arrows = DotTool.read_dot_file(dot_file)
        bnet_maker = NDC_BnetMaker(nns,
                                   arrows,
                                   hidden_nns=["h"])
        searcher = NDC_Searcher2(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    def main_napkin(verbose):
        """
        Parameters
        ----------
        verbose: bool

        Returns
        -------
        None
,
        """
        dot_file = "dot_atlas/napkin.dot"
        nns, arrows = DotTool.read_dot_file(dot_file)
        bnet_maker = NDC_BnetMaker(nns,
                                   arrows,
                                   hidden_nns=["u_1", "u_2"])
        searcher = NDC_Searcher2(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    # main_backdoor(True)
    # main_frontdoor(True)
    main_napkin(True)
