import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import GenerateCSV


def generate_input(name, range):
    values = GenerateCSV.generate_input(name, range)         
    return values

# Function to train the model
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Function to predict the next number
def predict_next_number(model, X_test):
    return model.predict(X_test)

# Function to evaluate the model accuracy
def evaluate_model(model, X_Train, Y_train):
    predictions = model.predict(X_Train)
    pred_mse = get_accuracy(Y_train, predictions)
    return pred_mse, predictions

def predict_next(name, length, model = None):
    # Split sequence into features (X) and target (y)
    data = generate_input(name, length)

    # Need at least 4 data elements to predict next 3 numbers
    if len(data) < 4:
        raise ValueError("Data Length must be at least 4 for proper prediction")

    # X_train created by taking each element in sequence up until last element and then 
    # shaping as 2D Array
    X_train = np.array([data[i] for i in range(len(data) - 3)]).reshape(-1, 1)

    # Y_train created by taking the next three elements after each element in X_train
    Y_train = np.array([data[i + 1 : i + 4] for i in range(len(data) - 3)])

    # Train the model if not provided
    if model is None:
        model = train_model(X_train, Y_train)

    # Predict the next three numbers
    next1 = []
    next2 = []
    next3 = []
    
    for x in X_train:
        prediction = model.predict(x.reshape(1, -1))
        next1.append(prediction[0, 0])
        next2.append(prediction[0, 1])
        next3.append(prediction[0, 2])

    # Evaluate the model accuracy
    numbers_mse = [
        get_accuracy(Y_train[:, 0], next1),
        get_accuracy(Y_train[:, 1], next2),
        get_accuracy(Y_train[:, 2], next3)
    ]

    # Print model
    # print_result(data, Y_train, next1, next2, next3, numbers_mse)

    # Return the original data, ground truth values, and predictions
    return data, Y_train, next1, next2, next3, numbers_mse


def print_result(data, Y_train, next1, next2, next3, numbers_mse):
    print("Original Sequence:", data)
    print("Ground Truth (y_Train): ", Y_train)
    print("Next Number Prediction 1:", next1)
    print("Next Number Prediction 2:", next2)
    print("Next Number Prediction 3:", next3)
    print("Numbers Mean Squared Error:", numbers_mse)

    # Plot the model
    plt.plot(data, label = "Input")
    plt.plot(next1, label = "Next Number 1")
    plt.plot(next2, label = "Next Number 2")
    plt.plot(next3, label = "Next Number 3")
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.show()

def get_accuracy(actual, expected):
    # Return means squared error difference from actual and expected
    return mean_squared_error (actual, expected) 

#predict_next('EURUSD_2023-2024.csv', 'open')