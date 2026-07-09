from NDC_Tester import *
from NDC_AdjBnetMaker import *


class NDC_Search1Tester(NDC_Tester):
    """
    This class is a subclass of the abstract class NDC_Tester. It overrides
    the method calc_adj_prob_y_bar_x(). This class uses within method
    calc_adj_prob_y_bar_x(), an input object `adj_bnet_maker` of class
    NDC_AdjBnetMaker. Objects of this class are created within NDC_Searcher1
    to search for valid AF.


    Attributes
    ----------
    adj_ampu_prob_y_bar_x: np.array
    adj_bnet_maker: NDC_AdjBnetMakerker
    adj_full_prob_y_bar_x: np.array
    """

    def __init__(self, bnet_maker, adj_bnet_maker):
        """
        Constructor

        Essentially, this class compares P(y|x) produced from
        bnet_maker and adj_bnet_maker.

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        adj_bnet_maker: NDC_AdjBnetMaker
        """
        NDC_Tester.__init__(self, bnet_maker)
        self.adj_bnet_maker = adj_bnet_maker
        self.calc_adj_prob_y_bar_x()

    def calc_adj_prob_y_bar_x(self):
        """
        This method sets

        self.adj_ampu_prob_y_bar_x

        and

        self.adj_full_prob_y_bar_x

        Returns
        -------
        None

        """
        self.adj_ampu_prob_y_bar_x = self.adj_bnet_maker.ampu_prob_y_bar_x
        # this is crucial: the full and ampu adj prob are the same
        # because the bnet should be amputated to begin with
        self.adj_full_prob_y_bar_x = self.adj_bnet_maker.ampu_prob_y_bar_x
