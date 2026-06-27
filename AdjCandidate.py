from BnetSample import *


class AdjCandidate:

    def __init__(self,
                 bnet_sample,
                 cid_to_clique):
        """
        cid_to_clique = clique id to clique

        Parameters
        ----------
        bnet_sample: BnetSample
        controls: list[str]
        cid_to_clique: dict[int, list[int]]
        """
        self.bnet_sample = bnet_sample
        self.cid_to_clique = cid_to_clique

        self.cid_to_clique_nds = {}
        controls = []
        for cid, clique in cid_to_clique:
            controls += clique
            self.cid_to_clique_nds[cid] = \
                [bnet_sample.name_to_nd[name] for name in clique]
        self.controls = controls
        self.control_nds = [bnet_sample.name_to_nd[name] for name in
                            controls]

    def get_adj_str(self):
        """

        Returns
        -------
        str

        """
        str1 = r"\frac{1}{\sum_y num}\sum_{"
        for name in self.controls:
            str1 += name + ", "
        str1 = str1[-2] + r"}P(x, y|"
        for name in self.controls:
            str1 += name + ", "
        str1 = str1[-2] + r")"
        for cid, clique in self.cid_to_clique:
            str1 += r"P("
            for name in clique:
                str1 += name + ", "
            str1 = str1[-2] + r")"

        return str1

    def get_adj_pot(self, in_pot):
        """

        Parameters
        ----------
        in_pot: Potential

        Returns
        -------
        Potential

        """
        nd_x = self.bnet_sample.name_to_nd["x"]
        nd_y = self.bnet_sample.name_to_nd["y"]
        xy_control_nds = [nd_x, nd_y] + self.control_nds
        pot_xy = in_pot.get_new_marginal(xy_control_nds)
        pot_controls = in_pot.get_new_marginal(self.control_nds)
        cid_to_pot = {}
        for cid, clique_nds in self.cid_to_clique_nds.items():
            cid_to_pot[cid] = in_pot.get_new_marginal(clique_nds)

        final_pot = pot_xy / pot_controls
        for cid, pot in cid_to_pot.items():
            final_pot = final_pot * pot

        return final_pot
