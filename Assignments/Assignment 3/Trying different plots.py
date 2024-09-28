import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


s = {'s_0': 9000.0, 's_1': 12000.0, 's_2': 0.0, 's_3': 4800.0, 's_4': 1800.0, 's_5': 5400.0, 's_6': 9600.0, 's_7': 10800.0, 's_8': 18000.0, 's_9': 600.0, 's_10': 21000.0, 's_11': 19200.0, 's_12': 16200.0, 's_13': 14400.0, 's_14': 12600.0, 's_15': 6600.0, 's_16': 2400.0}

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
plt.xticks(ticks1, ticks)


fig, ax = plt.subplots(figsize=(12, 8))
plt.legend()
plt.show()