# Data Modeling for Weather Prediction
# This script implements the data modeling phase for the weather prediction dataset as outlined in the datamodeling document.
# The goal is to build a Random Forest model to predict rain on the following day with proper handling of class imbalance using SMOTE.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("# Data Modeling for Weather Prediction")
print("This script implements the data modeling phase for the weather prediction dataset as outlined in the datamodeling document.")
print("The goal is to build a Random Forest model to predict rain on the following day with proper handling of class imbalance using SMOTE.\n")

# Load the prepared dataset
df = pd.read_csv('weatherAUS_prepared.csv')
print("Dataset shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

# Separate features (X) and target (y)
feature_columns = [col for col in df.columns if col not in ['HujanBesok', 'Tanggal']]
X = df[feature_columns]
y = df['HujanBesok']

print(f"\nFeatures shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Target distribution:\n{y.value_counts()}\n")
print(f"Target distribution (%):\n{(y.value_counts() / len(y)) * 100}")

# Split the dataset into training and testing sets (80% - 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nX_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")

print(f"\nTraining set target distribution (%):\n{(y_train.value_counts() / len(y_train)) * 100}")
print(f"\nTesting set target distribution (%):\n{(y_test.value_counts() / len(y_test)) * 100}")

# Apply SMOTE to balance the training data
print("\n## 4.2 Penanganan *Class Imbalance* dengan SMOTE")
print("Tujuan: Menyeimbangkan distribusi kelas pada data latih untuk meningkatkan performa model.\n")

print("Before SMOTE:")
print(f"Training set target distribution (%): {(y_train.value_counts() / len(y_train)) * 100}")

smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"\nAfter SMOTE:")
print(f"X_train_smote shape: {X_train_smote.shape}")
print(f"y_train_smote shape: {y_train_smote.shape}")
print(f"SMOTE target distribution (%): {(y_train_smote.value_counts() / len(y_train_smote)) * 100}")

# Initialize the Random Forest Classifier
print("\n## 4.3 Pemilihan dan Inisialisasi Model")
print("Tujuan: Menjelaskan model yang digunakan.\n")

# Note: Since we already used SMOTE to handle class imbalance, we don't need class_weight='balanced'
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2
)

print("Random Forest Classifier initialized with:")
print("- n_estimators: 100")
print("- max_depth: 10")
print("- min_samples_split: 5")
print("- min_samples_leaf: 2")
print("- random_state: 42")

# Train the model using the SMOTE-balanced training data
print("\n## 4.4 Pelatihan Model (*Training*)")
print("Tujuan: Menjelaskan proses \"belajar\" dari model.\n")

print("Training the Random Forest model with SMOTE data...")
model.fit(X_train_smote, y_train_smote)
print("Model training completed.")

# Make predictions on the original test set (not SMOTE)
print("\n## 4.5 Penerapan Model pada Data Uji")
print("Tujuan: Membuat prediksi pada data yang belum pernah dilihat.\n")

y_pred = model.predict(X_test)

print("Predictions completed.")
print(f"Shape of predictions: {y_pred.shape}")
print(f"Prediction distribution: {pd.Series(y_pred).value_counts()}")

# Model Evaluation
print("\n## Model Evaluation")

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy Score: {accuracy:.4f}")

# Detailed classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Rain', 'Rain']))

# Confusion Matrix
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Create a visualization of the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No Rain', 'Rain'], yticklabels=['No Rain', 'Rain'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Feature Importance
print("\nFeature Importance:")

feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values(by='importance', ascending=False)

print("Top 10 Most Important Features:")
print(feature_importance.head(10))

# Plot top 10 features
plt.figure(figsize=(10, 6))
top_features = feature_importance.head(10)
plt.barh(top_features['feature'], top_features['importance'])
plt.title('Top 10 Feature Importances')
plt.xlabel('Importance')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

print(f"\n## Summary")
print(f"The Random Forest model has been successfully trained using the SMOTE-balanced training data and evaluated on the original test set.")
print(f"The model achieved an accuracy of {accuracy:.4f}. The SMOTE technique helped address the class imbalance issue from the original dataset,")
print(f"which should improve the model's ability to correctly predict rain days.")