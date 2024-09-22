import genetic_algorithm as ga
import numpy as np
import config as cg
import time as tm
import csv
import matplotlib.pyplot as plt

#####################################################################################################################
#                                                  MAIN FUNCTION                                                    #
#####################################################################################################################


if __name__ == "__main__":


    start_time = tm.time()
   
    average_makespan_list = []

    ###1) Population Initialization:
    population_random = ga.initialization_random(cg.num_random)
    population_spt =  ga.spt_lpt_initialization(cg.processing_time_table,cg.setup_time_table, True, cg.num_spt)
    population_lpt = ga.spt_lpt_initialization(cg.processing_time_table,cg.setup_time_table, False, cg.num_lpt)

    population = np.concatenate([population_random,population_spt,population_lpt])

    print(population)

    ###2) Compute the makespan and take the best 
    #Define array to contain all the makespan in order to take the min
    makespan_array = np.zeros([len(population),1])
    for i in range(len(population)):
        #max_element, max_index, makespan = compute_makespan(population[i])
        max_element, max_index, makespan = ga.fitness_function(population[i],cg.processing_time_table)
        makespan_array[i] = max_element

    min_makespan = np.amin(makespan_array)
    index_min_makespan = np.argmin(makespan_array)

    print("makespan array", makespan_array)
    print("min makespan ", min_makespan)
    print("index_min_makespan ", index_min_makespan)
    print("Best chromosome ", population[index_min_makespan])

  
    t = 0
    lista = []
    b=0
    
    while t<1400: 
        t+=1
        ###3)Selection
        
        #3.1) Selection two parent randomly
        if cg.selection_random:
            parent1 = np.random.randint(0,len(population))
            parent2 = np.random.randint(0, len(population))
            while parent1==parent2:
                 parent2 = np.random.randint(0, len(population))
        
        #3.2) Selection the best and the worst chromosomes 
        if cg.selection_best_worst:
            parent1 = np.argmin(makespan_array)
            parent2 = np.argmax(makespan_array)

        #3.3) Selection k tournaments
        if cg.selection_k_tournament:
            parent1 = ga.selection_k_tournament(population, 4)
            parent2 = ga.selection_k_tournament(population, 4)
            while parent1==parent2:
                parent2 = np.random.randint(0,len(population))

        ##### 1
        #t = temperature / float (k+1)
        ### 4) Crossover
        crossover_prob = np.random.rand()
        if cg.rate_crossover >= crossover_prob:
            child =ga. single_crossover(population[parent1], population[parent2])
            #Repair the crossover operation to maintain the sequence of job
            child = ga.repairment_chromosome(child)
            makespan_cross = ga.fitness_function(child, cg.processing_time_table)
            population = np.append(population, [child], axis = 0)
                

        ###5) Mutation
        mutation_prob = np.random.rand()
        if cg.rate_mutation >= mutation_prob:

            #5.1) Random mutation
            if cg.mutation_random:
                index_chromosome_mutation = np.random.randint(0,len(population))
            
            #5.2) Mutation of the best chromosome
            if cg.mutation_best:
                index_chromosome_mutation = np.argmin(makespan_array)

            #5.3) Mutation of the worst chromosome
            if cg.mutation_worst:
                index_chromosome_mutation = np.argmax(makespan_array)

            
            child_mutation = ga.mutation(population[index_chromosome_mutation])
          
            makespan_child = ga.fitness_function(child_mutation, cg.processing_time_table)

            pippo = np.amin(makespan_array)
            difference_energy = makespan_child[0] - pippo


            assert cg.temperature > 0.0, "error messsage"
            metropolis = np.exp(-difference_energy/cg.temperature)
            min_check = min(1,metropolis)
            probability = np.random.rand()
           
            if min_check > probability:
                population = np.append(population, [child_mutation], axis = 0)
           
          
        #Compute makespan 
        ###6) Compute the makespan 
        # Write the makespan in the array
        makespan_array = np.zeros([len(population),1])
        for i in range(len(population)):
            max_element, max_index, makespan = ga.fitness_function(population[i], cg.processing_time_table)
            makespan_array[i] = max_element
        
        min_value = np.amin(makespan_array)
        if cg.minimum > min_value:
            cg.minimum =  min_value
            iteration = t
        
        average_makespan_list.append(np.average(makespan_array))

        if t-1 == iteration:
            count_without_improvment += 1
            iteration = t
        else:
           count_without_improvment = 0

        #If there is no improvment for k iterations stopped  
        if cg.stop_no_improvment:  
            if count_without_improvment>1000:
                print("Interrupt for no improvment")
                break


        lista.append(cg.temperature)
        b+=1
        temperature = max(cg.min_temperature, cg.k*(pow(cg.temperature_0,cg.n))/(pow(cg.temperature_0,cg.n)+pow(t,cg.n)))




      

stop_time = tm.time()

print("MIN ", np.amin(makespan_array))
print("Index min ", np.argmin(makespan_array))
print("len population ", len(population))
print("chromosoma minimo ", population[np.argmin(makespan_array)])

print("Tempo impiegato ", stop_time - start_time)

ga.create_gannt(population[np.argmin(makespan_array)], np.amin(makespan_array))

print(len(average_makespan_list))

x_axis = range(0,t)
y_axis = average_makespan_list

plt.plot(x_axis, y_axis)
plt.title('Average Fitness  per Iteration')
plt.xlabel('Iterations')
plt.ylabel('Average Fitness')
plt.show()

