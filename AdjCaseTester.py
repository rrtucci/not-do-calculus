from AdjCases import *
from BnetSample import *

class AdjCaseTester:
    """
    Attributes
    ----------

    adj_ampu_prob_y_bar_x: np.array
    adj_case: AdjCases
    adj_full_prob_y_bar_x: np.array
    bnet_sample: BnetSample
    empty_adj: bool

    """

    def __init__(self,
                 bnet_sample,
                 adj_version=1,
                 null_adj = False):
        """

        Parameters
        ----------
        bnet_sample: BnetSample
        adj_version: int
            the adjustment formula version. For the Napkin OP, there are
            currently 4 adjustment formulae that are tested
        null_adj: bool
        """
        self.bnet_sample = bnet_sample
        self.empty_adj = null_adj
        self.adj_ampu_prob_y_bar_x = None
        self.adj_full_prob_y_bar_x = None
        self.adj_case = AdjCases(bnet_sample.nn_to_nd,
                                 bnet_sample.dot_file,
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
        if self.empty_adj:
            self.adj_ampu_prob_y_bar_x = \
                self.bnet_sample.ampu_prob_y_bar_x
            self.adj_full_prob_y_bar_x = \
                self.bnet_sample.full_prob_y_bar_x
        else:
            self.adj_ampu_prob_y_bar_x = self.bnet_sample.get_prob_y_bar_x(
                self.adj_case.adj_pot_method(self.bnet_sample.ampu_pot))
            self.adj_full_prob_y_bar_x = self.bnet_sample.get_prob_y_bar_x(
                self.adj_case.adj_pot_method(self.bnet_sample.full_pot))

    def print_adj_full_and_ampu_prob_y_bar_x(self, verbose):
        """

        Returns
        -------
        None

        """
        if not self.bnet_sample.other_cond:
            print(f"adjusted P(y|x) from full_pot for "
                  f"Bnet{self.bnet_sample.sample_num} "
                  f"(determined from PO data):")
            pprint(self.adj_full_prob_y_bar_x)
            if verbose:
                print()
                print(f"adjusted P(y|x) from ampu_pot for "
                      f"Bnet{self.bnet_sample.sample_num} "
                      f"(determined from RCT data):")
                pprint(self.adj_ampu_prob_y_bar_x)
        else:
            print(f"adjusted P(y|x, {self.bnet_sample.other_cond}) "
                  f"from full_pot for "
                  f"Bnet{self.bnet_sample.sample_num} "
                  f"(determined from PO data):")
            pprint(self.adj_full_prob_y_bar_x)
            if verbose:
                print()
                print(f"adjusted P(y|x, {self.bnet_sample.other_cond}) "
                      f"from ampu_pot for "
                      f"Bnet{self.bnet_sample.sample_num} "
                      f"(determined from RCT data):")
                pprint(self.adj_ampu_prob_y_bar_x)

    def print_adj_report(self,
                         re_randomize_hidden_nds=True,
                         verbose=False):
        """
        This method and the analogous one `print_all_prob_y_bar_x_z` are the
        only ones used in the jupyter notebooks. All others are meant to be
        internal. This method prints 4 things for each bnet.
        `num_bnet_samples=2` means the default is two bnets, but it will do only
        one bnet if you input `num_bnet_samples=1`

        1. full P(y|x) for OP

        2. amputated P(y|x) for OP. Calculating this in real life requires data
        from an RCT.

        3. adjusted P(y|x) from full_pot

        4. adjusted P(y|x) from ampu_pot. Calculating this in real life requires
        data from an RCT.



        Parameters
        ----------
        re_randomize_hidden_nds: bool
        verbose: bool
            if this is set to True, the method prints also the CPT of each node
            of the bnet.

        Returns
        -------
        None

        """
        num_samples = 1
        if re_randomize_hidden_nds:
            num_samples = 2

        for k in range(num_samples):
            if k == 1:
                print("------------------------------")
                self.bnet_sample.randomize_these_nodes(
                    self.bnet_sample.hidden_nns)
            print(f"Random Bnet{self.bnet_sample.sample_num}:")
            if verbose:
                self.bnet_sample.print_CPTs()
            self.bnet_sample.print_full_and_ampu_prob_y_bar_x()

            print()
            self.calc_adj_prob_y_bar_x()
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
                           self.bnet_sample.ampu_prob_y_bar_x)
        return passed_test


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
        bnet_sample = BnetSample(dot_file="dot_atlas/back-door.dot",
                                 hidden_nns=[])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjCaseTester(bnet_sample)
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
        bnet_sample = BnetSample(dot_file="dot_atlas/front-door.dot",
                                 hidden_nns=["h"])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjCaseTester(bnet_sample)
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
            bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                                     hidden_nns=["u_1", "u_2"],
                                     other_cond="z",
                                     nn_to_size={"z": 3})
        else:
            bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                                     hidden_nns=["u_1", "u_2"])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjCaseTester(bnet_sample, adj_version=adj_version)
        tester.print_adj_report(verbose=verbose)


    # main_backdoor(False, False)
    # main_frontdoor(False, False)
    main_napkin(5, False, False)
