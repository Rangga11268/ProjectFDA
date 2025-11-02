import pandas as pd
import random

# Read the full dataset
file_path = 'D:/MATERI SLIDE/Materi SMT3/TUGAS SMT3/FUNDAMENTAL DATA ANALYST (0406)/Project/weatherAUS_rainfall_prediction_dataset_cleaned.csv'
df = pd.read_csv(file_path)

# Create subsets with specified row counts
# Subset 1: 50,025 rows
subset_50k = df.sample(n=50025, random_state=42)
subset_50k.to_csv('weatherAUS_50k.csv', index=False)

# Subset 2: 25,025 rows
subset_25k = df.sample(n=25025, random_state=42)
subset_25k.to_csv('weatherAUS_25k.csv', index=False)

# Subset 3: 10,025 rows
subset_10k = df.sample(n=10025, random_state=42)
subset_10k.to_csv('weatherAUS_10k.csv', index=False)

print("Subsets created successfully:")
print(f"50k subset: {len(subset_50k)} rows")
print(f"25k subset: {len(subset_25k)} rows")
print(f"10k subset: {len(subset_10k)} rows")