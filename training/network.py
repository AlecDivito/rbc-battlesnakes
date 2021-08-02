import numpy as np
import random

class Network:

    def __init__(self, inputNodes, hiddenNodes, outputNodes) -> None:
        self.inputNodes = inputNodes
        self.hiddenNodes = hiddenNodes
        self.outputNodes = outputNodes
        self.inputLayer = np.random.rand(hiddenNodes, inputNodes + 1, dtype=np.float32)
        self.hiddenLayer = np.random.rand(hiddenNodes, hiddenNodes + 1, dtype=np.float32)
        self.outputLayer = np.random.rand(outputNodes, hiddenNodes + 1, dtype=np.float32)
    
    def calculateOutput(self, inputs):
        """
        Takes an `inputs`, which is an array of floats (np.float32[])

        returns array of floats
        """
        # Input layer -> hidden layer
        inputBais = self.addBias(inputs) # Add bias
        hiddenInput = np.dot(self.inputLayer, [inputBais]) # Apply layer one weights to the inputs
        hiddenOutputs = self.activate(hiddenInput) # Apply activation function

        # Hidden layer -> output layer
        hiddenOutputsBias = self.addBias(hiddenOutputs) # Add bias
        hiddenInput2 = np.dot(self.hiddenLayer, hiddenOutputsBias) # Apply weights
        hiddenOutputs2 = self.activate(hiddenInput2) # Apply activation

        # Output layer
        hiddenOutputsBias2 = self.addBias(hiddenOutputs2)
        outputInputs = np.dot(self.outputLayer, hiddenOutputsBias2)
        outputs = self.activate(outputInputs)

        return np.squeeze(np.asarray(outputs))

    def mutate(self, rate):
        """
        mutation function for the genetic algorithm. Mutates each weight inside
        of each matrix. Rate should be a float value between 0 and 1.

        Returns nothing
        """
        # Ok this is a weird damn statements so lets walk through it together:
        # 1. If we randomly choose to mutate a variable, than lets do it otherwise...
        # 2. Make sure that the value is between -1 and 1
        # 3. If value is between -1 and 1, than just return it, it's fine
        mutateFunc = lambda i: random.gauss()/5 if (random.random() < rate) else 1 if i > 1 else -1 if i < -1 else i
        self.inputLayer = np.vectorize(mutateFunc)(self.inputLayer)
        self.hiddenLayer = np.vectorize(mutateFunc)(self.hiddenLayer)
        self.outputLayer = np.vectorize(mutateFunc)(self.outputLayer)

    def crossover(self, partnerNetwork):
        """
        Takes another network as input. This makes a genetic algorithm and mixes
        both networks together so they share similar values

        returns new child Network created from both networks
        """
        child = Network(self.inputNodes, self.hiddenNodes, self.outputNodes)
        child.inputLayer = self.applyCrossover(self.inputLayer, partnerNetwork.inputLayer)
        child.hiddenLayer = self.applyCrossover(self.hiddenLayer, partnerNetwork.hiddenLayer)
        child.outputLayer = self.applyCrossover(self.outputLayer, partnerNetwork.outputLayer)
        return child

    def applyCrossover(self, m1, m2):
        """
        Merge 2 matrixese together

        returns the result of the merging operation
        """
        randColumn = np.random.randint(1, m1.shape[0])
        randRow = np.random.randint(1, m1.shape[1])
        result = m1
        result[:randColumn][:randRow] = m2[:randColumn][:randRow]
        return result

    def addBias(self, input):
        """
        Takes matrix of floats: np.float32[][]

        returns the matrix with one extra column of 1's
        """
        shape = input.shape
        newInput = np.ones((shape[0], shape[1] + 1))
        newInput[:,:-1] = input
        return newInput

    def activate(self, inputs):
        """
        Takes matrix of floats: np.float32[][]

        returns the activation of all the elements np.float32[][]
        """
        sigmoid = lambda i: 1 / (1 + pow(Math.E, -i))
        return np.vectorize(sigmoid)(inputs)


