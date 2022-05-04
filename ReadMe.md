## Overview

This is a Python program for the modelling of simple evolving systems. It was inspired by the work of [David Miller](https://www.youtube.com/watch?v=N3tRFayqVtk). 

## TO DO

Still to implement:

- The Gene System
    - [X] Define a number of behaviour genes
    - [X] Create the network of neurons
    - [X] Add process for sensing / acting of every being
        - [ ] Expand the sensor system:
            - Sense population density gradient
            - Sense general motion gradient
        - [ ] Expand the action system:
            - Move towards / away from pop gradient
            - Move towards / away from motion gradient
    - [X] Test one generation of the simulation
    - [X] Implement the genetic algorithm (selection / fitness evaluation, reproduction, mutation)
        - [X] Geographical Selection
        - [X] Reproduction System
        - [X] Mutation System
    - [X] Multi generational runs
        - Fixed issue with internal neurons being mislabeled by forcing rebuild of the quick access arrays at the first sense step.
        - This doesn't fix the cause, but at least resolves the symptoms.
    - [ ] Additional methods of reproduction (asexual, intra-gene splicing)
- Animate the generation
    - [X] Produce an image for every step
    - [X] Join the images into a single animated file
- Generational Reports
    - [ ] Graphs showing: 
        - [ ] Genetic diversity
        - [X] Mortality Rate
 

## How to run

To run this script, first clone this repo. Then, create a virtual environment in the destination folder using the following command

```
python -m venv venv
```

After that, run the following command according to your operating system of choice.

```
# For Mac/Linux

source /venv/bin/activate

# For Windows
/venv/bin/activate.ps1
```

Then install the requisite dependencies using the following command

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

With everything installed, run the command.

```
python main.py
```

Then check the output folder to see the results.

## How to configure

To edit some of the parameters of the simulation, edit the config.py file of the root directory. This is an explanation of the params:

- image-output-path: The location of the output path for the images. By default, it will be a file in the downloaded repository which the executing code will itself generate. If you change this param, remember the code will try to create the output directory as part of its runtime.
- image-by-step: Change flag to `True` if you want to produce a separate image for every step of every generation. Good for debugging or visualizing data in a small amount of generations, but can quickly grow out of hand with many generations. 
- being-size: The size in pixels of the beings that populate the simulation. Larger sizes influence the resolution of the final image.
- board-size: The size of the grid, in being-size units. By default, the board is 180 beings wide and 180 beings tall. No current plan to implement rectangular boards exists.
- population-size: The amount of beings to create when populating the board
- max-generations: The number of generations a run of this simulation will generate
- max-steps: The number of steps the beings will be allowed to take until a generation is considered complete and selection criteria are applied.
- gene-length: The complexity of the genes every being will have.
- internal-neurons: Max number of separate internal neurons in the genetic pool
- action-threshold: The value needed to excite an action neuron. 
- mutation-enabled: Boolean flag to allow for beings to mutate on reproduction
- mutation-chance: Mutation chance per gene.
