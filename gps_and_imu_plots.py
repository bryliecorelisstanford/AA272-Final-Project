# -*- coding: utf-8 -*-
"""GPS and IMU Plots.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1K77V_ZWDRgQmOde14XQ6Y8HT1m8tKTBN
"""

from scipy.signal import butter, filtfilt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from collections import deque
import os

walking_straight_1 = "walking_straight_1.csv"
turn_1 = "turn_1.csv"
data1 = pd.read_csv(walking_straight_1)
spoofed_data1 = pd.read_csv(turn_1)
walking_straight_2 = "walking_straight_2.csv"
turn_2 = "turn_2.csv"
data2 = pd.read_csv(walking_straight_2)
spoofed_data2 = pd.read_csv(turn_2)

min_length = min(len(data1), len(spoofed_data1))
data1 = data1.iloc[:min_length].reset_index(drop=True)
spoofed_data1 = spoofed_data1.iloc[:min_length].reset_index(drop=True)

min_length = min(len(data2), len(spoofed_data2))
data2 = data2.iloc[:min_length].reset_index(drop=True)
spoofed_data2 = spoofed_data2.iloc[:min_length].reset_index(drop=True)

timestamps = pd.to_datetime(data1["time"])
time = (timestamps - timestamps.iloc[0]).dt.total_seconds()

timestamps_spoofed = pd.to_datetime(spoofed_data1["time"])
time_spoofed = (timestamps_spoofed - timestamps_spoofed.iloc[0]).dt.total_seconds()

timestamps_2 = pd.to_datetime(data2["time"])
time_2 = (timestamps_2 - timestamps_2.iloc[0]).dt.total_seconds()

timestamps_spoofed_2 = pd.to_datetime(spoofed_data2["time"])
time_spoofed_2 = (timestamps_spoofed_2 - timestamps_spoofed_2.iloc[0]).dt.total_seconds()

# lat and long
lat = data1["latitude"].to_numpy()
lon = data1["longitude"].to_numpy()
lat_spoofed = spoofed_data1["latitude"].to_numpy()
lon_spoofed = spoofed_data1["longitude"].to_numpy()
lat_2 = data2["latitude"].to_numpy()
lon_2 = data2["longitude"].to_numpy()
lat_spoofed_2 = spoofed_data2["latitude"].to_numpy()
lon_spoofed_2 = spoofed_data2["longitude"].to_numpy()

# IMU acceleration and gyroscope data from the CSV files
imu_ax = data1["ax"].to_numpy()
imu_ay = data1["ay"].to_numpy()
imu_az = data1["az"].to_numpy()
spoofed_imu_ax = spoofed_data1["ax"].to_numpy()
spoofed_imu_ay = spoofed_data1["ay"].to_numpy()
spoofed_imu_az = spoofed_data1["az"].to_numpy()
gyro_gx = data1["wx"].to_numpy()
gyro_gy = data1["wy"].to_numpy()
gyro_gz = data1["wz"].to_numpy()
spoofed_gyro_gx = spoofed_data1["wx"].to_numpy()
spoofed_gyro_gy = spoofed_data1["wy"].to_numpy()
spoofed_gyro_gz = spoofed_data1["wz"].to_numpy()
imu_ax_2 = data2["ax"].to_numpy()
imu_ay_2 = data2["ay"].to_numpy()
imu_az_2 = data2["az"].to_numpy()
spoofed_imu_ax_2 = spoofed_data2["ax"].to_numpy()
spoofed_imu_ay_2 = spoofed_data2["ay"].to_numpy()
spoofed_imu_az_2 = spoofed_data2["az"].to_numpy()
gyro_gx_2 = data2["wx"].to_numpy()
gyro_gy_2 = data2["wy"].to_numpy()
gyro_gz_2 = data2["wz"].to_numpy()
spoofed_gyro_gx_2 = spoofed_data2["wx"].to_numpy()
spoofed_gyro_gy_2 = spoofed_data2["wy"].to_numpy()
spoofed_gyro_gz_2 = spoofed_data2["wz"].to_numpy()

# Define a function to make subplots for better clarity
def plot_comparison(original, spoofed, time, time_spoofed, labels, ylabel, title):
    plt.figure(figsize=(12, 10))
    for i, label in enumerate(labels):
        plt.subplot(len(labels), 1, i + 1)
        plt.plot(time, original[i], label=f"{label} (Original)", linewidth=2, alpha=0.8)
        plt.plot(time_spoofed, spoofed[i], label=f"{label} (Spoofed)", linestyle="--", linewidth=2, alpha=0.8)
        plt.ylabel(ylabel)
        plt.title(f"{title} - {label}")
        plt.legend()
        plt.grid()
    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.show()

# Compare IMU acceleration data
imu_acc_original_2 = [imu_ax_2, imu_ay_2, imu_az_2]
imu_acc_spoofed_2 = [spoofed_imu_ax_2, spoofed_imu_ay_2, spoofed_imu_az_2]
labels_acc = ["ax", "ay", "az"]
plot_comparison(imu_acc_original_2, imu_acc_spoofed_2, time_2, time_spoofed_2, labels_acc, "Acceleration (m/s²)", "IMU Acceleration Comparison #2")

# Compare gyroscope data
gyro_original_2 = [gyro_gx_2, gyro_gy_2, gyro_gz_2]
gyro_spoofed_2 = [spoofed_gyro_gx_2, spoofed_gyro_gy_2, spoofed_gyro_gz_2]
labels_gyro = ["wx", "wy", "wz"]
plot_comparison(gyro_original_2, gyro_spoofed_2, time_2, time_spoofed_2, labels_gyro, "Angular Velocity (rad/s)", "Gyroscope Data Comparison #2")

# GPS trajectory with annotations
plt.figure(figsize=(10, 6))
plt.plot(lon_2, lat_2, label="Original GPS Path #2", marker="o", linestyle="-", linewidth=2, alpha=0.8, color="blue")
plt.plot(lon_spoofed_2, lat_spoofed_2, label="Spoofed GPS Path #2", marker="x", linestyle="--", linewidth=2, alpha=0.8, color="red")
plt.title("GPS Trajectories with Differences Highlighted")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.grid()

# Highlight differences if they exist
if not np.allclose(lat, lat_spoofed) or not np.allclose(lon, lon_spoofed):
    plt.annotate("Differences here",
                 xy=(lon_spoofed[5], lat_spoofed[5]),
                 xytext=(lon_spoofed[5] + 0.0005, lat_spoofed[5] + 0.0005),
                 arrowprops=dict(facecolor='black', arrowstyle='->'),
                 fontsize=10)
plt.show()