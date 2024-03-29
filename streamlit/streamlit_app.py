import streamlit as st
import requests
import pandas as pd

st.title('Property Price Prediction')

st.write('Enter the details of the property to get a price prediction.')

# Load the raw data
raw_data = pd.read_csv("./api/files/data/raw_data.csv")

# Extract unique values for dropdown fields
postal_codes = raw_data['PostalCode'].unique()
regions = raw_data['Region'].unique()
districts = raw_data['District'].unique()
provinces = raw_data['Province'].unique()
property_types = raw_data['PropertyType'].unique()
kitchen_types = raw_data['KitchenType'].unique()
conditions = raw_data['Condition'].unique()
epc_scores = raw_data['EPCScore'].unique()

# Default example house values
default_values = {
    "PostalCode": 9940,
    "Region": "FLANDERS",
    "District": "East Flanders",
    "Province": "Gent",
    "PropertyType": "House",
    "PropertySubType": "House",
    "BedroomCount": 3,
    "LivingArea": 155,
    "KitchenType": "Installed",
    "Furnished": 0,
    "Fireplace": 0,
    "Terrace": 0,
    "TerraceArea": 0,
    "Garden": 0,
    "GardenArea": 0,
    "Facades": 0,
    "SwimmingPool": 0,
    "EnergyConsumptionPerSqm": 200,
    "Condition": "Good",
    "EPCScore": "B",
    "Latitude": 51.1114671,
    "Longitude": 3.6997650
}

# Create dropdown widgets
selected_postal_code = st.selectbox("Postal Code", postal_codes)
selected_region = st.selectbox("Region", regions)
selected_district = st.selectbox("District", districts)
selected_province = st.selectbox("Province", provinces)
selected_property_type = st.selectbox("Property Type", property_types)
selected_property_subtype = st.selectbox("Property Subtype", property_subtypes)
selected_kitchen_type = st.selectbox("Kitchen Type", kitchen_types)
selected_condition = st.selectbox("Condition", conditions)
selected_epc_score = st.selectbox("EPC Score", epc_scores)

# Create sliders for numeric inputs
bedroom_count = st.slider("Number of Bedrooms", min_value=raw_data['BedroomCount'].min(), max_value=raw_data['BedroomCount'].max())
living_area = st.slider("Living Area", min_value=raw_data['LivingArea'].min(), max_value=raw_data['LivingArea'].max())
terrace_area = st.slider("Terrace Area", min_value=raw_data['TerraceArea'].min(), max_value=raw_data['TerraceArea'].max())
garden_area = st.slider("Garden Area", min_value=raw_data['GardenArea'].min(), max_value=raw_data['GardenArea'].max())
facades = st.slider("Facades", min_value=raw_data['Facades'].min(), max_value=raw_data['Facades'].max())
energy_consumption_per_sqm = st.slider("Energy Consumption Per Sqm", min_value=raw_data['EnergyConsumptionPerSqm'].min(), max_value=raw_data['EnergyConsumptionPerSqm'].max())
latitude = st.slider("Latitude", min_value=raw_data['Latitude'].min(), max_value=raw_data['Latitude'].max())
longitude = st.slider("Longitude", min_value=raw_data['Longitude'].min(), max_value=raw_data['Longitude'].max())

# Create toggle for binary inputs
furnished = st.checkbox("Furnished")
fireplace = st.checkbox("Fireplace")
terrace = st.checkbox("Terrace")
garden = st.checkbox("Garden")
swimming_pool = st.checkbox("Swimming Pool")

# Show garden area slider if garden checkbox is checked
garden = st.checkbox("Garden", value=default_values['Garden'])
if garden:
    garden_area = st.slider("Garden Area", min_value=0, max_value=200, value=default_values['GardenArea'])

# Show Energy Consumption if EPC Score is selected
if selected_epc_score:
    selected_energy_consumption = st.slider("Energy Consumption (kW/sqm)", min_value=-200, max_value=1000, value=epc_energy_map[selected_epc_score])

# Button to submit values
if st.button("Submit"):
    # Create a dictionary to hold the selected values
    selected_values = {
        "PostalCode": selected_postal_code,
        "Region": selected_region,
        "District": selected_district,
        "Province": selected_province,
        "PropertyType": selected_property_type,
        "PropertySubType": selected_property_subtype,
        "BedroomCount": bedroom_count,
        "LivingArea": living_area,
        "KitchenType": selected_kitchen_type,
        "Furnished": furnished,
        "Fireplace": fireplace,
        "Terrace": terrace,
        "TerraceArea": terrace_area,
        "Garden": garden,
        "GardenArea": garden_area,
        "Facades": facades,
        "SwimmingPool": swimming_pool,
        "EnergyConsumptionPerSqm": energy_consumption_per_sqm,
        "Condition": selected_condition,
        "EnergyConsumptionPerSqm": selected_energy_consumption if selected_epc_score else default_values['EnergyConsumptionPerSqm'],  # Include energy_consumption if epc score is selected
        "EPCScore": selected_epc_score,
        "Latitude": latitude,
        "Longitude": longitude
    }

    # Make API request to FastAPI
    response = requests.post('https://immo-deployment.onrender.com/predict/', json=selected_values)

    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.success(f'Predicted Price: €{prediction}')
    else:
        st.error('Error occurred. Please try again.')