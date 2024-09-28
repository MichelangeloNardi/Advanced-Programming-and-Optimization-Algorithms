# add import of pulp and other things you need here
import pulp

def ex1():
    retval = {}
    retval["x"] = None
    retval["y"] = None
    retval["obj"] = None
    retval["tight_constraints"] = [ None ]
    # Insert your code below:
    
    problem = pulp.LpProblem('LPproblem', pulp.LpMinimize)
  
    x = pulp.LpVariable('x')
    y = pulp.LpVariable('y')
    
    problem += 122 * x + 143 * y, 'Objective Function'
    
    problem += x >= -10, '1'
    problem += y <= 10, '2'
    problem += 3 * x + 2 * y <= 10, '3'
    problem += 12 * x + 14 * y >= -12.5, '4'
    problem += 2 * x + 3 * y >= 3, '5'
    problem += 5 * x - 6 * y >= -100, '6'
    
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # Return retval dictionary
    retval["x"] = x.value()
    retval["y"] = y.value()
    retval["obj"] = pulp.value(problem.objective)
    
    
    retval["tight_constraints"] = []
    
    for i, constraint in enumerate(problem.constraints, start = 1):
        if problem.constraints[constraint].slack == 0:
            retval["tight_constraints"].append(i)
    return retval

def ex2():
    retval = {}
    retval['x1'] = None
    retval['x2'] = None
    retval['x3'] = None
    retval['x4'] = None
    retval['x5'] = None
    retval['x6'] = None
    retval['obj'] = None
    # Insert your code below:
    problem = pulp.LpProblem("LPproblem", pulp.LpMaximize)
    
    x1 = pulp.LpVariable('x1', lowBound = 0)
    x2 = pulp.LpVariable('x2', lowBound = 0)
    x3 = pulp.LpVariable('x3', lowBound = 0)
    x4 = pulp.LpVariable('x4', lowBound = 0)
    x5 = pulp.LpVariable('x5', lowBound = 0)
    x6 = pulp.LpVariable('x6', lowBound = 0)
    
    payoff = pulp.LpVariable('payoff')
    
    problem += payoff
    
    problem += x1 + x2 + x3 + x4 + x5 + x6 == 1
    
    problem += payoff <= -2*x2 + x3 + x4 + x5 + x6
    problem += payoff <= 2*x1 -2*x3 + x4 + x5 + x6
    problem += payoff <= -x1 + 2*x2 -2*x4 + x5 + x6
    problem += payoff <= -x1 -x2 + 2*x3 -2*x5 + x6
    problem += payoff <= -x1 -x2 - x3 + 2*x4 -2*x6
    problem += payoff <= -x1 -x2 - x3 - x4 + 2*x5
    
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
 

    # return retval dictionary
    retval["x1"] = x1.value()
    retval["x2"] = x2.value()
    retval["x3"] = x3.value()
    retval["x4"] = x4.value()
    retval["x5"] = x5.value()
    retval["x6"] = x6.value()
    
    retval["obj"] = pulp.value(problem.objective)
    
    
    return retval


def ex3():
    retval = {}
    retval['obj'] = None
    retval['x1'] = None
    # there should be retval['xi'] for each company number i
    # Insert your code below:
    
    problem = pulp.LpProblem("LPProblem", pulp.LpMinimize)
    
    variables = []
    for i in range(69):
        variables.append(pulp.LpVariable(f'x{i+1}', lowBound = 0))
    
    problem += sum(variables)
    
    contracts = []
    with open("hw1-03.txt") as file:
        for line in file:
            contracts.append(line.split())
            problem += variables[int(contracts[-1][0]) -1] + variables[int(contracts[-1][1]) -1] >= 2
        
    problem.solve()

    # return retval dictionary
    retval['obj'] = pulp.value(problem.objective)
    for i in range(69):
        retval[f'x{i+1}'] = variables[i].value()
    
    return retval

print("hello world")
