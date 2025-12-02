import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# BAB 2: Data understanding

# Load the dataset
# Assuming the csv file is in the same directory
try:
    data = pd.read_csv('weatherAUS.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: weatherAUS.csv not found. Please ensure the file is in the same directory.")
    exit()

# Display first few rows
print("\nFirst 5 rows of the dataset:")
print(data.head())

# Data Info
print("\nDataset Information:")
data.info()

# Data Description
print("\nDataset Description:")
print(data.describe())

# Check for missing values
print("\nMissing Values per Column:")
missing_values = data.isnull().sum().sort_values(ascending=False)
print(missing_values)

# Visualizations
# Note: In a script, plt.show() is needed to display plots. 
# These might block execution until the window is closed.

print("\nGenerating Histograms for Numerical Variables...")
data[['SuhuMin','SuhuMax','CurahHujan','Penguapan','SinarMatahari','KecepatanAnginKencang']].hist(
    figsize=(10,8), bins=20, color='skyblue', edgecolor='black')
plt.suptitle("Distribusi Variabel Numerik Utama", fontsize=14)
plt.show()

print("\nGenerating Boxplot for Rainfall...")
plt.figure(figsize=(8, 6))
sns.boxplot(x=data['CurahHujan'], color='skyblue')
plt.title("Deteksi Outlier pada Variabel CurahHujan (Rainfall)")
plt.xlabel("CurahHujan (mm)")
plt.show()

# Correlation Analysis
# We need to encode RainTomorrow to calculate correlation if it's not already numeric
if 'HujanBesok' in data.columns:
    # Simple encoding for correlation check
    data['HujanBesok_encoded'] = data['HujanBesok'].map({'Yes': 1, 'No': 0})
    
    # Select numerical columns for correlation
    numerical_cols = data.select_dtypes(include=[np.number]).columns
    
    print("\nCorrelation of Numerical Variables with HujanBesok (Encoded):")
    correlation = data[numerical_cols].corr()['HujanBesok_encoded'].sort_values(ascending=False)
    print(correlation)
else:
    print("\nHujanBesok column not found for correlation analysis.")
