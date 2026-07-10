from NDC_Tester import *
from NDC_global_funs import bnet_has_x_parent_that_is_hidden


class NDC_Search2Tester(NDC_Tester):
    """
    This class is a subclass of the abstract class NDC_Tester. Objects of
    this class are created within NDC_Searcher2 to search for valid
    adjustments.

    Essentially, this class creates the pot for an adjustment of the form

    P(y|do(x)) = \frac{1}{\sum_y numer} \sum_{u, v} P(x,y|u, v) P(u)P(v)

    where we are assuming there are two hidden nodes h1 and h2 which are
    replaced by u and v, respectively

    Attributes
    ----------
    adj_ampu_prob_y_bar_x: np.array
        P(y|x) numpy array for adjustment calculated from amputated bnet
    adj_full_prob_y_bar_x: np.array
        P(y|x) numpy array for adjustment calculated from full bnet
    nn_to_nd: dict[str, BayesNode]
        dict mapping each nn (node name) to its nd (BayesNode)
    subs: list[str]
        list of substitutions. subs[k] is hidden_nns[k]

    """

    def __init__(self, bnet_maker, subs):
        """
        Constructor

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        subs: list[str]
        """
        NDC_Tester.__init__(self, bnet_maker)
        self.nn_to_nd = bnet_maker.nn_to_nd
        self.subs = subs
        self.calc_adj_prob_y_bar_x()

    def calc_adj_prob_y_bar_x(self):
        """
        This method calculates

        self.adj_ampu_prob_y_bar_x

        and

        self.adj_full_prob_y_bar_x

        using the function self.get_adj_pot

        Returns
        -------
        None

        """
        if self.subs:
            self.adj_ampu_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
                self.get_adj_pot(self.bnet_maker.ampu_pot))
            self.adj_full_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
                self.get_adj_pot(self.bnet_maker.full_pot))
        else:
            self.adj_ampu_prob_y_bar_x = self.bnet_maker.ampu_prob_y_bar_x
            # this is crucial: the full and ampu adj prob are the same
            # because the bnet should be amputated to begin with
            self.adj_full_prob_y_bar_x = self.bnet_maker.ampu_prob_y_bar_x

    def get_adj_pot(self, in_pot):
        """
        This method returns the adjustment's pot. This pot depends on self.subs
        and in_pot. in_pot is either full_pot or ampu_pot.

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential

        """
        assert self.subs

        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']
        subs_nds = [self.nn_to_nd[nn] for nn in self.subs]
        subs_xy_nds = subs_nds + [nd_x, nd_y]

        pot_subs_xy = in_pot.get_new_marginal(subs_xy_nds)
        pot_subs = pot_subs_xy.get_new_marginal(subs_nds)
        final_pot = pot_subs_xy / pot_subs
        for nn in self.subs:
            final_pot = final_pot * in_pot.get_new_marginal(
                [self.nn_to_nd[nn]])
        return final_pot
