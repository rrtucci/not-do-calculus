from NDC_Tester import *
from NDC_AdjBnetMaker import *

class NDC_SearchTester(NDC_Tester):

    def __init__(self, bnet_maker, adj_bnet_maker):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        adj_bnet_maker: NDC_AdjBnetMaker
        """
        NDC_Tester.__init__(self, bnet_maker)
        self.adj_ampu_prob_y_bar_x = adj_bnet_maker.ampu_prob_y_bar_x
        self.adj_full_prob_y_bar_x = adj_bnet_maker.full_prob_y_bar_x


    def calc_adj_prob_y_bar_x(self):
        return

