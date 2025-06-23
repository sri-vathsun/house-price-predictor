import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("house_price_model.pkl")

st.title("House Price Estimator")
st.markdown("Enter house details below to get an estimated price and EMI.")

# Input features with user-friendly labels
bedrooms = st.slider("Number of Bedrooms", 1.0, 10.0, 3.0)
poverty_percent = st.slider("Percentage of Population Below Poverty Line", 1.0, 40.0, 12.0)
student_teacher_ratio = st.slider("Average Number of Students per Teacher", 10.0, 30.0, 18.0)

# Currency selection
currency = st.selectbox("Select Currency", ["INR (₹)", "USD ($)"])

# Predict house price
if st.button("Estimate Price"):
    features = np.array([[bedrooms, poverty_percent, student_teacher_ratio]])
    predicted_price_usd = model.predict(features)[0]  # Price in $1000s

    if currency == "INR (₹)":
        price = predicted_price_usd * 1000 * 83  # Convert to INR
        st.success(f"Estimated House Price: ₹{price:,.0f}")
        loan_amount = price
    else:
        price = predicted_price_usd * 1000  # Keep in USD
        st.success(f"Estimated House Price: ${price:,.2f}")
        loan_amount = price

    # EMI calculator section
    st.markdown("---")
    st.subheader("EMI Calculator")

    st.markdown(f"Loan Amount (based on estimated price): {currency.split()[1]}{loan_amount:,.0f}")

    interest = st.number_input("Annual Interest Rate (%)", min_value=1.0, max_value=15.0, value=7.0)
    years = st.number_input("Loan Tenure (in years)", min_value=1, max_value=30, value=15)

    monthly_interest = interest / (12 * 100)
    months = years * 12
    emi = loan_amount * monthly_interest * ((1 + monthly_interest) ** months) / (((1 + monthly_interest) ** months) - 1)

    st.success(f"Estimated Monthly EMI: {currency.split()[1]}{emi:,.0f}")
