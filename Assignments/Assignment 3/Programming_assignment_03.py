from pulp import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

preparation_time = []
baking_time = []
deadline = []

# open the pastry dataset
with open("Pastry_data.txt") as file:
    for line in file:
        line = line.split()
        preparation_time.append(int(line[1]))
        baking_time.append(int(line[3]))
        deadline.append(int(line[2]))


#Define the LP problem
problem = LpProblem("Bakery_problem", LpMinimize)

#Variables
start_time = []
for i in range(17):
    start_time.append(LpVariable(f"start time of pastry {i}", lowBound= 0, cat="integer"))

x = {}
for i in range(17):
    for j in range(17):
        if i < j:
            x[i, j] = LpVariable(f"{i} is in oven before {j} ", cat="Binary")

y = LpVariable("y", lowBound= 0)

#Objctive function
problem += y

#Constraint
M = 3600*24
for i in range(17):
    problem += start_time[i] >= preparation_time[i]
    problem += start_time[i] + baking_time[i] <= deadline[i]
    problem += y >= start_time[i] + baking_time[i]

    for j in range(17):
        if i < j:
            problem +=  start_time[i] + baking_time[i] <= start_time[j] + M*x[i, j]
            problem += start_time[j] + baking_time[j] <= start_time[i] + M*(1 - x[i, j])
            
    
#Solve the problem
problem.solve()

print(problem.objective.value())

if problem.status == 1:
    s = {}
    for i in range(17):
        s[f's_{i}'] = start_time[i].value()
    
    print(s)
else:
    print('Optimization failed')


##Plotting

#List of Pastry correct cooking order
sorted_indices = [int(item[0].split('_')[1]) for item in sorted(s.items(), key=lambda x: x[1])]

#Transform seconds in minutes and put in correct order

s = {k: v/60 for k, v in s.items()}
s_time = np.array([v[1] for v in s.items()])
s_time = np.array([s_time[i] for i in sorted_indices])

preparation_time = [preparation_time[i] for i in sorted_indices]
preparation_time = np.array(preparation_time)
preparation_time = preparation_time/60

baking_time = [baking_time[i] for i in sorted_indices]
baking_time = np.array(baking_time)
baking_time = baking_time/60

end_time = s_time + baking_time

deadline = [deadline[i] for i in sorted_indices]
deadline = np.array(deadline)
deadline = deadline/60

waiting_time = s_time - preparation_time


#List of names of pastries
names = []
for i in range(17):
    names.append(f'{i}')
names = [names[i] for i in sorted_indices]


# #Plotting
# plt.barh(names, preparation_time, label= 'Preparation')
# plt.barh(names, baking_time, left= s_time, label= 'Baking', edgecolor= 'red')
# plt.barh(names, deadline - end_time, left= end_time, label= 'waiting for customer')
# plt.barh(names, waiting_time, left=preparation_time, label= 'Waiting for oven', color=(1.0, 1.0, 0.48))

# Plotting
fig, ax = plt.subplots()
rects1 = ax.barh(names, preparation_time, label='Preparation', color= (0.2, 0.5, 0.8))
rects2 = ax.barh(names, waiting_time, left=preparation_time, label='Waiting for oven', color=(1.0, 1.0, 0.48))
rects3 = ax.barh(names, baking_time, left=s_time, label='Baking', color='orange')
rects4 = ax.barh(names, deadline-end_time, left=end_time, label='Waiting for customer', color=(0.3, 0.7, 0.3))

# Set the edge color for critical pastries
for i in range(17):
    if deadline[i] - end_time[i] == 0:
        rects3[i].set_edgecolor('red')


plt.xlabel('Time')
plt.ylabel('Pastries')
plt.title('Baking schedule')

#hours on the x-axis
ticks = np.arange(0, 500, 30)
ticks = list(ticks)
for i in range(len(ticks)):
    if ticks[i] % 60 == 0:
        ticks[i] = f'0{ticks[i]//60}:00'
    else:
        ticks[i] = f'0{ticks[i]//60}:{ticks[i] % 60}'
ticks1 = list(np.arange(0, 500, 30))
plt.xticks(ticks1, ticks, rotation=90)

plt.legend()
plt.show()