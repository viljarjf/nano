import sys, pygame
from numpy.random import randint
import numpy as np
import numba
from matplotlib import pyplot as plt

from reaction_system import Substance, Reaction, System
from typing import Any, Tuple

# convert tuple of ints to a single 24bit int
rgb_to_int = lambda r,g,b: (2**16 * r) ^ (2**8 * g) ^ (2**0 * b)


class AnimatedSubstance(Substance):

    def __init__(self, name: str, color: Tuple[int, int, int], amount: int = 1):
        self.color = color
        super().__init__(name, amount)
    
    # overload to create correct type
    def __mul__(self, other: int):
        # only works for int
        if isinstance(other, int):
            return AnimatedSubstance(self.name, self.color, other)
        else:
            raise TypeError("Unsupported operand. Supported operands are \"int\"")


class AnimatedSystem(System):

    # static 
    VOID_SUBSTANCE = AnimatedSubstance("Void", (0,0,0))

    def __init__(self, height, width):
        # first, initialize the pygame stuff
        self._SIZE = self._WIDTH, self._HEIGHT = width, height

        self._keybinds = dict()

        self._brush_color = rgb_to_int(255, 255, 255) # default to white
        self._OFF_COLOR = rgb_to_int(0, 0, 0)

        self._radius = 10

        self._entropy_arr = np.zeros((10000), dtype = np.float32)
        
        # second, compile the numba functions 
        @numba.jit(numba.int32[:,:](numba.int32[:,:]), nopython = True)
        def inert(arr):
            # (0, 0, 0) -> 0
            black = 0

            # iterate in random order. 
            # If done in order, the particles tend to move towards (0,0)
            iter1 = np.arange(1, height-1)
            iter2 = np.arange(1, width-1)
            np.random.shuffle(iter1)
            np.random.shuffle(iter2)

            # iterate over all particles
            for i in iter1:
                for j in iter2:
                    if arr[i,j] != black:
                        # if a lattice point is occupied, try moving it in a random direction
                        n = np.random.randint(4)
                        if n == 0:
                            if arr[i-1, j] == black:
                                arr[i-1, j] = arr[i, j]
                                arr[i, j] = black
                        elif n == 1:
                            if arr[i+1, j] == black:
                                arr[i+1, j] = arr[i, j]
                                arr[i, j] = black
                        elif n == 2:
                            if arr[i, j-1] == black:
                                arr[i, j-1] = arr[i, j]
                                arr[i, j] = black
                        else:
                            if arr[i, j+1] == black:
                                arr[i, j+1] = arr[i, j]
                                arr[i, j] = black
            return arr

        optional_int = numba.optional(numba.int64)
        @numba.jit(numba.int32[:,:](numba.int32[:,:], numba.int64, numba.int64, numba.float64, optional_int, optional_int), nopython = True)
        def react(arr, in_1: int, out_1: int, p_f: float, in_2: int = None, out_2: int = None):
            if in_2 is None:
                in_2 = in_1
            if out_2 is None:
                out_2 = out_1
            # iterate in random order. 
            # If done in order, the particles tend to move towards (0,0)
            iter1 = np.arange(1, height-1)
            iter2 = np.arange(1, width-1)
            np.random.shuffle(iter1)
            np.random.shuffle(iter2)

            # iterate over all particles
            for i in iter1: 
                for j in iter2:
                    if arr[i,j] == in_1:
                        # if a lattice point is occupied, check a random direction
                        n = np.random.randint(4)
                        # if the random direction is occupied by the correct substance, do the reaction
                        if n == 0:
                            if arr[i-1, j] == in_2:
                                if np.random.random() < p_f:
                                    arr[i-1, j] = out_1
                                    arr[i, j] = out_2
                        elif n == 1:
                            if arr[i+1, j] == in_2:
                                if np.random.random() < p_f:
                                    arr[i+1, j] = out_1
                                    arr[i, j] = out_2
                        elif n == 2:
                            if arr[i, j-1] == in_2:
                                if np.random.random() < p_f:
                                    arr[i, j-1] = out_1
                                    arr[i, j] = out_2
                        else:
                            if arr[i, j+1] == in_2:
                                if np.random.random() < p_f:
                                    arr[i, j+1] = out_1
                                    arr[i, j] = out_2
                    elif arr[i,j] == in_2:
                        # also check the other reactant
                        n = np.random.randint(4)
                        if n == 0:
                            if arr[i-1, j] == in_1:
                                if np.random.random() < p_f:
                                    arr[i-1, j] = out_1
                                    arr[i, j] = out_2
                        elif n == 1:
                            if arr[i+1, j] == in_1:
                                if np.random.random() < p_f:
                                    arr[i+1, j] = out_1
                                    arr[i, j] = out_2
                        elif n == 2:
                            if arr[i, j-1] == in_1:
                                if np.random.random() < p_f:
                                    arr[i, j-1] = out_1
                                    arr[i, j] = out_2
                        else:
                            if arr[i, j+1] == in_1:
                                if np.random.random() < p_f:
                                    arr[i, j+1] = out_1
                                    arr[i, j] = out_2
                    # also check for the reverse reaction
                    elif arr[i,j] == out_1:
                        n = np.random.randint(4)
                        if n == 0:
                            if arr[i-1, j] == out_2:
                                if np.random.random() > p_f:
                                    arr[i-1, j] = in_1
                                    arr[i, j] = in_2
                        elif n == 1:
                            if arr[i+1, j] == out_2:
                                if np.random.random() > p_f:
                                    arr[i+1, j] = in_1
                                    arr[i, j] = in_2
                        elif n == 2:
                            if arr[i, j-1] == out_2:
                                if np.random.random() > p_f:
                                    arr[i, j-1] = in_1
                                    arr[i, j] = in_2
                        else:
                            if arr[i, j+1] == out_2:
                                if np.random.random() > p_f:
                                    arr[i, j+1] = in_1
                                    arr[i, j] = in_2
                    elif arr[i,j] == out_2:
                        # also check the other product
                        n = np.random.randint(4)
                        if n == 0:
                            if arr[i-1, j] == out_1:
                                if np.random.random() > p_f:
                                    arr[i-1, j] = in_1
                                    arr[i, j] = in_2
                        elif n == 1:
                            if arr[i+1, j] == out_1:
                                if np.random.random() > p_f:
                                    arr[i+1, j] = in_1
                                    arr[i, j] = in_2
                        elif n == 2:
                            if arr[i, j-1] == out_1:
                                if np.random.random() > p_f:
                                    arr[i, j-1] = in_1
                                    arr[i, j] = in_2
                        else:
                            if arr[i, j+1] == out_1:
                                if np.random.random() > p_f:
                                    arr[i, j+1] = in_1
                                    arr[i, j] = in_2
                                    
            return arr

        # entropy
        @numba.jit(numba.float64(numba.int32[:,:]), nopython = True)
        def entropy(arr) -> float:
            black = 0
            arr_copy = arr.copy()
            x_arr = arr_copy[0, :]
            for y in range(arr.shape[0]):
                x_arr |= arr_copy[y, :]
            x_max = np.max(np.nonzero(x_arr)[0])
            x_min = np.min(np.nonzero(x_arr)[0])

            y_arr = arr_copy[:, 0]
            for x in range(arr.shape[1]):
                y_arr |= arr_copy[:, x]
            y_max = np.max(np.nonzero(y_arr.flatten())[0])
            y_min = np.min(np.nonzero(y_arr.flatten())[0])

            x_diff = x_max - x_min
            y_diff = y_max - y_min

            M = y_diff*x_diff
            N = np.count_nonzero(arr != black)

            # use stirling's
            return M*np.log(M) - M -(N*np.log(N) - N + (M-N)*np.log(M-N) -(M-N))

        # compile
        a = inert(np.zeros(self._SIZE, dtype = np.int32))
        a = react(a, 1, 2, 0.5, 3, 4)
        a = entropy(np.zeros((3,3), dtype = np.int32)+1)
        del a

        self._update_array_inert = inert
        self._update_array_reaction = react
        self._calculate_entropy = entropy

        # last, run the parent constructor
        v = height * width
        super().__init__(v)
        
    
    def bind_key(self, key: str, substance: AnimatedSubstance) -> None:
        """bind a key to a substance. 
        when pressing the key, the brush will add the selected substance.

        Rebinds the key if it is already bound.

        Bind a key to "None" to unbind it.

        Args:
            key (str): key, e.g. "3" or "a"
            substance (AnimatedSubstance): corresponding substance

        Raises:
            KeyError: if the substance is not in the system
        """

        if substance not in self._substances:
            raise KeyError("Can't bind key: substance not in the system")
        
        # unbind other keys
        if key is not None:
            for k, v in self._keybinds.items():
                if v == key:
                    self._keybinds[k] = None

        self._keybinds[substance] = key


    @staticmethod
    def get_particle_count(arr: np.array, substance: AnimatedSubstance) -> int:
        return np.count_nonzero(arr == rgb_to_int(*substance.color))


    # overload this func, since this is used for individual reactions here
    def _get_forward_probability(self, reaction: Reaction) -> float:
        return reaction.get_k_f() / (reaction.get_k_f() + reaction.get_k_r())
    
    
    # overload add_reaction, since reactions NEED two reactants and two products
    def add_reaction(self, reaction: Reaction) -> None:
        if len(reactant := reaction.get_reactants()) != 2:
            if reactant[0].amount == 2:
                reaction._reactants.append(self.VOID_SUBSTANCE)
            else:
                raise ValueError("Invalid reaction. Reaction must have two reactants and two products")
        elif len(product := reaction.get_products()) != 2:
            if product[0].amount == 2:
                reaction._products.append(self.VOID_SUBSTANCE)
            else:
                raise ValueError("Invalid reaction. Reaction must have two reactants and two products")
        
        
        # basically a copy of super().add_reaction, but we DON'T add void to self._substances
        if reaction not in self._reactions:
            self._reactions.append(reaction)
            for substance in reaction.get_substances():
                if substance not in self._substances.keys() and substance is not self.VOID_SUBSTANCE:
                    self._substances[substance] = 0
        else:
            raise KeyError("Reaction already in the system")
        

    def animate(self):
        """Start the animation. This is a while-loop, and will not stop unless the window is closed.

        An entropy-plot (first 10k steps) is shown when the window is closed.
        """
        pygame.init()
        self._SCREEN = pygame.display.set_mode(self._SIZE)
        draw = True
        i = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self._entropy_arr = self._entropy_arr[self._entropy_arr > 0]
                    plt.plot(np.arange(len(self._entropy_arr)), self._entropy_arr)
                    plt.show()
                    sys.exit()   

                elif event.type == pygame.KEYDOWN:
                    
                    # change colors
                    for key, val in self._keybinds.items():
                        if event.unicode == val:
                            self._brush_color = rgb_to_int(*key.color)                    
                    
                    # change brush size
                    if event.unicode == "+":
                        self._radius += 3
                    elif event.unicode == "-":
                        self._radius -= 3
                        self._radius = 1 if self._radius < 0 else self._radius

                    # pause
                    elif event.unicode == " ":
                        draw = not draw
                    
                    # reset
                    elif event.key == 8:
                        pygame.surfarray.blit_array(self._SCREEN, np.zeros(self._SIZE))
                        pygame.display.flip()
                        continue

            if pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(self._SCREEN, self._brush_color, (pygame.mouse.get_pos()), self._radius)


            if draw:    
                arr = pygame.surfarray.array2d(self._SCREEN)
                # first move the particles
                arr = self._update_array_inert(arr)
                
                # then do the reactions
                for reaction in self._reactions:
                    # use the private variable for speed
                    # (instead of get_reactants)
                    a, b = reaction._reactants
                    c, d = reaction._products
                    arr = self._update_array_reaction(
                        arr, 
                        rgb_to_int(*a.color), 
                        rgb_to_int(*c.color), 
                        self._get_forward_probability(reaction),
                        None if b is self.VOID_SUBSTANCE else rgb_to_int(*b.color),
                        None if d is self.VOID_SUBSTANCE else rgb_to_int(*d.color)
                    )

                # calculate local entropy
                if np.count_nonzero(arr != 0) and i < 10000:
                    self._entropy_arr[i] = self._calculate_entropy(arr)
                    i += 1
                
                pygame.surfarray.blit_array(self._SCREEN, arr)

                # update particle amounts
                for substance in self._substances:
                    self._substances[substance] = self.get_particle_count(arr, substance)

            pygame.display.flip()


##################################################
##      Here we define our specific system      ##
##################################################

if __name__ == "__main__":
    
    # define our substances
    A = AnimatedSubstance("A", (255, 0, 0))
    B = AnimatedSubstance("B", (0, 255, 0))
    C = AnimatedSubstance("C", (255, 255, 0))
    D = AnimatedSubstance("D", (0, 255, 255))

    # define the reactions
    reac1 = Reaction([A, B], [C, D], kinetic_forward=1, kinetic_reverse=0.01)
    print(reac1)

    #reac2 = Reaction([C, D], [2*A], kinetic_forward=1, kinetic_reverse= 0.5)
    #print(reac2)

    # put the reactions in a system
    anisys = AnimatedSystem(800, 800)
    anisys.add_reaction(reac1)
    #anisys.add_reaction(reac2)

    # bind keys to be able to add substance to the system
    anisys.bind_key("1", A)
    anisys.bind_key("2", B)
    anisys.bind_key("3", C)
    anisys.bind_key("4", D)

    # calculate the behaviour
    anisys.animate()
