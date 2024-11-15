import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point

file_path = 'cleaned_weather.csv'  # Replace with the path to your CSV file
try:
    accident_data = pd.read_csv("/content/cleaned_weather.csv")
except FileNotFoundError:
    print(f"Error: The file was not found. Please check the file path.")
    exit()
    
print("Dataset Info:")
print(accident_data.info())
print("\nSample Data:")
print(accident_data.head())

accident_data.columns = accident_data.columns.str.strip()  # Remove whitespace from headers

# Convert 'Start_Time' to datetime and extract hour
if 'Start_Time' in accident_data.columns:
    accident_data['Start_Time'] = pd.to_datetime(accident_data['Start_Time'], errors='coerce')
    accident_data['Hour'] = accident_data['Start_Time'].dt.hour  # Extract the hour of the day
else:
    print("Warning: Column 'Start_Time' not found in dataset. Check column names.")

if 'Weather_Condition' in accident_data.columns:
    accident_data['Weather_Condition'] = accident_data['Weather_Condition'].fillna('Unknown')
else:
    print("Warning: Column 'Weather_Condition' not found in dataset. Check column names.")

if 'Road_Condition' not in accident_data.columns:
    print("Note: Column 'Road_Condition' not found in dataset.")

if 'Hour' in accident_data.columns:   # Plot accident distribution by hour of the day
    plt.figure(figsize=(10, 6))
    sns.countplot(data=accident_data, x='Hour', palette='viridis')
    plt.title('Accident Frequency by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Accidents')
    plt.xticks(range(0, 24))
    plt.show()
else:
    print("Note: Column 'Hour' not found in dataset. Skipping hour distribution plot.")

# Plot accident severity by weather condition
if 'Severity' in accident_data.columns and 'Weather_Condition' in accident_data.columns:
    plt.figure(figsize=(12, 6))
    sns.countplot(data=accident_data, x='Weather_Condition', hue='Severity', palette='coolwarm')
    plt.title('Accident Severity by Weather Condition')
    plt.xlabel('Weather Condition')
    plt.ylabel('Number of Accidents')
    plt.legend(title='Severity')
    plt.xticks(rotation=90)
    plt.show()
else:
    print("Note: Columns 'Severity' or 'Weather_Condition' not found in dataset. Skipping severity plot.")

# Visualize accident hotspots on a map
if 'Start_Lat' in accident_data.columns and 'Start_Lng' in accident_data.columns:
    # Create a GeoDataFrame for geographic plotting
    geometry = [Point(xy) for xy in zip(accident_data['Start_Lng'], accident_data['Start_Lat'])]
    geo_df = gpd.GeoDataFrame(accident_data, geometry=geometry)
    
    # Plot the accident hotspots
    plt.figure(figsize=(12, 8))
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    ax = world.plot(color='white', edgecolor='black')
    geo_df.plot(ax=ax, markersize=1, alpha=0.5, color='red')
    plt.title('Accident Hotspots')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
else:
    print("Note: Columns 'Start_Lat' and 'Start_Lng' not found in dataset. Skipping hotspot visualization.")
