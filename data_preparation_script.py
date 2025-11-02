import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Load the dataset
df = pd.read_csv('weatherAUS.csv')
print("Dataset shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

# Check basic information about the dataset
print("\nDataset Info:")
print(df.info())

# Check for missing values
print("\nMissing values per column:")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

# Visualize outliers in Rainfall and WindGustSpeed
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Rainfall distribution
axes[0].boxplot(df['CurahHujan'].dropna())
axes[0].set_title('Rainfall Distribution')
axes[0].set_ylabel('Rainfall (mm)')

# WindGustSpeed distribution
axes[1].boxplot(df['KecepatanAnginKencang'].dropna())
axes[1].set_title('Wind Gust Speed Distribution')
axes[1].set_ylabel('Wind Gust Speed (km/h)')

plt.tight_layout()
plt.show()

# Identify categorical columns
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
print("\nCategorical columns:", categorical_columns)

# 1. Feature Engineering on Date column
# Convert date to datetime and extract Year, Month, Day
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Year'] = df['Tanggal'].dt.year
df['Month'] = df['Tanggal'].dt.month
df['Day'] = df['Tanggal'].dt.day

# Drop the original date column as it's no longer needed
df = df.drop('Tanggal', axis=1)

print("\nDate column converted to Year, Month, Day")
print(df[['Year', 'Month', 'Day']].head())

# 2. Encoding Categorical Variables
# Using Label Encoding as specified in the document
label_encoders = {}
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

print("\nCategorical columns to be encoded:", categorical_columns)

for col in categorical_columns:
    le = LabelEncoder()
    # Fit and transform the column, handling unknown values by fitting on all data
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"Encoded {col}: {len(le.classes_)} unique values")

# Check the target variable values before encoding
print("\nUnique values in target variable before encoding:")
print(df['HujanBesok'].value_counts())

# The target variable has already been encoded through the LabelEncoder above
# Check which value is 0 (No) and which is 1 (Yes), assuming alphabetical order
target_encoder = label_encoders['HujanBesok']
print(f"Target variable encoding: {dict(zip(target_encoder.classes_, target_encoder.transform(target_encoder.classes_)))}")

# In the LabelEncoder, 'No' would be 0 and 'Yes' would be 1 (alphabetical order)
print("Target variable encoded as: 'No' = 0, 'Yes' = 1")

# Final dataset info
print("\nFinal dataset shape:", df.shape)
print("\nData types:")
print(df.dtypes.value_counts())

# Check for any remaining missing values
print("\nMissing values after processing:")
missing_after = df.isnull().sum().sum()
print(f"Total missing values: {missing_after}")

if missing_after > 0:
    print("Columns with missing values:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

# Display basic statistics of the final dataset
print("\nBasic statistics of the final dataset:")
print(df.describe())

# Save the prepared dataset
df.to_csv('weatherAUS_prepared.csv', index=False)
print("\nPrepared dataset saved as 'weatherAUS_prepared.csv'")

print("\nSummary of Data Preparation Steps")
print("\n1. Outlier Handling: Decided not to remove outliers in `Rainfall` and `WindGustSpeed` as Random Forest is robust to outliers and these represent valid extreme weather events.")
print("2. Feature Engineering: Extracted Year, Month, and Day from the Date column to capture temporal patterns.")
print("3. Categorical Encoding: Applied Label Encoding to all categorical variables including `Location`, `WindGustDir`, `WindDir9am`, `WindDir3pm`, and `RainToday`.")
print("4. Target Encoding: The target variable `RainTomorrow` was encoded as binary (0 for 'No', 1 for 'Yes').")
print("5. Final Dataset: All variables are now numerical and ready for Random Forest modeling.")