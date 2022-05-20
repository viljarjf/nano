# nano
Programs made during nanotechnology studies


The earlier courses (namely TDT4110 ITGK, TFY4115 fysikk 1, and to some degree TDT4102 C++) contain mostly bad code. 
I've improved by the time TKJ4215 statterm comes around, although some exercises were solved in a memey way. Beware.

# 6th semester

### TFY4235 Numerical Physics

- 1: Numerically solving the wave equation with a Koch snowflake as boundary. Quite optimized python code, somehow running significantly faster than my classmates. Optionally solve the eigensystem on GPU, but the cupy library is not ready for solving huge sparse eigenproblems it seems. This is the exercise I am most proud of, pushing hardware to its limit on good code. Also, the resulting figures were pretty.

- 2: A fun development experiment, using C to generate data and Python for plotting. The program simulates particles moving in a temporally modulated saw potential.

- 3: Barely started to work on it. I think the groundwork is good. The program was going to simulate gamma radiation from nuclear decay, which would further interact with the surrounding nuclei.

- exam: The exam went all right. I decided to write genrally from the start, so 0D, 1D and 2D simulations were programatically identical. Everything is completely vectorized in numpy, with one numba-accellerated exception where I iterate. The program simulates the spin of atoms in a magnetic field.

### TFY4220 Solid state physics

- Some tweaks to a library I found for simulating XRD, alongside plotting tools and other utilities

# 5th semester
### TMT4320 Nanomaterials

- Exercises in nanomaterials with python and latex. Did not finish this course

### TDT4120 Algorithms and data structures

- The programming part of exercises in algorithms and data structures. Some went very well, some I did not get to work fast enough

### TFY4335 Nano life science

- Exercises in nano life science, with python and latex

### TFY4330 Nanotools

- Data analysis of different electron microscopes in nano tools


# 4th semester
### TFE4120 Electromagnetism

- latex code for a compendium in electromagnetism

### TKJ4215 Statistical thermodynamics

- python exercises in statistical thermodynamics. 

- 1: meme oneliner
- 2: meme oneliner
- 3: decently fast algorithm and fast implementation for calculating density of states exactly for 2D microsystems. Even so, the problem itself is exponential, so anything greater than, say, 36 particles will take minutes
- 4: simulate chemical reactions. Write arbitrary reactions, enter their rates, and watch the system develop. 
There is also a graphical simulator, with 1000x1000 grid of particles performing random walks, entered with a paint-like interface, and different colors reacting with each other.
This is about the only time I've used inheritance with OOP, since I wanted to force myself to use it. Not too bad, but I still prefer a more functional approach
- 5: particle physics simulator. At one point, it made videos of particles in a general force field, but then I hard-coded the RK4-method with gravity and broke the video encoder thing.

### TBT4170 Biotechnology

- Latex document of exam notes, made the day before the exam, so don't use them as a source


# 3rd semester
### TMA4130 Mathemathics 4N 

- python exercises in numerical analysis, e.g. implementing a general Runge-Kutta solver accepting an arbitrary Butcher tableu.

### TMA4240 Statistics

- python snippets used for some statistics exercises

### TMT4185 Materials science

- python snippet for a task in an exercise in materials science

# 2nd semester
### TMA4105 Mathemathics 2

- latex code for multivariate calculus exercises

### TMA4115 Mathemathics 3

- latex code for linear algebra exercises

### TDT4102 Procedure- and object-oriented programming

- C++ exercises

# 1st semester
### TDT4110 Information technology

- Python exercises

### TFY4115 Physics

- bad python code for simulating a ball rolling along a predetermined path
