class NDC_Cases:
    """
    This class is a collection of different adjustments for the bnets 
    backdoor, frontdoor and napkin. When there is more than one adjustment 
    for a bnet (e.g., napkin) the various adjustments are given an 
    adjustment version adj_version. For each adjustment, there is a method 
    in this class that returns a pot. That pot returning function is called 
    by NDC_CaseTester.


    Attributes
    ----------
    adj_pot_function: Function
        method that returns a pot. For example, adj_pot_function =
        get_backdoor_adj_pot
    adj_version: int
        adjustment version. This int is used to distinguish between several
        adjustments for the same bnet. For example, napkin has several
        adjustments.
    dot_file: str
        dot file (i.e., graphviz format) of the OP (Original Promise) bnet.
    has_other_cond: bool
        whether there is another condition. If there isn't we are
        calculating P(y|x). If there is and other_cond = 'z', we are
        calculating P(y|x, z).  For example, has_other_cond = True for napkin
        adj_version=4
    nn_to_nd: dict[str, BayesNode]
        dict mapping a nn (node name) to its nd (BayesNode)


    """

    def __init__(self,
                 nn_to_nd,
                 dot_file,
                 adj_version):
        """
        Constructor

        Parameters
        ----------
        nn_to_nd: dict[str, BayesNode]
        dot_file: str
        adj_version: int
        """
        self.nn_to_nd = nn_to_nd
        self.dot_file = dot_file
        self.adj_version = adj_version
        self.adj_pot_function = None
        self.has_other_cond = False
        self.set_adj_pot_function()

    def set_adj_pot_function(self):
        """
        This method decides from self.dot_file and self.adj_version,
        what should be the self.adj_pot_function and returns the latter.
        It also sets self.has_other_cond

        Returns
        -------
        None

        """
        dotf_strings = ["back-door", "front-door", "napkin"]
        adj_id_to_adj_pot_function = {
            "back-door1": self.get_backdoor_adj_pot,
            "front-door1": self.get_frontdoor_adj_pot,
            "napkin1": self.get_napkin1_adj_pot,
            "napkin2": self.get_napkin2_adj_pot,
            "napkin3": self.get_napkin3_adj_pot,
            "napkin4": self.get_napkin4_adj_pot,
            "napkin5": self.get_napkin5_adj_pot
        }

        adj_pot_function = None
        has_other_cond = False
        for dotf_str in dotf_strings:
            if dotf_str in self.dot_file:
                adj_id = dotf_str + str(self.adj_version)
                adj_pot_function = adj_id_to_adj_pot_function[adj_id]
                if adj_id in ["napkin4"]:
                    has_other_cond = True
                break
        if not adj_pot_function:
            assert None, "No adjustment pot function found"
        self.adj_pot_function = adj_pot_function
        self.has_other_cond = has_other_cond

    def get_backdoor_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the BACK-DOOR bnet. It returns an
        adjustment pot.
    
        Parameters
        ----------
        in_pot: Potential
    
        Returns
        -------
        Potential
        """
        nd_z = self.nn_to_nd['z']
        nd_x = self.nn_to_nd['x']

        pot_xz = in_pot.get_new_marginal([nd_x, nd_z])
        pot_z = in_pot.get_new_marginal([nd_z])
        final_pot = (in_pot / pot_xz) * pot_z
        return final_pot

    def get_frontdoor_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the FRONT-DOOR bnet. It returns an
        adjustment pot.

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        # nd_h = self.nn_to_nd['h']
        nd_m = self.nn_to_nd['m']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']
        pot_mxy = in_pot.get_new_marginal([nd_m, nd_x, nd_y])
        pot_mx = in_pot.get_new_marginal([nd_m, nd_x])
        pot_x = pot_mx.get_new_marginal([nd_x])

        pot_ym = (pot_mxy * pot_x / pot_mx).get_new_marginal([nd_y, nd_m])
        final_pot = pot_ym * pot_mx / pot_x
        return final_pot

    def get_napkin1_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the NAPKIN bnet. It returns an
        adjustment pot (adj_version=1).

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        nd_w = self.nn_to_nd['w']
        nd_z = self.nn_to_nd['z']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']

        pot_wzxy = in_pot.get_new_marginal([nd_w, nd_z, nd_x, nd_y])
        pot_wz = pot_wzxy.get_new_marginal([nd_w, nd_z])
        pot_w = pot_wz.get_new_marginal([nd_w])
        pot_z = pot_wz.get_new_marginal([nd_z])

        final_pot = pot_wzxy * pot_w * pot_z / pot_wz
        return final_pot

    def get_napkin2_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the NAPKIN bnet. It returns an
        adjustment pot (adj_version=2).

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        nd_z = self.nn_to_nd['z']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']

        pot_zxy = in_pot.get_new_marginal([nd_z, nd_x, nd_y])
        pot_zx = pot_zxy.get_new_marginal([nd_z, nd_x])
        pot_z = pot_zx.get_new_marginal([nd_z])

        final_pot = (pot_zxy / pot_zx) * pot_z
        return final_pot

    def get_napkin3_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the NAPKIN bnet. It returns an
        adjustment pot (adj_version=3).

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        nd_w = self.nn_to_nd['w']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']

        pot_wxy = in_pot.get_new_marginal([nd_w, nd_x, nd_y])
        pot_wx = pot_wxy.get_new_marginal([nd_w, nd_x])
        pot_w = pot_wx.get_new_marginal([nd_w])

        final_pot = (pot_wxy / pot_wx) * pot_w
        return final_pot

    def get_napkin4_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the NAPKIN bnet. It returns an
        adjustment pot (adj_version=4).

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        nd_w = self.nn_to_nd['w']
        nd_z = self.nn_to_nd['z']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']

        pot_wzxy = in_pot.get_new_marginal([nd_w, nd_z, nd_x, nd_y])
        pot_wz = pot_wzxy.get_new_marginal([nd_w, nd_z])
        pot_w = pot_wz.get_new_marginal([nd_w])
        # print("nnmf", pot_w.pot_arr)

        final_pot = (pot_wzxy / pot_wz) * pot_w
        return final_pot

    def get_napkin5_adj_pot(self, in_pot):
        """
        This method takes as input a pot `in_pot` (which is either a
        `full_pot` or an `ampu_pot`) for the NAPKIN bnet. It returns an
        adjustment pot (adj_version=5).

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential
        """
        nd_w = self.nn_to_nd['w']
        nd_x = self.nn_to_nd['x']
        nd_y = self.nn_to_nd['y']

        pot_wxy = in_pot.get_new_marginal([nd_w, nd_x, nd_y])
        pot_wx = pot_wxy.get_new_marginal([nd_w, nd_x])
        pot_w = pot_wx.get_new_marginal([nd_w])
        pot_yx = ((pot_wxy / pot_wx) * pot_w).get_new_marginal([nd_y, nd_x])
        final_pot = pot_yx * pot_wx
        return final_pot