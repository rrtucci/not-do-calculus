from NDC_Tester import *


class NDC_NullAdjTester(NDC_Tester):
    """
    The purpose of this class is to test whether the null adjustment is
    valid. The null adjustment is valid iff P(y|do(x)) = P(y|x)

    adj_ampu_prob_y_bar_x: np.array
    adj_full_prob_y_bar_x: np.array


    """

    def __init__(self,
                 bnet_maker,
                 re_randomize_hidden_nds=False):
        """

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        re_randomize_hidden_nds: bool
        """
        NDC_Tester.__init__(self,
                            bnet_maker,
                            re_randomize_hidden_nds)

    def calc_adj_prob_y_bar_x(self):
        """

        Returns
        -------
        None

        """
        self.adj_ampu_prob_y_bar_x = \
            self.bnet_maker.ampu_prob_y_bar_x
        self.adj_full_prob_y_bar_x = \
            self.bnet_maker.full_prob_y_bar_x
