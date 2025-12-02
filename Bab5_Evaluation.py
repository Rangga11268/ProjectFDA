import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings

# BAB 5: EVALUATION

warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("Starting Evaluation Phase...")

# 5.1 Load Data and Model
print("\nLoading test dataset and trained model...")
try:
    test_data = pd.read_csv('X_test.csv')
    model = joblib.load('random_forest_model.pkl')
    
    X_test = test_data.drop('HujanBesok', axis=1)
    y_test = test_data['HujanBesok']
    
    print(f"Test data shape: {X_test.shape}")
    print("Model loaded successfully.")
    
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure Bab3 and Bab4 scripts have been run.")
    exit()

# 5.2 Make Predictions
print("\nMaking predictions on test data...")
y_pred = model.predict(X_test)

# 5.3 Accuracy Score
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy Score: {accuracy:.4f} ({accuracy:.2%})")

# 5.4 Confusion Matrix
print("\nGenerating Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Tidak Hujan', 'Hujan'], yticklabels=['Tidak Hujan', 'Hujan'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# 5.5 Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Tidak Hujan', 'Hujan']))

# 5.6 Feature Importance
print("\nAnalyzing Feature Importance...")
feature_importances = model.feature_importances_
feature_names = X_test.columns

# Create a DataFrame for better visualization
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=True)

# Visualize Top 10 Features
plt.figure(figsize=(10, 8))
top_features = importance_df.tail(10)
plt.barh(range(len(top_features)), top_features['Importance'], align='center')
plt.yticks(range(len(top_features)), top_features['Feature'])
plt.xlabel('Importance Score')
plt.ylabel('Features')
plt.title('Top 10 Feature Importance')
plt.tight_layout()
plt.show()

print("\nTop 5 Most Important Features:")
print(importance_df.tail(5).sort_values(by='Importance', ascending=False))

print("\nEvaluation Phase Complete.")
