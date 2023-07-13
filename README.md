# nano
Programs made during nanotechnology studies at the Norwegian University of Science and Technology, and an exchange at the Technical University of Munich.

Focus area of nanoelectronics.
# 8th semester (at TUM)

### [Computational Methods in Many-Body Physics](year_4/TUM_manybody_physics/)

Simulation of many-body systems, mainly quantum many-body systems.

- Exercise 1-3: Classical Ising model for spin-spin interactions. A small library ([ising_model](year_4/TUM_manybody_physics/ising_model/)) was written and used for the simulations.

- Exercise 4-: Exact diagonalization, sparse matrix tools, and the quantum Ising model.

### [Computational Physics II](year_4/TUM_computational_physics_2/)

Computational physics. Classical ising model, Monte-Carlo integration, chaos ect. 

I did not solve all exercises.

### [Computational Methods for Nanoelectronics: Quantum Models](year_4/TUM_quantum_nano_sim/)

I decided not to continue with this course.

### [Superconducting Qubits: Architecture and Algorithms](year_4/TUM_quantum_computing/)

Mainly fiddling around with qiskit

# 7th semester (at TUM)

### [Simulation of Quantum Devices](year_4/TUM_quantum_sim/)

Different simulation methods for quantum devices, course taken at TU Munich.
In the beginning, I spent way too much time writing the code abstractly. The more advanced simulations have not even been split into multiple files...

To be able to import stuff into different exercises, I made the entire folder a python module. I might refactor most of it, since these exercises ended up as a baseline for my quantum simulation library [QM-sim](https://pypi.org/project/qm-sim/).

- Dual QW: Thermal equilibrium electron occupation in a double well potential, simulated using finite difference.

- QCL: Quantum Cascade Laser simulation, with a strange non-periodic multi-well potential. Non-temporally simulated with finite difference, using the Schrödinger-Poisson equation.

- QW: Quantum wire simulation, using finite difference

- RTD: Resonant Tunneling Diode simulated with transfer matrices

- SQUID: Supposedly simulating a Superconducting QUantum Interference Device, but it's just the same potential as the dual QW. Simulated temporally with finite difference.

# 6th semester

### [TFY4235 Numerical Physics](year_3/TFY4235_numfys/)

- [Exercise 1](year_3/TFY4235_numfys/1/): Numerically solving the wave equation with a Koch snowflake as boundary. Quite optimized python code, somehow running significantly faster than my classmates. Optionally solve the eigensystem on GPU, but the cupy library is not ready for solving huge sparse eigenproblems it seems. This is the exercise I am most proud of, pushing hardware to its limit on good code. Also, the resulting figures were pretty.

- [Exercise 2](year_3/TFY4235_numfys/2/): A fun development experiment, using C to generate data and Python for plotting. The program simulates particles moving in a temporally modulated saw potential.

- [Exercise 2](year_3/TFY4235_numfys/3/): Barely started to work on it. I think the groundwork is good. The program was going to simulate gamma radiation from nuclear decay, which would further interact with the surrounding nuclei.

- [Exam](year_3/TFY4235_numfys/exam): The exam went all right. I decided to write genrally from the start, so 0D, 1D and 2D simulations were programatically identical. Everything is completely vectorized in numpy, with one numba-accellerated exception where I iterate. The program simulates the spin of atoms in a magnetic field.

###  [TFY4220 Solid state physics](year_3/TFY4220_faststoff/)

Some tweaks to a library I found for simulating XRD, alongside plotting tools and other utilities

# 5th semester
### [TMT4320 Nanomaterials](year_3/TMT4320_nanomat/)

Exercises in nanomaterials with python and latex. Did not finish this course, but since it is required for my degree I plan to finish it in the 9th semester.

### [TDT4120 Algorithms and data structures](year_3/TDT4120_algdat/)

The programming part of exercises in algorithms and data structures. Some went very well, some I did not get to work fast enough

### [TFY4335 Nano life science](year_3/TFY4335_bionano/)

Exercises in nano life science, with python and latex

### [TFY4330 Nanotools](year_3/TFY43330_nanotools/)

Data analysis of different electron microscopes in nano tools.

# 4th semester

### [TFE4120 Electromagnetism](year_2/TFE4120_elmag/)

Latex code for a compendium in electromagnetism

### [TKJ4215 Statistical thermodynamics](year_2/TKJ4215_statterm/)

Python exercises in statistical thermodynamics. 

- 1: meme oneliner
- 2: meme oneliner
- 3: decently fast algorithm and fast implementation for calculating density of states exactly for 2D microsystems. Even so, the problem itself is exponential, so anything greater than, say, 36 particles will take minutes
- 4: simulate chemical reactions. Write arbitrary reactions, enter their rates, and watch the system develop. 
There is also a graphical simulator, with 1000x1000 grid of particles performing random walks, entered with a paint-like interface, and different colors reacting with each other.
This is about the only time I've used inheritance with OOP, since I wanted to force myself to use it. Not too bad, but I still prefer a more functional approach
- 5: particle physics simulator. At one point, it made videos of particles in a general force field, but then I hard-coded the RK4-method with gravity and broke the video encoder thing.

### [TBT4170 Biotechnology](year_2/TBT4170_biotek/)

Latex document of exam notes, made the day before the exam, so don't use them as a source

# 3rd semester

### [TMA4130 Mathemathics 4N](year_2/TMA4130_4N/)

Python exercises in numerical analysis, e.g. implementing a general Runge-Kutta solver accepting an arbitrary Butcher tableu.

### [TMA4240 Statistics](year_2/TMA4240_statistikk/)

Python functions used for some statistics exercises

### [TMT4185 Materials science](year_2/TMT4185_mattek/)

Python function for a task in an exercise in materials science

# 2nd semester

### [TMA4105 Mathemathics 2](year_1/TMA4105_2/)

Latex code for multivariate calculus exercises

### [TMA4115 Mathemathics 3](year_1/TMA4115_3/)

Latex code for linear algebra exercises

### [TDT4102 Procedure- and object-oriented programming](year_1/TDT4102_cpp/)

C++ exercises

# 1st semester

### [TDT4110 Information technology](year_1/TDT4110_itgk/)

Python exercises

### [TFY4115 Physics](year_1/TFY4115_fysikk/)

Bad python code for simulating a ball rolling along a predetermined path
