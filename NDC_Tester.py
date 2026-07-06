from NDC_BnetMaker import *

class NDC_Tester:
    def __init__(self,
                 bnet_maker,
                 re_randomize_hidden_nds=False,
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
        self.bnet_maker = bnet_maker
        self.re_randomize_hidden_nds  = re_randomize_hidden_nds
        self.null_adj = null_adj
        self.adj_ampu_prob_y_bar_x = None
        self.adj_full_prob_y_bar_x = None

    def calc_adj_prob_y_bar_x(self):
        assert False

    def print_adj_full_and_ampu_prob_y_bar_x(self, verbose):
        """

        Returns
        -------
        None

        """
        if not self.bnet_maker.other_cond:
            print(f"adjusted P(y|x) from full_pot for "
                  f"Bnet{self.bnet_maker.sample_num} "
                  f"(determined from PO data):")
            pprint(self.adj_full_prob_y_bar_x)
            if verbose:
                print()
                print(f"adjusted P(y|x) from ampu_pot for "
                      f"Bnet{self.bnet_maker.sample_num} "
                      f"(determined from RCT data):")
                pprint(self.adj_ampu_prob_y_bar_x)
        else:
            print(f"adjusted P(y|x, {self.bnet_maker.other_cond}) "
                  f"from full_pot for "
                  f"Bnet{self.bnet_maker.sample_num} "
                  f"(determined from PO data):")
            pprint(self.adj_full_prob_y_bar_x)
            if verbose:
                print()
                print(f"adjusted P(y|x, {self.bnet_maker.other_cond}) "
                      f"from ampu_pot for "
                      f"Bnet{self.bnet_maker.sample_num} "
                      f"(determined from RCT data):")
                pprint(self.adj_ampu_prob_y_bar_x)

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


    def conduct_closeness_test(self):
        """
        verbose: bool

        Returns
        -------
        bool

        """
        passed_test = np.allclose(self.adj_full_prob_y_bar_x,
                           self.bnet_maker.ampu_prob_y_bar_x)
        return passed_test
