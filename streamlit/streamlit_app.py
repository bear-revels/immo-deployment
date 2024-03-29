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

# Create a mapping from postal code to region, district, and province
postal_code_map = {code: (region, district, province) for code, region, district, province in zip(raw_data['PostalCode'], raw_data['Region'], raw_data['District'], raw_data['Province'])}

# Create a mapping from epc score to energy consumption
epc_energy_map = raw_data.groupby('EPCScore')['EnergyConsumptionPerSqm'].median().to_dict()


# Default example house values
default_values = {
    "PostalCode": None,
    "PropertyType": None,
    "PropertySubType": None,
    "BedroomCount": None,
    "LivingArea": None,
    "KitchenType": None,
    "Furnished": 0,
    "Fireplace": 0,
    "Terrace": 0,
    "TerraceArea": 0,
    "Garden": 0,
    "GardenArea": 0,
    "Facades": 0,
    "SwimmingPool": 0,
    "EnergyConsumptionPerSqm": 0,
    "Condition": None,
    "EPCScore": None,
    "Latitude": None,
    "Longitude": None
}

# Placeholder elements for region, district, province, latitude, and longitude
region_placeholder = st.empty()
district_placeholder = st.empty()
province_placeholder = st.empty()
latitude_placeholder = st.empty()
longitude_placeholder = st.empty()

# Create dropdown widgets
selected_postal_code = st.selectbox("Postal Code", [None] + postal_codes.tolist())

# Show region, district, province, latitude, and longitude inputs once postal code is selected
if selected_postal_code:
    selected_region, selected_district, selected_province = postal_code_map[selected_postal_code]
    selected_region = region_placeholder.selectbox("Region", [None] + raw_data['Region'].unique().tolist(), index=raw_data['Region'].unique().tolist().index(selected_region))
    selected_district = district_placeholder.selectbox("District", [None] + raw_data['District'].unique().tolist(), index=raw_data['District'].unique().tolist().index(selected_district))
    selected_province = province_placeholder.selectbox("Province", [None] + raw_data['Province'].unique().tolist(), index=raw_data['Province'].unique().tolist().index(selected_province))
    latitude, longitude = raw_data[raw_data['PostalCode'] == selected_postal_code][['Latitude', 'Longitude']].median()
    latitude_placeholder.number_input("Latitude", value=latitude)
    longitude_placeholder.number_input("Longitude", value=longitude)

# Hide Property Subtype until Property Type is selected
if default_values["PropertyType"] is not None:
    selected_property_type_index = property_types.tolist().index(default_values["PropertyType"])
    property_type_options = property_types.tolist()
else:
    selected_property_type_index = None
    property_type_options = [None] + property_types.tolist()

selected_property_type = st.selectbox("Property Type", property_type_options, index=selected_property_type_index)
if selected_property_type:
    property_subtype_options = raw_data[raw_data['PropertyType'] == selected_property_type]['PropertySubType'].unique()
    
    if default_values["PropertySubType"] is not None and default_values["PropertySubType"] in property_subtype_options:
        selected_property_subtype_index = property_subtype_options.tolist().index(default_values["PropertySubType"])
    else:
        selected_property_subtype_index = None
    
    selected_property_subtype = st.selectbox("Property Subtype", [None] + property_subtype_options.tolist(), index=selected_property_subtype_index)

selected_kitchen_type = st.selectbox("Kitchen Type", [None] + kitchen_types.tolist(), index=kitchen_types.tolist().index(default_values["KitchenType"]))
selected_condition = st.selectbox("Condition", [None] + conditions.tolist(), index=conditions.tolist().index(default_values["Condition"]))
selected_epc_score = st.selectbox("EPC Score", [None] + epc_scores.tolist(), index=epc_scores.tolist().index(default_values["EPCScore"]))

# Show Living Area if Number of Bedrooms is selected
bedroom_count = st.slider("Number of Bedrooms", min_value=0, max_value=10, value=default_values['BedroomCount'])
if bedroom_count is not None:
    living_area = st.slider("Living Area", min_value=0, max_value=200, value=default_values['LivingArea'])

# Create toggle for binary inputs
furnished = st.checkbox("Furnished", value=default_values['Furnished'])
fireplace = st.checkbox("Fireplace", value=default_values['Fireplace'])
swimming_pool = st.checkbox("Swimming Pool", value=default_values['SwimmingPool'])

# Show terrace area slider if terrace checkbox is checked
terrace = st.checkbox("Terrace", value=default_values['Terrace'])
if terrace:
    terrace_area = st.slider("Terrace Area", min_value=0, max_value=200, value=default_values['TerraceArea'])

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
        "TerraceArea": terrace_area if terrace else default_values['TerraceArea'],  # Include terrace_area if terrace is checked
        "Garden": garden,
        "GardenArea": garden_area if garden else default_values['GardenArea'],  # Include garden_area if garden is checked
        "SwimmingPool": swimming_pool,
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