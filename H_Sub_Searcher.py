from itertools import combinations
from itertools import permutations


def get_hidden_nd_to_hosts(hidden_nds, nd_to_parents):
    hidden_nd_to_hosts = {h_nd:[] for h_nd in hidden_nds}
    nds = nd_to_parents.keys()
    for h_nd in hidden_nds:
        for nd in nds:
            if h_nd == nd or h_nd in nd_to_parents[nd]:
                hidden_nd_to_hosts[h_nd].append(nd)
    return hidden_nd_to_hosts

def good_sub(h_nd_to_sub, nd_to_parents, hidden_nds):
    new_nd_to_parents = {}
    for nd, parents in nd_to_parents.items():
        new_parents = []
        if nd != "x":
            for pa in parents:
                for h_nd in hidden_nds:
                    if pa == h_nd:
                        new_parents.append(h_nd_to_sub[pa]+"$")
                    else:
                        new_parents.append(pa)
            new_nd_to_parents[nd]= new_parents

    dollar_nd_to_parents = {}
    for nd, parents in new_nd_to_parents:
        if nd in hidden_nds:
            dollar_nd_to_parents[h_nd_to_sub[nd]+"$"]= parents
        else:
            dollar_nd_to_parents[nd]=parents



    dollar_nd_to_valid = {}
    for nd, parents in dollar_nd_to_parents.items():
        family = strip_dollar(parents + [nd])
        if len(family) != len(set(family)):
            dollar_nd_to_valid[nd] = False
        else:
            dollar_nd_to_valid[nd] = True
    return dollar_nd_to_parents, dollar_nd_to_valid

def strip_dollar(li):
    new_li = []
    for x in li:
        new_li.append(x.replace("$", ""))
    return new_li









def get_viable_subs(nds, hidden_nd_to_hosts):
    hidden_nds = hidden_nd_to_hosts.keys()
    num_hidden_nds = len(hidden_nds)
    possible_subs = []
    if num_hidden_nds:
        for sublist in combinations(nds, num_hidden_nds):
            for perm in permutations(sublist):
                if
                    possible_subs.append(perm)





