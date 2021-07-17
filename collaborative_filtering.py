import numpy as np

class CollabFilter:
    def __init__(self,latent_vector_dim, number_users, number_food, gamma_factor):
        self.number_users = number_users
        self.number_food = number_food
        self.food_vector = np.random.randn(self.number_food, latent_vector_dim)
        self.user_vector = np.random.randn(latent_vector_dim,number_users)
        self.gamma_factor = gamma_factor

    def sigmoid(self,x):
        return 1/(1+np.exp(-x))
    def derivative_sigmoid(self, x):
        return x*(1-x)
    def learn(self, user_rating ,user_has_eaten_food, learning_rate, epochs):
        for i in range(epochs):
            z_values = np.matmul(self.food_vector, self.user_vector)
            activation_value = self.sigmoid(z_values)
            y_diff = activation_value - user_rating
            valid_y_diff = np.multiply(y_diff,user_has_eaten_food)
            error = (1/2)*np.sum(np.square(valid_y_diff))
            + self.gamma_factor*(1/2)*np.sum(np.square(self.food_vector))
            + self.gamma_factor*(1/2)*np.sum(np.square(self.user_vector))
            print("Error: ", error, "Epoch: ", epochs)
            sigmoid_delta = np.multiply(valid_y_diff, self.derivative_sigmoid(activation_value))
            food_gradient = np.matmul(sigmoid_delta,np.transpose(self.user_vector)) + self.gamma_factor*self.food_vector
            user_gradient = np.matmul(np.transpose(sigmoid_delta), self.food_vector) + self.gamma_factor*self.user_vector
            self.user_vector = self.user_vector - learning_rate*user_gradient
            self.food_vector = self.food_vector - learning_rate*food_gradient

    def print_data(self):
        print(self.food_vector);
        print(self.user_vector);
        print(self.sigmoid(np.matmul(self.food_vector,self.user_vector)))



hello = CollabFilter(2,2,2, 0.0001)
hello.learn(np.array([[0.25,0.5],[0.1,0.9]]), np.array([[1,1],[1,1]]), 0.03, 2000)
hello.print_data()
