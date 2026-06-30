from itertools import combinations
from more_itertools import set_partitions
from AdjCandidate import *
from AdjTester import *
from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))

class AdjSearcher:
    """
    Attributes
    ----------
    bnet_sample: BnetSample
    """

    def __init__(self, bnet_sample):
        """

        Parameters
        ----------
        bnet_sample: BnetSample
        """
        self.bnet_sample = bnet_sample

    @staticmethod
    def get_candidate_partitions(
            nd_names,
            hidden_nd_names):
        """

        Returns
        -------
        list[list[list[int]]]
            for example [ [[1,2], [3]],  [[1], [2,3]] ]
        """
        possible_trols = []
        for name in nd_names:
            if name == "y" or name in hidden_nd_names:
                continue
            else:
                possible_trols.append(name)

        num_hidden_nds = len(hidden_nd_names)

        candy_partitions = []
        if num_hidden_nds:
            for sublist in combinations(possible_trols,
                                       num_hidden_nds):
                for partition in set_partitions(sublist):
                    if len(partition)>1:
                        candy_partitions.append(partition)
        return candy_partitions


    def conduct_search(self, verbose):
        """
        verbose: bool

        Returns
        -------
        None

        """
        candy_partitions = AdjSearcher.get_candidate_partitions(
            self.bnet_sample.nd_names,
            self.bnet_sample.hidden_nd_names)

        for candy_partition in candy_partitions:
            cid_to_clique = {}
            for cid in range(len(candy_partition)):
                cid_to_clique[cid] = candy_partition[cid]
            candy = AdjCandidate(self.bnet_sample,
                                 cid_to_clique)
            tester = AdjTester(self.bnet_sample, candy.get_adj_pot)
            print("--------------------")
            passed_test = True
            # passed_test = tester.conduct_closeness_test(verbose)
            print()
            print(candy.get_adj_str())
            print()
            if passed_test:
                print("Adj formula PASSED")
            else:
                print("Adj formula FAILED")
        if not candy_partitions:
            candy = AdjCandidate(self.bnet_sample)
            tester = AdjTester(self.bnet_sample, null_adj=True)
            print("--------------------")
            passed_test = tester.conduct_closeness_test(verbose)
            print()
            print(candy.get_adj_str())
            print()
            if passed_test:
                print("Adj formula PASSED")
            else:
                print("Adj formula FAILED")

if __name__ == "__main__":

    def main1():
        nd_names = ["x", "y", "m", "z", "h"]
        hidden_nd_names = ["h"]
        cps = AdjSearcher.get_candidate_partitions(nd_names,
                                                  hidden_nd_names)
        print(cps)

    def main2():
        nd_names = ["x", "y", "m", "z", "h1", "h2"]
        hidden_nd_names = ["h1", "h2"]
        cps = AdjSearcher.get_candidate_partitions(nd_names,
                                                  hidden_nd_names)
        print(cps)

    def main3():
        nd_names = ["x", "y", "m", "z", "a", "h1", "h2", "h3"]
        hidden_nd_names = ["h1", "h2", "h3"]
        cps = AdjSearcher.get_candidate_partitions(nd_names,
                                                  hidden_nd_names)
        print(cps)

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
        bnet_sample = BnetSample(dot_file="dot_atlas/back-door.dot",
                                 hidden_nd_names=[])
        if draw:
            bnet_sample.draw(jupyter=False)
        searcher = AdjSearcher(bnet_sample)
        searcher.conduct_search(verbose)

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
        bnet_sample = BnetSample(dot_file="dot_atlas/front-door.dot",
                                 hidden_nd_names=["h"])
        if draw:
            bnet_sample.draw(jupyter=False)
        searcher = AdjSearcher(bnet_sample)
        searcher.conduct_search(verbose)

    def main_napkin(draw, verbose):
        """
        Parameters
        ----------
        draw: bool
        verbose: bool

        Returns
        -------
        None

        """
        bnet_sample = BnetSample(dot_file="dot_atlas/napkin.dot",
                                 hidden_nd_names=["u_1", "u_2"])
        if draw:
            bnet_sample.draw(jupyter=False)
        searcher = AdjSearcher(bnet_sample)
        searcher.conduct_search(verbose)

    # main_backdoor(False, False)
    # main_frontdoor(False, False)
    # main_napkin(False, False)

    main1()
    # main2()
    # main3()