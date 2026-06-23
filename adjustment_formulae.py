from potentials.DiscreteCondPot import *
from graphs.BayesNet import *

"""
All the methods in this file return a conditional probability P(y|x) or P(
y|x, z) dictated by an adjustment formula (AF).

The AFs considered are

1. backdoor AF
2. frontdoor AF
3. Napkin1 AF
4. Napkin2 AF (fails to reproduce P(y|do(x))
5. Napkin3 AF (fails to reproduce P(y|do(x))
6. Napkin4 AF (fails to reproduce P(y|do(x))

1 to 5 return a P(y|x). 6 returns a P(y|x, z)

"""
  
  
def get_adj_pot_method(dot_file,
                  adj_version):
    dotf_strings = ["back-door", "front-door", "napkin"]
    adj_id_to_adj_method = {
        "back-door1": get_backdoor_adjustment_pot,
        "front-door1": get_frontdoor_adjustment_pot,
        "napkin1": get_napkin1_adjustment_pot,
        "napkin2": get_napkin2_adjustment_pot,
        "napkin3": get_napkin3_adjustment_pot,
        "napkin4": get_napkin4_adjustment_pot,
    }

    adj_method = None
    has_other_cond = False
    for dotf_str in dotf_strings:
        if dotf_str in dot_file:
            adj_id = dotf_str + str(adj_version)
            adj_method = adj_id_to_adj_method[adj_id]
            if adj_id in ["napkin4"]:
                has_other_cond = True
            break
    if not adj_method:
        assert None
    return adj_method, has_other_cond


def get_backdoor_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    nd_z = name_to_nd['z']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']
    pot_xz = in_pot.get_new_marginal([nd_x, nd_z])
    pot_z = in_pot.get_new_marginal([nd_z])
    final_pot = (in_pot / pot_xz) * pot_z
    return final_pot

def get_frontdoor_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    # nd_h = name_to_nd['h']
    nd_m = name_to_nd['m']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']
    pot_mxy = in_pot.get_new_marginal([nd_m, nd_x, nd_y])
    pot_mx = in_pot.get_new_marginal([nd_m, nd_x])
    pot_x = pot_mx.get_new_marginal([nd_x])

    pot_my = (pot_mxy * pot_x / pot_mx).get_new_marginal([nd_m, nd_y])
    final_pot = pot_my * pot_mx / pot_x
    return final_pot


def get_napkin1_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    nd_w = name_to_nd['w']
    nd_z = name_to_nd['z']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']

    pot_wzxy = in_pot.get_new_marginal([nd_w, nd_z, nd_x, nd_y])
    pot_wz = pot_wzxy.get_new_marginal([nd_w, nd_z])
    pot_w = pot_wz.get_new_marginal([nd_w])
    pot_z = pot_wz.get_new_marginal([nd_z])

    final_pot = pot_wzxy * pot_w * pot_z / pot_wz
    return final_pot



def get_napkin2_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    nd_z = name_to_nd['z']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']

    pot_zxy = in_pot.get_new_marginal([nd_z, nd_x, nd_y])
    pot_zx = pot_zxy.get_new_marginal([nd_z, nd_x])
    pot_z = pot_zx.get_new_marginal([nd_z])

    final_pot = (pot_zxy / pot_zx) * pot_z
    return final_pot



def get_napkin3_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    nd_w = name_to_nd['w']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']

    pot_wxy = in_pot.get_new_marginal([nd_w, nd_x, nd_y])
    pot_wx = pot_wxy.get_new_marginal([nd_w, nd_x])
    pot_w = pot_wx.get_new_marginal([nd_w])

    final_pot = (pot_wxy / pot_wx) * pot_w
    return final_pot



def get_napkin4_adjustment_pot(name_to_nd,  in_pot):
    """

    Parameters
    ----------
    bnet: BayesNet
    in_pot: Potential

    Returns
    -------
    np.array

    """
    nd_w = name_to_nd['w']
    nd_z = name_to_nd['z']
    nd_x = name_to_nd['x']
    nd_y = name_to_nd['y']

    pot_wzxy = in_pot.get_new_marginal([nd_w, nd_z, nd_x, nd_y])
    pot_wz = pot_wzxy.get_new_marginal([nd_w, nd_z])
    pot_w = pot_wz.get_new_marginal([nd_w])
    # print("nnmf", pot_w.pot_arr)

    final_pot = (pot_wzxy / pot_wz) * pot_w
    return final_pot