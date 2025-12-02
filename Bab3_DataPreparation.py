import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import pickle

# BAB 3: Data preparation

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("Starting Data Preparation...")

# Load the dataset
try:
    df = pd.read_csv('weatherAUS.csv')
    print(f"Dataset loaded. Shape: {df.shape}")
except FileNotFoundError:
    print("Error: weatherAUS.csv not found.")
    exit()

# 3.1 Handling Outliers
# Document states outliers in Rainfall and WindGustSpeed are valid extreme weather events.
# We visualize them but do not remove them.
print("\nVisualizing Outliers (Rainfall & WindGustSpeed)...")
# In a script, we might skip showing plots to avoid blocking, or save them.
# For now, I'll comment out the show() to keep the script running smoothly, 
# or just print a message that we are skipping removal.
print("Skipping outlier removal as per documentation (valid extreme weather events).")

# 3.2 Feature Engineering (Date)
print("\nPerforming Feature Engineering on Date...")
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
df['Year'] = df['Tanggal'].dt.year
df['Month'] = df['Tanggal'].dt.month
df['Day'] = df['Tanggal'].dt.day
df = df.drop('Tanggal', axis=1)
print("Date column converted to Year, Month, Day.")

# 3.3 Encoding Categorical Variables
print("\nEncoding Categorical Variables...")
label_encoders = {}
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

print(f"Categorical columns to encode: {categorical_columns}")

for col in categorical_columns:
    le = LabelEncoder()
    # Handle potential missing values by converting to string first if necessary, 
    # though dataset info suggested no missing values in the notebook view.
    # The notebook used: df[col] = le.fit_transform(df[col].astype(str))
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"Encoded {col}: {len(le.classes_)} unique values")

# 3.4 Target Variable Encoding
# RainTomorrow is already encoded in the loop above if it was object type.
# Let's verify mapping.
if 'HujanBesok' in label_encoders:
    target_encoder = label_encoders['HujanBesok']
    mapping = dict(zip(target_encoder.classes_, target_encoder.transform(target_encoder.classes_)))
    print(f"Target variable (HujanBesok) encoding: {mapping}")
else:
    print("HujanBesok was not in categorical list (maybe already numeric?)")

# Final check
print(f"\nFinal dataset shape: {df.shape}")
print(f"Total missing values: {df.isnull().sum().sum()}")

# Save prepared dataset (optional, but good for reference)
df.to_csv('weatherAUS_prepared.csv', index=False)
print("Saved 'weatherAUS_prepared.csv'.")

# 3.5 Data Splitting
print("\nSplitting Data...")
feature_columns = [col for col in df.columns if col not in ['HujanBesok']]
X = df[feature_columns]
y = df['HujanBesok']

# Stratified split 80-20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")

# 3.6 Handling Class Imbalance with SMOTE
print("\nApplying SMOTE to Training Data...")
print(f"Before SMOTE - HujanBesok distribution: {y_train.value_counts(normalize=True).to_dict()}")

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"After SMOTE - X_train_smote shape: {X_train_smote.shape}")
print(f"After SMOTE - HujanBesok distribution: {y_train_smote.value_counts(normalize=True).to_dict()}")

# Save the processed data for Modelling
print("\nSaving processed datasets for Modelling...")
# Save feature names
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)

# Save Train Data (SMOTE)
train_data = pd.concat([pd.DataFrame(X_train_smote, columns=feature_columns), 
                        pd.DataFrame(y_train_smote, columns=['HujanBesok'])], axis=1)
train_data.to_csv('X_train_smote.csv', index=False)

# Save Test Data
test_data = pd.concat([pd.DataFrame(X_test, columns=feature_columns), 
                      pd.DataFrame(y_test, columns=['HujanBesok'])], axis=1)
test_data.to_csv('X_test.csv', index=False)

print("Data Preparation Complete. Files saved: 'X_train_smote.csv', 'X_test.csv', 'feature_columns.pkl'")
