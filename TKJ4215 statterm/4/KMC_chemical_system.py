import numpy as np
from random import uniform
import matplotlib.pyplot as plt #Will be used to create the relevant plots
from typing import List, Dict, Union


class Substance:

    def __init__(self, name: str, amount: int = 1):
        """
        Class to keep track of substances.

        Equality is  kept track of ONLY by name, and NOT amount. 

        Can be multiplied by integers, which returns a new substance object with the integer as amount
        """
        self.name = name
        self.amount = amount

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __str__(self):
        return str(self.amount) + self.name if self.amount > 1 else self.name

    def __mul__(self, other):
        # only works for int
        if isinstance(other, int):
            return Substance(self.name, other)
        else:
            raise TypeError("Unsupported operand. Supported operands are \"int\"")
    
    def __rmul__(self, other):
        return self * other
    

class Reaction:

    def __init__(self, reactants: List[Substance], products: List[Substance], kinetic_forward: float, kinetic_reverse: float):
        """
        Class to handle reactions. It's really just a data container. 

        Implements the __str__methos, so it looks nice when printing

        Args:
            reactants (List[Substance]): List of reactants
            products (List[Substance]): List of products
            kinetic_forward (float): rate coefficient for the forward reaction
            kinetic_reverse (float): rate coefficient for the backwards reaction
        """
        self._reactants = reactants
        self._products = products
        self._k_f = kinetic_forward
        self._k_r = kinetic_reverse
    
    def get_k_f(self) -> float:
        return self._k_f
    
    def get_k_r(self) -> float:
        return self._k_r
    
    def get_K(self) -> float:
        return self._k_f / self._k_r


    def get_reactants(self) -> List[Substance]:
        """return a copy of the reactants

        Returns:
            List[str]
        """
        return self._reactants.copy()
    

    def get_products(self) -> List[Substance]:
        """return a copy of the products

        Returns:
            List[str]
        """
        return self._products.copy()
    

    def get_substances(self) -> List[Substance]:
        """return a copy of all substances in the reaction

        Returns:
            List[str]
        """
        return self.get_products() + self.get_reactants()
    

    def is_reactant(self, substance: Substance) -> bool:
        """return True if the substance is a reactant in the reaction

        Args:
            substance (str): substance to check. Case-sentitive.

        Returns:
            bool
        """
        return substance in self._reactants


    def is_product(self, substance: Substance) -> bool:
        """return True if the substance is a product in the reaction

        Args:
            substance (str): substance to check. Case-sentitive.

        Returns:
            bool
        """
        return substance in self._products


    def __eq__(self, other):
        return self.get_substances() == other.get_substances() and self._k_r == other._k_r and self._k_f == other._k_f


    def __str__(self):
        res = ""
        for s in self._reactants:
            res += str(s) + " + "
        res =  res[:-2] + "<=> "
        for s in self._products:
            res += str(s) + " + "
        return res[:-3]


class System:

    def __init__(self, volume: float = 1):
        """Class to keep track of multiple reactions, and calculate how the amount of substances vary over time.

        Add reactions with `add_reaction`,

        Set substance amount with `set_amount`,

        Calculate the behaviour with `calculate`,

        Plot the result with `plot_data`

        See each functions documentation for more info.

        Args:
            volume (float, optional ): The volume of the system. Defaults to 1
        """
        self._V = volume
        self._reactions = list()
        self._substances = dict() # {Substance: int}
        
    
    def get_state(self) -> Dict[Substance, int]:
        """return a copy of the state of the system

        Returns:
            Dict[Substance, int]: dictionary where the key of a substance returns the amount of that substance
        """
        return self._substances.copy()

    
    def get_reactions(self) -> List[Reaction]:
        """returns a copy of the reactions

        Returns:
            List[Reaction]
        """
        return self._reactions.copy()


    def add_reaction(self, reaction: Reaction) -> None:
        """add a reaction to the system

        Args:
            reaction (Reaction): the (initialized) reaction to be added

        Raises:
            KeyError: if the reaction is already in the system
        """
        if reaction not in self._reactions:
            self._reactions.append(reaction)
            for substance in reaction.get_substances():
                if substance not in self._substances.keys():
                    self._substances[substance] = 0
        else:
            raise KeyError("Reaction already in the system")


    def set_amount(self, substance: str, amount: int) -> None:
        """set the amount of a substance in the system

        Args:
            substance (str): substance to set
            amount (int): amount to set it to

        Raises:
            KeyError: if the substance is not in the system
        """
        try:
            self._substances[substance] = amount
        except KeyError:
            raise KeyError("Substance not in system")
    

    def _get_forward_rate(self, reaction: Reaction) -> float:
        """return the forward rate of a given reaction

        Args:
            reaction (Reaction): the reaction to get a forward rate for

        Raises:
            KeyError: if the reaction is not in the system

        Returns:
            float
        """

        if reaction not in self._reactions:
            raise KeyError("Reaction not part of system")

        res = reaction.get_k_f()
        for reactant in reaction.get_reactants():
            res *= self._substances[reactant] / self._V
        return res
    

    def _get_reverse_rate(self, reaction: Reaction) -> float:
        """return the reverse rate of a given reaction

        Args:
            reaction (Reaction): the reaction to get a forward rate for

        Raises:
            KeyError: if the reaction is not in the system

        Returns:
            float
        """
        if reaction not in self._reactions:
            raise KeyError("Reaction not part of system")

        res = reaction.get_k_r()
        for product in reaction.get_products():
            res *= self._substances[product] / self._V
        return res


    def _get_forward_probability(self, reaction: Reaction) -> float:
        """get the probability of a reaction happening

        Args:
            reaction (Reaction): reaction to check
        
        Raises:
            KeyError: if the reaction is not in the system

        Returns:
            float: probability of the forward reaction happening
        """
        rf = self._get_forward_rate(reaction)
        rb = self._get_reverse_rate(reaction)
        return rf / (rf + rb)
    

    def _get_reverse_probability(self, reaction: Reaction) -> float:
        """get the probability of a reaction being reversed

        Args:
            reaction (Reaction): reaction to check
        
        Raises:
            KeyError: if the reaction is not in the system

        Returns:
            float: probability of the reverse reaction happening
        """
        return 1 - self._get_forward_probability(reaction)
    

    def _update_all(self) -> np.array:
        """
        update the system state by comparing the random number with reaction probabilities

        returns:
            np.array: timestep until next reaction, same indices as self._reactions
        """
        random_num = uniform(0,1)
        
        # first, get all directions of reactions
        signs = [1 if random_num < self._get_forward_probability(reaction) else -1 for reaction in self._reactions]

        # then, update the amounts. Done separately to calculate each probability for the same particle amounts
        for i, reaction in enumerate(self._reactions):
            sign = signs[i]
            for reactant in reaction.get_reactants():
                self._substances[reactant] -= reactant.amount * sign
            for product in reaction.get_products():
                self._substances[product] += product.amount * sign

        log_p = np.log(random_num)
        return np.array([-log_p / (self._get_forward_rate(reaction) + self._get_reverse_rate(reaction)) for reaction in self._reactions])
    

    def _update_single(self, reaction: Reaction) -> float:
        """update the system state by comparing the random number with the reaction probability

        Args:
            reaction (Reaction): reaction to calculate for

        Returns:
            float: time until next reaction

        Raises:
            KeyError: if reaction is not in the system
        """
        random_num = uniform(0,1)

        if reaction not in self._reactions:
            raise KeyError("Reaction not part of system")
        
        sign = 1 if random_num < self._get_forward_probability(reaction) else -1
        for reactant in reaction.get_reactants():
            self._substances[reactant] -= reactant.amount * sign
        for product in reaction.get_products():
            self._substances[product] += product.amount * sign

        return -np.log(random_num) / (self._get_forward_rate(reaction) + self._get_reverse_rate(reaction))

    def _is_equilibrium(self, verbose: bool = False) -> bool:
        """returns True if the system is in equilibrium

        Returns:
            bool
        """
        # max error allowed, as a ratio
        max_error = 0.01
        Qs = []
        for reaction in self._reactions:
            reactants = reaction.get_reactants()
            products = reaction.get_products()

            Q_num = 1
            for substance in products:
                Q_num *= (self._substances[substance] / self._V) ** substance.amount

            Q_den = 1
            for substance in reactants:
                Q_den *= (self._substances[substance] / self._V) ** substance.amount
            
            if Q_den == 0:
                continue

            Q = Q_num / Q_den
            K = reaction.get_K()
            
            print(Q, K, abs(1 - Q / K)) if verbose else None
            Qs.append(Q)

        for Q in Qs:
            if abs(1 - Q / K) > max_error:
                return False

        return True


    def calculate(self, save_timestep: float, end_time: float) -> Union[Dict[Substance, List[int]], np.array]:
        # setup
        data = [self.get_state()]
        timesteps = np.array([0])
        time = 0
        update_times = self._update_all()
        
        iters = 0
        # main loop
        while time < end_time:
            iters += 1
            # find the time to wait
            min_idle = min(update_times)

            # find the first reaction that will happen
            i = update_times.tolist().index(min_idle)

            # do the reaction
            add_time = self._update_single(self._reactions[i])

            # update the times
            update_times -= min_idle
            update_times[i] += add_time
            time += min_idle
            print(max(update_times))
            # check if we should save the state
            if (time - timesteps[-1]) >= save_timestep:
                data.append(self.get_state())
                timesteps = np.append(timesteps, [time])

            if self._is_equilibrium():
                print(f"Equilibrium reached at time = {time}, which is {round(100*time/end_time, 1)}% of the requested timeframe")
                data.append(self.get_state())
                timesteps = np.append(timesteps, [time])
                break
        
        # reformat the data, to be a dict: {Substance: list(amounts)}
        reformat = {}
        for substance in data[0].keys():
            reformat[substance] = [d[substance] for d in data]

        print(iters, "iterations")
        return reformat, timesteps


    @staticmethod
    def plot_data(data: Dict[Substance, List[int]], timesteps: np.array) -> None:
        legend = []
        for substance in data.keys():
            plt.plot(timesteps, data[substance])
            legend.append(substance.name)
        plt.xlabel("Time")
        plt.xscale("log")
        plt.ylabel("Amount")
        plt.legend(legend)
        plt.show()


##################################################
##      Here we define our specific system      ##
##################################################

A = Substance("A")
B = Substance("B")
C = Substance("C")
D = Substance("D")

reac1 = Reaction([A, B], [C], kinetic_forward=1, kinetic_reverse=0.01)
print(reac1)

reac2 = Reaction([C, D], [A], kinetic_forward=1, kinetic_reverse= 0.1)
print(reac2)

simple_reac = Reaction([A], [B], 1, 0.51)

sys = System()
sys.add_reaction(reac1)
sys.add_reaction(reac2)
sys.add_reaction(simple_reac)
sys.set_amount(A, 1000)
sys.set_amount(B, 500)
# C is at 0, as is default
sys.set_amount(D, 1000)

data, timesteps = sys.calculate(save_timestep= 0.00001, end_time=15)
avg_data = {}
for substance in data.keys():
            tmp = np.array(data[substance])
            avg_data[substance] = [np.average(tmp[max(0, i-5):min(i+5, len(tmp))]) for i in range(len(tmp))]


sys.plot_data(avg_data, timesteps)
