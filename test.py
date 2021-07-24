'''
XOR problem
'''

import random as rnd
from tkinter import *
import numpy as np
import copy


pop_Size = 10
inputN = 2 # number is actually one extra due to bias neuron. i.e: if inputN is 2, actuall inputs will be 3 due to bias neuron
hiddenN = 1
outputN = 2
percent_Conn = 1

innovations = {}
max_innovation_ID = 0

maxnodeID = hiddenN + inputN + outputN + 1

for i in range(1, maxnodeID + 1):
    innovations[str(i)] = {}
    for j in range(1, maxnodeID + 1):
        innovations[str(i)][str(j)] = 0 #Initialise empty lookup table for innovations

'''
Node format:
{
    nodeID: int,
    nodeType: "In", "Hidden", "Out" or "BIAS",
    nodeLayer: int,
    activationFunction: str,
    sumInputs: float,
    sumOutputs: float
}

Connections format:
{
    innovationID: int,
    inNodeID: int,
    outNodeID: int,
    weight: float,
    enabled: bool,
    isRecurrent: bool
}

Activation functions:
{
    LIN: Linear activation
    SIN: Sinusoidal activation
}
'''



class Brain:
    fitness = 0

    def getFitness(self, XOR_input_nbr):
        if XOR_input_nbr == 0 or XOR_input_nbr == 2:
            self.fitness += self.getOutput(4)
        elif XOR_input_nbr == 1 or XOR_input_nbr == 3:
            self.fitness += (1 - self.getOutput(4))

    speciesID = -1

    def __init__(self) -> None:
        self.node_Arr = []
        self.conn_Arr = []
        self.activationFunctions = ["LIN", "SIN", "SIG"]
        
        self.initNodes()
        self.initConns()

        #print(self.node_Arr)

        

        self.layer_nbr = 0

        for i in range(len(self.node_Arr)):
            if self.node_Arr[i]["nodeLayer"] > self.layer_nbr:
                self.layer_nbr = self.node_Arr[i]["nodeLayer"] #Get number of layers
       
    def initNodes(self):
        neuronData = {}

        #Add input nodes to node array
        for i in range(inputN):

            neuronData = {
                "nodeID": i+1,
                "nodeType": 0,
                "nodeLayer": 1,
                "activationFunction": "LIN",
                "sumInputs": 0,
                "sumOutputs": 0
            }

            self.node_Arr.append(neuronData)

        #Add a bias node
        neuronData = {
                "nodeID": inputN+1,
                "nodeType": 3,
                "nodeLayer": 1,
                "activationFunction": "LIN",
                "sumInputs": 1,
                "sumOutputs": 1
            }
        
        self.node_Arr.append(neuronData)
        
        #Add output nodes
        for i in range(outputN):

            neuronData = {
                "nodeID": i + inputN+2,
                "nodeType": 2,
                "nodeLayer": 3,
                "activationFunction": "SIG",
                "sumInputs": 0,
                "sumOutputs": 0
            }

            self.node_Arr.append(neuronData)

        #Add hidden nodes
        for i in range(hiddenN):

            neuronData = {
                "nodeID": i + inputN + outputN+2,
                "nodeType": 1,
                "nodeLayer": 2,
                "activationFunction": self.activationFunctions[int(rnd.random() * len(self.activationFunctions))],
                "sumInputs": 0,
                "sumOutputs": 0
            }

            self.node_Arr.append(neuronData) 

    def getInnovationID(self, inNodeID, outNodeID):
        global innovations, max_innovation_ID

        if innovations[str(inNodeID)][str(outNodeID)] == 0:
            max_innovation_ID += 1
            innovations[str(inNodeID)][str(outNodeID)] = max_innovation_ID
            return max_innovation_ID
        else:
            return innovations[str(inNodeID)][str(outNodeID)]

    def initConns(self):
        connectionData = {}

        for i in range(len(self.node_Arr)):
            if hiddenN != 0: #check if hidden layers exist
                if self.node_Arr[i]["nodeType"] == 1: #check for hidden layers
                    for j in range(inputN + 1):
                        inNodeID = self.node_Arr[j]["nodeID"]
                        outNodeID = self.node_Arr[i]["nodeID"]

                        connectionData = {
                            "innovationID": self.getInnovationID(inNodeID, outNodeID), #create connection between input and hidden layer
                            "inNodeID": inNodeID,
                            "outNodeID": outNodeID,
                            "weight": rnd.uniform(-1, 1) * 2,
                            "enabled": True,
                            "isRecurrent": False
                        }

                        if rnd.random() <= percent_Conn: #if random number below percentage chance threshold, connenction is added
                            self.conn_Arr.append(connectionData)

                    for j in range(inputN + 1, inputN + outputN + 1):
                        inNodeID = self.node_Arr[i]["nodeID"] #hidden layer nodeID
                        outNodeID = self.node_Arr[j]["nodeID"] #output layer nodeID

                        connectionData = {
                            "innovationID": self.getInnovationID(inNodeID, outNodeID), #create connection between hidden and output layer
                            "inNodeID": self.node_Arr[i]["nodeID"],
                            "outNodeID": self.node_Arr[j]["nodeID"],
                            "weight": rnd.uniform(-1, 1) * 2,
                            "enabled": True,
                            "isRecurrent": False
                        }

                        if rnd.random() <= percent_Conn: #if random number below percentage chance threshold, connenction is added
                            self.conn_Arr.append(connectionData)
            else:
                if self.node_Arr[i]["nodeType"] == 2: #check for output layers
                    for j in range(inputN + 1):

                        inNodeID = self.node_Arr[j]["nodeID"]
                        outNodeID = self.node_Arr[i]["nodeID"]

                        connectionData = {
                            "innovationID": self.getInnovationID(inNodeID, outNodeID), #create connection between input and hidden layer
                            "inNodeID": inNodeID,
                            "outNodeID": outNodeID,
                            "weight": rnd.uniform(-1, 1) * 2,
                            "enabled": True,
                            "isRecurrent": False
                        }

                        if rnd.random() <= percent_Conn: #if random number below percentage chance threshold, connenction is added
                            self.conn_Arr.append(connectionData)

    def draw_Network(self):
        
        master = Tk()

        canvasWidth = 1000
        canvasHeight = 500

        w = Canvas(master, 
           width=canvasWidth,
           height=canvasHeight) #Init canvas
        w.pack()

        drawNeurons = True

        if drawNeurons:
            
            layers = [[] for i in range(self.layer_nbr)] #create list with a list in it for each layer

            for i in range(len(self.node_Arr)):
                    layers[self.node_Arr[i]["nodeLayer"] -1].append((0,0)) #give default coord to each neuron

            node_radius = 10

            x_pos = 0
            y_pos = 0
            for i in range(self.layer_nbr):
                nodes = len(layers[i])

                x_pos = (canvasWidth/self.layer_nbr)/2 + (canvasWidth/self.layer_nbr) * i
                
                for j in range(nodes):
                    y_pos = (canvasHeight/nodes)/2 + (canvasHeight/nodes) * j
                    layers[i][j] = (x_pos, y_pos) #save neuron coords



            #Put outputs to second position in layers array to make adding connection lines easier
            layers.insert(1, layers[-1])
            layers.pop()     
            

        drawConns = True

        if drawConns:
            for i in range(len(self.conn_Arr)):
                #print(self.conn_Arr[i])
                inNodeID = self.conn_Arr[i]["inNodeID"]
                outNodeID = self.conn_Arr[i]["outNodeID"]
                enabled = self.conn_Arr[i]["enabled"]
                #print(inNodeID, outNodeID)
                inCoords = (0, 0)
                outCoords = (0, 0)
                
                maxElements = 0
                for j in range(len(layers)):
                    prev_sum = maxElements
                    maxElements += len(layers[j])
                #    print("I/O:",inNodeID, outNodeID)
                #    print("M/P:", maxElements, prev_sum)
                    if inNodeID <= maxElements and inNodeID > prev_sum: 
                        inCoords = layers[j][inNodeID-prev_sum-1]
                #        print("IN:", inCoords)
                    if outNodeID <= maxElements and outNodeID > prev_sum:
                        outCoords = layers[j][outNodeID-prev_sum-1]
                #        print("OUT:", outCoords)

                        
                            
                if enabled:
                    w.create_line(inCoords[0], inCoords[1], outCoords[0], outCoords[1], fill="blue", width=3)
                elif not enabled:
                    w.create_line(inCoords[0], inCoords[1], outCoords[0], outCoords[1], fill="red", width=3)
            

            species_txt = "Species: " + str(self.speciesID)
            w.create_text(50, 15, text=species_txt)

        

        layers.append(layers[1]) #reset to normal order
        layers.pop(1)  

        prev_sum_elems = 0
        for i in range(self.layer_nbr):
            if i != 0:
                prev_sum_elems += nodes
            nodes = len(layers[i])
            
            for j in range(nodes):
                x_pos, y_pos = layers[i][j]#save neuron coords
                
                w.create_oval(x_pos - node_radius,y_pos - node_radius,x_pos + node_radius,y_pos + node_radius, fill="black")

                if i == 0:
                    w.create_text(x_pos, y_pos, text=self.node_Arr[prev_sum_elems + j]["nodeID"], fill="white") #displays node layer

                elif i != 0 and i != self.layer_nbr - 1:
                    w.create_text(x_pos, y_pos + 20, text=self.node_Arr[prev_sum_elems + j + outputN]["activationFunction"]) #Displays activations function
                    w.create_text(x_pos, y_pos, text=self.node_Arr[prev_sum_elems + j + outputN]["nodeID"], fill="white")
                elif i == self.layer_nbr - 1:
                    w.create_text(x_pos, y_pos, text=self.node_Arr[inputN + j + 1]["nodeID"], fill="white")



        mainloop()
    
    def Add_Node(self):
        pass
    
    def Add_Connection(self):
        pass
    
    def Mutate(self):
        pass
    
    def Load_Inputs(self, inputs):
        node_Arr_copy = copy.deepcopy(self.node_Arr)
        #Input must be as numpy array type
        for i in range(np.shape(inputs)[0]):
            for j in range(len(self.node_Arr)):

                nodeType = node_Arr_copy[j]["nodeType"]
                if nodeType == 0 :
                    self.node_Arr[j]["sumInputs"] = inputs[i]
                    self.node_Arr[j]["sumOutputs"] = inputs[i]

                    node_Arr_copy[j]["nodeType"] = -1 #Done to prevent setting all inputs to the same node.
                    break
    
    def Activations(self, node):
        act_func = node["activationFunction"]

        if act_func == "LIN": #Linear function
            output = node["sumInputs"]
        elif act_func == "SIN": #sinus function
            output = np.sin(node["sumInputs"])
        elif act_func == "SIG": #Sigmoid function
            output = 1 / ( 1 + np.exp(- node["sumInputs"]))
        else:
            output = 0
        return output

    def Run(self):
        for i in range(1, self.layer_nbr): #go through each layer, starting at layer 2
            layer = i + 1

            for node in self.node_Arr: #Go through each node to check what layer its at
                if node["nodeLayer"] == layer: #if node is at correct layer, save node id
                    outNodeID = node["nodeID"]
                    node["sumInputs"] = 0 #Reset inputs

                    for conn in self.conn_Arr: #find connections that end at the correct node id
                        if conn["outNodeID"] == outNodeID:
                            connWeight = conn["weight"]
                            inNodeID = conn["inNodeID"]

                            for inNode in self.node_Arr:
                                if inNode["nodeID"] == inNodeID:
                                    node["sumInputs"] += inNode["sumOutputs"] * connWeight
                    
                    node["sumOutputs"] = self.Activations(node)

    def getOutput(self, nodeID):
        for node in self.node_Arr:
            if node["nodeID"] == nodeID:
                return node["sumOutputs"]
          

class Species:
    pass


'''brain = Brain()
brain.Load_Inputs(np.array([0, 1]))
#print(brain.node_Arr)
brain.Run()'''


all_pop_members = []
for i in range(pop_Size):
    temp = Brain()
    all_pop_members.append(temp)

input_list = [[0, 1], [0, 0], [1, 0], [1, 1]]

for i in range(len(input_list)):
    for pop_mem in all_pop_members:
        pop_mem.Load_Inputs(np.array(input_list[i]))
        pop_mem.Run()
        #print(pop_mem.node_Arr)
        pop_mem.getFitness(i)

for i in range(len(all_pop_members)):
    print(all_pop_members[i].conn_Arr)
    print("Network", i, "\nFitness:", all_pop_members[i].fitness, "\n")


#Speciation
c1, c3 = 1, .4

comp_diff = 0
disjoinAndExcessGenes = 0
avgWeightDiffOfMatchingGenes = 0
species = 0
speciate_threshold = 2

### ONLY WORKS IF CONNECTIONS ARE SORTED BY INNOVATION ID
### WE CONSIDER DISJOINT GENES AND EXCESS GENES TOGETHER
### ALL SPECIES NEED TO BE RESET TO -1 BEFORE USE
for j in range(len(all_pop_members)):
    #j = int(rnd.random() * len(all_pop_members)) #get random pop member

    if all_pop_members[j].speciesID == -1: #Check if that current pop member doesnt already got a species

        comp_diff = 0
        species += 1
        print("Species",species)
        all_pop_members[j].speciesID = species

        for i in range(len(all_pop_members)): #Iterate through all other pop members

            if all_pop_members[i].speciesID == -1 : #Check if that current pop member doesnt already got a species

                disjoinAndExcessGenes = 0
                weightDiffSum = 0
                commonGenes = 1e-5
                n = max(len(all_pop_members[i].conn_Arr),len(all_pop_members[j].conn_Arr)) + 1e-5

                for conn_A in all_pop_members[j].conn_Arr: #Iterate through biggest connection array of the two pop members
                    
                    if conn_A["enabled"] == False:
                        continue

                    isCommon = False
                    for conn_B in all_pop_members[i].conn_Arr:

                        if conn_B["enabled"] == False:
                            continue

                        if conn_A == all_pop_members[j].conn_Arr[0]: #check for disjoint genes in B network on first iteration
                            if conn_A["innovationID"] == conn_B["innovationID"]:
                                commonGenes += 1
                                weightDiffSum += abs(conn_A["weight"] - conn_B["weight"])
                                isCommon = True
                                continue

                            if conn_A["innovationID"] != conn_B["innovationID"]:
                                disjoinAndExcessGenes += 1
                        
                        else: #If not first iteration, break instead of continue 
                            if conn_A["innovationID"] == conn_B["innovationID"]:
                                    commonGenes += 1
                                    weightDiffSum += abs(conn_A["weight"] - conn_B["weight"])
                                    isCommon = True
                                    break
                    
                    if isCommon:
                        continue
                    else:
                        disjoinAndExcessGenes += 1

                comp_diff = (c1 * disjoinAndExcessGenes / n) + (weightDiffSum / commonGenes)
                

                if comp_diff < speciate_threshold:
                    all_pop_members[i].speciesID = species
                    all_pop_members[i].draw_Network()


