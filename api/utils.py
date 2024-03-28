import joblib
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

class FilterRows(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if 'Price' in X.columns and 'LivingArea' in X.columns and 'SaleType' in X.columns and 'BidStylePricing' in X.columns:
            X_filtered = X[(X['Price'].notnull()) & (X['LivingArea'].notnull()) & 
                           (X['SaleType'] == 'residential_sale') & (X['BidStylePricing'] != 1)]
            return X_filtered
        else:
            return X

class ReplaceNulls(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.columns_to_fill = ['Furnished', 'Fireplace', 'Terrace', 'TerraceArea', 'Garden', 'GardenArea', 'SwimmingPool', 'BidStylePricing', 'ViewCount', 'bookmarkCount']

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_filled = X.copy()
        for column in self.columns_to_fill:
            if column in X_filled.columns:
                X_filled[column] = X_filled[column].fillna(0)
        return X_filled
    
class JoinData(BaseEstimator, TransformerMixin):
    def __init__(self):
        # Get the absolute path of the directory containing the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        # Construct the absolute paths to the external datasets
        postal_refnis_path = os.path.join(parent_dir, "api", "files", "data", "REFNIS_Mapping.xlsx")
        pop_density_path = os.path.join(parent_dir, "api", "files", "data", "PopDensity.xlsx")
        house_income_path = os.path.join(parent_dir, "api", "files", "data", "HouseholdIncome.xlsx")
        property_value_path = os.path.join(parent_dir, "api", "files", "data", "PropertyValue.xlsx")
        
        # Load external datasets
        self.postal_refnis = pd.read_excel(postal_refnis_path, dtype={'Refnis': int})
        self.pop_density_data = pd.read_excel(pop_density_path, dtype={'Refnis': int})
        self.house_income_data = pd.read_excel(house_income_path, dtype={'Refnis': int})
        self.property_value_data = pd.read_excel(property_value_path, dtype={'Refnis': int})
        
    def fit(self, X, y=None):
        return self

    def transform(self, raw_data):
        if isinstance(raw_data, pd.DataFrame):
            geo_data = pd.DataFrame(raw_data)
        else:
            geo_data = pd.DataFrame.from_dict(raw_data, orient='index').T

        # Merge Refnis
        if 'PostalCode' in geo_data.columns:
            joined_data = geo_data.merge(self.postal_refnis[['PostalCode', 'Refnis']], 
                                    left_on='PostalCode', 
                                    right_on='PostalCode', 
                                    how='left')

        # Data Merge
        datasets = [self.pop_density_data, self.property_value_data, self.house_income_data]
        for dataset in datasets:
            if 'Refnis' in joined_data.columns:
                joined_data = joined_data.merge(dataset, left_on='Refnis', right_on='Refnis', how='left')

        return joined_data

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.columns_to_drop = ['ID', 'Street', 'HouseNumber', 'Box', 'Floor', 'City', 
                           'SaleType', 'KitchenType', 'Latitude', 'Longitude', 
                           'ListingCreateDate', 'ListingExpirationDate', 
                           'ListingCloseDate', 'PropertyUrl', 'Property url',
                           'bookmarkCount', 'ViewCount', 'Refnis', 'BidStylePricing',
                           'ConstructionYear']

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            columns_to_drop = [col for col in self.columns_to_drop if col in X.columns]
            X_dropped = X.drop(columns=columns_to_drop, errors='ignore')
            return X_dropped
        else:
            return X

class EncodeCategorical(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X_encoded = X.copy()

        condition_mapping = {
            'nan': None,
            'TO_BE_DONE_UP': 2,
            'TO_RENOVATE': 1,
            'JUST_RENOVATED': 4,
            'AS_NEW': 5,
            'GOOD': 3,
            'TO_RESTORE': 0
        }

        if 'Condition' in X_encoded.columns:
            X_encoded['Condition'] = X_encoded['Condition'].map(condition_mapping)

        if 'EPCScore' in X_encoded.columns:
            X_encoded['EPCScore'] = X_encoded['EPCScore'].str.split('_').str[0]

        for column in X_encoded.columns:
            if X_encoded[column].dtype == 'object':
                X_encoded[column] = LabelEncoder().fit_transform(X_encoded[column])
        return X_encoded

class FeatureTransformer:
    def __init__(self):
        self.columns_to_transform = ['Price', 'LivingArea', 'BedroomCount', 'GardenArea']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        transformed_data = X.copy()

        for column in self.columns_to_transform:
            if column in transformed_data.columns and pd.api.types.is_numeric_dtype(transformed_data[column]):
                transformed_data[column] = np.log10((transformed_data[column] + 1))

        return transformed_data

# Define a preprocessing pipeline with ColumnTransformer
preprocessing = Pipeline(steps=[
    ('filter_rows', FilterRows()),  
    ('replace_nulls', ReplaceNulls()),  
    ('join_data', JoinData()),  
    ('drop_columns', DropColumns()),  
    ('encode_categorical', EncodeCategorical()),  
    ('feature_transformer', FeatureTransformer())
])

import os

def import_data(refresh=False):
    # Get the absolute path of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    if refresh:
        print("Loading and preprocessing new data...")
        raw_data = pd.read_csv("https://raw.githubusercontent.com/bear-revels/immo-eliza-scraping-Python_Pricers/main/data/all_property_details.csv", dtype={'PostalCode': str})
        raw_data.to_csv(os.path.join(parent_dir, "files", "data", "raw_data.csv"), index=False, encoding='utf-8')
    else:
        print("Preprocessing the existing data...")
        raw_data = pd.read_csv(os.path.join(parent_dir, "files", "data", "raw_data.csv"))
    return raw_data

def visualize_metrics(metrics, y_test, y_pred):
    mae = metrics.get("Mean Absolute Error")
    r_squared = metrics.get("R-squared value")
    r_squared_percent = round(r_squared * 100, 2)
    formatted_mae = "{:,.2f}".format(mae)

    print("Evaluation Metrics:")
    print("Mean Absolute Error:", formatted_mae)
    print("R-squared value:", f"{r_squared_percent:.2f}%")

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].bar(["Mean Absolute Error"], [mae], color='blue')
    ax[0].set_title(f"Mean Absolute Error: {formatted_mae}")
    ax[1].bar(["R-squared value"], [r_squared_percent], color='green')
    ax[1].set_title(f"R-squared value: {r_squared_percent:.2f}%")
    ax[1].set_ylim([0, 100])

    ax[2].scatter(y_test, y_pred, color='blue', alpha=0.5)
    ax[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    ax[2].set_xlabel('Actual')
    ax[2].set_ylabel('Predicted')
    ax[2].set_title('Predicted vs Actual')

    plt.tight_layout()
    plt.show()

def save_model(model, filename, params=None, preprocessing_pipeline=None):
    model_data = {
        "model": model,
        "params": params,
        "preprocessing_pipeline": preprocessing_pipeline
    }

    # Get the absolute path of the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Construct the absolute path to save the model
    filepath = os.path.join(parent_dir, "api", filename + ".pkl")
    joblib.dump(model_data, filepath)
    
    print(f"Model saved as {filepath}")