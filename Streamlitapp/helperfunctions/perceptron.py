import numpy as np
import pandas as pd


class Perceptron():

    def __init__(self,df, xcols, ycol):
        # Seed the random number generator
        np.random.seed(1)

        self.df = df
        self.xcols = xcols
        self.ycol = ycol
        # Set synaptic weights to a nx1 matrix,
        # with values from -1 to 1 and mean 0
        self.synaptic_weights = 2 * np.random.random((len(xcols), 1)) - 1
        self.iterations = 0

        self.training_history = []
        self.accuracy_cutoff = .4

        # n is the number of X Columns

    def sigmoid(self, x):
        """
        Takes in weighted sum of the inputs and normalizes
        them through between 0 and 1 through a sigmoid function
        """
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        """
        The derivative of the sigmoid function used to
        calculate necessary weight adjustments
        """
        return x * (1 - x)

    def train(self, training_inputs, training_outputs, training_iterations):
        """
        We train the model through trial and error, adjusting the
        synaptic weights each time to get a better result
        """
        for iteration in range(training_iterations):
            # Pass training set through the neural network
            output = self.think(training_inputs)

            # Calculate the error rate
            error = training_outputs - output
            abs_error = abs(error)
            og_abs_error = pd.DataFrame(abs_error,columns=["Abs_Error"])
            fl_abs_error = og_abs_error[og_abs_error["Abs_Error"] < self.accuracy_cutoff ]
            accuracy = len(fl_abs_error) / len(og_abs_error)

            # Multiply error by input and gradient of the sigmoid function
            # Less confident weights are adjusted more through the nature of the function
            adjustments = np.dot(training_inputs.T, error * self.sigmoid_derivative(output))

            # Adjust synaptic weights
            self.synaptic_weights += adjustments
            self.iterations += 1

            temp_list = self.synaptic_weights.flatten().tolist()
            temp_list.append(sum(error)[0])
            temp_list.append(accuracy)
            self.training_history.append(temp_list)


    def think(self, inputs):
        """
        Pass inputs through the neural network to get output
        """

        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.synaptic_weights))
        return output
