from adjustment_formulae import *
from BnetSample import *

class AdjFormulaTester:



def print_all_prob_y_bar_x(bnet_sample,
                           verbose=True,
                           adj_version=1,
                           re_randomize_hidden_nds=True):
    """
    This method and the analogous one `print_all_prob_y_bar_x_z` are the
    only ones used in the jupyter notebooks. All others are meant to be
    internal. This method prints 4 things for each bnet.
    `num_bnet_samples=2` means the default is two bnets, but it will do only
    one bnet if you input `num_bnet_samples=1`

    1. full P(y|x) for OP

    2. amputated P(y|x) for OP. Calculating this in real life requires data
    from an RCT.

    3. adjusted P(y|x) from full_pot

    4. adjusted P(y|x) from ampu_pot. Calculating this in real life requires
    data from an RCT.


    Parameters
    ----------
    dot_file: str
        the dot file (i.e., graphviz format) of the OP bnet
    hidden_nd_names: list[str]
        the names of the hidden nodes
    nd_to_size: dict[str, int]| None
        a node name to node size dict for those nodes that you don't want to
        have default sizes.
    verbose: bool
        if this is set to True, the method prints also the CPT of each node
        of the bnet.
    adj_version: int
        the adjustment formula version. For the Napkin OP, there are
        currently 4 adjustment formulae that are tested.
    num_bnet_samples: int
        number of random bnets considered. This can be either 1 or 2.

    Returns
    -------
    None

    """
    num_samples = 1
    if re_randomize_hidden_nds:
        num_samples = 2

    for k in range(num_samples):
        if k == 2:
            print("------------------------------")
            bnet_sample.randomize_these_nodes()
        print(f"Random Bnet{bnet_sample.sample_num}:")
        if verbose:
            bnet_sample.print_CPTs()
        bnet_sample.print_ampu_and_full_prob_y_bar_x()
        dotf_strings = ["back-door", "front-door", "napkin"]
        adj_id_to_adj_method = {
            "back-door1": get_backdoor_adjustment_prob,
            "front-door1": get_frontdoor_adjustment_prob,
            "napkin1": get_napkin1_adjustment_prob,
            "napkin2": get_napkin2_adjustment_prob,
            "napkin3": get_napkin3_adjustment_prob}
        adj_method = None
        for dotf_str in dotf_strings:
            if dotf_str in bnet_sample.dot_file:
                adj_id = dotf_str + str(adj_version)
                adj_method = adj_id_to_adj_method[adj_id]
                break
        if adj_method:
            print()
            print(f"adjusted P(y|x) from full_pot for "
                  f"Bnet{bnet_sample.sample_num}:")
            pprint(adj_method(bnet_sample.name_to_nd, bnet_sample.full_pot))
            print()
            print(f"adjusted P(y|x) from ampu_pot for "
                  f"Bnet{bnet_sample.sample_num}:"
                  f"(REQUIRES RCT)")
            pprint(adj_method(bnet_sample.name_to_nd, bnet_sample.ampu_pot))


def print_all_prob_y_bar_x_z(dot_file,
                             hidden_nd_names,
                             other_cond,
                             nd_to_size=None,
                             verbose=True,
                             adj_version=1,
                             num_bnet_samples=2):
    """
    The analogous method `print_all_prob_y_bar_x` prints 4 probabilities P(
    y|x). This method prints 4 probabilities P(y| x, z) instead.

    Parameters
    ----------
    dot_file: str
    hidden_nd_names: list[str]
    other_cond: str
    nd_to_size: list[str, int]
    verbose: bool
    adj_version: int
    num_bnet_samples: int

    Returns
    -------
    None

    """
    assert isinstance(other_cond, str)
    nd_to_size = fill_nd_to_size(dot_file, hidden_nd_names, nd_to_size)
    nodes, arrows = DotTool.read_dot_file(dot_file)

    bnet = create_random_bnet(
        nodes,
        arrows,
        nd_to_size)

    if num_bnet_samples == 1:
        bnet_strings = ["bnet1"]
    else:
        bnet_strings = ["bnet1", "bnet2"]
    for bnet_str in bnet_strings:
        if bnet_str == "bnet2":
            print("--------------Now randomizing hidden nodes of bnet1")
            randomize_these_nodes(bnet, hidden_nd_names)
        print(f"Random {bnet_str}:")
        if verbose:
            print(bnet)
        ampu_pot, full_pot = calc_ampu_and_full_pots(bnet)
        ampu_prob_y_bar_x_z, full_prob_y_bar_x_z = \
            calc_ampu_and_full_prob_y_bar_x_z(
                bnet, ampu_pot, full_pot, other_cond)
        print()
        print(f"full P(y|x, z) for {bnet_str}:")
        pprint(full_prob_y_bar_x_z)
        print()
        print(f"amputated P(y|x, z) for {bnet_str}: (REQUIRES RCT)")
        pprint(ampu_prob_y_bar_x_z)
        dotf_strings = ["napkin"]
        adj_id_to_adj_method = {
            "napkin4": get_napkin4_adjustment_prob}
        adj_method = None
        for dotf_str in dotf_strings:
            if dotf_str in dot_file:
                adj_id = dotf_str + str(adj_version)
                adj_method = adj_id_to_adj_method[adj_id]
                break
        if adj_method:
            print()
            print(f"adjusted P(y|x, "
                  f"{other_cond}) from full_pot for {bnet_str}:")
            pprint(adj_method(bnet, full_pot))
            print()
            print(f"adjusted P(y|x, "
                  f"{other_cond}) from ampu_pot for {bnet_str}:"
                  f"(REQUIRES RCT)")
            pprint(adj_method(bnet, ampu_pot))


if __name__ == "__main__":
    def main_backdoor(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x(dot_file="dot_atlas/back-door.dot",
                               hidden_nd_names=[],
                               verbose=verbose)


    def main_frontdoor(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x(dot_file="dot_atlas/front-door.dot",
                               hidden_nd_names=["h"],
                               verbose=verbose)


    def main_napkin1(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"],
                               adj_version=1,
                               verbose=verbose)


    def main_napkin2(draw, verbose):
        """     
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"],
                               adj_version=2,
                               verbose=verbose)


    def main_napkin3(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x(dot_file="dot_atlas/napkin.dot",
                               hidden_nd_names=["u_1", "u_2"],
                               adj_version=3,
                               verbose=verbose)


    def main_napkin4(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        print_all_prob_y_bar_x_z(dot_file="dot_atlas/napkin.dot",
                                 hidden_nd_names=["u_1", "u_2"],
                                 other_cond="z",
                                 nd_to_size={"z": 3},
                                 adj_version=4,
                                 verbose=verbose)


    # main_backdoor(False, False)
    # main_frontdoor(False, False)
    # main_napkin1(False, False)
    # main_napkin2(False, False)
    main_napkin3(False, False)
    # main_napkin6(False, False)
