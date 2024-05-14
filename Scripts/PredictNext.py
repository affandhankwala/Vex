import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    return accuracy, predictions

def predict_next(name, range):
    # Split sequence into features (X) and target (y)
    data = generate_input(name, range)

    X_train = data[:-1].reshape(-1, 1)
    y_train = data[1:]

    # Train the model
    model = train_model(X_train, y_train)

    # Predict the next number
    next_number = predict_next_number(model, [[data[-1]]])[0]

    # Evaluate the model accuracy
    accuracy, predictions = evaluate_model(model, X_train, y_train)

    # Print model
    # print_result(data, predictions, next_number, accuracy)

    # Return the original versus predicted data
    return data, predictions


def print_result(data, predictions, next_number, accuracy):
    print("Original Sequence:", data)
    print("Predictions:", predictions)
    print("Next number prediction:", next_number)
    print("Model accuracy:", accuracy)

    # Plot the model
    plt.plot(data, label = "Input")
    plt.plot(predictions, label = "Predictions")
    plt.xlabel("Count")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()
