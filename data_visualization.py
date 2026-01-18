import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Project3 Data Visualization - Plot preprocessed sensor data trends
df = pd.read_csv("preprocessed_data.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df.set_index("Timestamp", inplace=True)

# Create 3 stacked subplots with shared x-axis
plt.style.use("seaborn-v0_8-whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# Plot Soil Moisture Trend
axes[0].plot(df.index, df["Soil_Moisture_Denoised"], color="green", linewidth=2, label="Denoised Soil Moisture")
axes[0].set_ylabel("Soil Moisture (0-1023 Scale)")
axes[0].set_title("Project3: Soil Moisture Trend Over 48 Hours", fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot Temperature Trend
axes[1].plot(df.index, df["Temperature_Denoised"], color="red", linewidth=2, label="Denoised Temperature")
axes[1].set_ylabel("Temperature (°C)")
axes[1].set_title("Project3: Ambient Temperature Trend Over 48 Hours", fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Plot Air Humidity Trend
axes[2].plot(df.index, df["Air_Humidity_Denoised"], color="blue", linewidth=2, label="Denoised Air Humidity")
axes[2].set_ylabel("Air Humidity (%)")
axes[2].set_xlabel("Time", fontsize=12)
axes[2].set_title("Project3: Air Humidity Trend Over 48 Hours", fontsize=12)
axes[2].legend()
axes[2].grid(True, alpha=0.3)

# Format x-axis for time display
axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
axes[2].xaxis.set_major_locator(mdates.HourLocator(interval=6))
plt.xticks(rotation=45)

# Save visualization plot
plt.tight_layout()
plt.savefig("data_trends.png", dpi=300, bbox_inches="tight")
plt.show()

print("Project3: Data visualization completed - plot saved as data_trends.png")
