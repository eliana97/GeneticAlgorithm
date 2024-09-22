import numpy as np
import genetic_algorithm as ga

def sorting_processing_table(index_job, time_table, shortest, longest):
    '''Function that orders the time taken by machines to perform the job in an increasing or decreasing order. 
        Input:  int -> index_job: Corresponds to the index of the job we want to consider for ordering the array
                np.array[][] -> time_table: the take that we want to consider: makespan or setup time 
                bool -> shortest: To sort in ascending order 
                bool -> longest: To sort in descenting order
        Returns: np.array -> index_sorted_array: Array with the 'old' index of ordered values
                            For example: 
                            1) table = [5, 1, 3, 4, 6]
                            2) sorted_array = [1, 3, 4, 5, 6]
                            3) index_sorted_array = [1, 2, 3, 0, 4]
                int -> count: Counter indicating how many times the minimum value appears in the array 
    '''
    table = time_table[:][index_job-1]
    if(shortest):
        #Shortest processing time
        sorted_array = np.sort(table)
        #Index of shortest processing time
        index_sorted_array = np.argsort(table)
    elif(longest):
        #Longest processing time
        sorted_array = np.sort(table)[::-1]
        #Index of longest processing time
        index_sorted_array = np.argsort(table)[::-1]

    count = 0
    #It counts how many times the minimum vaue appears in the array: In this way it is possible to consider all the equal minimum time 
    #to initialize the population
    for i in range(len(sorted_array)):
        if(sorted_array[i] == sorted_array[i+1]):
            count=+1
        else:
            break
    
    return index_sorted_array, count


def order_matrix(matrix_individuals,num_machines, num_jobs):

    '''Function that allows you to stack the jobs without leaving empty cells, like that:

          J1  J2  J3  J4  J5  
      M1 [5   0   0   0   0 ]
      M2 [0   1   0   2   0 ]
      M3 [0   3   0   0   0 ]
      M4 [0   0   0   4   0 ]

      Input: matrix individuals -> array 2d with size (num_machines x num_jobs), it is one element of the initial_population list
             num_machines -> int
             num_jobs = int
      Return: Matrix like that:

          J1  J2  J3  J4  J5  
      M1 [5   0   0   0   0 ]
      M2 [1   2   0   0   0 ]
      M3 [3   0   0   0   0 ]
      M4 [4   0   0   0   0 ]
    '''

    #funzione che incolonna i job sulla prima colonna disponibile 
    for i in range(num_machines):
        for j in range(num_jobs):
            if(matrix_individuals[i][j] == 0):
                index = j
                a = j
                a+=1
                while(a != num_jobs):
                    if(matrix_individuals[i][a] != 0):
                        matrix_individuals[i][index] = matrix_individuals[i][a]
                        matrix_individuals[i][a] = 0
                    
                        break
                    else:
                        a+=1
    return matrix_individuals

def zeros_chrom_init(rows,columns):
    '''Function that initialize the chromosoma with dimension: num_jobs x num_machines+1
    Input: rows -> type(int) : number of rows of the matrix 
           columns -> type(int) : number of columns of the matrix
    Return: matrix initialized with all zeros
    '''
    return np.zeros([rows,columns+1])

