from NDC_Cases import *
from NDC_BnetMaker import *
from NDC_Tester import *


class NDC_CaseTester(NDC_Tester):
    """
    This class is a subclass of the abstract class NDC_Tester. It overrides
    the method calc_adj_prob_y_bar_x(). This class creates and uses within
    method calc_adj_prob_y_bar_x(), an object of class NDC_Cases.

    Attributes
    ----------
    adj_ampu_prob_y_bar_x: np.array
        P(y|x) for adjustment, calculated from the amputated bnet
    adj_case: NDC_Cases
        an object of NDC_Cases
    adj_full_prob_y_bar_x: np.array
        P(y|x) for adjustment, calculated from the full bnet


    """

    def __init__(self,
                 bnet_maker,
                 dot_file,
                 re_randomize_hidden_nds=True,
                 adj_version=1):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        dot_file: str
        re_randomize_hidden_nds: bool
        adj_version: int
            the adjustment formula version. For the Napkin bnet, there are
            several. All except one (adj_version=1) are invalid.

        """
        NDC_Tester.__init__(self,
                            bnet_maker,
                            re_randomize_hidden_nds)
        """
        Constructor
        
        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        re_randomize_hidden_nds: bool
        
        """
        # self.bnet_maker = bnet_maker
        # self.re_randomize_hidden_nds =  re_randomize_hidden_nds
        # self.adj_ampu_prob_y_bar_x = None
        # self.adj_full_prob_y_bar_x = None

        self.adj_case = NDC_Cases(bnet_maker.nn_to_nd,
                                  dot_file,
                                  adj_version)
        self.calc_adj_prob_y_bar_x()

    def calc_adj_prob_y_bar_x(self):
        """
        This method calculates P(y|x) for the adjustment, from either
        in_pot= full_pot or ampu_pot. It does this using
        self.adj_case.adj_pot_function()

        Returns
        -------
        None

        """
        self.adj_ampu_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
            self.adj_case.adj_pot_function(self.bnet_maker.ampu_pot))
        self.adj_full_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
            self.adj_case.adj_pot_function(self.bnet_maker.full_pot))


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
