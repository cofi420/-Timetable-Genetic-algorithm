# Optimal Timetable Generator using Genetic Algorithm

## Overview
This project implements a timetable generator using a genetic algorithm in Python. The goal is to generate an optimal timetable for classes based on certain criteria. The criteria used for optimization is the sum of x * y, where:
- x is the time passed between 7 am and the beginning of classes.
- y is the time passed between the end of classes and 7 pm.

## Features
- Generates an optimal timetable based on specified constraints.
- Utilizes a genetic algorithm to find the optimal solution.
- Allows customization of input parameters such as class timings, number of classes, etc.

## Requirements
- Python 3.x
- Additional Python libraries: [numpy](https://numpy.org/), [genetic](https://pypi.org/project/genetic/)

## Installation
1. Clone this repository.
2. Install required Python libraries:
    ```bash
    pip install numpy genetic
    ```

## Usage
1. Configure the parameters in `config.py` according to your requirements.
2. Run the `main.py` script:
    ```bash
    python main.py
    ```
3. The generated timetable will be displayed in the console output.

## Parameters
- `NUM_CLASSES`: Number of classes to schedule.
- `CLASS_TIMINGS`: Time slots for each class.
- `POPULATION_SIZE`: Size of the population in the genetic algorithm.
- `MUTATION_RATE`: Rate of mutation in the genetic algorithm.
- `GENERATIONS`: Number of generations for the genetic algorithm to run.
- `CROSSOVER_RATE`: Rate of crossover in the genetic algorithm.

## Example
```python
NUM_CLASSES = 5
CLASS_TIMINGS = [(8, 9), (9, 10), (10, 11), (11, 12), (13, 14)]
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 100
CROSSOVER_RATE = 0.8
