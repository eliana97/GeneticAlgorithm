#########################################################################################
#                               import the libraries                                    #
#########################################################################################

from cgitb import text
from select import select
from turtle import color
import pandas as pd
import numpy as np
import time as tm
import copy
import random
import matplotlib.pyplot as plt
import warnings
import csv
import config as cg

warnings.filterwarnings('ignore')


def chromosome_initialization():
    """initialization of the chromosome"""
    return np.zeros([cg.num_jobs*cg.num_sub_jobs, cg.num_machines+2])

def random_index_subjobs():
    return random.randint(0,(cg.num_jobs*cg.num_sub_jobs)-1) 


def initialization_random(num_random):
    '''initialization random of the chromosome
    Input: num_random -> int 
    Return: initial_population_random -> np.array '''

    initial_population_random = np.zeros([num_random, cg.num_jobs*cg.num_sub_jobs, cg.num_machines+2])

    for rand in range(num_random):
        #Number of possible sequence indices
        number_sequence = cg.num_jobs*cg.num_sub_jobs
        #Chromosome initialization
        chromosome = chromosome_initialization()
        #Random sequence
        sequence = np.random.permutation(number_sequence)

        #List of sub job
        job_list_occupated_index = np.zeros([cg.num_sub_jobs])

        index = 0

        for job in range(cg.num_jobs):
            for e in range(cg.num_sub_jobs):
                #Append the index as they appear in the sequence and add them to a list 
                job_list_occupated_index[e] = sequence[index]
                index+=1
            #Sorting the array in descending order
            sub_job_sorted = np.sort(job_list_occupated_index)
            for i, sub_job in enumerate(sub_job_sorted):
                chromosome[int(sub_job)][0] = job+1
                chromosome[int(sub_job)][1] = i+1

                rand_machines = np.random.randint(1,cg.num_machines+1)
                chromosome[int(sub_job)][rand_machines+1] = 1

        initial_population_random[rand] = chromosome
    return initial_population_random 


def spt_lpt_initialization(processing_time_table, setup_time_table, spt, num_population):
    '''initialization of the population based on shortest processing time and longest processing time
       Input: processing_time_table -> np.array
              setup time table -> np.array
              spt -> bool 
              num -> int 
        Return: initial_population -> np.array
    '''
   
     #Array that contains the initial population
    initial_population = np.zeros([num_population, cg.num_jobs*cg.num_sub_jobs, cg.num_machines+2])

    for pop in range(num_population):
        #Number of possible sequence indices
        number_sequence = cg.num_jobs*cg.num_sub_jobs
        #Initialization of the chromosome
        chromosome = chromosome_initialization()
        #Random sequence
        sequence = np.random.permutation(number_sequence)
        #List of the sub_job
        job_list_occupated_index = np.zeros([cg.num_sub_jobs])

        list_time = np.zeros([cg.num_machines])
        index = 0
        for job in range(cg.num_jobs):
            for e in range(cg.num_sub_jobs):
                #Append the index as they appear in the sequence and add them to a list
                job_list_occupated_index[e] = sequence[index]
                index+=1
            #Sorting the array in descending order
            sub_job_sorted = np.sort(job_list_occupated_index)
            for i, sub_job in enumerate(sub_job_sorted):
                chromosome[int(sub_job)][0] = job+1
                chromosome[int(sub_job)][1] = i+1


                for m in range(cg.num_machines):
                    list_time[m] = processing_time_table[m][job][i]
                
                if spt:
                    minimum_value = np.amin(list_time)
                    x = np.where(list_time == minimum_value) 
                    #Randomly select the index with the minimum
                    min_machines_proc_time = np.random.randint(len(x))
              
                    index_min = x[min_machines_proc_time][0]
                    
                    chromosome[int(sub_job)][index_min+2] = 1
                else:
                    maximum_value = np.amax(list_time)
                    x = np.where(list_time == maximum_value)

                    #Randomly select the index with the minimum 
                    max_machines_proc_time = np.random.randint(len(x))

                    index_max = x[max_machines_proc_time][0]
            
                    chromosome[int(sub_job)][index_max+2] = 1

        initial_population[pop] = chromosome
        
    return initial_population


def single_crossover(parent1, parent2):
    '''Function that does the cross over operation given two parents
    Input: parent1 -> np.array -> chromosome 
        parent2 -> np.array -> chromosome
    Return: child -> np.array 
    '''
    lis = []
    parent1_copy = parent1.copy()
    parent2_copy = parent2.copy()

    #Initialization of child1
    child1 = np.zeros([cg.num_jobs*cg.num_sub_jobs, cg.num_machines+2])

    #Initialize randomly the two indexes 
    first_index = random_index_subjobs()   #changes: num_jobs-1
    second_index = random_index_subjobs()
    
    #Ensure that second_index is greater than first_index
    while(first_index >= second_index):
        first_index = random_index_subjobs()
        second_index = random_index_subjobs()
    
    #Initiliaze first index
    index = first_index
    while index <= second_index:
        child1[index] = parent1_copy[index]
        lis.append(int(str(int(child1[index][0])) + str(int((child1[index][1])))) )
        index+=1
    index_child = index
    while index_child!= first_index:
        if index == cg.num_jobs*cg.num_sub_jobs: 
            index = 0
        if index_child == cg.num_jobs*cg.num_sub_jobs:  
            index_child=0
        var = int(str(int(parent2_copy[index][0])) + str(int(parent2_copy[index][1]))) 
        if var not in lis:
            child1[index_child] = parent2_copy[index]
            lis.append(int(str(int(child1[index_child][0]))+str(int((child1[index_child][1])))))
            index_child+=1
            index+=1
        else: index+=1

        if len(lis) == cg.num_jobs*cg.num_sub_jobs:                
            break
   
    return child1

def mutation(chromosome):
       """Function that takes a random two index of the chromosome and inverts the job
       Input: chromosome -> np.array
       Return: mutation chrosome -> np.array
       """
       chromosome_copy = np.zeros([cg.num_jobs*cg.num_sub_jobs, cg.num_machines+2])
       chromosome_copy = chromosome.copy()
       while True:
           #random choose position of the chromosome
           num_one = random_index_subjobs()
           num_two = random_index_subjobs()
           while num_one == num_two:
               num_two = random_index_subjobs()

           index_machine_one=1
           value_machines=0
       
           #Find the number of machines that does the job
           while value_machines != 1:
               index_machine_one += 1

               value_machines = chromosome_copy[num_one][index_machine_one]
           

           index_machine_two = 1
           value_machines_two=0

           #Find the number of machines that does the job
           while value_machines_two !=1:
                index_machine_two+=1
                value_machines_two = chromosome_copy[num_two][index_machine_two]
           

           #Se i job sono associati a diverse macchine altrimenti rifaccio la mutazione cambiando indici 
           if index_machine_two+1 != index_machine_one+1: 
               chromosome_copy[num_one][index_machine_one] = 0
               chromosome_copy[num_two][index_machine_two] = 0
               break

        #Invert the machine 
       chromosome_copy[num_one][index_machine_two] = 1
       chromosome_copy[num_two][index_machine_one] = 1   

       return chromosome_copy

    
def fitness_function(chromosome,table):
    #Stores the end time of a sub-job
    time_completed_job =  np.zeros([cg.num_jobs,cg.num_sub_jobs])

    makespan = np.zeros([cg.num_machines])  
    for i in range((cg.num_jobs*cg.num_sub_jobs)):
   
        jobs = int(chromosome[i][0])
        sub_jobs = int(chromosome[i][1])
        for m in range(cg.num_machines):
            machines = int(chromosome[i][m+2])
            if  machines == 1:
                if sub_jobs != 1:
                    wait_time = time_completed_job[jobs-1][sub_jobs-2] - makespan[m] 
                    if wait_time > 0:
                        proc = table[m][jobs-1][sub_jobs-1]
                        makespan[m] +=  wait_time + table[m][jobs-1][sub_jobs-1] 
                        time_completed_job[jobs-1][sub_jobs-1] = makespan[m]
                        break
                    else: 
                        makespan[m] +=  table[m][jobs-1][sub_jobs-1] 
                        time_completed_job[jobs-1][sub_jobs-1] = makespan[m]
                        break
                else:
                    makespan[m] +=  table[m][jobs-1][sub_jobs-1] 
                    time_completed_job[jobs-1][sub_jobs-1] = makespan[m]
                    break
    
    max_element = np.max(makespan)   
    max_index = np.argmax(makespan) 

    return max_element, max_index + 1, makespan

def repairment_chromosome(chromosome):
    '''Repairing the chromosome after single crossover
    Input: chromosome -> np.array
    Return: chromosome -> np.array'''

    #Saving index of each dub_job to see if they are ordered 
    sequence_sub_job = np.zeros(cg.num_sub_jobs)
    #Saving sub-job rows to reverse the order if they are not in sequence
    single_chromosome_sub_job = np.zeros([cg.num_sub_jobs, cg.num_machines+2])

    job = 1
    i=0
    #Counter to see how many sub_jobs have been found, to check the order if all sub_jobs have been found
    num_find_sub = 0

    while True:
    
            if chromosome[i][0] == job:
                sequence_sub_job[int(chromosome[i][1])-1] = i
                single_chromosome_sub_job[int(chromosome[i][1])-1] = chromosome[i]
                num_find_sub+=1

                #If at the last sub_jobs I check the order of the array
                if num_find_sub == cg.num_sub_jobs:
                    num_find_sub = 0
                    copy = sequence_sub_job.copy()
                    sorted_array = np.sort(copy)

                    #If the two arrays are equal the sequence is respected, otherwise not
                    #Fixing by keeping the assignment to a machine but reversing the indices 
                    if not np.array_equal(sequence_sub_job, sorted_array):
                        e = 0
                        for index, element in enumerate(sorted_array):
                       
                            chromosome[int(element)] = single_chromosome_sub_job[e]
                            e+=1

                    job+=1
                    if job > cg.num_jobs:
                        break
                    

            if i == (cg.num_jobs*cg.num_sub_jobs)-1: i = 0
            else: i+=1
    return chromosome 

def selection_k_tournament(initial_population,k):
    '''Take random k individuals from population and take the best one
    Input: initial_population -> np.array
           k -> int 
    Return chromosome_number -> np.array'''
    
    makespan_array = np.zeros([k,1])
    k_list = []
    #Select chromosome randomly
    for i in range(k):
        x = random.randint(0,len(initial_population)-1)
        while(x in k_list):
            x = random.randint(0,len(initial_population)-1)
        k_list.append(x)
    
    for e in range(len(k_list)):
        #take the max of makespan and the correspondent index machine_max
        fitness_max, machine_max_index, makespan_save = fitness_function(initial_population[k_list[e]], cg.processing_time_table)        #take the first index
        makespan_array[e] =  fitness_max

    #take the  best
    index_min_makespan = np.argmin(makespan_array)
    chromosome_number = k_list[index_min_makespan]

    return chromosome_number  


def create_gannt(chromosome,min_makespan):
    '''Creating the gannt diagram'''
    
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
 
    # Setting Y-axis limits
    #gnt.set_ylim(0,100)
    gnt.set_ylim(0,200)
 
    # Setting X-axis limits
    gnt.set_xlim(0, min_makespan+5)

    #Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Machine')
 
    # Setting ticks on y-axis
    gnt.set_yticks([5,25,45,65,85,105,125,145,165,185])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(['M1', 'M2', 'M3','M4','M5','M6','M7','M8','M9','M10'])
 
    # Setting graph attribute
    gnt.grid(True)

    m1 = (2.5, 8)
    m2 = (22.5,8)
    m3 = (42.5,8)
    m4 = (62.5,8)
    m5 = (82.5,8)
    m6 = (102.5,8)
    m7 = (122.5,8)
    m8 = (142.5,8)
    m9 = (162.5,8)
    m10 = (182.5,8)

    colori = ["#a39ae9", "#8fc8cf","#66a1ed","#7366d0","#93380e","#a27559","#299d58","#37245c","#653989","#272b54","#938ac8","#db739b","#fb6a3c",
              "#db3c4c","#35b5ba","#b2a340","#272b54","#c32e5b","#eb7d27","#502f53","#742640","#718d6a","#082a3e","#2a4c25","#151c0b",
              "#0c071e","#21022d","#655370","#4f2856","#7f2623","#00a86b","#a968c7","#006b3c","#fca600","#fa3033","#c33e97","#8464ae","#0b57bb","#6d904f","#3b3944","#260e25",
              "#bc441c","#ba1010","#16537e","#000000","#5b7c99","#423629","#800020","#373a38","#a3616e","#184700","#0b2494"]

    #Stores the end time of a sub-job
    time_completed_job =  np.zeros([cg.num_jobs,cg.num_sub_jobs])

    makespan = np.zeros([cg.num_machines])  
    c = 0
    for i in range((cg.num_jobs*cg.num_sub_jobs)):
        
        jobs = int(chromosome[i][0])
        sub_jobs = int(chromosome[i][1])
        for m in range(cg.num_machines):
            machines = int(chromosome[i][m+2])
            if  machines == 1:
                if sub_jobs != 1:
                    wait_time = time_completed_job[jobs-1][sub_jobs-2] - makespan[m] 
                    if wait_time > 0:
                        proc = cg.processing_time_table[m][jobs-1][sub_jobs-1]
                        makespan[m] +=  wait_time + cg.processing_time_table[m][jobs-1][sub_jobs-1]
                        time_completed_job[jobs-1][sub_jobs-1] = makespan[m]
             
                    else: 
                        proc = cg.processing_time_table[m][jobs-1][sub_jobs-1]
                        makespan[m] +=  cg.processing_time_table[m][jobs-1][sub_jobs-1] 
                        time_completed_job[jobs-1][sub_jobs-1] = makespan[m]
               
                else:
                    proc = cg.processing_time_table[m][jobs-1][sub_jobs-1]
                    makespan[m] +=  cg.processing_time_table[m][jobs-1][sub_jobs-1]
                    time_completed_job[jobs-1][sub_jobs-1] = makespan[m]

                if m==0:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m1, color =colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,5.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==1:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m2, color =colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,25.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==2:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m3, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,45.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==3:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m4, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,65.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==4:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m5, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,85.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==5:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m6, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,105.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==6:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m7, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,125.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==7:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m8, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,145.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==8:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m9, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,165.5,str(jobs)+"."+str(sub_jobs),color = 'white')
                elif m==9:
                    gnt.broken_barh([((makespan[m]-proc), proc)],m10, color = colori[c])
                    gnt.text((makespan[m]-proc/2)-4.5,185.5,str(jobs)+"."+str(sub_jobs),color = 'white')
               
                if c+1<len(colori):
                    c+=1
                else: 
                    c = 0

                    
                break
        #plt.show()


   
    #plt.savefig("gantt1.png")
    plt.title("Gantt Chart with Makespan = " + str(min_makespan))
    plt.show()