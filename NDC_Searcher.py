from itertools import product
from NDC_BnetMaker import *
from NDC_AdjBnetMaker import *
from NDC_SearchTester import *


class NDC_Searcher:
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
        self.bnet_maker = bnet_maker
        self.adj_bnet_maker = None

    @staticmethod
    def get_nn_to_parents(arrows, nns):
        """
        This static method returns a dict mapping each nn to the list of names
        of its parents.

        Parameters
        ----------
        arrows: list[tuple(str, str)]
            list of arrows. Example of arrow: ["a", "b"] This represents a->b
        nns: list[str]
            all node names.

        Returns
        -------
        dict[str, list[str]]

        """
        # nn = node name
        nn_to_parents = {nn: [] for nn in nns}
        for arrow in arrows:
            pa, child = arrow
            nn_to_parents[child].append(pa)
        return nn_to_parents

    @staticmethod
    def substitution_is_plausible(nn_to_parents, nn_to_sub):
        """
        This static method returns True iff nn_to_sub is a plausible
        substitution.

        Parameters
        ----------
        nn_to_parents: dict[str, list[str]]
            dict mapping all nn to a list of names of its parents
        nn_to_sub: dict[str, str]
            dict mapping all nn to their substitution names. All nn that are
            not hidden are mapped to themselves.

        Returns
        -------
        bool

        """
        plausible = True
        for nn, parents in nn_to_parents.items():
            sub_parents = [nn_to_sub[nn] for nn in parents]
            # print("czvb, nn, parents, sub_parents", nn, parents, sub_parents)
            if len(sub_parents) != len(set(sub_parents)):
                plausible = False
                break
        # print("xxcv", "plausible", plausible)
        # print()
        return plausible

    def conduct_search(self, verbose):
        """
        This method tests the validity of each adjustment in a set of
        plausible ones. A plausible adjustment is one with a plausible
        substitution `subs`.


        verbose: bool
            True iff every time that a substitution is not plausible, a line
            is printed giving the substitution and saying that it's not
            plausible.

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

            nn_to_parents = NDC_Searcher.get_nn_to_parents(
                self.bnet_maker.arrows, self.bnet_maker.nns)
            nn_to_sub = NDC_AdjBnetMaker.get_nn_to_sub(
                self.bnet_maker.nns,
                self.bnet_maker.hidden_nns,
                subs
            )

            plausible_subs = NDC_Searcher.substitution_is_plausible(
                nn_to_parents, nn_to_sub)
            if plausible_subs:
                print("===================")
                print(f"{self.bnet_maker.hidden_nns}>{subs}"
                      f" is a PLAUSIBLE substitution")
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
        searcher = NDC_Searcher(bnet_maker)
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
        searcher = NDC_Searcher(bnet_maker)
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
        searcher = NDC_Searcher(bnet_maker)
        searcher.conduct_search(verbose=verbose)


    # main_backdoor(True)
    # main_frontdoor(True)
    main_napkin(True)
