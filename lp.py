from scipy.optimize import linprog
import numpy as np
import pulp

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

def ip_working_schedule(*args):
    employees = ["employee1", "employee2", "employee3", "employee4", "employee5", "employee6", "employee7", "employee8"]
    working_hours = ["00-02", "02-04", "04-06", "06-08", "08-10", "10-12", "12-14", "14-16", "16-18", "18-20", "20-22", "22-24"]
    min_hours = args[0][0]
    max_hours = args[0][1]
    hourly_wage = args[0][2]
    #hourly_wage = [30, 40, 45, 50, 55, 60, 30, 40]
    #columns are 2 hours blocks
    #rows are employees
    """costs = [[0, 0, 0, 30, 30, 30, 30, 30, 30, 30, 0, 0],
                [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40],
                [45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45],
                [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
                [0, 0, 0, 55, 55, 55, 55, 55, 55, 0, 0, 0],
                [60, 60, 60, 0, 0, 0, 0, 0, 0, 60, 60, 60],
                [0, 0, 0, 0, 30, 30, 30, 30, 0, 0, 0, 0],
                [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]]"""
    availability = args[0][3]
    #sum of min hours is daily needed
    min_hours = [min_hour / 2 for min_hour in min_hours]
    max_hours = [max_hour / 2 for max_hour in max_hours]
    min_working_hours = dict(zip(employees, min_hours))
    max_working_hours = dict(zip(employees, max_hours))
    costs = []
    for i in range(len(hourly_wage)):
        available = availability[i]
        if len(available) <= 0:
            employee_cost = 12 * [hourly_wage[i]]
            costs.append(employee_cost)
        elif available.find(",") == -1:
            employee_cost = [0] * 12
            mid_val = available.find("-")
            first_val = int(int(available[:mid_val])/2)
            second_val = int(int(available[mid_val+1:])/2)
            employee_cost[first_val:second_val] = (second_val-first_val) * [hourly_wage[i]]
            costs.append(employee_cost)
        else:
            employee_cost = [0] * 12
            mid_availability = available.find(",")
            first_availability = available[:mid_availability]
            second_availability = available[mid_availability + 2:]
            first_mid_val = first_availability.find("-")
            first_val = int(int(first_availability[:first_mid_val])/2)
            second_val = int(int(first_availability[first_mid_val+1:])/2)
            employee_cost[first_val:second_val] = (second_val-first_val) * [hourly_wage[i]]
            second_mid_val = second_availability.find("-")
            first_val = int(int(second_availability[:second_mid_val])/2)
            second_val = int(int(second_availability[second_mid_val+1:])/2)
            employee_cost[first_val:second_val] = (second_val-first_val) * [hourly_wage[i]]
            costs.append(employee_cost)
    costs = pulp.makeDict([employees, working_hours],costs,0)
    prob = pulp.LpProblem("IPWorkingSchedule", pulp.LpMinimize)
    schedule = [(e, w) for e in employees for w in working_hours]
    works = pulp.LpVariable.dicts("work",(employees, working_hours), 0, None, pulp.LpBinary)
    prob += pulp.lpSum([works[e][w]*costs[e][w] for (e,w) in schedule]), "CostOfEmployee"

    for e in employees:
        prob += pulp.lpSum([works[e]]) <= max_working_hours[e], "MaxWorkingHours_%s"%e

    for e in employees:
        prob += pulp.lpSum([works[e]]) >= min_working_hours[e], "MinWorkingHours_%s"%e
        
    prob.solve()
    results = {}
    for v in prob.variables():
        results[v.name] = v.varValue
    # The status of the solution is printed to the screen
    #print("Status:", pulp.LpStatus[prob.status])
    # The optimised objective function value is printed to the screen    
    #print("Total Daily COst = ", pulp.value(prob.objective))
    return(results)