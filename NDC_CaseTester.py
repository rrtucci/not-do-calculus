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
                 adj_version=1,
                 re_randomize_hidden_nds=True,
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
        NDC_Tester.__init__(self, bnet_maker, null_adj)
        # self.bnet_maker = bnet_maker
        # self.null_adj = null_adj
        # self.adj_ampu_prob_y_bar_x = None
        # self.adj_full_prob_y_bar_x = None
        self.re_randomize_hidden_nds =  re_randomize_hidden_nds
        self.adj_case = NDC_Cases(bnet_maker.nn_to_nd,
                                  bnet_maker.dot_file,
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



    def print_adj_report(self,
                         verbose=False):
        """
        This method and the analogous one `print_all_prob_y_bar_x_z` are the
        only ones used in the jupyter notebooks. All others are meant to be
        internal. This method prints 4 things for each bnet.
        `num_bnet_makers=2` means the default is two bnets, but it will do only
        one bnet if you input `num_bnet_makers=1`

        1. full P(y|x) for OP

        2. amputated P(y|x) for OP. Calculating this in real life requires data
        from an RCT.

        3. adjusted P(y|x) from full_pot

        4. adjusted P(y|x) from ampu_pot. Calculating this in real life requires
        data from an RCT.



        Parameters
        ----------
        verbose: bool
            if this is set to True, the method prints also the CPT of each node
            of the bnet.

        Returns
        -------
        None

        """
        num_samples = 1
        if self.re_randomize_hidden_nds:
            num_samples = 2

        for k in range(num_samples):
            if k == 1:
                print("------------------------------")
                self.bnet_maker.randomize_these_nodes(
                    self.bnet_maker.hidden_nns)
                self.calc_adj_prob_y_bar_x()
            print(f"Random Bnet{self.bnet_maker.sample_num}:")
            if verbose:
                self.bnet_maker.print_CPTs()
            self.bnet_maker.print_full_and_ampu_prob_y_bar_x()

            print()
            self.print_adj_full_and_ampu_prob_y_bar_x(verbose)
            passed = self.conduct_closeness_test()
            print()
            if passed:
                print("Last 2 matrices are close so VALID adjustment")
            else:
                print("Last 2 matrices are not close so INVALID adjustment")




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
        tester = NDC_CaseTester(bnet_maker)
        tester.print_adj_report(verbose=verbose)


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
        tester = NDC_CaseTester(bnet_maker)
        tester.print_adj_report(verbose=verbose)


    def main_napkin(adj_version, draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None
,
        """
        if adj_version == 4:
            bnet_maker = NDC_BnetMaker(dot_file="dot_atlas/napkin.dot",
                                        hidden_nns=["u_1", "u_2"],
                                        other_cond="z",
                                        nn_to_size={"z": 3})
        else:
            bnet_maker = NDC_BnetMaker(dot_file="dot_atlas/napkin.dot",
                                        hidden_nns=["u_1", "u_2"])
        if draw:
            bnet_maker.draw(jupyter=False)
        tester = NDC_CaseTester(bnet_maker, adj_version=adj_version)
        tester.print_adj_report(verbose=verbose)


    # main_backdoor(False, False)
    main_frontdoor(False, False)
    # main_napkin(5, False, False)
