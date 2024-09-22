'''This file contains all the initialization constants of the algorithms'''
import numpy as np


num_jobs = 10
num_sub_jobs = 5
num_machines = 5

#Deinition of the size of the population
size_initial_population = 50
#Definition of the rate of the shortest processing time individuals
rate_spt = 0.2
#Definition of the rate of the shortest processing time individuals
rate_lpt = 0.2
#Compute number of individual of shortest processing time given the rate
num_spt = int(size_initial_population*rate_spt)
#Compute number of individual of longest processing time given the rate
num_lpt = int(size_initial_population*rate_lpt)
#Compute number of individual of random that is equal to  remaining idividuals
num_random = size_initial_population - num_spt - num_lpt

#Rate of crossover
rate_crossover = 0.8
#Rate mutation
rate_mutation = 0.2

#Simulated Annealing
temperature_0 = 50
k = 0.85
n = 2
    
temperature = 1
min_temperature = 0.0001

minimum = 10000
count_without_improvment = 0

# Example of processing time table and setup time table
processing_time_table = np.array([[[10,40,52,18,36],[20,47,41,25,56],[15,27,36,64,33],[26,25,66,24,35],[40,36,54,26,47],[50,57,33,53,24],[19,32,35,43,12],[25,25,37,28,24],[26,14,37,36,23],[60,28,33,22,31]],
                                      [[20,46,21,34,47],[22,32,21,27,28],[32,33,37,45,24],[59,26,44,59,28],[40,24,36,47,38],[35,21,41,56,37],[25,53,25,46,27],[29,32,15,12,27],[32,25,32,27,28],[34,43,52,16,37]],
                                      [[10,36,33,27,18],[48,21,35,22,33],[35,26,32,25,36],[54,24,14,26,35],[65,15,31,16,27],[17,28,37,26,34],[27,33,25,19,32],[38,15,26,37,28],[25,27,26,24,11],[34,41,17,16,23]],
                                      [[19,35,34,12,35],[19,23,45,17,25],[14,22,44,63,27],[18,32,26,17,28],[25,37,32,24,16],[29,33,25,36,27],[15,14,26,37,53],[31,35,27,28,18],[19,22,23,14,21],[41,34,25,22,15]],
                                      [[16,34,15,21,44],[27,44,56,27,23],[24,35,17,41,25],[34,46,27,34,16],[53,24,33,27,23],[42,33,14,25,16],[72,33,25,26,13],[57,23,36,25,15],[37,26,41,25,18],[20,15,26,34,16]]])


setup_time_table =      np.array([[[1,4,6,7,3],[2,3,5,6,3],[2,6,8,2,1],[2,2,3,3,4],[2,2,1,7,3],[2,4,3,5,2],[2,4,5,2,8],[9,1,2,6,6],[3,3,2,5,3],[2,3,4,5,1]],
                                      [[2,2,3,5,9],[6,6,4,3,2],[5,4,3,2,5],[1,2,4,6,7],[3,4,5,6,3],[2,4,6,7,7],[2,1,8,6,4],[2,9,5,2,4],[2,5,6,7,9],[1,1,2,6,8]],
                                      [[4,6,2,8,9],[1,3,6,8,9],[2,9,7,8,2],[2,7,0,4,2],[7,4,9,9,6],[3,4,9,6,7],[5,8,5,7,4],[1,5,7,4,8],[2,3,7,9,9],[2,7,8,9,9]],
                                      [[6,4,7,9,9],[1,5,3,6,7],[2,6,9,7,9],[4,8,0,7,9],[4,8,9,9,7],[4,7,9,0,4],[2,5,9,6,4],[2,6,3,7,9],[9,6,8,4,3],[6,8,9,9,1]],
                                      [[1,6,7,9,5],[1,4,9,5,8],[4,8,9,5,8],[5,8,5,7,8],[6,8,5,7,9],[4,7,5,9,0],[4,7,0,5,8],[7,9,9,4,8],[6,7,8,9,6],[8,6,8,8,1]]])

# STOP IN CASE OF NO IMPROVMENT
stop_no_improvment = True





# Different configuration
# Choose only one for type

###################################################################################
# SELECTION
###################################################################################

# Selection two parent randomly
selection_random = False
# Selection the best and the worst chromosomes
selection_best_worst = False
#Selection k tournaments
selection_k_tournament = True

###################################################################################
# MUTATION
###################################################################################

# Random mutation
mutation_random = False
# Mutation of the best chromosome
mutation_best = True
# Mutation of the worst chromosome
mutation_worst = False


