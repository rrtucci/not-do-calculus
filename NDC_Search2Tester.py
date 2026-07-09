from NDC_Tester import *
from NDC_global_funs import bnet_has_x_parent_that_is_hidden


class NDC_Search2Tester(NDC_Tester):

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

        Returns
        -------
        None

        """
        self.adj_ampu_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
            self.get_adj_pot_method(self.bnet_maker.ampu_pot))
        self.adj_full_prob_y_bar_x = self.bnet_maker.get_prob_y_bar_x(
            self.get_adj_pot_method(self.bnet_maker.full_pot))

    def get_adj_pot_method(self, in_pot):
        """

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential

        """

        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']
        hidden_nds = [self.nn_to_nd[h_nn] for h_nn in
                      self.bnet_maker.hidden_nns]
        hidden_xy_nds = hidden_nds + [nd_x, nd_y]

        pot_hidden_xy = in_pot.get_new_marginal(hidden_xy_nds)
        pot_hidden = pot_hidden_xy.get_new_marginal(hidden_nds)
        final_pot = pot_hidden_xy / pot_hidden
        for nn in self.subs:
            final_pot = final_pot * in_pot.get_new_marginal(self.nn_to_nd[nn])
        return final_pot
