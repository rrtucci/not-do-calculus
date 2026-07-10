from NDC_BnetMaker import *


class NDC_Tester:
    """
    This class is an abstract class because its method
    calc_adj_prob_y_bar_x() is abstract; i.e., must be overridden by
    subclasses. The classes NDC_CaseTester and NDC_Search1Tester are
    subclasses of this class. The purpose of this class is to test
    adjustments. The adjustment is said to be valid if the numpy arrays

    adj_ampu_prob_y_bar_x

    and

    adj_full_prob_y_bar_x

    are close (the same to a high precision)


    Attributes
    ----------
    adj_ampu_prob_y_bar_x: np.array
        the probability P(y|x) for the adjustment under consideration,
        calculated from the amputated self.bnet_maker.bnet
    adj_full_prob_y_bar_x: np.array
        the probability P(y|x) for the adjustment under consideration,
        calculated from the amputated self.bnet_maker.bnet
    bnet_maker: NDC_BnetMaker
        bnet_maker.bnet is used to calculate the adjustment pot via the
        abstract method calc_adj_prob_y_bar_x()
    """

    def __init__(self,
                 bnet_maker,
                 re_randomize_hidden_nds=False):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        re_randomize_hidden_nds: bool
            This bool is True iff we consider 2 bnets instead of one.
            The second bnet differs from the first in that the CTPs for the
            hidden nodes are randomized.
        """
        self.bnet_maker = bnet_maker
        self.re_randomize_hidden_nds = re_randomize_hidden_nds
        self.adj_ampu_prob_y_bar_x = None
        self.adj_full_prob_y_bar_x = None

    def calc_adj_prob_y_bar_x(self):
        """
        abstract method

        Returns
        -------
        None

        """
        assert False

    def print_adj_full_and_ampu_prob_y_bar_x(self, verbose):
        """
        If other_cond=None, this method prints two numpy arrays:

        adjusted P(y|x) from full_pot

        adjusted P(y|x) from ampu_pot

        If other_cond= "z", it prints P(y|x,z) instead of P(y|x)

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
        This method prints the following 4 things for each bnet.
        re_randomize_hidden_nds = True means the default is two bnets.
        Otherwise, it will do just one.

        1. full P(y|x) for OP

        2. amputated P(y|x) for OP. This probability is what a CPT yields

        3. adjusted P(y|x) from full_pot

        4. adjusted P(y|x) from ampu_pot.



        Parameters
        ----------
        verbose: bool
            if this is set to True, the method prints also the CPT of each
            node of the bnet.

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
        This method returns True iff the numpy arrays

        self.adj_full_prob_y_bar_x

        and

        self.bnet_maker.ampu_prob_y_bar_x

        are close (the same to a high precision)

        Returns
        -------
        bool

        """
        passed_test = np.allclose(self.adj_full_prob_y_bar_x,
                                  self.bnet_maker.ampu_prob_y_bar_x)
        return passed_test
