import numpy as np
import csv

LEARNING_RATE = 0.01
NODES = 256

#sigmoid
def activation(x, derivative=False):
    if derivative:
        return x * (1.0 - x)
    return 1/(1+np.exp(-x))

def softmax():
    pass

class NeuralNetwork:
    def __init__(self, _input = 784, neurons=256, output=10):
        
        #Weights from input layer to the hidden layer
        self.weights1   = np.random.rand(_input, neurons)          #Initiate 784x256 vector filled with random videos between 0-1

        #Weights from hidden to output layer
        self.weights2   = np.random.rand(neurons, output)          #Initiate 256x10 vector filled with random videos between 0-1




    def propagate_forward(self, x):
        # Jag vill att x ska ha shape (784,1)

        self.layer1 = activation(np.dot(x, self.weights1),False)
        self.output = activation(np.dot(self.layer1, self.weights2),False)
        #print(np.shape(x))
        #print(np.shape(self.weights1))
        #print(self.weights1)
        #print(self.layer1)
        #print(self.output)

    def backprop(self, x, target):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(target - self.output) * activation(self.output)))
        d_weights1 = np.dot(self.x.T,  (np.dot(2*(target - self.output) * activation(self.output), self.weights2.T) * activation(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2

def loadAllData():

    data = []
    
    with open('assignment5.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            data.append([int(i) for i in row])
    
    return data


if __name__ == "__main__":
    #Load all the data from the csv file
    all_data = loadAllData()

    # 70 % of all_data for training
    training = all_data[0:int(len(all_data)*0.7)]

    # 10 % of all_data for validation
    validation = all_data[int(len(all_data)*0.7):int(len(all_data)*0.8)]

    # 20 % of all_data for testing
    test = all_data[int(len(all_data)*0.8):len(all_data)]

    # Initiate neural network
    nn = NeuralNetwork()

    for t in training:
        #Create a target vector and set the label index to 1
        target = np.zeros(10)
        target[t[0]] = 1
        row = [1, 0, None]
        nn.propagate_forward(t[1:])
        #nn.backprop(training[1:], target)
        print("En iteration")
    # for i in range(int(len(all_data)*0.7)):
    #     nn.feedforward(training[i][1:])
    #     nn.backprop()


    print(nn.output)


