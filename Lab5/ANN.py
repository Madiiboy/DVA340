import numpy as np
import matplotlib.pyplot as plot
import csv
import copy
import random

# TODO: 
    # Apply ANN with backpropagation as a learning algorithm to classify correctly the numbers
    # Input layer
    # Hidden layer, räcker med ett
    # Output layer 0-9
    # Weights, mellan input och hidden, hidden och output lagret
    # Bias
    # Activation function, sigmoid
    # Feed forward, sen backpropagation

class ANN:
    def __init__(self, x, y):
        self.input = x
        self.y = y
        self.weights1 = np.random.rand(len(self.input),4)
        self.weights2 = np.random.rand(4,1) 
        self.output = np.zeros(y.shape) #MNIST 0-9???

    def feedForward(self):
        self.layer1 = activation(np.dot(self.input, self.weights1))
        self.output = activation(np.dot(self.layer1, self.weights2))

    def backPropagation(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * activation(self.output, True)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * activation(self.output, True), self.weights2.T) * activation(self.layer1, True)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2

class MNIST:
    def __init__(self, label, data):
        self.label = label
        self.data = data

#sigmoid
def activation(x, derivative=False):
    if derivative:
        return x * (1.0 - x)
    return 1/(1+np.exp(-x))

def loadAllData():

    data = []
    
    with open('assignment5.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)

    del data[0]
    
    labeled_data = []
    for d in data:
        labeled_data.append(MNIST(d[0], d[1::]))

    return labeled_data

if __name__ == "__main__":
    all_data = loadAllData()

    # 70 % of all_data for training
    training = []
    for i in range(int(len(all_data)*0.7)):
        training.append(all_data[i])

    # 10 % of all_data for validation
    validation = []
    for i in range(int(len(all_data)*0.7), int(len(all_data)*0.8)):
        validation.append(all_data[i])

    # 20 % of all_data for testing
    test = []
    for i in range(int(len(all_data)*0.8), len(all_data)):
        test.append(all_data[i])

    print(len(all_data[0].data))
    ann = ANN(len(all_data[0].data), 10)

    for d in training:




    # print(len(all_data))
