import pandas as pd
import numpy as np


def load_data():
    data = pd.read_csv("data/household_power_consumption.txt", sep=';', low_memory=False)

    data.columns = data.columns.str.strip()
    data.replace('?', np.nan, inplace=True)

    data['Global_active_power'] = data['Global_active_power'].astype(float)
    data['Global_intensity'] = data['Global_intensity'].astype(float)
    data['Voltage'] = data['Voltage'].astype(float)

    noise = np.random.normal(0, 0.2, len(data))
    data['Global_active_power'] *= (1 + noise)

    data['Random_noise'] = np.random.normal(0, 1, len(data))

    data['Time'] = pd.to_datetime(data['Time'], format='%H:%M:%S', errors='coerce')
    data['Hour'] = data['Time'].dt.hour

    data.dropna(inplace=True)

    data = data.sample(2000, random_state=42)

    return data