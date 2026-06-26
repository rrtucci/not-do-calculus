from potentials.DiscreteCondPot import *

class GenericAdjustmentFormula:

    def __init__(self,
                 bnet,
                 hidden_nd_names,
                 adj_names,
                 partition_id_to_adj_names):
        self.bnet = bnet
        self.hidden_nd_names = hidden_nd_names
        self.adj_names = adj_names
        self.partition_id_to_adj_names = partition_id_to_adj_names

        self.adj_nds = [bnet.get_nd_named(name) for name in adj_names]
        self.partition_id_to_adj_nds = {}
        for pid, names in partition_id_to_adj_names:
            self.partition_id_to_adj_nds[pid] = \
                [bnet.get_nd_named(name) for name in names]

    def get_adj_formula_str(self):
        str1 = r"\frac{1}{\sum_y num}\sum_{"
        for name in self.adj_names:
            str1 += name + ", "
        str1 = str1[-2] + r"}P(x, y|"
        for name in self.adj_names:
            str1 += name + ", "
        str1 = str1[-2] + r")"
        for pid, names in self.partition_id_to_adj_names:
            str1 += r"P("
            for name in names:
                str1 += name + ", "
            str1 = str1[-2] + r")"

        return str1

    def get_adj_probs(self, full_pot):
        nd_x = self.bnet.get_nd_named("x")
        nd_y = self.bnet.get_nd_named("y")
        xy_adj_nds = [nd_x, nd_y] + self.adj_nds
        pot_xy_adj = full_pot.get_new_marginal(xy_adj_nds)
        pot_adj = full_pot.get_new_marginal(self.adj_nds)
        pid_to_pot = {}
        for pid, adj_nds in self.partition_id_to_adj_nds.items():
            pid_to_pot[pid] = full_pot.get_new_marginal(adj_nds)

        final_pot = pot_xy_adj/pot_adj
        for pid, pot in pid_to_pot.items():
            final_pot = final_pot*pot

        arr_y_bar_x = final_pot.get_new_marginal([nd_x, nd_y]).pot_arr
        pot_y_bar_x = DiscreteCondPot(False,
                                      [nd_x, nd_y],
                                      arr_y_bar_x)
        pot_y_bar_x.normalize_self()
        prob_y_bar_x = pot_y_bar_x.pot_arr
        return prob_y_bar_x



