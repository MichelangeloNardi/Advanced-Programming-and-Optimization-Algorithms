import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# images = []

# for i in range(16):
#     with open(f"C:/Users/nardi/Desktop/Università/BOCCONI/Secondo anno/Semestre 2.2/Advanced programming/Programming assignments/Assignment 2/files/P{i}.txt", "r") as file:
#         lines = file.readlines()
#         image = np.array([list(map(int, line.strip())) for line in lines])
#         images.append(image)



#Opening the files

def openfile(filename):
    image = [[] for i in range(10)]
    with open(f"C:/Users/nardi/Desktop/Università/BOCCONI/Secondo anno/Semestre 2.2/Advanced programming/Programming assignments/Assignment 2/files/{filename}") as file:
        for i, line in enumerate(file):
            for pixel in line[:-1]:
                image[i].append(int(pixel))
    return np.array(image)


images = []
for i in range(1, 16):
    newfile = openfile(f"P{i}.txt")
    images.append(newfile)
images = np.array(images)


#Normalizing

def sum_pixels(image):
    tot = 0
    for j in range(10):
        tot += sum(image[j])
    return tot

list_sumpixels = []
for i in range(15):
    list_sumpixels.append(sum_pixels(images[i]))



for i in range(15):
    if sum_pixels(images[i]) == 80:
        images[i] = images[i]*39
    else:
         images[i] = images[i]*80

list_sumpixels = []
for i in range(15):
    list_sumpixels.append(sum_pixels(images[i]))



#Wasserstein function

def Wasserstein(image1, image2):

    G = nx.DiGraph()
    for i in range(10):
        for j in range(80):
            if image1[i][j] != 0:
                G.add_node((1, i, j), demand = -image1[i][j])
    for i in range(10):
        for j in range(80):
            G.add_node((2, i, j), demand = image2[i][j])

    for i in range(10):
        for j in range(80):
            if image1[i][j] != 0:
                for k in range(10):
                    for l in range(80):
                        column_distance = l - j if l - j >= 0 else 80 - j + l
                        G.add_edge((1, i, j), (2, k, l), weight = column_distance, capacity = image2[k][l])

    
    flow_dict = nx.min_cost_flow(G)
    min_cost = nx.cost_of_flow(G, flow_dict)

    return min_cost



# Computing all the distances from P1

distance_fromP1 = []
for i in range(15):
    distance = Wasserstein(images[0], images[i])
    distance_fromP1.append((distance, i))

sorted_distances = sorted(distance_fromP1)
print([x[1] + 1 for x in sorted_distances])

