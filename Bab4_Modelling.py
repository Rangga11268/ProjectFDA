import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import warnings

# BAB 4: MODELLING

warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("Starting Modelling Phase...")

# 4.1 Model Selection and Initialization
print("\nInitializing Random Forest Classifier...")
# Random Forest selected for its ability to handle outliers and provide feature importance.
model = RandomForestClassifier(random_state=42)
print("Model initialized with random_state=42.")

# 4.2 Model Training
print("\nLoading prepared datasets...")
try:
    train_data = pd.read_csv('X_train_smote.csv')
    test_data = pd.read_csv('X_test.csv')
    
    X_train_smote = train_data.drop('HujanBesok', axis=1)
    y_train_smote = train_data['HujanBesok']
    
    X_test = test_data.drop('HujanBesok', axis=1)
    # y_test is needed for evaluation later, but here we just need X_test for prediction if we were to predict.
    # However, the notebook flow trains on SMOTE data.
    
    print(f"Training data shape: {X_train_smote.shape}")
    print(f"Test data shape: {X_test.shape}")
    
except FileNotFoundError:
    print("Error: Prepared datasets not found. Please run Bab3_DataPreparation.py first.")
    exit()

print("\nTraining the model (this may take a moment)...")
model.fit(X_train_smote, y_train_smote)
print("Model training complete.")

# 4.3 Prediction on Test Data
print("\nMaking predictions on test data...")
y_pred = model.predict(X_test)

print(f"Predictions made: {len(y_pred)}")
print(f"Prediction distribution: {pd.Series(y_pred).value_counts().to_dict()}")

# Save the trained model
print("\nSaving the trained model...")
joblib.dump(model, 'random_forest_model.pkl')
print("Model saved as 'random_forest_model.pkl'.")

print("\nModelling Phase Complete.")
