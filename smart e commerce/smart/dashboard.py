import streamlit as st
import pandas as pd
import requests

# =========================
# 🎨 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Ecommerce Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 🎨 CUSTOM STYLING (PRO UI)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

# =========================
# 🔐 LOGIN (CENTERED)
# =========================
if "token" not in st.session_state:
    st.session_state.token = None

st.markdown("## 🔐 Login")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        res = requests.post(f"{API_URL}/users/login", json={
            "email": email,
            "password": password
        })

        if res.status_code == 200:
            st.session_state.token = res.json().get("access_token")
            st.success("✅ Logged in successfully")
        else:
            st.error("❌ Invalid credentials")

# stop if not logged in
if not st.session_state.token:
    st.warning("⚠️ Please login to view dashboard")
    st.stop()

# =========================
# 📡 FETCH DATA
# =========================
headers = {
    "Authorization": f"Bearer {st.session_state.token}"
}

orders_res = requests.get(f"{API_URL}/orders/", headers=headers)
products_res = requests.get(f"{API_URL}/products/")

orders = orders_res.json() if orders_res.status_code == 200 else []
products = products_res.json() if products_res.status_code == 200 else []

orders_df = pd.DataFrame(orders)
products_df = pd.DataFrame(products)

# =========================
# 🔧 FIX DATA
# =========================
if not orders_df.empty and "total_amount" in orders_df.columns:
    orders_df["total_amount"] = pd.to_numeric(
        orders_df["total_amount"], errors="coerce"
    ).fillna(0)

# =========================
# 🏆 HEADER
# =========================
st.markdown("# 📊 Ecommerce Analytics Dashboard")

# =========================
# 💎 KPI CARDS
# =========================
total_orders = len(orders_df)
total_revenue = orders_df["total_amount"].sum() if not orders_df.empty else 0
total_products = len(products_df)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>🧾 Total Orders</h3>
        <h1>{total_orders}</h1>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰 Revenue</h3>
        <h1>₹ {int(total_revenue)}</h1>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>📦 Products</h3>
        <h1>{total_products}</h1>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 📈 CHARTS
# =========================
st.markdown("## 📈 Insights")

if not orders_df.empty and "created_at" in orders_df.columns:

    orders_df["created_at"] = pd.to_datetime(
        orders_df["created_at"], errors="coerce"
    )
    orders_df = orders_df.dropna(subset=["created_at"])
    orders_df["date"] = orders_df["created_at"].dt.date

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Orders Over Time")
        st.line_chart(orders_df.groupby("date").size())

    with col2:
        st.markdown("### Revenue Trend")
        st.line_chart(orders_df.groupby("date")["total_amount"].sum())

else:
    st.warning("No order data available")

# =========================
# 📦 PRODUCT STOCK
# =========================
if not products_df.empty:
    st.markdown("## 📦 Product Inventory")

    if "product_name" in products_df.columns and "stock" in products_df.columns:
        st.bar_chart(products_df.set_index("product_name")["stock"])

# =========================
# 📋 RAW DATA (COLLAPSIBLE)
# =========================
with st.expander("🔍 View Orders Data"):
    st.dataframe(orders_df)

with st.expander("🔍 View Products Data"):
    st.dataframe(products_df)