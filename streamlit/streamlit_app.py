import streamlit as st
import requests

st.title('Property Price Prediction')

st.write('Enter the details of the property to get a price prediction.')

# Form inputs
postal_code = st.number_input('Postal Code')
region = st.text_input('Region')
district = st.text_input('District')
province = st.text_input('Province')
property_type = st.selectbox('Property Type', ['House', 'Apartment', 'Villa'])
property_subtype = st.text_input('Property Sub Type')
bedroom_count = st.number_input('Number of Bedrooms', min_value=1, max_value=10)
living_area = st.number_input('Living Area (sqm)', min_value=10, max_value=1000)
kitchen_type = st.selectbox('Kitchen Type', [None, 'Installed', 'Semi-equipped', 'Hyper-equipped'])
furnished = st.selectbox('Furnished', [None, 'Yes', 'No'])
fireplace = st.selectbox('Fireplace', [None, 'Yes', 'No'])
terrace = st.selectbox('Terrace', ['Yes', 'No'])
terrace_area = st.number_input('Terrace Area (sqm)', min_value=0, max_value=1000)
garden = st.selectbox('Garden', ['Yes', 'No'])
garden_area = st.number_input('Garden Area (sqm)', min_value=0, max_value=1000)
facades = st.number_input('Facades', min_value=0, max_value=10)
swimming_pool = st.selectbox('Swimming Pool', [None, 'Yes', 'No'])
energy_consumption_per_sqm = st.number_input('Energy Consumption Per Sqm', min_value=0.0, max_value=1000.0)
condition = st.selectbox('Condition', [None, 'TO_BE_DONE_UP', 'TO_RENOVATE', 'JUST_RENOVATED', 'AS_NEW', 'GOOD', 'TO_RESTORE'])
epc_score = st.selectbox('EPC Score', [None, 'A', 'B', 'C', 'D', 'E', 'F', 'G'])
latitude = st.number_input('Latitude')
longitude = st.number_input('Longitude')

if st.button('Predict Price'):
    # Prepare data
    data = {
        'PostalCode': postal_code,
        'Region': region,
        'District': district,
        'Province': province,
        'PropertyType': property_type,
        'PropertySubType': property_subtype,
        'BedroomCount': bedroom_count,
        'LivingArea': living_area,
        'KitchenType': kitchen_type,
        'Furnished': furnished,
        'Fireplace': fireplace,
        'Terrace': 1 if terrace == 'Yes' else 0,
        'TerraceArea': terrace_area if terrace_area else None,
        'Garden': 1 if garden == 'Yes' else 0,
        'GardenArea': garden_area if garden_area else None,
        'Facades': facades if facades else None,
        'SwimmingPool': 1 if swimming_pool == 'Yes' else 0,
        'EnergyConsumptionPerSqm': energy_consumption_per_sqm if energy_consumption_per_sqm else None,
        'Condition': condition,
        'EPCScore': epc_score,
        'Latitude': latitude if latitude else None,
        'Longitude': longitude if longitude else None
    }

    # Make API request to FastAPI
    response = requests.post('https://immo-deployment.onrender.com/predict/', json=data)

    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.success(f'Predicted Price: €{prediction}')
    else:
        st.error('Error occurred. Please try again.')
