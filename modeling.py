import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib
import warnings
warnings.filterwarnings("ignore")

# Project3 Core Module - Soil Moisture Trend Prediction with ML Models
df = pd.read_csv("preprocessed_data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)

# Prepare features (Temperature, Air Humidity) and target (Soil Moisture)
X = df[["Temperature_Norm", "Air_Humidity_Norm"]].values
y = df["Soil_Moisture_Norm"].values

# Split training and testing dataset (80% train / 20% test)
train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# ---------------- Linear Regression Model ----------------
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

# Evaluate Linear Regression Performance
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
print("=== Project3 Linear Regression Performance ===")
print(f"Mean Squared Error (MSE): {mse_lr:.4f}")
print(f"R Squared (R²): {r2_lr:.4f}\n")

# ---------------- LSTM Model for Time Series Prediction ----------------
def create_sequences(X, y, time_steps=3):
    X_seq, y_seq = [], []
    for i in range(len(X) - time_steps):
        X_seq.append(X[i:i+time_steps])
        y_seq.append(y[i+time_steps])
    return np.array(X_seq), np.array(y_seq)

time_steps = 3
X_train_seq, y_train_seq = create_sequences(X_train, y_train, time_steps)
X_test_seq, y_test_seq = create_sequences(X_test, y_test, time_steps)

# Build LSTM Neural Network
lstm_model = Sequential()
lstm_model.add(LSTM(50, activation="relu", input_shape=(time_steps, X_train.shape[1])))
lstm_model.add(Dense(1))
lstm_model.compile(optimizer="adam", loss="mse")

# Train LSTM Model
history = lstm_model.fit(X_train_seq, y_train_seq, epochs=20, batch_size=4, validation_split=0.1)

# Predict and Evaluate LSTM
y_pred_lstm = lstm_model.predict(X_test_seq)
mse_lstm = mean_squared_error(y_test_seq, y_pred_lstm)
r2_lstm = r2_score(y_test_seq, y_pred_lstm)
print("=== Project3 LSTM Model Performance ===")
print(f"Mean Squared Error (MSE): {mse_lstm:.4f}")
print(f"R Squared (R²): {r2_lstm:.4f}\n")

# ---------------- Save Models and Metrics ----------------
joblib.dump(lr_model, "linear_regression_model.pkl")
lstm_model.save("lstm_model.h5")

# Save performance metrics to file
with open("model_performance.txt", "w") as f:
    f.write("Project3 - Soil Moisture Prediction Model Performance Metrics\n")
    f.write("="*60 + "\n")
    f.write(f"Linear Regression - MSE: {mse_lr:.4f}, R²: {r2_lr:.4f}\n")
    f.write(f"LSTM Model - MSE: {mse_lstm:.4f}, R²: {r2_lstm:.4f}\n")

# Plot Prediction Results
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.scatter(y_test, y_pred_lr, color="blue", alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.xlabel("Actual Moisture (Normalized)")
plt.ylabel("Predicted Moisture (Normalized)")
plt.title(f"Linear Regression (R²={r2_lr:.4f})")

plt.subplot(1,2,2)
plt.plot(y_test_seq, color="green", label="Actual Moisture")
plt.plot(y_pred_lstm, color="orange", linestyle="--", label="Predicted Moisture")
plt.xlabel("Time Steps")
plt.ylabel("Soil Moisture (Normalized)")
plt.title(f"LSTM Prediction (R²={r2_lstm:.4f})")
plt.legend()

plt.tight_layout()
plt.savefig("model_predictions.png", dpi=300)
plt.show()

print("Project3: All models and performance metrics saved successfully!")
