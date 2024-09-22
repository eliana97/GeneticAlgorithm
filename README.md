# Genetic Algorithm for Job Shop Scheduling Problem

## Project Description

This project implements a genetic algorithm to solve the Job Shop Scheduling Problem (JSSP), a classic combinatorial optimization problem. The algorithm aims to minimize the total completion time of operations across various machines.

## Project Structure

- **`config.py`**: This file contains all the configurable numerical variables used by the algorithm. These variables can be modified to find the optimal combination of parameters.
  - `num_jobs`, `num_sub_jobs`, `num_machines`
  - Population size (`size_initial_population`)
  - Rates for shortest and longest processing time individuals (`rate_spt`, `rate_lpt`)
  - Crossover and mutation rates (`rate_crossover`, `rate_mutation`)
  - Simulated annealing parameters (`temperature_0`, `k`, `min_temperature`)
  - Processing and setup time tables
  - Selection and mutation configurations (e.g., `random_selection', 'selection_best_worst', 'selection_k_tournament`, `mutation_best`, `mutation_worst`,  `mutation_random`)
    
- **`genetic_algorithm.py`**: Contains all the methods and functions used by the genetic algorithm to perform operations such as selection, crossover, mutation, and fitness evaluation.
- **`main.py`**: The core of the genetic algorithm, where the main loop of the algorithm is executed, and the different methods are combined to find the best solution.
