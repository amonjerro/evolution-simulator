## Overview

This is a Python program for the modelling of simple evolving systems. It was inspired by the work of [David Miller](https://www.youtube.com/watch?v=N3tRFayqVtk). 

## The big picture

This software populates a space with beings that are given a number of steps to act before the generation is done and a set of selection criteria are applied. The beings share the same blueprint of available neurons and these neurons are categorized in three main sets:

1. Sensors: Neurons that perceive aspects of the surrounding environment to gain activation values
2. Internals: Neurons that are passed values from sensors or other internals
3. Actions: Neurons that - when excited beyond a threshold - cause the being to act in a certain way.

Beings are defined by a set of genes which are randomly populated in the first generation. A gene is a 6-character hexadecimal string that defines the links that exist between neurons for that being and, so, a being's genetics is a directed graph or network of these connections. Which character encodes what information is established in the `Gene` class.

1. One character dictates whether the originating neuron is either a sensor or an internal neuron. Even values for said character represent sensors. As of now, odd values for this character indicate internal neurons.
2. Another character represents _which_ neuron is the source and the value is modulo divided by total available neurons of that type. The full list of sensors can be found in the `src/behavior_constants.py` file.
3. A third character dictates whether the target neuron is either an internal or an action. Even values for it represent actions.
4. A fourth character represents _which_ neuron is the target. The logic for it is identical to (2).
5. The last two characters represent how sensitive the connection is in the range of [0,2]. Excitability between 0 and 1 can be interpreted as an inhibitor gene as it dampens the activation signal passed through. Excitability between 1 and 2 can be interpreted as exciter genes, as they enhance the activation signal passed through. In the example, '4f' represents the value 79 in base 10. When divided by 128, this produces the excitability value of 0.62, so this is an inhibitor neuron.

After the amount of steps to a generation are done, selection criteria are applied to determine the beings that will pass on their genes. The survivors then are sampled and new beings are created by mixing their genes. If enabled, mutations can happen during this process. The process is then repeated for as many generations as is specified in the config file.

After the simulation is done, a GIF file for every generation will have been created in the `/gen_gifs` directory of the specified output path. Along with this, other reports can be found in the `/reports` under the same output path. 

## Example Outputs

For a particular simulation, this is the first generation. The red area represents which beings will survive.

![generation_0](https://user-images.githubusercontent.com/9394777/169456944-8346e0c9-615c-4594-878e-21218b7ce95a.gif)


This is a visualization of the 29th generation of selecting using the red rectangle. 

![generation_29](https://user-images.githubusercontent.com/9394777/169456969-b33880b9-123e-4803-97c5-442ab796e99a.gif)

And this is a look into the genetic network of one of those beings. This current image shows some problems with the neuron creation algorithm that are intended to be sorted out soon.

![being0_network](https://github.com/amonjerro/evolution-simulator/assets/9394777/5f136900-ebb7-4b31-a875-3bcbdab83b01)



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
    - [X] Inhibitor genes
- Genetic Algorithm Implementations
    - [ ] More reproduction functions
    - [ ] More mutation variants than just replacement (further reading necessary)
- Animate the generation
    - [X] Produce an image for every step
    - [X] Join the images into a single animated file
- Visualizations
    - [ ] Graphs showing: 
        - [ ] Genetic diversity
        - [X] Mortality Rate
    - [X] Neuron Networks

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
