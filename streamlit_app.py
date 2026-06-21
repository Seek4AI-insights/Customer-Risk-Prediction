import streamlit as st
import requests

# ==========================
# FastAPI Endpoint
# ==========================
API_URL = "https://customer-risk-prediction-1.onrender.com/predict"

# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="Customer Risk Prediction",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Customer Risk Prediction")
st.markdown("Enter customer and order details to predict fraud/risk.")

# ==========================
# Customer Information
# ==========================
st.subheader("👤 Customer Information")

customer_order_count = st.number_input(
    "Customer Order Count",
    min_value=0,
    value=1
)

customer_total_spending = st.number_input(
    "Customer Total Spending",
    min_value=0.0,
    value=50.0
)

avg_order_value = st.number_input(
    "Average Order Value",
    min_value=0.0,
    value=50.0
)

customer_state = st.selectbox(
    "Customer State",
    [
        "SP","RJ","MG","RS","PR","SC",
        "BA","DF","GO","ES","PE","CE",
        "MT","PA","MS","MA","PB","PI",
        "RN","AL","SE","TO","RO","AM",
        "AC","AP","RR"
    ]
)

# ==========================
# Order Information
# ==========================
st.subheader("📦 Order Information")

price = st.number_input(
    "Product Price",
    min_value=0.0,
    value=20.0
)

freight_value = st.number_input(
    "Freight Value",
    min_value=0.0,
    value=40.0
)

payment_type = st.selectbox(
    "Payment Type",
    [
        "credit_card",
        "boleto",
        "voucher",
        "debit_card"
    ]
)

# ==========================
# Seller Information
# ==========================
st.subheader("🏪 Seller Information")

seller_order_count = st.number_input(
    "Seller Order Count",
    min_value=0,
    value=1
)

seller_state = st.selectbox(
    "Seller State",
    [
        "SP","MG","PR","RJ","SC","RS",
        "DF","BA","GO","PE","MA","ES",
        "MT","CE","RN","MS","PB","RO",
        "PI","SE","PA","AM","AC"
    ]
)

# Hidden Fixed Category
product_category_name = "electronics"

# ==========================
# Prediction Button
# ==========================
if st.button("🚀 Predict Risk"):

    payload = {
        "customer_order_count": customer_order_count,
        "customer_total_spending": customer_total_spending,
        "price": price,
        "freight_value": freight_value,
        "seller_state": seller_state,
        "product_category_name": product_category_name,
        "payment_type": payment_type,
        "customer_state": customer_state,
        "avg_order_value": avg_order_value,
        "seller_order_count": seller_order_count
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction Completed Successfully")

            risk_probability = result.get(
                "risk_probability",
                0
            )

            risk_label = result.get(
                "risk_label",
                "Unknown"
            )

            st.metric(
                label="Risk Probability",
                value=f"{risk_probability:.2%}"
            )

            if risk_label.lower() == "high risk":
                st.error("⚠️ HIGH RISK CUSTOMER")
            else:
                st.success("✅ LOW RISK CUSTOMER")

            with st.expander("Prediction Details"):
                st.json(result)

        else:
            st.error(
                f"API Error ({response.status_code})"
            )
            st.write(response.text)

    except Exception as e:
        st.error(
            f"Failed to connect to API: {e}"
        )
