from NDC_Searcher import *
from itertools import product
from NDC_BnetMaker import *
from NDC_AdjBnetMaker import *
from NDC_Search1Tester import *
from NDC_global_funs import get_nn_to_parents
from NDC_global_funs import substitution_is_plausible
from NDC_global_funs import get_nn_to_sub


class NDC_Searcher1(NDC_Searcher):
    """
    The purpose of this class is to test the validity of each adjustment in
    a set of plausible ones. The adjustment is assumed to be the amputated
    promise obtained by substituting every hidden node by an observed one.
    `subs` are the substitutions for the hidden node names `hidden_nns`. For
    example, if "h1" and "h2" are all the hidden node names, and "u" and "v"
    are observed nns, a possible substitution might be ["h1", "h2"] -> [
    "u", "v"]

    DC_AdjBnetMaker is a subclass of NDC_BnetMaker. Both self.adj_bnet_maker
    and self.bnet_maker construct a bnet. The bnet constructed by
    self.adj_bnet_maker uses CPTs calculated from observed nodes of the bnet
    constructed a priori by self.bnet_maker

    Attributes
    ----------
    adj_bnet_maker: NDC_AdjBnetMaker
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
        self.adj_bnet_maker = None

    def conduct_search(self, verbose):
        """
        This method overrides its namesake abstract method. See description
        of this method in docstring for NDC_Searcher.conduct_search()

        Returns
        -------
        None

        """
        hidden_nns = self.bnet_maker.hidden_nns
        num_hidden_nns = len(hidden_nns)
        non_hidden_nns = [nn for nn in self.bnet_maker.nns if nn not in
                          hidden_nns]

        for subs in product(non_hidden_nns, repeat=num_hidden_nns):

            subs = list(subs)

            nn_to_parents = get_nn_to_parents(
                self.bnet_maker.arrows, self.bnet_maker.nns)
            nn_to_sub = get_nn_to_sub(
                self.bnet_maker.nns,
                self.bnet_maker.hidden_nns,
                subs
            )

            plausible_subs = substitution_is_plausible(
                nn_to_parents, nn_to_sub)
            if plausible_subs:
                print("===================")
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
                      f" is a PLAUSIBLE substitution")
                if not subs:
                    self.adj_bnet_maker = self.bnet_maker
                else:
                    self.adj_bnet_maker = NDC_AdjBnetMaker(self.bnet_maker,
                                                       subs)
                tester = NDC_SearchTester(self.bnet_maker,
                                          self.adj_bnet_maker)
                tester.print_adj_report(False)
            else:
                if verbose:
                    print("===================")
                    print(f"{self.bnet_maker.hidden_nns}>{subs}"
                          f" is a NON-PLAUSIBLE substitution")


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
        searcher = NDC_Searcher1(bnet_maker)
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
        searcher = NDC_Searcher1(bnet_maker)
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
        searcher = NDC_Searcher1(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    # main_backdoor(True)
    # main_frontdoor(True)
    main_napkin(True)
