from numpy.lib.stride_tricks import broadcast_to

from NDC_BnetSample import *

GLUE = ">"
class NDC_AdjBnetSample(NDC_BnetSample):
    def __init__(self, bnet_sample, hidden_nn_subs):
        NDC_BnetSample.__init__(self, 
                                bnet_sample.dot_file,
                                bnet_sample.hidden_nns,
                                import_bnet=True)
        self.arrows = bnet_sample.arrows
        # self.dot_file = bnet_sample.dot_file
        # self.hidden_nns = bnet_sample.hidden_nns
        self.nn_to_size = bnet_sample.nn_to_size
        self.nns = bnet_sample.nns
        self.other_cond = bnet_sample.other_cond
        # self.import_bnet = bnet_sample.import_bnet
        
        
        self.bnet_sample = bnet_sample
        self.hidden_nn_subs = hidden_nn_subs

        self.nn_to_sub = \
            {nn: nn for nn in bnet_sample.nns}
        for k in range(len(bnet_sample.hidden_nns)):
            self.nn_to_sub[bnet_sample.hidden_nns[k]] = \
                hidden_nn_subs[k]

        self.nn_to_parents = NDC_AdjBnetSample.get_nn_to_parents(
            self.arrows, self.nns)
        self.valid_sub = NDC_AdjBnetSample.substitution_is_valid(
            self.nn_to_parents, self.nn_to_sub)
        if self.valid_sub:
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
    def bnet_has_x_parent_that_is_hidden(arrows, hidden_nns):
        for arrow in arrows:
            if arrow[0] == "x" and arrow[1] in hidden_nns:
                return True
        return False
    
    @staticmethod
    def get_nn_to_parents(arrows, nns):
        #nn = node name
        nn_to_parents = {nn:[] for nn in nns}
        for nn in nns:
            for arrow in arrows:
                pa, child = arrow
                nn_to_parents[child].append(pa)
        return nn_to_parents
    
    @staticmethod
    def substitution_is_valid(nn_to_parents, nn_to_sub):
        for nn, parents in nn_to_parents.items():
            sub_parents = [nn_to_sub[nn] for nn in parents]
            print("nn, parents, sub_parents", nn, parents, sub_parents)
            if len(sub_parents) != len(set(sub_parents)):
                return False
        return True
        
    def create_random_bnet(self):
        if not NDC_AdjBnetSample.\
                bnet_has_x_parent_that_is_hidden(self.arrows, 
                                                 self.hidden_nns):
            bnet = self.bnet_sample.bnet
            return bnet

        for h_name in self.hidden_nns:
            self.nn_to_size[h_name]= \
                self.bnet_sample.nn_to_size[self.nn_to_sub[h_name]]
            
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
        for nn, nd in self.bnet_sample.nn_to_nd.items():
            nd_to_self_nd[nd] = self.nn_to_nd[nn]
        
        for nd, self_nd in nd_to_self_nd.items():
            self_ord_nodes = [nd_to_self_nd[nd] for
                             nd in nd.potential.ord_nodes]
            # print("llkjh", ord_nodes)
            self_nd.potential = DiscreteCondPot(False, 
                                               self_ord_nodes)
            ord_nns = [nd.name for nd in nd.potential.ord_nodes]
            sub_ord_nns = [self.bnet_sample.nn_to_sub[nn]
                           for nn in ord_nns]


            if len(sub_ord_nns) == len(set(sub_ord_nns)):
                num_pot = self.bnet_sample.full_pot.get_self_marginal(
                    [self.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_self_marginal(
                    [self.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                self_nd.potential.pot_arr = (num_pot/denom_pot).pot_arr
            else:
                colon_list = []
                k0 = sub_ord_nns.index(sub_ord_nns[-1])
                for k in range(len(sub_ord_nns)):
                    if k != k0:
                        colon_list.append(slice(None))
                    else:
                        colon_list.append(None)
                size_list = [self.nn_to_size[nn] for nn in sub_ord_nns]
                # this removes first occurrence of sub_ord_nns[-1]
                # second occurence at the end of list is kept
                sub_ord_nns.remove(sub_ord_nns[-1])
                num_pot = self.bnet_sample.full_pot.get_self_marginal(
                    [self.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_self_marginal(
                    [self.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                small_pot_arr = (num_pot/denom_pot).pot_arr
                self_nd.potential.pot_arr = \
                    np.broadcast_to(small_pot_arr[colon_list],
                                    size_list)
            # nd.potential.normalize_self()
        return bnet
        