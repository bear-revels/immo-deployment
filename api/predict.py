import joblib
import json
import importlib
import numpy as np
import os
import subprocess

# Function to load preprocessing steps from JSON file
def load_preprocessing_steps(file_path):
    with open(file_path, 'r') as json_file:
        preprocessing_steps = json.load(json_file)
    return preprocessing_steps

# Function to apply preprocessing steps to input data
def apply_preprocessing(input_data, preprocessing_steps):
    processed_data = input_data.copy()
    for step, function in preprocessing_steps.items():
        module_name = function.split('.')[0]
        function_name = function.split('.')[1]
        module_path = f"./source/utils/{module_name}.py"
        
        # Check if the preprocessing function file exists, if not, download it using curl
        if not os.path.isfile(module_path):
            module_url = f"https://raw.githubusercontent.com/bear-revels/immo-ml/main/source/utils/{module_name}.py"
            subprocess.run(['curl', '-o', module_path, module_url])
        
        module = importlib.import_module(f"source.utils.{module_name}")
        process_function = getattr(module, function_name)
        processed_data = process_function(processed_data)
    return processed_data

# Function to predict the price using the trained Random Forest model
def predict_price(input_data):
    # Load the trained Random Forest model
    model = joblib.load("./models/random_forest.pkl")

    # Load preprocessing steps from JSON file
    preprocessing_steps = load_preprocessing_steps("./preprocessing_steps.json")

    # Apply preprocessing steps to input data
    preprocessed_data = apply_preprocessing(input_data, preprocessing_steps)

    # Make predictions
    predicted_price = model.predict(preprocessed_data)

    predicted_price = np.power(10, predicted_price) - 1

    return predicted_price[0]