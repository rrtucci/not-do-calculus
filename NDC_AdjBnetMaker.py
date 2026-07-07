from numpy.lib.stride_tricks import broadcast_to

from NDC_BnetMaker import *

GLUE = ">"
class NDC_AdjBnetMaker(NDC_BnetMaker):
    def __init__(self,
                 bnet_maker,
                 subs,
                 nn_to_size=None,
                 other_cond=None):
        NDC_BnetMaker.__init__(self,
                               bnet_maker.nns,
                               bnet_maker.arrows,
                               bnet_maker.hidden_nns,
                               nn_to_size=nn_to_size,
                               other_cond=other_cond,
                               import_bnet=True)


        self.bnet_maker = bnet_maker
        self.subs = subs
        self.nn_to_sub = NDC_AdjBnetMaker.get_nn_to_sub(self.nns,
                                                        self.hidden_nns,
                                                        subs)

        self.bnet, self.nn_to_nd = self.create_random_bnet()
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
            if arrow[1] == "x" and arrow[0] in hidden_nns:
                return True
        return False
    

    def create_random_bnet(self):
        if not NDC_AdjBnetMaker.\
                bnet_has_x_parent_that_is_hidden(self.arrows, 
                                                 self.hidden_nns):
            new_bnet = self.bnet_maker.bnet
            nn_to_new_nd = {name: new_bnet.get_node_named(name)
                             for name in self.nns}
            return new_bnet, nn_to_new_nd

        for h_name in self.hidden_nns:
            self.nn_to_size[h_name]= \
                self.bnet_maker.nn_to_size[self.nn_to_sub[h_name]]
            
        bnet_nodes = []
        for k, node_name in enumerate(self.nns):
            nd = BayesNode(k, name=node_name)
            nd.size = self.nn_to_size[node_name]
            bnet_nodes.append(nd)
        new_bnet = BayesNet(set(bnet_nodes))
        nn_to_new_nd = {name: new_bnet.get_node_named(name)
                         for name in self.nns}

        for arrow in self.arrows:
            pa_nd = nn_to_new_nd[arrow[0]]
            child_nd = nn_to_new_nd[arrow[1]]
            child_nd.add_parent(pa_nd)
            

        nd_to_new_nd = {}
        for nn, nd in self.bnet_maker.nn_to_nd.items():
            nd_to_new_nd[nd] = nn_to_new_nd[nn]
        
        for nd, new_nd in nd_to_new_nd.items():
            # print("kloi", "new node================")
            ord_new_nodes = [nd_to_new_nd[nd] for
                             nd in nd.potential.ord_nodes]
            new_nd.potential = DiscreteCondPot(False,
                                               ord_new_nodes)
            ord_nns = [nd.name for nd in nd.potential.ord_nodes]
            sub_ord_nns = [self.nn_to_sub[nn] for nn in ord_nns]

            len_list = len(sub_ord_nns)
            len_set = len(set(sub_ord_nns))
            if len_list == len_set:
                # print("vvbn", "==, sub_ord_nns", sub_ord_nns)
                sub_ord_nds =\
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns]
                numer_pot = self.bnet_maker.full_pot.get_new_marginal(
                    sub_ord_nds)
                denom_pot = numer_pot.get_new_marginal(sub_ord_nds[:-1])
                final_pot = numer_pot/denom_pot
                # print("mnbn final pot", final_pot)
                final_pot.set_to_transpose(sub_ord_nds)
                # print("mnbn final pot", final_pot)
                new_nd.potential.pot_arr = final_pot.pot_arr
                # new_nd.potential.normalize_self()
                # print("mcvth", new_nd.potential)
            else:
                assert len_list == len_set + 1
                colon_list = []
                k0 = sub_ord_nns.index(sub_ord_nns[-1])
                for k in range(len(sub_ord_nns)):
                    if k != k0:
                        colon_list.append(slice(None))
                    else:
                        colon_list.append(None)
                # print("ccvb", colon_list)
                # print("vvbn", "!=, k0, sub_ord_nns", k0, sub_ord_nns)
                size_list = [self.bnet_maker.nn_to_size[nn] for nn in
                             sub_ord_nns]
                # this removes first occurrence of sub_ord_nns[-1]
                # second occurrence at the end of list is kept
                xx = sub_ord_nns.pop(k0)
                assert xx ==  sub_ord_nns[-1]
                sub_ord_nds =\
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns]

                numer_pot = self.bnet_maker.full_pot.get_new_marginal(
                    sub_ord_nds)
                denom_pot = numer_pot.get_new_marginal(
                    sub_ord_nds[:-1])
                small_pot = numer_pot/denom_pot
                small_pot.set_to_transpose(sub_ord_nds)
                new_nd.potential.pot_arr = \
                    (broadcast_to(small_pot.pot_arr[tuple(colon_list)],
                                    tuple(size_list))).copy()
                # print("mvbh", new_nd.potential)
                # new_nd.potential.normalize_self()
        # print("mdrf new_bnet\n\n", new_bnet)
        # print("xcvt old bnet\n\n", self.bnet_maker.bnet)
        return new_bnet, nn_to_new_nd
        