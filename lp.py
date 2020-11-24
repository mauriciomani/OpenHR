import pulp 

'''plants = ["CDMX", "Monterrey", "Guadalajara", "Queretaro", "Merida"]
#includes list of list with maximum units to be supplied and fixed_cost
supply_fixed_cost = [[5000, 10000], [3500, 12000], [2500, 8000], [1000, 5000], [1500, 6000]]
plants_supply_fixed_cost = dict(zip(plants, supply_fixed_cost))

stores = ["Campeche", "Aguscalientes", "Cuernavaca", "Xalapa"]
demand = [2000, 3000, 5500, 3000]
stores_demand = dict(zip(stores, demand))

#columns are stores and rows are plants. Lets pretend cost of transporation
cost_matrix = [[100, 80, 10, 60],
               [120, 80, 80, 80], 
               [100, 22, 60, 150], 
               [80, 80, 40, 50], 
               [30, 150, 200, 100]]

#create all possible routes
routes = [(p, s) for p in plants for s in stores]

#splitdict is a function of pulp, thoug we are  going to use it, I recommend creating separate dictionaries since the beginning
(max_supply, fixedCost) = pulp.splitDict(plants_supply_fixed_cost)

#makedict 0 value can be any value different than None 
#create dictionary of dictionaries with main key, the plants and each dictionary with Key stores and value the cost.  
costs = pulp.makeDict([plants,stores], cost_matrix, 0)

#flow on the arcs
flow = pulp.LpVariable.dicts("Route", (plants, stores), 0, None, pulp.LpInteger)

build = pulp.LpVariable.dicts("BuildPlant", plants, 0, 1, pulp.LpInteger)

prob = pulp.LpProblem("ComputerPlantProblem", pulp.LpMinimize)

prob += pulp.lpSum([flow[p][s] * costs[p][s] for (p,s) in routes]) + pulp.lpSum([fixedCost[p] * build[p] for p in plants]), "totalCosts"

for p in plants:
    prob += pulp.lpSum([flow[p][s] for s in stores]) <= max_supply[p]*build[p], "SumProductOutPlant %s"%p

for s in stores:
    prob += pulp.lpSum([flow[p][s] for p in plants]) >= stores_demand[s], "SumProductIntoStore %s"%s

prob.writeLP("milp_prueba.lp")
prob.solve()
print("Estado: ", pulp.LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total Cost: ", pulp.value(prob.objective))'''

plants = []
stores = []
cost_matrix = []
max_supply = dict()
fixed_cost = dict()
demand = dict()

while True:
    value = input("Plant option: ")
    if value == "":
        break
    else:
        plants.append(value)

for p in plants:
    max_supp = input("Maximum supply by plant " + p + " : ")
    cost = input("Fixed cost for plant " + p + " : ")
    max_supply[p] = max_supp
    fixed_cost[p] = cost

while True:
    value = input("Current stores: ")
    if value == "":
        break
    else:
        stores.append(value)

for s in stores:
    dem = input("Demand by store " + s + " : ")
    demand[s] = dem

for p in plants:
    var_costs_plant = []
    for s in stores:
        var_cost = input("Variable cost coming from plant " + p + " and store " + s + " : ") #can be distance
        var_costs_plant.append(var_cost)
    cost_matrix.append(var_costs_plant)

print("Número de arcos en la red (sistema): " + str(len(plants)*len(stores)))

print(plants)
print(max_supply)
print(fixed_cost)
print("--------------------------------")
print(stores)
print(demand)
print("--------------------------------")
print(cost_matrix)