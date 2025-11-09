import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("weatherAUS_rainfall_prediction_dataset_cleaned.csv")

# Convert 'RainTomorrow' to numeric using Label Encoding
le = LabelEncoder()
data['RainTomorrow_encoded'] = le.fit_transform(data['RainTomorrow'])

# Calculate correlation for numeric columns including the encoded target variable
corr_with_target = data.corr(numeric_only=True)['RainTomorrow_encoded'].sort_values(ascending=False)

# Display the correlation with the encoded target variable
print("Korelasi Variabel Numerik terhadap RainTomorrow (Encoded):")
display(corr_with_target)

# Optional: Visualize the correlation with the encoded target variable
plt.figure(figsize=(10,6))
corr_with_target.drop('RainTomorrow_encoded').plot(kind='bar', color='skyblue')
plt.title("Korelasi Variabel Numerik terhadap RainTomorrow (Encoded)")
plt.xlabel("Variabel")
plt.ylabel("Nilai Korelasi")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()