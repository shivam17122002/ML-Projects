import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load the dataset
df = pd.read_csv("wallet_features_with_scores.csv")

# Prepare data
X = df.drop(columns=["userWallet", "credit_score"])
y = df["credit_score"]

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a simple model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE: {mae:.2f}")

# Save the model
joblib.dump(model, "credit_score_model.pkl")
print("✅ Model saved as credit_score_model.pkl")
