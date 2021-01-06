from scipy.optimize import linprog
import numpy as np

#MILP for the nurse scheduling problem
#employee name or id, min hours of work, max hours of work, hourly wage, and availability.

#work for 8 consecutive hours, however shifts start every four hours
#00-4; 4-8; 8-12; 12-16; 16-20; 20-24 
#hire the minimum number of officers

def simple_working_schedule(*args):
    """
    Linear programming to solve how many workers to have at each change of shift
    """
    available_workers = np.array([args]) * -1
    work_matrix = np.array([[1, 0, 0, 0, 0, 1],
                   [1, 1, 0, 0, 0, 0],
                   [0, 1, 1, 0, 0, 0],
                   [0, 0, 1, 1, 0, 0],
                   [0, 0, 0, 1, 1, 0],
                   [0, 0, 0, 0, 1, 1]])
    
    obj_function = work_matrix.sum(axis = 0)
    work_matrix = work_matrix * -1
    opt = linprog(c=obj_function, A_ub=work_matrix, b_ub=available_workers, method="revised simplex")
    num_workers = opt['x']
    return(list(num_workers))