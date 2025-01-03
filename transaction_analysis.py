import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache
def load_data(filepath):
    return pd.read_csv(filepath)

# Sidebar
st.sidebar.title("Interactive Dashboard")
st.sidebar.markdown("Use the controls to customize your view.")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV)", type="csv")
if uploaded_file:
    data = load_data(uploaded_file)
    
    # Main Dashboard
    st.title("Interactive Transaction Dashboard")

    # Overview Section
    st.header("Dataset Overview")
    st.write("First 5 rows of the dataset")
    st.dataframe(data.head())

    # Account Type Distribution
    st.subheader("Account Type Distribution")
    account_counts = data['Account Type'].value_counts()
    fig1 = px.pie(values=account_counts.values, names=account_counts.index, title="Account Type Distribution")
    st.plotly_chart(fig1)

    # Geographic Heatmap of Transactions
    st.subheader("Transaction Intensity by Region")
    transaction_intensity = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
    transaction_intensity['Total Transactions'] = transaction_intensity['Credit'] + transaction_intensity['Debit']
    fig2 = px.bar(transaction_intensity, x='Region', y='Total Transactions', color='Region', title="Transaction Intensity by Region")
    st.plotly_chart(fig2)

    # Top 5 Banks by Region
    st.subheader("Top 5 Beneficiary Banks by Region")
    data['Transaction To'] = data['Transaction To'].fillna('Unknown')  # Handle missing values
    top_banks = data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
    top_banks = top_banks.groupby('Region').apply(lambda x: x.nlargest(5, 'Credit')).reset_index(drop=True)
    fig3 = px.bar(top_banks, x='Transaction To', y='Credit', color='Region', title="Top 5 Beneficiary Banks")
    st.plotly_chart(fig3)

    # Transaction Trends Over Time
    if 'Date' in data.columns:
        st.subheader("Transaction Trends Over Time")
        data['Date'] = pd.to_datetime(data['Date'])
        time_data = data.groupby('Date')[['Credit', 'Debit']].sum().reset_index()
        fig4 = px.line(time_data, x='Date', y=['Credit', 'Debit'], title="Transaction Trends Over Time")
        st.plotly_chart(fig4)

    # Correlation Matrix
    st.subheader("Correlation Heatmap")
    fig5 = px.imshow(data[['Credit', 'Debit']].corr(), text_auto=True, color_continuous_scale='coolwarm', title="Correlation Matrix")
    st.plotly_chart(fig5)
else:
    st.warning("Please upload a dataset to get started!")

