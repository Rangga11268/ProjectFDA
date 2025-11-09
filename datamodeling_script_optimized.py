# Data Modeling for Weather Prediction
# This script implements the data modeling phase for the weather prediction dataset.
# The prepared dataset has already been processed in the data preparation phase with:
# 1. Data splitting (80% training, 20% testing) 
# 2. SMOTE application to handle class imbalance
# This phase focuses on implementing the Random Forest algorithm to build and evaluate the model.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("# Data Modeling for Weather Prediction")
print("This script implements the data modeling phase for the weather prediction dataset.")
print("The prepared dataset has already been processed in the data preparation phase with:")
print("1. Data splitting (80% training, 20% testing)")
print("2. SMOTE application to handle class imbalance")
print("This phase focuses on implementing the Random Forest algorithm to build and evaluate the model.\n")

# Loading and Preparing the Pre-Split Datasets
print("## Loading and Preparing the Pre-Split Datasets")
print("Loading the training and test datasets that were created in the data preparation phase:")
print("- X_train_smote.csv: Training dataset with SMOTE applied to balance the classes")
print("- X_test.csv: Test dataset for final evaluation")
print("This ensures consistency with the data preparation workflow.\n")

# Load the pre-processed datasets from data preparation phase
print("Loading prepared datasets...")

# Load the SMOTE-balanced training dataset
train_data = pd.read_csv('X_train_smote.csv')
X_train_smote = train_data.drop('HujanBesok', axis=1)
y_train_smote = train_data['HujanBesok']

# Load the test dataset
test_data = pd.read_csv('X_test.csv')
X_test = test_data.drop('HujanBesok', axis=1)
y_test = test_data['HujanBesok']

print(f"X_train_smote shape: {X_train_smote.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train_smote shape: {y_train_smote.shape}")
print(f"y_test shape: {y_test.shape}")

print(f"\nTraining set target distribution (%):\n{y_train_smote.value_counts(normalize=True) * 100}")
print(f"\nTesting set target distribution (%):\n{y_test.value_counts(normalize=True) * 100}")

# Initialize the Random Forest Classifier
print("\n## Pemilihan dan Inisialisasi Model")
print("Tujuan: Menjelaskan model yang digunakan.\n")

# Note: Since we already have SMOTE-balanced training data, we don't need class_weight='balanced'
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
print("\n## Pelatihan Model (*Training*)")
print("Tujuan: Menjelaskan proses \"belajar\" dari model.\n")

print("Training the Random Forest model with SMOTE-balanced training data...")
model.fit(X_train_smote, y_train_smote)
print("Model training completed.")

# Make predictions on the test set that was prepared in the data prep phase (not SMOTE)
print("\n## Penerapan Model pada Data Uji")
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

feature_columns = [col for col in X_train_smote.columns]
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
print(f"The Random Forest model has been successfully trained using the SMOTE-balanced training data from the data preparation phase and evaluated on the test set.")
print(f"The model achieved an accuracy of {accuracy:.4f}. The SMOTE technique helped address the class imbalance issue,")
print(f"which should improve the model's ability to correctly predict rain days.")