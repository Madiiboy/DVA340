import numpy as np
import csv
import matplotlib.pyplot as plt

LEARNING_RATE = 0.1
NODES = 128

class NeuralNetwork:
    def __init__(self, network_shapes, learning_rate):
        
        # Create shapes of the weights
        w_shapes = [(x, y) for x, y in zip(network_shapes[1:], network_shapes[:-1])]

        # Save all the different layers shapes
        self.shapes = network_shapes

        # Initialize all the weights with a random value between -1 and 1
        self.weights = [np.random.standard_normal(s) for s in w_shapes]

        # Vector for all the biases
        self.biases = [np.zeros((i, 1)) for i in network_shapes[1:]]

        self.learning_rate = learning_rate

    @staticmethod
    def sigmoid(x, derivative=False):
        if derivative:
            return x * (1.0 - x)
        return 1/(1+np.exp(-x))

    @staticmethod
    def softmax(x, derivative=False):
        if derivative:
            return 1
        return np.divide(np.exp(x), (sum([np.exp(i) for i in x])))

    def propagate_forward(self, data):
        #print(data.shape)
        #print(self.weights[-1].shape)
        outputs = []
        # For each weight and bias run acivation function
        for weight, bias in zip(self.weights[:-1], self.biases[:-1]):
            data = self.sigmoid(np.matmul(weight, data) + bias)
            outputs.append(data)

        # Softmax activation function for the output layer
        data = self.softmax(np.matmul(self.weights[-1], data) + self.biases[-1])        
        outputs.append(data)

        return outputs

    def backpropagation(self, data, outputs, target):
    
        #Create a target vector filled with 0, except the labeled index    
        target_vector = np.array([1.0 if i == target else 0.0 for i in range(self.shapes[-1])]).reshape(self.shapes[-1], 1)

        errors = []

        #Initiate our errors list with an empty list for each output
        for i in range(len(outputs)):
            errors.append([])

        # Propagate backwards
        for i in reversed(range(len(outputs))):

            o = outputs[i]

            # If we are at the output layer
            if i == len(outputs) - 1:

                error = np.subtract(target_vector, o)
                # Calculate errors for nodes
                errors[i] = np.multiply(self.softmax(o, True), error)
            else:
                index = i + 1

                # calculate errors
                error = np.matmul(self.weights[index].T, errors[index])
                delta = np.multiply(error, self.sigmoid(o,True))
                errors[i] = delta

        for i in reversed(range(len(outputs))):

            # The input is the previous layers output or the input data at the input layer
            data_in = data.reshape((self.shapes[0], 1)) if i == 0 else outputs[i - 1]

            # Calculate delta for all weights
            delta_w = np.multiply(np.multiply(errors[i], data_in.T), self.learning_rate)
            # Calculate delta for all biases
            delta_b = np.multiply(np.multiply(errors[i], 1), self.learning_rate)

            # Update with the new values
            self.weights[i] = np.add(self.weights[i], delta_w)
            self.biases[i] = np.add(self.biases[i], delta_b)

    def training(self, training_data):
        print("Training initiated")
        accurate_guesses = 0
        data = []
        labels = []
        for d in training_data:
            data.append(d[1:])
            labels.append(d[0])

        #np.divide(data,255) normalizes the data
        for (i, (t, label)) in enumerate(zip(np.divide(data,255), labels)):
            arr = np.array(t)
            outputs = self.propagate_forward(arr.reshape(self.shapes[0],1))
            #print(outputs[-1])
            #Get the index of best guess
            guess = np.argmax(outputs[-1])
            
            if guess == label:
                accurate_guesses = accurate_guesses + 1

            # Backpropagate through the network
            self.backpropagation(arr, outputs, labels[i])

        # Return the accuracy of the network
        print(accurate_guesses)
        return accurate_guesses / len(training_data)

    def validate(self, validation_data):
        print("Validation initiated")
        accurate_guesses = 0
        data = []
        labels = []
        for d in validation_data:
            data.append(d[1:])
            labels.append(d[0])

        # print(len(validation_data))
        for (i, (t, label)) in enumerate(zip(np.divide(data,255), labels)):
            arr = np.array(t)
            outputs = self.propagate_forward(arr.reshape(self.shapes[0],1))
            #Get the index of accurate guess
            guess = np.argmax(outputs[-1])
            
            if guess == label:
                accurate_guesses = accurate_guesses + 1

        # Return the accuracy of the network
        # print(accurate_guesses)
        print(accurate_guesses, "out of", len(validation_data))
        return accurate_guesses / len(validation_data)

    def test(self, test_data):
        print("Testing initiated")
        accurate_guesses = 0
        data = []
        labels = []
        for d in test_data:
            data.append(d[1:])
            labels.append(d[0])


        result_deviation = np.zeros(10)
        amount_of_each = np.zeros(10)
        # print(len(validation_data))
        for (i, (t, label)) in enumerate(zip(np.divide(data,255), labels)):
            # print(label)
            arr = np.array(t)
            outputs = self.propagate_forward(arr.reshape(self.shapes[0],1))
            #Get the index of accurate guess
            guess = np.argmax(outputs[-1])
            amount_of_each[int(label)] += 1

            if guess == label:
                result_deviation[guess] += 1
                accurate_guesses = accurate_guesses + 1

        percentage = np.divide(result_deviation, amount_of_each)
        print(percentage)
        #objects = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        #y_pos = np.arange(len(objects))
        #plt.bar(y_pos, percentage, align='center', alpha=0.5)
        #plt.xticks(y_pos, objects)
        #plt.ylabel('Correct guesses')
        #plt.xlabel('Digit')
        #plt.show()

        # Return the accuracy of the network
        # print(accurate_guesses)
        print(accurate_guesses, "out of", len(test_data))
        return accurate_guesses / len(test_data)

def loadAllData():

    data = []
    
    with open('assignment5.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            # Normalize and append data
            data.append([float(i) for i in row])
    
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

    network_shapes = [784, NODES, 10]

    # Initiate neural network
    nn = NeuralNetwork(network_shapes, LEARNING_RATE)
    training_sets = []
    index = 1
    for i in range(0, len(training), int(len(training)/10)):
        training_sets.append(training[i:int(len(training)/10)*index])
        index += 1

    training_results = []
    validation_results = []
    for sets in training_sets:
        training_results.append(nn.training(sets))
        validation_results.append(nn.validate(validation))
    print(training_results)
    print(validation_results)

    plt.plot(range(len(validation_results)), validation_results)
    plt.xlabel('Validation')
    plt.ylabel('Accuracy')
    plt.show()

    #print(nn.training(training))
    #Divide the training set by 10

    #print(nn.validate(validation))
    print(nn.test(test))


    


