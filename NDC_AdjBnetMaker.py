from numpy.lib.stride_tricks import broadcast_to

from NDC_BnetMaker import *

GLUE = ">"
class NDC_AdjBnetMaker(NDC_BnetMaker):
    def __init__(self, bnet_maker, subs):
        NDC_BnetMaker.__init__(self,
                               bnet_maker.dot_file,
                               bnet_maker.hidden_nns,
                               import_bnet=True)
        self.arrows = bnet_maker.arrows
        # self.dot_file = bnet_maker.dot_file
        # self.hidden_nns = bnet_maker.hidden_nns
        self.nn_to_size = bnet_maker.nn_to_size
        self.nns = bnet_maker.nns
        self.other_cond = bnet_maker.other_cond
        # self.import_bnet = bnet_maker.import_bnet
        
        
        self.bnet_maker = bnet_maker
        self.subs = subs

        self.nn_to_sub = NDC_AdjBnetMaker.get_nn_to_sub(
            bnet_maker.nns, bnet_maker.hidden_nns, subs
        )

        self.bnet = self.create_random_bnet()
        self.nn_to_nd = {name: self.bnet.get_node_named(name)
                         for name in self.nns}
        self.ampu_pot = None
        self.full_pot = None
        self.ampu_prob_y_bar_x = None
        self.full_prob_y_bar_x = None
        self.calc_full_and_ampu_pots()
        self.calc_full_and_ampu_probs()

    @staticmethod
    def get_nn_to_sub(nns, hidden_nns, subs):
        nn_to_sub = \
            {nn: nn for nn in nns}
        for k in range(len(hidden_nns)):
            nn_to_sub[hidden_nns[k]] = subs[k]
        return nn_to_sub

    @staticmethod
    def bnet_has_x_parent_that_is_hidden(arrows, hidden_nns):
        for arrow in arrows:
            if arrow[0] == "x" and arrow[1] in hidden_nns:
                return True
        return False
    

    def create_random_bnet(self):
        if not NDC_AdjBnetMaker.\
                bnet_has_x_parent_that_is_hidden(self.arrows, 
                                                 self.hidden_nns):
            bnet = self.bnet_maker.bnet
            return bnet

        for h_name in self.hidden_nns:
            self.nn_to_size[h_name]= \
                self.bnet_maker.nn_to_size[self.nn_to_sub[h_name]]
            
        bnet_nodes = []
        for k, node_name in enumerate(self.nns):
            nd = BayesNode(k, name=node_name)
            nd.size = self.nn_to_size[node_name]
            bnet_nodes.append(nd)
        bnet = BayesNet(set(bnet_nodes))
        self.nn_to_nd = {name: bnet.get_node_named(name)
                         for name in self.nns}

        for arrow in self.arrows:
            pa_nd = self.nn_to_nd[arrow[0]]
            child_nd = self.nn_to_nd[arrow[1]]
            child_nd.add_parent(pa_nd)
            

        nd_to_self_nd = {}
        for nn, nd in self.bnet_maker.nn_to_nd.items():
            nd_to_self_nd[nd] = self.nn_to_nd[nn]
        
        for nd, self_nd in nd_to_self_nd.items():
            self_ord_nodes = [nd_to_self_nd[nd] for
                             nd in nd.potential.ord_nodes]
            # print("llkjh", ord_nodes)
            self_nd.potential = DiscreteCondPot(False, 
                                               self_ord_nodes)
            ord_nns = [nd.name for nd in nd.potential.ord_nodes]
            sub_ord_nns = [self.nn_to_sub[nn] for nn in ord_nns]

            len_list = len(sub_ord_nns)
            len_set = len(set(sub_ord_nns))
            if len_list == len_set:
                num_pot = self.bnet_maker.full_pot.get_self_marginal(
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_self_marginal(
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                self_nd.potential.pot_arr = (num_pot/denom_pot).pot_arr
            else:
                assert len_list == len_set + 1
                colon_list = []
                k0 = sub_ord_nns.index(sub_ord_nns[-1])
                for k in range(len(sub_ord_nns)):
                    if k != k0:
                        colon_list.append(slice(None))
                    else:
                        colon_list.append(None)
                size_list = [self.bnet_maker.nn_to_size[nn] for nn in
                             sub_ord_nns]
                # this removes first occurrence of sub_ord_nns[-1]
                # second occurrence at the end of list is kept
                xx = sub_ord_nns.pop(k0)
                assert xx ==  sub_ord_nns[-1]
                num_pot = self.bnet_maker.full_pot.get_self_marginal(
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_self_marginal(
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                small_pot_arr = (num_pot/denom_pot).pot_arr
                self_nd.potential.pot_arr = \
                    np.broadcast_to(small_pot_arr[colon_list],
                                    tuple(size_list))
            # nd.potential.normalize_self()
        return bnet
        