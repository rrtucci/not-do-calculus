from itertools import combinations
from more_itertools import set_partitions
from AdjCandidate import *
from AdjTester import *
from itertools import chain
def flatten(partition):
    return list(chain.from_iterable(partition))

class AdjSearcher:

    def __init__(self, bnet_sample):
        self.bnet_sample = bnet_sample
        self.num_hidden_nds = len(self.bnet_sample.hidden_nd_names)
        self.candy_partitions  = self.get_candidate_partitions()

    def get_candidate_partitions(self):
        possible_trols = [name for name in self.bnet_sample.nd_names
                          if name != "y"]

        candy_partitions = []
        for sublist in combinations(possible_trols,
                                   self.num_hidden_nds):
            for partition in set_partitions(sublist):
                candy_partitions += partition
        return candy_partitions

    def conduct_search(self):
        for candy_partition in self.candy_partitions:
            cid_to_clique = {}
            for cid in range(len(candy_partition)):
                cid_to_clique[cid] = candy_partition[cid]
            candy = AdjCandidate(self.bnet_sample,
                                 cid_to_clique)
            tester = AdjTester(self.bnet_sample, candy.get_adj_pot)
            test_result = tester.conduct_test()
            print("--------------------")
            print(candy.get_adj_str())
            if test_result:
                print("VALID adjustment formula")
            else:
                print("failed")
