from NDC_BnetMaker import *

class NDC_Searcher:

    def __init__(self, bnet_maker):
        """
        Constructor

        Parameters
        ----------
        bnet_maker: NDC_BnetMaker
        """
        self.bnet_maker = bnet_maker

    def conduct_search(self, verbose):
        """
        This abstract method must be overriden by its subclasses. Its
        purpose is to tests the validity of each adjustment in a set of
        plausible ones. A plausible adjustment is one with a plausible
        substitution `subs`.


        verbose: bool
            True iff every time that a substitution is not plausible, a line
            is printed giving the substitution and saying that it's not
            plausible.

        Returns
        -------
        None

        """
        assert False

    def substitution_is_plausible(self, subs):
        """
        This abstract method must be overridden by the subclasses of this
        abstract class. The method should return True iff subs is a
        plausible substitution.

        Parameters
        ----------
        subs: list[str]

        Returns
        -------
        bool

        """