# Author:  Allen Best

# triads.py identifies all of the triads in the graph from a given csv
# To run from terminal window:   python3 triads.py 
# Once run, enter name of csv file within folder

import networkx as nx
from itertools import combinations as comb
from os import path
import datetime

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

# get file name from and determine if it is valid 
csvFileName = str(input("Input your csv file name: "))
if(not path.exists(csvFileName)):
    raise Exception("Sorry, this is not a valid file name")

# read file and parse into graph
Data = open(csvFileName, "r")
Graphtype = nx.Graph()
G = nx.parse_edgelist(Data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))

# find total triangles and edges
full_triangles_list = [edge for edge in nx.enumerate_all_cliques(G) if len(edge) == 3]
total_triangles = len(full_triangles_list)
edges_list = list(G.edges.data("weight", default=1))
total_edges = len(edges_list)

# find the total amount of positive and negative edges
positive = 0
negative = 0
for x in edges_list:
    if x[2] > 0: positive += 1
    if x[2] < 0: negative += 1

# calculate the probability for each edge to be positive or negative
probOfPos = positive / total_edges
probOfNeg = 1 - (positive/total_edges)	

# calculate the expected probability for each edge to be a type
probOfTTT = (probOfPos * probOfPos * probOfPos)
probOfTTD = (probOfPos * probOfPos * probOfNeg * 3)
probOfTDD = (probOfPos *probOfNeg *probOfNeg * 3)
probOfDDD = (probOfNeg * probOfNeg * probOfNeg)

# finds the weight of the edges
weight = nx.get_edge_attributes(G, 'weight')

# determines the list of all triads
tri_list = []
for tri in full_triangles_list:
    tri_list.append(list(map(lambda edge: (edge, weight[edge]), comb(tri, 2))))

# sets total amounts of triad types to 0
totalTTT = totalTTD = totalTDD = totalDDD = 0

# loops through all triads to find the types of each
for triad in tri_list:
    # determines the weight of each edge in a triad
    weightOfEdge1, weightOfEdge2, weightOfEdge3 = triad[0][1], triad[1][1], triad[2][1]

    # find total triads of each type based on the weights
    if weightOfEdge1==1 and weightOfEdge2==1 and weightOfEdge3==1: totalTTT = totalTTT +1
    if(weightOfEdge1==1 and weightOfEdge2==1 and weightOfEdge3==-1) or (weightOfEdge1==-1 and weightOfEdge2==1 and weightOfEdge3==1) or (weightOfEdge1==1 and weightOfEdge2==-1 and weightOfEdge3==1): totalTTD=totalTTD+1
    if(weightOfEdge1==-1 and weightOfEdge2==-1 and weightOfEdge3==1) or (weightOfEdge1==1 and weightOfEdge2==-1 and weightOfEdge3==-1) or (weightOfEdge1==-1 and weightOfEdge2==1 and weightOfEdge3==-1): totalTDD =totalTDD + 1
    if weightOfEdge1==-1 and weightOfEdge2==-1 and weightOfEdge3==-1: totalDDD=totalDDD+1

# output results of data
print("RESULTS FOR FILE: ", csvFileName)
print(" ")

print("Number of Triangles: ", total_triangles)
print("TTT:\t" + str(totalTTT) + "\t\tEdges Used: " + str(total_edges))
print("TTD:\t" + str(totalTTD) + "\t\tTrust Edges: " + str(positive) + "\t\tProbability %: {:.2f}".format(positive/total_edges * 100))
print("TDD:\t" + str(totalTDD) + "\t\tDistrust Edges: " + str(negative) + "\tProbability %: {:.2f}".format((1 - (positive/total_edges)) * 100))
print("DDD:\t" + str(totalDDD) + "\t\tTotal: " + str(total_edges))
print(" ")

print("Expected Distubution\t\tActual Distibution")
print(" ")
print("\tPercent Number\t\t\tPercent Number")
print(" ")
print("TTT:\t{:.2f}".format(probOfTTT * 100) + "\t{:.2f}".format(probOfTTT * total_triangles) + "\t\tTTT:\t{:.2f}".format(totalTTT / total_triangles * 100) + "\t" + str(totalTTT))
print("TTD:\t{:.2f}".format(probOfTTD * 100) + "\t{:.2f}".format(probOfTTD * total_triangles) + "\t\tTTD:\t{:.2f}".format(totalTTD / total_triangles * 100) + "\t" + str(totalTTD))
print("TDD:\t{:.2f}".format(probOfTDD * 100) + "\t{:.2f}".format(probOfTDD * total_triangles) + "\t\tTDD:\t{:.2f}".format(totalTDD / total_triangles * 100) + "\t" + str(totalTDD))
print("DDD:\t{:.2f}".format(probOfDDD * 100) + "\t{:.2f}".format(probOfDDD * total_triangles) + "\t\tDDD:\t{:.2f}".format(totalDDD / total_triangles * 100) + "\t" + str(totalDDD))
print("Total:\t100\t{:.1f}".format(probOfTTT + probOfTTD + probOfTDD + probOfDDD) + "\t\tTotal\t" + str(100) + "\t" + str(total_triangles))	

print (" ")
now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))