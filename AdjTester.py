from AdjCases import *
from BnetSample import *


class AdjTester:

    def __init__(self,
                 bnet_sample,
                 adj_pot_method=None,
                 adj_version=1):
        self.bnet_sample = bnet_sample
        self.adj_pot_method = adj_pot_method
        if not adj_pot_method:
            self.adj_case = AdjCases(bnet_sample.name_to_nd,
                                bnet_sample.dot_file,
                                adj_version)

        self.adj_ampu_prob_y_bar_x = None
        self.adj_full_prob_y_bar_x = None

    def calc_adj_prob_y_bar_x(self, adj_pot_method=None):
        if not adj_pot_method:
            adj_pot_method = self.adj_case.adj_pot_method
        self.adj_ampu_prob_y_bar_x= self.bnet_sample.calc_prob_y_bar_x(
            adj_pot_method(self.bnet_sample.ampu_pot))
        self.adj_full_prob_y_bar_x= self.bnet_sample.calc_prob_y_bar_x(
            adj_pot_method(self.bnet_sample.full_pot))

    def print_adj_full_and_ampu_prob_y_bar_x(self):
        if not self.bnet_sample.other_cond:
            print(f"adjusted P(y|x) from full_pot for "
                  f"Bnet{self.bnet_sample.sample_num}:")
            pprint(self.adj_ampu_prob_y_bar_x)
            print()
            print(f"adjusted P(y|x) from ampu_pot for "
                  f"Bnet{self.bnet_sample.sample_num} (REQUIRES RCT)")
            pprint(self.adj_ampu_prob_y_bar_x)
        else:
            print(f"adjusted P(y|x, {self.bnet_sample.other_cond}) "
                  f"from full_pot for "
                  f"Bnet{self.bnet_sample.sample_num}:")
            pprint(self.adj_full_prob_y_bar_x)
            print()
            print(f"adjusted P(y|x, {self.bnet_sample.other_cond}) "
                  f"from full_pot for "
                  f"Bnet{self.bnet_sample.sample_num} (REQUIRES RCT)")
            pprint(self.adj_full_prob_y_bar_x)

    def print_test_results(self,
                           adj_version=1,
                           re_randomize_hidden_nds=True,
                           verbose=True):
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
        dot_file: str
            the dot file (i.e., graphviz format) of the OP bnet
        hidden_nd_names: list[str]
            the names of the hidden nodes
        nd_to_size: dict[str, int]| None
            a node name to node size dict for those nodes that you don't want to
            have default sizes.
        verbose: bool
            if this is set to True, the method prints also the CPT of each node
            of the bnet.
        adj_version: int
            the adjustment formula version. For the Napkin OP, there are
            currently 4 adjustment formulae that are tested.
        num_bnet_samples: int
            number of random bnets considered. This can be either 1 or 2.

        Returns
        -------
        None

        """
        num_samples = 1
        if re_randomize_hidden_nds:
            num_samples = 2

        for k in range(num_samples):
            if k == 2:
                print("------------------------------")
                self.bnet_sample.randomize_these_nodes()
            print(f"Random Bnet{self.bnet_sample.sample_num}:")
            if verbose:
                self.bnet_sample.print_CPTs()
            self.bnet_sample.print_ampu_and_full_prob_y_bar_x()

            print()
            self.calc_adj_prob_y_bar_x(self.adj_pot_method)
            self.print_adj_full_and_ampu_prob_y_bar_x()





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
                                 hidden_nd_names=[]
                                 )
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample)
        tester.print_test_results(verbose=verbose)


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
                               hidden_nd_names=["h"])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample)
        tester.print_test_results(verbose=verbose)


    def main_napkin1(draw, verbose):
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
        bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample, adj_version=1)
        tester.print_test_results(verbose=verbose)


    def main_napkin2(draw, verbose):
        """     
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"])

        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample, adj_version=2)
        tester.print_test_results(verbose=verbose)

    def main_napkin3(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"])
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample, adj_version=3)
        tester.print_test_results(verbose=verbose)

    def main_napkin4(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                                 hidden_nd_names=["u_1", "u_2"],
                                 other_cond="z",
                                 nd_to_size={"z": 3})
        if draw:
            bnet_sample.draw(jupyter=False)
        tester = AdjTester(bnet_sample, adj_version=4)
        tester.print_test_results(verbose=verbose)

    # main_backdoor(False, False)
    # main_frontdoor(False, False)
    # main_napkin1(False, False)
    # main_napkin2(False, False)
    main_napkin3(False, False)
    # main_napkin6(False, False)
