import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
import random
import matplotlib.pyplot as plt
import seaborn as sns

# --- Streamlit Page Config ---
st.set_page_config(page_title="Cart Abandonment Dashboard", layout="wide")

# --- Custom CSS for KPI Cards ---
st.markdown("""
    <style>
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px;
    }
    .kpi-title {
        font-size: 16px;
        color: #555;
        margin-bottom: 5px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #2E86C1;
    }
    </style>
""", unsafe_allow_html=True)

# --- Authenticate with GSheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gsheets"], scopes=scope)
client = gspread.authorize(creds)

# --- Load Data ---
SHEET_KEY = "1-rBtxAnKu0Lco7lpmJP_ZY21JUJCwVmIGITgK-w8rNs"
spreadsheet = client.open_by_key(SHEET_KEY)
worksheets = spreadsheet.worksheets()

all_dfs = []
for ws in worksheets:
    if ws.title.startswith("Sheet2_part"):
        data = ws.get_all_records()
        df = pd.DataFrame(data)
        all_dfs.append(df)

if all_dfs:
    sdf = pd.concat(all_dfs, ignore_index=True)
else:
    st.error("No matching sheets found.")
    st.stop()

# --- Synthetic Recovery Data ---
sdf['recovered'] = sdf['user_id'].apply(lambda x: random.choice([0,1,0,0,1]))

# --- KPIs ---
total_abandoners = len(sdf)
unique_users = sdf['user_id'].nunique()
repeat_abandoners = total_abandoners - unique_users
total_recovered = sdf['recovered'].sum()
recovery_rate = (total_recovered / total_abandoners) * 100 if total_abandoners > 0 else 0
avg_abandonments_per_user = total_abandoners / unique_users if unique_users > 0 else 0
abandonment_rate = (total_abandoners / (total_abandoners + total_recovered)) * 100 if total_abandoners > 0 else 0

# Additional Insights
most_abandoned_product = sdf['product_id'].mode()[0] if 'product_id' in sdf.columns else "N/A"
most_abandoned_brand = sdf['brand'].mode()[0] if 'brand' in sdf.columns else "N/A"
most_abandoned_category = sdf['category_code'].mode()[0] if 'category_code' in sdf.columns else "N/A"

if 'event_time' in sdf.columns:
    sdf['event_time'] = pd.to_datetime(sdf['event_time'], errors='coerce')
    sdf = sdf.dropna(subset=['event_time'])
    most_abandon_time = sdf['event_time'].dt.hour.mode()[0]
else:
    most_abandon_time = "N/A"

# --- Dashboard Title ---
st.markdown("<h1 style='font-size:40px;'>🛒 Cart Abandonment Dashboard</h1>", unsafe_allow_html=True)

# --- KPI Cards Layout ---
kpi_cols = st.columns(6)
metrics = {
    "Total Abandoners": f"{total_abandoners:,}",
    "Unique Users": f"{unique_users:,}",
    "Repeat Abandoners": f"{repeat_abandoners:,}",
    "Recovered Carts": f"{total_recovered:,}",
    "Recovery Rate": f"{recovery_rate:.2f}%",
    "Abandonment Rate": f"{abandonment_rate:.2f}%"
}

for col, (title, value) in zip(kpi_cols, metrics.items()):
    col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

# --- Additional Insights ---
st.subheader("🔎 Key Insights")
insight_cols = st.columns(4)
insight_cols[0].metric("Most Abandoned Product ID", most_abandoned_product)
insight_cols[1].metric("Most Abandoned Brand", most_abandoned_brand)
insight_cols[2].metric("Most Abandoned Category", most_abandoned_category)
insight_cols[3].metric("Peak Abandonment Hour", most_abandon_time)

# =========================================================
# 📊 User-Level Insights
# =========================================================
st.subheader("👤 User-Level Insights")

st.write("### Top 10 Abandoners (by number of abandonments)")
abandon_counts = sdf.groupby('user_id').size()  # abandonment count per user
top_abandoners = abandon_counts.sort_values(ascending=False).head(10)

# Show as a bar chart
st.bar_chart(top_abandoners)

# Optional: also show exact numbers
st.dataframe(top_abandoners.reset_index().rename(
    columns={0: "abandon_count"}
))

# =========================================================
# 📦 Product-Level Insights
# =========================================================
st.subheader("📦 Product-Level Insights")

if 'product_id' in sdf.columns:
    st.write("### Top 10 Abandoned Products")
    product_counts = sdf['product_id'].value_counts().head(10)
    st.bar_chart(product_counts)

if 'price' in sdf.columns:
    st.write("### Abandonments by Price Bucket")
    bins = [0,200,500,1000,1500,2000]
    labels = ["<200","200-500","500-1000","1000-1500","2000+"]
    sdf['price_bucket'] = pd.cut(sdf['price'], bins=bins, labels=labels, right=False)
    bucket_counts = sdf['price_bucket'].value_counts().sort_index()
    st.bar_chart(bucket_counts)

    avg_price = sdf['price'].mean()
    st.metric("Average Price of Abandoned Products", f"${avg_price:,.2f}")

# =========================================================
# 🏷️ Brand & Category Insights
# =========================================================
st.subheader("🏷️ Brand & Category Insights")

if 'brand' in sdf.columns:
    st.write("### Top 10 Abandoned Brands")
    brand_counts = sdf['brand'].value_counts().head(10)
    st.bar_chart(brand_counts)

if 'category_code' in sdf.columns:
    st.write("### Abandonment Share by Category")
    cat_counts = sdf['category_code'].value_counts().head(10)
    st.bar_chart(cat_counts)

# =========================================================
# ⚡ Behavioral Insights
# =========================================================
st.subheader("⚡ Behavioral Insights")

# if 'cum_views' in sdf.columns:
#     st.metric("Average cum_views Before Abandonment", f"{sdf['cum_views'].mean():.2f}")

if 'cum_carts' in sdf.columns:
    st.metric("Average cumulative add_to_carts Before Abandonment", f"{sdf['cum_carts'].mean():.2f}")

if 'time_since_start' in sdf.columns:
    st.metric("Average Time to Abandon (mins)", f"{sdf['time_since_start'].mean():.2f}")

# =========================================================
# ⏰ Time-Based Insights
# =========================================================
st.subheader("⏰ Time-Based Insights")

if 'event_time' in sdf.columns:
    st.write("### Abandonments Over Time (Daily)")
    trend = sdf.groupby(sdf['event_time'].dt.date).size().reset_index(name='count')
    trend = trend.rename(columns={'event_time': 'date'}).sort_values("date")
    st.line_chart(trend.set_index("date"))

    st.write("### Abandonments by Hour of Day")
    hourly = sdf.groupby(sdf['event_time'].dt.hour).size()
    st.bar_chart(hourly)

    st.write("### Abandonments by Day of Week")
    dow = sdf.groupby(sdf['event_time'].dt.day_name()).size().sort_values(ascending=False)
    st.bar_chart(dow)

# # --- Recovery Trend Over Time ---
# if 'event_time' in sdf.columns:
#     st.subheader("Recovery Trend Over Time")

#     # Make sure event_time is datetime
#     sdf['event_time'] = pd.to_datetime(sdf['event_time'], errors='coerce')
#     sdf = sdf.dropna(subset=['event_time'])

#     # Group by date
#     recovery_trend = sdf.groupby(sdf['event_time'].dt.date)['recovered'].sum().reset_index()
#     recovery_trend = recovery_trend.rename(columns={'event_time': 'date', 'recovered': 'recoveries'})

#     st.line_chart(recovery_trend.set_index("date"))

# =========================================================
# 📌 End Note
# =========================================================
# st.markdown("""
# ---
# ✅ This dashboard provides a comprehensive view of cart abandonment patterns – user behaviors, product/brand insights, pricing sensitivity, and temporal trends. Use these insights to design better recovery strategies and improve conversion rates.
# """)
