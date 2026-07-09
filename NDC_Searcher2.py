from itertools import product
from NDC_BnetMaker import *
from NDC_Search2Tester import *

class NDC_Searcher2:

    def __init__(self, bnet_maker):
        """
        Constructor

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        """
        self.bnet_maker = bnet_maker

    def conduct_search(self, verbose):
        """

        Parameters
        ----------
        verbose: bool

        Returns
        -------
        None

        """
        hidden_nns = self.bnet_maker.hidden_nns
        num_hidden_nns = len(hidden_nns)
        non_hidden_xy_nns = [nn for nn in self.bnet_maker.nns if nn not in
                          hidden_nns + ["x", "y"]]

        for subs in product(non_hidden_xy_nns, repeat=num_hidden_nns):
            subs = list(subs)
            tester = NDC_Search2Tester(self.bnet_maker,
                                      subs)
            tester.print_adj_report(False)
