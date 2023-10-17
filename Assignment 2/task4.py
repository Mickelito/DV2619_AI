import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.models import Sequential
from keras.layers import Dense

#1.1
def generate_data_points():
    """
    Generates data points to be used for rest of task
    """
    x_data = np.linspace(-0.5, 0.5, 200)[:, np.newaxis]
    noise = np.random.normal(0, 0.02, x_data.shape)
    y_data = np.square(x_data) + noise
    return x_data, y_data

#a
def establish_linear_model(x, y):
    """
    Establishes linear regression model from data points generated in 1.1
    Prediction model on the form: y = ax + b
    """
    #create linear model
    lin_reg = LinearRegression().fit(x, y)
    print("Linear regression coefficient of determination:", lin_reg.score(x, y))

    #get predicted values
    y_pred = lin_reg.predict(x)
    #plot data and prediction as line
    plt.scatter(x, y, color = 'b')
    plt.plot(x, y_pred, color = 'r')
    plt.show()

    return y_pred

#b
def establish_polynomial_model(x, y):
    """
    Establishes polynomial regression model of degree 2 from data points generated in 1.1
    Prediction model on the form: y = a + bx + cx^2
    """
    #create polynomial features to apply on regression model
    poly = PolynomialFeatures(degree = 2)
    poly_features = poly.fit_transform(x)
    #create regression model, fit model to polynomial
    poly_reg = LinearRegression().fit(poly_features, y)
    print("Polynomial regression: y = a + bx + cx^2")
    print("[a]:", poly_reg.intercept_,"[b c]", poly_reg.coef_)

    #get predicted values
    y_pred = poly_reg.predict(poly_features)
    #plot prediction and data
    plt.scatter(x, y, color = 'b')
    plt.plot(x, y_pred, color ='r')
    plt.show()

    return y_pred

#c
def establish_neural_network(x, y):

    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    model = Sequential()

    # input layer added automatically
    model.add(Dense(units=6, input_dim=1, activation='relu')) #hidden layer 6 nodes
    model.add(Dense(units=1, activation='linear'))

    model.compile(loss = "mean_squared_error" , optimizer='adam')

    model.fit(x_train, y_train, epochs=1000, verbose=0)

    y_pred = model.predict(x_test)
    plt.scatter(x, y, color = 'b')
    plt.scatter(x_test, y_pred, color = 'r')
    plt.show()

    return y_pred, y_test

#d
def compare_mse(predictions, y):
    """
    predictions[0]: linear regression
    predictions[1]: polynomial regression
    predictions[2]: [neural network predictions, test, data]
    """
    mse_lst = []
    mse_lst.append(mean_squared_error(y, predictions[0]))
    print("Linear regression MSE:", mse_lst[0])
    mse_lst.append(mean_squared_error(y, predictions[1]))
    print("Polynomial regression MSE:", mse_lst[1])
    mse_lst.append(mean_squared_error(predictions[2][1], predictions[2][0]))
    print("Neural network MSE:", mse_lst[2])

#e
# Already plotting in linear and polynomial regression in a) and b)

def main():
    x, y = generate_data_points()
    pred = []
    pred.append(establish_linear_model(x, y))
    pred.append(establish_polynomial_model(x, y))
    pred.append(establish_neural_network(x, y))

    compare_mse(pred, y)

if __name__ == "__main__":
    main()
