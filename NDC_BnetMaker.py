from potentials.DiscreteCondPot import *
from graphs.BayesNet import *
from pprint import pprint
from DotTool import *


class NDC_BnetMaker:
    """
    Attributes
    ----------
    ampu_pot: Potential
    ampu_prob_y_bar_x: np.array
    arrows: list[tuple[str, str]]
            example: [('a', 'b'), ('a', 'c')], where ('a', 'b') means a->b
    bnet: BayesNet
        BayesNet object created by `create_random_bnet`. BayesNet or bnet
        stand for Bayesian network.
    dot_file: str
        dot file (i.e., graphviz format) of the OP (Original Promise) bnet.

    full_pot: Potential
    full_prob_y_bar_x: np.array
    hidden_nns: list[str]
        names of hidden nodes
    nn_to_nd: dict[str, BayesNode]
    nns: list[str]
        example: ['a', 'b', 'c']
    nn_to_size: dict[str, int] | None
        dict mapping each node name to its size. This input need only be a
        partial list of those nodes that you don't want to have default
        values. dictionary mapping node name to its size (i.e., the number
        of values or states). In this method, `nn_to_size` must contain all
        the nodes. In all other methods in this file (for example,
        in `fill_node_to_size( )`), `nn_to_size` contains only special nodes
        which you don't want to have a default size. Default sizes are 2 for
        non-hidden nodes and 3 for hidden ones.
    other_cond: str | None
    sample_num: int

    """

    def __init__(self,
                 dot_file,
                 hidden_nns,
                 nn_to_size=None,
                 other_cond=None,
                 import_bnet=False):
        """

        Parameters
        ----------
        dot_file: str
        hidden_nns: list[str]
        nn_to_size: dict[str, int] | None
        other_cond: str | None
        """
        self.dot_file = dot_file
        self.hidden_nns = hidden_nns
        self.sample_num = 1
        if other_cond:
            assert isinstance(other_cond, str)
        self.other_cond = other_cond
        self.import_bnet = import_bnet

        self.nns, self.arrows = None, None
        self.nn_to_size = None
        self.bnet = None
        self.nn_to_nd = None
        self.ampu_pot = None
        self.full_pot = None
        self.ampu_prob_y_bar_x = None
        self.full_prob_y_bar_x = None
        if not import_bnet:
            self.nns, self.arrows = DotTool.read_dot_file(dot_file)
            self.nn_to_size = self.fill_nn_to_size(nn_to_size)
            self.bnet = self.create_random_bnet()
            self.calc_full_and_ampu_pots()
            self.calc_full_and_ampu_probs()


    def fill_nn_to_size(self, nn_to_size):
        """
        This method compiles the list of node names from the dot file
        `dot_file`. It then produces a default dict `nn_to_size1` that maps
        hidden nodes to 3 (i.e., they will have 3 states) and non-hidden ones to
        2. Then the method overrides `nn_to_size1` with the request of
        `nn_to_size` whenever they disagree. Finally, the method returns
        `nn_to_size1`

        Parameters
        ----------
        nn_to_size: dict[str, int] | None

        Returns
        -------
        dict[str, int]

        """
        nn_to_size1 = {}
        for nd in self.nns:
            nn_to_size1[nd] = 2
        for nn in self.hidden_nns:
            assert nn in self.nns, (f"hidden node '{nn}'"
                                    f" not in full node list")
            nn_to_size1[nn] = 3
        if nn_to_size:
            for nn in nn_to_size:
                if nn in nn_to_size1:
                    nn_to_size1[nn] = nn_to_size[nn]
        return nn_to_size1

    def create_random_bnet(self):

        """
        This method returns a BayesNet object whose structure is given by
        'nodes' and 'arrows'. The TPM (transition probability matrix, a.k.a.
        CPT, conditional probability table) for each node is created at random,
        with the only other constraint being that the number of states of each
        node be as specified by the input 'nn_to_size'.

        Returns
        -------
        BayesNet

        """
        found_x = False
        found_y = False
        for name in self.nns:
            if name == "x":
                found_x = True
            if name == "y":
                found_y = True
        assert found_x and found_y, \
            "can't find 'x' or 'y' in list of node names"

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

        # print("ccvv", bnet.nodes)
        for nd in bnet_nodes:
            ord_nodes = list(nd.parents) + [nd]
            # print("llkjh", ord_nodes)
            nd.potential = DiscreteCondPot(False, ord_nodes)
            nd.potential.set_to_random()
            nd.potential.normalize_self()
        # print("aadf", bnet)
        return bnet

    def randomize_these_nodes(self,
                              some_node_names):
        """
        This method randomizes (i.e., replaces by random ones) the CPT (
        Conditional Probability Tables) of the nodes in the list
        `some_node_names` in the BayesNet object bnet.

        Parameters
        ----------
        some_node_names: list[str]
            This is a partial list of node names. Normally one uses for this a
            list of nodes that are hidden.

        Returns
        -------
        None

        """
        self.sample_num += 1
        for name in some_node_names:
            nd = self.nn_to_nd[name]
            nd.potential.set_to_random()
            nd.potential.normalize_self()
        self.calc_full_and_ampu_pots()
        self.calc_full_and_ampu_probs()

    def calc_full_and_ampu_pots(self):
        """
        This method calculates the probability distribution for

        (1) the "full" OP and

        (2) the "ampu" OP. By (ampu=amputated) OP, we mean a bnet whose
        arrows entering node "x" are amputated.

        These two probability distributions are outputted as 2 Potential
        objects, `full_pot` and `dot_pot`. Remember, a Potential can be thought
        of an arbitrary function f(x,y,z) where `x,y,z` are a partial list of
        the nodes of the OP bnet. A Potential is usually used to carry either a
        joint probability distribution like P(x,y,z) or a conditional one like
        P(z| x, y).

        Returns
        -------
        None

        """

        nd_x = self.nn_to_nd['x']

        ampu_pot = None
        for name, nd in self.nn_to_nd.items():
            if nd != nd_x:
                if not ampu_pot:
                    ampu_pot = nd.potential
                else:
                    ampu_pot = ampu_pot * nd.potential
        self.ampu_pot = ampu_pot
        self.full_pot = ampu_pot * nd_x.potential

    def calc_full_and_ampu_probs(self):
        """

        Returns
        -------
        None

        """
        self.full_prob_y_bar_x = self.get_prob_y_bar_x(self.full_pot)
        self.ampu_prob_y_bar_x = self.get_prob_y_bar_x(self.ampu_pot)

    def get_prob_y_bar_x(self, in_pot):
        """
        This method takes the two Potentials `ampu_pot` and `full_pot` and
        calculates from these the two conditional probabilities
        `ampu_prob_y_bar_x`, `full_prob_y_bar_x'. The probabilities are of the
        type P(y|x) and expressed as numpy arrays. `ampu_prob_y_bar_x` equals P(
        y|do(x)).

                The analogous method `calc_ampu_and_full_prob_y_bar_x` calculates P(
        y|x). This method calculates P(y| x, z) instead. If you don't want
        the name of the extra node to be "conditioned on" to default to 'z',
        you can tell the method the name of your alternative to "z" using
        the input variable `other_cond`

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        np.array

        """
        if not self.other_cond:
            nd_x = self.nn_to_nd['x']
            nd_y = self.nn_to_nd['y']

            arr_xy = in_pot.get_new_marginal(
                [nd_x, nd_y]).pot_arr
            pot_y_bar_x = DiscreteCondPot(
                False,
                [nd_x, nd_y],
                arr_xy)
            pot_y_bar_x.normalize_self()
            return pot_y_bar_x.pot_arr
        else:
            nd_x = self.nn_to_nd['x']
            nd_y = self.nn_to_nd['y']
            nd_z = self.nn_to_nd[self.other_cond]
            arr_xzy = in_pot.get_new_marginal(
                [nd_x, nd_z, nd_y]).pot_arr
            pot_y_bar_x_z = DiscreteCondPot(
                False,
                [nd_x, nd_z, nd_y],
                arr_xzy)

            pot_y_bar_x_z.normalize_self()
            return pot_y_bar_x_z.pot_arr

    def print_full_and_ampu_prob_y_bar_x(self):
        """

        Returns
        -------
        None

        """
        if not self.other_cond:
            print()
            print(f"full P(y|x) for Bnet{self.sample_num} "
                  f"(determined from PO data):")
            pprint(self.full_prob_y_bar_x)
            print()
            print(f"amputated P(y|x) for Bnet{self.sample_num} "
                  f"(determined from RCT data):")
            pprint(self.ampu_prob_y_bar_x)
        else:
            print()
            print(f"full P(y|x, {self.other_cond}) for "
                  f"Bnet{self.sample_num} "
                  f"(determined from PO data):")
            pprint(self.full_prob_y_bar_x)
            print()
            print(f"amputated P(y|x, {self.other_cond}) for "
                  f"Bnet{self.sample_num} "
                  f"(determined from RCT data):")
            pprint(self.ampu_prob_y_bar_x)

    def print_CPTs(self):
        """

        Returns
        -------
        None

        """
        print(self.bnet)

    def draw(self, jupyter=True):
        """

        Parameters
        ----------
        jupyter: bool

        Returns
        -------
        None

        """
        DotTool.draw(self.dot_file, jupyter=jupyter)
