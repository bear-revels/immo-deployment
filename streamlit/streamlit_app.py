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
property_subtypes = raw_data['PropertySubType'].unique()
kitchen_types = raw_data['KitchenType'].unique()
conditions = raw_data['Condition'].unique()
epc_scores = raw_data['EPCScore'].unique()

# Create a mapping from postal code to region, district, and province
postal_code_map = {code: (region, district, province) for code, region, district, province in zip(raw_data['PostalCode'], raw_data['Region'], raw_data['District'], raw_data['Province'])}

# Default example house values
default_values = {
    "PostalCode": 9940,
    "PropertyType": "House",
    "PropertySubType": "House",
    "BedroomCount": 3,
    "LivingArea": 155,
    "KitchenType": "Installed",
    "Furnished": 0,
    "Fireplace": 0,
    "Terrace": 0,
    "TerraceArea": 0,
    "Garden": 1,
    "GardenArea": 35,
    "Facades": 3,
    "SwimmingPool": 0,
    "Condition": "Good",
    "EPCScore": "B",
    "Latitude": 51.1114671,
    "Longitude": 3.6997650
}

# Placeholder elements for region, district, and province
region_placeholder = st.empty()
district_placeholder = st.empty()
province_placeholder = st.empty()

# Create dropdown widgets
selected_postal_code = st.selectbox("Postal Code", postal_codes)

# Show region, district, and province inputs once postal code is selected
if selected_postal_code:
    selected_region, selected_district, selected_province = postal_code_map[selected_postal_code]
    selected_region = region_placeholder.selectbox("Region", regions, index=regions.tolist().index(selected_region))
    selected_district = district_placeholder.selectbox("District", districts, index=districts.tolist().index(selected_district))
    selected_province = province_placeholder.selectbox("Province", provinces, index=provinces.tolist().index(selected_province))

selected_property_type = st.selectbox("Property Type", property_types)
selected_property_subtype = st.selectbox("Property Subtype", property_subtypes)
selected_kitchen_type = st.selectbox("Kitchen Type", kitchen_types)
selected_condition = st.selectbox("Condition", conditions)
selected_epc_score = st.selectbox("EPC Score", epc_scores)

# Create sliders for numeric inputs
bedroom_count = st.slider("Number of Bedrooms", min_value=0, max_value=10, value=default_values['BedroomCount'])
living_area = st.slider("Living Area", min_value=0, max_value=200, value=default_values['LivingArea'])
latitude = st.number_input("Latitude", value=default_values['Latitude'])
longitude = st.number_input("Longitude", value=default_values['Longitude'])

# Create toggle for binary inputs
furnished = st.checkbox("Furnished", value=default_values['Furnished'])
fireplace = st.checkbox("Fireplace", value=default_values['Fireplace'])
garden = st.checkbox("Garden", value=default_values['Garden'])
terrace = st.checkbox("Terrace", value=default_values['Terrace'])
swimming_pool = st.checkbox("Swimming Pool", value=default_values['SwimmingPool'])

# Show garden area slider if garden checkbox is checked
if garden:
    garden_area = st.slider("Garden Area", min_value=0, max_value=200, value=default_values['GardenArea'])

# Show terrace area slider if terrace checkbox is checked
if terrace:
    terrace_area = st.slider("Terrace Area", min_value=0, max_value=200, value=default_values['TerraceArea'])

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
        "TerraceArea": terrace_area if terrace else default_values['TerraceArea'],  # Include terrace_area if terrace is checked
        "Garden": garden,
        "GardenArea": garden_area if garden else default_values['GardenArea'],  # Include garden_area if garden is checked
        "SwimmingPool": swimming_pool,
        "Condition": selected_condition,
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