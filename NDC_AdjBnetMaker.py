from numpy.lib.stride_tricks import broadcast_to
from NDC_BnetMaker import *
from NDC_global_funs import get_nn_to_sub, bnet_has_x_parent_that_is_hidden


class NDC_AdjBnetMaker(NDC_BnetMaker):
    """
    This class is a subclass of NDC_BnetMaker. Like its parent class,
    it creates a BayesNet, self.bnet. However, to create self.bnet, it uses
    parts from a bnet created by a previous NDC_BnetMaker object 'bnet_maker'.


    Attributes
    ----------
    bnet: BayesNet
        BayesNet object created by `create_random_bnet`. BayesNet or bnet
        stand for Bayesian network.
    bnet_maker: BnetMaker
        bnet_maker.net is used to create self.bnet
    nn_to_nd: dict[str, BayesNode]
        dict mapping node name (nn) to node (nd). nd is an object of BayesNode
    nn_to_sub: dict[str, str]
        dict mapping each node name to its substitute name. Those nodes which
        are not being substituted are mapped to themselves.
    subs: list[str]
        list of substitutions. self.hidden_nns is a list of the names of the
        hidden nodes, and subs is a list of their substitutes in the
        same order, so that subs[k] is the substitute of self.hidden_nns[k].
        self.hidden_nns and subs have the same length, of course.


    """

    def __init__(self,
                 bnet_maker,
                 subs,
                 nn_to_size=None,
                 other_cond=None):
        """
        Constructor

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        subs: list[str]
        nn_to_size: dict[str, int]
        other_cond: str
        """
        NDC_BnetMaker.__init__(self,
                               bnet_maker.nns,
                               bnet_maker.arrows,
                               bnet_maker.hidden_nns,
                               nn_to_size=nn_to_size,
                               other_cond=other_cond,
                               import_bnet=True)

        self.bnet_maker = bnet_maker
        self.subs = subs
        self.nn_to_sub = get_nn_to_sub(self.nns,
                                       self.hidden_nns,
                                       subs)

        self.bnet, self.nn_to_nd = self.create_random_bnet()
        self.calc_full_and_ampu_pots()
        self.calc_full_and_ampu_probs()

    def create_random_bnet(self):
        """
        This method creates a BayesNet self.bnet from the BayesNet
        self.BnetMaker.bnet. It returns self.bnet and a nn_to_nd for that
        bnet. nn_to_nd is a dict that maps each nn (str)  to its
        corresponding nd (BayesNode). This map is easily constructed from a
        BayesNet object and is very useful.

        This method overrides the namesake method in the parent class
        BnetMaker.

        Returns
        -------
        BayesNet, dict[str, BayesNode]

        """
        if not bnet_has_x_parent_that_is_hidden(self.arrows,
                                                self.hidden_nns):
            new_bnet = self.bnet_maker.bnet
            nn_to_new_nd = {name: new_bnet.get_node_named(name)
                            for name in self.nns}
            return new_bnet, nn_to_new_nd

        for h_name in self.hidden_nns:
            self.nn_to_size[h_name] = \
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
                sub_ord_nds = \
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns]
                numer_pot = self.bnet_maker.full_pot.get_new_marginal(
                    sub_ord_nds)
                denom_pot = numer_pot.get_new_marginal(sub_ord_nds[:-1])
                final_pot = numer_pot / denom_pot
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
                assert xx == sub_ord_nns[-1]
                sub_ord_nds = \
                    [self.bnet_maker.nn_to_nd[nn] for nn in sub_ord_nns]

                numer_pot = self.bnet_maker.full_pot.get_new_marginal(
                    sub_ord_nds)
                denom_pot = numer_pot.get_new_marginal(
                    sub_ord_nds[:-1])
                small_pot = numer_pot / denom_pot
                small_pot.set_to_transpose(sub_ord_nds)
                new_nd.potential.pot_arr = \
                    (broadcast_to(small_pot.pot_arr[tuple(colon_list)],
                                  tuple(size_list))).copy()
                # print("mvbh", new_nd.potential)
                # new_nd.potential.normalize_self()
        # print("mdrf new_bnet\n\n", new_bnet)
        # print("xcvt old bnet\n\n", self.bnet_maker.bnet)
        return new_bnet, nn_to_new_nd
