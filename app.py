import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Sales Analytics", layout="wide")
st.title("📊 Sales Analytics Dashboard")
st.caption("Built in VS Code • Deployed in minutes")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")

df = load_data()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${df['total_bill'].sum():,.0f}")
col2.metric("Avg. Sale", f"${df['total_bill'].mean():.2f}")
col3.metric("Total Tips", f"${df['tip'].sum():,.0f}")
col4.metric("Best Day", df.groupby('day')['total_bill'].sum().idxmax())

st.divider()

# Charts
tab1, tab2, tab3 = st.tabs(["Sales Analysis", "Customer Insights", "Predictor"])

with tab1:
    # Sales by Day
    daily = df.groupby('day')['total_bill'].sum().reset_index()
    fig1 = px.bar(daily, x='day', y='total_bill', 
                  title='Sales by Day', text_auto='$.0f')
    st.plotly_chart(fig1, use_container_width=True)
    
    # Time analysis
    fig2 = px.box(df, x='time', y='total_bill', 
                  title='Lunch vs Dinner Sales')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # Customer segments
    col_left, col_right = st.columns(2)
    
    with col_left:
        fig3 = px.pie(df, names='sex', values='total_bill',
                      title='Sales by Gender')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_right:
        fig4 = px.scatter(df, x='total_bill', y='tip',
                         color='smoker', size='size',
                         title='Tip vs Bill Amount')
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    # Simple ML Predictor
    st.header("Bill Amount Predictor")
    
    col1, col2 = st.columns(2)
    with col1:
        time = st.selectbox("Meal Time", ["Lunch", "Dinner"])
        size = st.slider("Party Size", 1, 8, 2)
    with col2:
        day = st.selectbox("Day", ["Thur", "Fri", "Sat", "Sun"])
        smoker = st.radio("Smoker?", ["Yes", "No"])
    
    if st.button("🔮 Predict Bill", type="primary"):
        # Find similar transactions
        similar = df[
            (df['time'] == time.lower()) &
            (df['size'] == size) &
            (df['day'] == day) &
            (df['smoker'] == smoker)
        ]
        
        if len(similar) > 0:
            pred = similar['total_bill'].mean()
            st.success(f"**Estimated Bill: ${pred:.2f}**")
            
            # Insight
            if pred > df['total_bill'].mean():
                st.info("📈 Above average • Suggest premium items")
            else:
                st.info("📊 Average range • Focus on volume")
        else:
            avg = df['total_bill'].mean()
            st.warning(f"Using overall average: **${avg:.2f}**")

# Footer
st.divider()
st.markdown("---")

# ==================== END COPY ====================


