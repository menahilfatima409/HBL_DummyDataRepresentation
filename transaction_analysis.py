import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

# Load dataset
def load_data(filepath):
    return pd.read_csv(filepath)

# Visualization: Account Type Distribution
def account_type_distribution(data):
    account_counts = data['Account Type'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(account_counts.values, labels=account_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
    plt.title("Account Type Distribution")
    plt.show()

# Visualization: Top 5 Beneficiary Banks by Region
def top_beneficiary_banks(data):
    top_beneficiaries = data.groupby(['Region', 'Transaction To'])['Credit'].sum().reset_index()
    top_beneficiaries = top_beneficiaries.groupby('Region').apply(lambda x: x.nlargest(5, 'Credit')).reset_index(drop=True)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_beneficiaries, x='Transaction To', y='Credit', hue='Region', palette='Set2')
    plt.title("Top 5 Beneficiary Banks by Region")
    plt.xlabel("Beneficiary Bank")
    plt.ylabel("Credit Amount")
    plt.xticks(rotation=45)
    plt.legend(title="Region")
    plt.show()

# Visualization: Geographic Heatmap of Transactions
def geographic_heatmap(data):
    transaction_intensity = data.groupby('Region')[['Credit', 'Debit']].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.heatmap(transaction_intensity.set_index('Region'), annot=True, cmap='BuGn', fmt='.0f', linewidths=0.5, linecolor='white')
    plt.title("Transaction Intensity by Region")
    plt.show()

# Visualization: Comparative Analysis by Account Type
def transaction_boxplot(data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='Account Type', y='Credit', palette='Set2')
    sns.boxplot(data=data, x='Account Type', y='Debit', palette='Set3')
    plt.title("Transaction Type Comparison Across Account Types")
    plt.show()

# Additional: Correlation Analysis
def correlation_heatmap(data):
    correlation_matrix = data[['Credit', 'Debit']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Between Credit and Debit Transactions")
    plt.show()

# Main script
if __name__ == "__main__":
    # Load the dataset
    filepath = "path_to_your_dataset.csv"  # Replace with your CSV file path
    data = load_data(filepath)

    # Call visualizations
    print("Creating visualizations...")
    account_type_distribution(data)
    top_beneficiary_banks(data)
    geographic_heatmap(data)
    transaction_boxplot(data)
    correlation_heatmap(data)

    print("Visualizations created successfully!")
