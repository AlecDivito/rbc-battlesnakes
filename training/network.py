import math
import numpy as np
import random


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def relu(Z):
    return np.maximum(0, Z)


def softmax(x):
    exps = np.exp(x - x.max())
    return exps / np.sum(exps, axis=0)


class Layer:
    def __init__(self, data, func) -> None:
        self.data = data
        self.func = func

    def crossover(self, other):
        """
        Merge 2 matrixese together

        returns the result of the merging operation
        """
        randColumn = np.random.randint(1, self.data.shape[0])
        randRow = np.random.randint(1, self.data.shape[1])
        result = self.data
        result[:randColumn][:randRow] = other.data[:randColumn][:randRow]
        return result


class Network:

    def __init__(self, layers) -> None:
        """
        An array of tuples is passed in, defining the network:
        - [0]: The number of inputs into that layer
        - [1]: The activation function to apply to that layer
        """
        self.number_of_layers = len(layers)
        self.layers = layers
        self.values = {}

        for index, (input, layer) in enumerate(layers):
            layer_index = index
            layer_input_size = input
            layer_function = layer
            if index + 1 == len(layers):
                # if this is the last one
                layer_output_size = layers[index][0]
            else:
                layer_output_size = layers[index + 1][0]

            self.values['W{}'.format(layer_index)] = Layer(
                data=np.random.randn(
                    layer_output_size, layer_input_size) * 0.1,
                func=layer_function,
            )
            self.values['b{}'.format(layer_index)] = Layer(
                data=np.ones(layer_output_size) * 0.1,
                func=layer_function
            )

    def print_network(self):
        for index in range(self.number_of_layers):
            print(self.values['W{}'.format(index)].data.shape,
                  self.values['W{}'.format(index)].func)

    def single_layer_forward_propagation(self, activation, weight, bias, func):
        z = np.dot(weight, activation) + bias
        if func == "relu":
            return relu(z), z
        elif func == "sigmoid":
            return sigmoid(z), z
        else:
            raise Exception('Non-supported activation function')

    def full_forward_propagation(self, input):
        memory = {}
        current = input
        for index in range(self.number_of_layers):
            previous = current
            weights = self.values['W{}'.format(index)].data
            func = self.values['W{}'.format(index)].func
            bias = self.values['b{}'.format(index)].data
            current, output = self.single_layer_forward_propagation(
                previous, weights, bias, func)
            # print('dot({}, {}) + {} = ({}, {})'.format(previous.shape, weights.shape, bias.shape, current.shape, output.shape))

            memory["A".format(index)] = previous
            memory["Z".format(index)] = output

        return current, memory

    def calculateOutput(self, inputs):
        """
        Takes an `inputs`, which is an array of floats (np.float32[])

        returns array of floats
        """
        current, _ = self.full_forward_propagation(inputs)
        output = np.squeeze(np.asarray(current))
        # print(output)
        return output

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
        for index in range(self.number_of_layers):
            data = self.values['W{}'.format(index)].data
            for (x, y), _ in np.ndenumerate(data):
                if (random.random() < rate):
                    data[x][y] = random.random()

    def crossover(self, partnerNetwork):
        """
        Takes another network as input. This makes a genetic algorithm and mixes
        both networks together so they share similar values

        returns new child Network created from both networks
        """
        child = Network(self.layers)
        for index in range(self.number_of_layers):
            me = self.values['W{}'.format(index)]
            partner = partnerNetwork.values['W{}'.format(index)]
            child.values['W{}'.format(index)].data = me.crossover(partner)
        return child

    def save(self, path):
        for index in range(self.number_of_layers):
            self.values['W{}'.format(index)].data.dump(
                "{}/{}".format(path, "W{}.dat".format(index)))
