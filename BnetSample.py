from potentials.DiscreteCondPot import *
from graphs.BayesNet import *
from pprint import pprint
from DotTool import *


class BnetSample:
    """
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
    hidden_nd_names: list[str]
        names of hidden nodes
    name_to_nd: dict[str, BayesNode]
    nd_names: list[str]
        example: ['a', 'b', 'c']
    nd_to_size: dict[str, int] | None
        dict mapping each node name to its size. This input need only be a
        partial list of those nodes that you don't want to have default
        values. dictionary mapping node name to its size (i.e., the number
        of values or states). In this method, `nd_to_size` must contain all
        the nodes. In all other methods in this file (for example,
        in `fill_node_to_size( )`), `nd_to_size` contains only special nodes
        which you don't want to have a default size. Default sizes are 2 for
        non-hidden nodes and 3 for hidden ones.
    other_cond: str | None
    sample_num: int

    """

    def __init__(self,
                 dot_file,
                 hidden_nd_names,
                 nd_to_size=None,
                 sample_num=1,
                 other_cond=None):
        """

        Parameters
        ----------
        dot_file: str
        hidden_nd_names: list[str]
        nd_to_size: dict[str, int] | None
        sample_num: int
        other_cond: str | None
        """
        self.dot_file = dot_file
        self.hidden_nd_names = hidden_nd_names
        self.sample_num = sample_num
        self.nd_names, self.arrows = DotTool.read_dot_file(dot_file)
        self.nd_to_size = self.fill_nd_to_size(nd_to_size)
        if other_cond:
            assert isinstance(other_cond, str)
        self.other_cond = other_cond

        self.bnet = self.create_random_bnet()
        self.name_to_nd = {name: self.bnet.get_node_named(name)
                           for name in self.nd_names}

        self.ampu_pot = None
        self.full_pot = None
        self.ampu_prob_y_bar_x = None
        self.full_prob_y_bar_x = None
        self.calc_full_and_ampu_pots()
        self.calc_full_and_ampu_probs()

    def fill_nd_to_size(self, nd_to_size):
        """
        This method compiles the list of node names from the dot file
        `dot_file`. It then produces a default dict `nd_to_size1` that maps
        hidden nodes to 3 (i.e., they will have 3 states) and non-hidden ones to
        2. Then the method overrides `nd_to_size1` with the request of
        `nd_to_size` whenever they disagree. Finally, the method returns
        `nd_to_size1`

        Parameters
        ----------
        nd_to_size: dict[str, int] | None

        Returns
        -------
        dict[str, int]

        """
        nd_to_size1 = {}
        for nd in self.nd_names:
            nd_to_size1[nd] = 2
        for nd_name in self.hidden_nd_names:
            assert nd_name in self.nd_names, (f"hidden node '{nd_name}'"
                                              f" not in full node list")
            nd_to_size1[nd_name] = 3
        if nd_to_size:
            for nd_name in nd_to_size:
                if nd_name in nd_to_size1:
                    nd_to_size1[nd_name] = nd_to_size[nd_name]
        return nd_to_size1

    def create_random_bnet(self):

        """
        This method returns a BayesNet object whose structure is given by
        'nodes' and 'arrows'. The TPM (transition probability matrix, a.k.a.
        CPT, conditional probability table) for each node is created at random,
        with the only other constraint being that the number of states of each
        node be as specified by the input 'nd_to_size'.

        Returns
        -------
        BayesNet

        """
        bnet_nodes = []
        found_x = False
        found_y = False
        for name in self.nd_names:
            if name == "x":
                found_x = True
            if name == "y":
                found_y = True
        assert found_x and found_y, \
            "can't find 'x' or 'y' in list of node names"

        for k, node_name in enumerate(self.nd_names):
            nd = BayesNode(k, name=node_name)
            nd.size = self.nd_to_size[node_name]
            bnet_nodes.append(nd)
        bnet = BayesNet(set(bnet_nodes))
        for arrow in self.arrows:
            pa_nd = bnet.get_node_named(arrow[0])
            child_nd = bnet.get_node_named(arrow[1])
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
            nd = self.bnet.get_node_named(name)
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

        nd_x = self.name_to_nd['x']

        ampu_pot = None
        for name, nd in self.name_to_nd.items():
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
            nd_x = self.name_to_nd['x']
            nd_y = self.name_to_nd['y']

            arr_xy = in_pot.get_new_marginal(
                [nd_x, nd_y]).pot_arr
            pot_y_bar_x = DiscreteCondPot(
                False,
                [nd_x, nd_y],
                arr_xy)
            pot_y_bar_x.normalize_self()
            return pot_y_bar_x.pot_arr
        else:
            nd_x = self.name_to_nd['x']
            nd_y = self.name_to_nd['y']
            nd_z = self.name_to_nd[self.other_cond]
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
            print(f"full P(y|x) for Bnet{self.sample_num}:")
            pprint(self.full_prob_y_bar_x)
            print()
            print(f"amputated P(y|x) for Bnet{self.sample_num}:"
                  f" (REQUIRES RCT)")
            pprint(self.ampu_prob_y_bar_x)
        else:
            print()
            print(f"full P(y|x, {self.other_cond}) for "
                  f"Bnet{self.sample_num}:")
            pprint(self.full_prob_y_bar_x)
            print()
            print(f"amputated P(y|x, {self.other_cond}) for "
                  f"Bnet{self.sample_num}: (REQUIRES RCT)")
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
