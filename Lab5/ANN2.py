import numpy as np
import csv
import math

INPUT_SIZE = 784
weight1=np.array([])
weight2=np.array([])

class ANN:
    def __init__(self, x, y, learning_rate):
        global weight1, weight2

        self.x=x
        self.y=y
        self.lr = learning_rate
        self.output=np.zeros(y.shape)
        
        #Weights between input and hidden layer
        self.weights1=np.random.rand(self.x.shape[1], 4)
        #Weights between         
        self.weights2=np.random.rand(4, 1)

    def sigmoid(self, x, derivate=False):
        if derivate:
            return x*(1-x)
        return np.exp(x)/(1+np.exp(x))
    
    def feedforward(self):
        global weight1, weight2

        self.layer1=self.sigmoid(np.dot(self.x, weight1))
        self.output=self.sigmoid(np.dot(self.layer1, weight2))

    def backprop(self):
        global weight1, weight2

        d_weights2=np.dot(self.layer1.T, 2*(self.y-self.output)*self.sigmoid(self.output, True))
        
        d_weights1 = np.dot(self.x.T,  (np.dot(2*(self.y - self.output)*self.sigmoid(self.output, True), self.weights2.T)*self.sigmoid(self.layer1, True)))

        self.weights1 += d_weights1
        weight1=self.weights1[:]
        
        self.weights2 += d_weights2
        weight2=self.weights2[:]


class MNIST:
    def __init__(self, label, data):
        self.label = label
        self.data = data


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

    #train = ANN(#input, output, 0.01)

    for i in range(1500):
        ANN.feedforward(train)
        ANN.backprop(train)

