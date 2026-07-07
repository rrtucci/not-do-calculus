from NDC_Cases import *
from NDC_BnetMaker import *
from NDC_Tester import *


class NDC_CaseTester(NDC_Tester):
    """
    Attributes
    ----------

    adj_ampu_prob_y_bar_x: np.array
    adj_case: NDC_Cases
    adj_full_prob_y_bar_x: np.array
    bnet_maker: NDC_BnetMaker
    null_adj: bool

    """

    def __init__(self,
                 bnet_maker,
                 dot_file,
                 re_randomize_hidden_nds=True,
                 adj_version=1,
                 null_adj=False):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        adj_version: int
            the adjustment formula version. For the Napkin OP, there are
            currently 4 adjustment formulae that are tested
        null_adj: bool
        """
        NDC_Tester.__init__(self,
                            bnet_maker,
                            re_randomize_hidden_nds,
                            null_adj)
        # self.bnet_maker = bnet_maker
        # self.re_randomize_hidden_nds =  re_randomize_hidden_nds
        # self.null_adj = null_adj
        # self.adj_ampu_prob_y_bar_x = None
        # self.adj_full_prob_y_bar_x = None
        self.adj_case = NDC_Cases(bnet_maker.nn_to_nd,
                                  dot_file,
                                  adj_version)
        self.calc_adj_prob_y_bar_x()

    def calc_adj_prob_y_bar_x(self):
        """

        Parameters
        ----------
        adj_pot_method: Function | None

        Returns
        -------
        None

        """
        if self.null_adj:
            self.adj_ampu_prob_y_bar_x = \
                self.bnet_maker.ampu_prob_y_bar_x
            self.adj_full_prob_y_bar_x = \
                self.bnet_maker.full_prob_y_bar_x
        else:
            self.adj_ampu_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
                self.adj_case.adj_pot_method(self.bnet_maker.ampu_pot))
            self.adj_full_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
                self.adj_case.adj_pot_method(self.bnet_maker.full_pot))


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
        tester = NDC_CaseTester(bnet_maker, dot_file)
        tester.print_adj_report(verbose=verbose)


    def main_frontdoor(verbose):
        """
        Parameters
        ----------
        draw: bool
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

        tester = NDC_CaseTester(bnet_maker, dot_file)
        tester.print_adj_report(verbose=verbose)


    def main_napkin(adj_version, verbose):
        """
        Parameters
        ----------
        adj_version: int
        verbose: bool

        Returns
        -------
        None
,
        """
        dot_file = "dot_atlas/napkin.dot"
        nns, arrows = DotTool.read_dot_file(dot_file)
        if adj_version == 4:
            bnet_maker = NDC_BnetMaker(nns,
                                       arrows,
                                       hidden_nns=["u_1", "u_2"],
                                       other_cond="z",
                                       nn_to_size={"z": 3})
        else:
            bnet_maker = NDC_BnetMaker(nns,
                                       arrows,
                                       hidden_nns=["u_1", "u_2"])
        tester = NDC_CaseTester(bnet_maker, dot_file, adj_version=adj_version)
        tester.print_adj_report(verbose=verbose)


    # main_backdoor(False)
    main_frontdoor(False)
    # main_napkin(5, False)
