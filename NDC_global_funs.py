def get_nn_to_parents(arrows, nns):
    """
    This method returns a dict mapping each nn to the list of names
    of its parents.

    Parameters
    ----------
    arrows: list[tuple(str, str)]
        list of arrows. Example of arrow: ["a", "b"] This represents a->b
    nns: list[str]
        all node names.

    Returns
    -------
    dict[str, list[str]]

    """
    # nn = node name
    nn_to_parents = {nn: [] for nn in nns}
    for arrow in arrows:
        pa, child = arrow
        nn_to_parents[child].append(pa)
    return nn_to_parents


def bnet_has_x_parent_that_is_hidden(arrows, hidden_nns):
    """
    This method returns True iff there is at least one arrow pointing from a
    hidden node to the "x" node.

    Parameters
    ----------
    arrows: list[tuple(str, str)]
    hidden_nns: list[str]

    Returns
    -------
    bool

    """
    for arrow in arrows:
        if arrow[1] == "x" and arrow[0] in hidden_nns:
            return True
    return False


def substitution_is_plausible(nn_to_parents, nn_to_sub):
    """
    This method returns True iff nn_to_sub is a plausible substitution.

    Parameters
    ----------
    nn_to_parents: dict[str, list[str]]
        dict mapping all nn to a list of names of its parents
    nn_to_sub: dict[str, str]
        dict mapping all nn to their substitution names. All nn that are
        not hidden are mapped to themselves.

    Returns
    -------
    bool

    """
    plausible = True
    for nn, parents in nn_to_parents.items():
        sub_parents = [nn_to_sub[nn] for nn in parents]
        # print("czvb, nn, parents, sub_parents", nn, parents, sub_parents)
        if len(sub_parents) != len(set(sub_parents)):
            plausible = False
            break
    # print("xxcv", "plausible", plausible)
    # print()
    return plausible


def get_nn_to_sub(nns, hidden_nns, subs):
    """
    This method returns a dict mapping every nn to its substitute str. If nn
    has no substitute because its a non-hidden (observed node), then nn is
    mapped to itself.

    Parameters
    ----------
    nns: list[str]
        list of all node names
    hidden_nns: list[str]
        list of hidden node names
    subs: list[str]
        list of substitutes  for hidden_nns. subs[k] is the substitute
        for hidden_nns[k].

    Returns
    -------
    dict[str, str]

    """
    nn_to_sub = \
        {nn: nn for nn in nns}
    for k in range(len(hidden_nns)):
        nn_to_sub[hidden_nns[k]] = subs[k]
    return nn_to_sub
