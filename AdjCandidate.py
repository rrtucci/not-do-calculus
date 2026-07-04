from numpy.lib.stride_tricks import broadcast_to

from BnetSample import *

GLUE = ">"
class AdjCandidate:
    def __init__(self, bnet_sample, hidden_nn_subs, verbose=True):
        self.bnet_sample = bnet_sample
        
        self. nn_to_sub= \
            {name: name for name in bnet_sample.nns}
        for k in range(len(bnet_sample.hidden_nns)):
            self.nn_to_sub[bnet_sample.hidden_nns[k]] =\
                hidden_nn_subs[bnet_sample.new_hidden_nns[k]]
            
        self.nn_to_parents = AdjCandidate.get_nn_to_parents(
            bnet_sample.arrows, bnet_sample.nns)
        self.new_bnet_sample = None
        self.valid_sub = AdjCandidate.substitution_is_valid(
            self.nn_to_parents, self.nn_to_sub)
        if not self.valid_sub:
            if verbose:
                print(f"mapping {bnet_sample.hidden_nns} "
                      f"to {hidden_nn_subs} is illegal")
        else:
            self.create_new_bnet_sample()

    def bnet_has_x_parent_that_is_hidden(self):
        for arrow in self.bnet_sample.arrows:
            arrow0, arrow1 = arrow
            if arrow0 == "x" and arrow1 in self.bnet_sample.hidden_nns:
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
            if len(sub_parents) != len(set(sub_parents)):
                return False
        return True
        
    def create_new_bnet_sample(self):
        if not self.bnet_has_x_parent_that_is_hidden():
            self.new_bnet_sample = self.bnet_sample
            return
        self.new_bnet_sample = BnetSample(self.bnet_sample.dot_file,
                                     self.bnet_sample.hidden_nns,
                                     import_bnet=True)
        new_bs = self.new_bnet_sample
        for h_name in new_bs.hidden_nns:
            new_bs.nn_to_size[h_name]= \
                self.bnet_sample.nn_to_size[self.nn_to_sub[h_name]]
            
        new_bnet_nodes = []
        for k, node_name in enumerate(new_bs.nns):
            nd = BayesNode(k, name=node_name)
            nd.size = new_bs.nn_to_size[node_name]
            new_bnet_nodes.append(nd)
        new_bnet = BayesNet(set(new_bnet_nodes))
        for arrow in new_bs.arrows:
            pa_nd = new_bnet.get_node_named(arrow[0])
            child_nd = new_bnet.get_node_named(arrow[1])
            child_nd.add_parent(pa_nd)
            
        new_bs.bnet = new_bnet

        nd_to_new_nd = {}
        for nn, nd in self.bnet_sample.nn_to_nd.items():
            nd_to_new_nd[nd] = new_bs.nn_to_nd[nn]
        
        for nd, new_nd in nd_to_new_nd.items():
            new_ord_nodes = [nd_to_new_nd[nd] for
                             nd in nd.potential.ord_nodes]
            # print("llkjh", ord_nodes)
            new_nd.potential = DiscreteCondPot(False, new_ord_nodes)
            ord_nns = [nd.name for nd in nd.potential.ord_nodes]
            sub_ord_nns = [self.bnet_sample.nn_to_sub[nn]
                           for nn in ord_nns]


            if len(sub_ord_nns) == len(set(sub_ord_nns)):
                num_pot = self.bnet_sample.full_pot.get_new_marginal(
                    [new_bs.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_new_marginal(
                    [new_bs.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                new_nd.potential.pot_arr = (num_pot/denom_pot).pot_arr
            else:
                colon_list = []
                k0 = sub_ord_nns.index(sub_ord_nns[-1])
                for k in range(len(sub_ord_nns)):
                    if k != k0:
                        colon_list.append(slice(None))
                    else:
                        colon_list.append(None)
                size_list = [new_bs.nn_to_size[nn] for nn in sub_ord_nns]
                # this removes first occurrence of sub_ord_nns[-1]
                # second occurence at the end of list is kept
                sub_ord_nns.remove(sub_ord_nns[-1])
                num_pot = self.bnet_sample.full_pot.get_new_marginal(
                    [new_bs.nn_to_nd[nn] for nn in sub_ord_nns])
                denom_pot = num_pot.get_new_marginal(
                    [new_bs.nn_to_nd[nn] for nn in sub_ord_nns[:-1]])
                small_pot_arr = (num_pot/denom_pot).pot_arr
                new_nd.potential.pot_arr = \
                    np.broadcast_to(small_pot_arr[colon_list],
                                    size_list)
            # nd.potential.normalize_self()
        
        