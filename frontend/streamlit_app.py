import streamlit as st
import requests
import pandas as pd

# Set the title of the Streamlit app
st.title("SuperKart Sales Forecasting")

# Sidebar for user input
st.sidebar.header("Input Features")

# Input fields for the user to enter product details
product_weight = st.sidebar.number_input("Product Weight (kg)", min_value=0.0, format="%.2f")
product_sugar_content = st.sidebar.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.sidebar.number_input("Product Allocated Area (ratio)", min_value=0.0, format="%.3f")
product_mrp = st.sidebar.number_input("Product MRP ($)", min_value=0.0, format="%.2f")
store_size = st.sidebar.selectbox("Store Size", ["High", "Medium", "Low"])
store_location_city_type = st.sidebar.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.sidebar.selectbox("Store Type", ["Departmental Store", "Supermarket Type 1", "Supermarket Type 2", "Food Mart"])
product_id_char = st.sidebar.text_input("Product ID (2 letters + number)", max_chars=5)
store_age_years = st.sidebar.number_input("Store Age (years)", min_value=0)
product_type_category = st.sidebar.text_input("Product Type Category", max_chars=50)

# Button to make prediction
if st.sidebar.button("Predict Sales"):
    # Prepare the payload for the API request
    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_id_char,
        "Store_Age_Years": store_age_years,
        "Product_Type_Category": product_type_category
    }
    
    # Make a POST request to the backend API
    model_url = "http://backend:5000/v1/predict"  # Update with the correct backend URL
    response = requests.post(model_url, json=payload)
    
    # Display the prediction result
    if response.status_code == 200:
        prediction = response.json()
        st.success(f"Predicted Sales: ${prediction['sales']:.2f}")
    else:
        st.error("Error in prediction. Please check your input values.")

# Option to upload a batch file for predictions
st.sidebar.header("Batch Prediction")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    batch_data = pd.read_csv(uploaded_file)
    if st.sidebar.button("Predict Batch Sales"):
        batch_input = {'file': batch_data.to_csv(index=False).encode('utf-8')}
        model_batch_url = "http://backend:5000/v1/predictbatch"  # Update with the correct backend URL
        response = requests.post(model_batch_url, files=batch_input)
        
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions received!")
            st.write(predictions)
        else:
            st.error("Error in batch prediction. Please check the uploaded file.")