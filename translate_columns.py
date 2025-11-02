import pandas as pd

# Define the translation mapping
translation_map = {
    'Date': 'Tanggal',
    'Location': 'Lokasi',
    'MinTemp': 'SuhuMin',
    'MaxTemp': 'SuhuMax',
    'Rainfall': 'CurahHujan',
    'Evaporation': 'Penguapan',
    'Sunshine': 'SinarMatahari',
    'WindGustDir': 'ArahAnginKencang',
    'WindGustSpeed': 'KecepatanAnginKencang',
    'WindDir9am': 'ArahAnginJam9',
    'WindDir3pm': 'ArahAnginJam3',
    'WindSpeed9am': 'KecepatanAnginJam9',
    'WindSpeed3pm': 'KecepatanAnginJam3',
    'Humidity9am': 'KelembabanJam9',
    'Humidity3pm': 'KelembabanJam3',
    'Pressure9am': 'TekananUdaraJam9',
    'Pressure3pm': 'TekananUdaraJam3',
    'Cloud9am': 'AwanJam9',
    'Cloud3pm': 'AwanJam3',
    'Temp9am': 'SuhuJam9',
    'Temp3pm': 'SuhuJam3',
    'RainToday': 'HujanHariIni',
    'RainTomorrow': 'HujanBesok'
}

# Read the original CSV file
df = pd.read_csv('weatherAUS_50k.csv')

# Rename the columns using the translation map
df.rename(columns=translation_map, inplace=True)

# Save the DataFrame with Indonesian column names to a new CSV file
df.to_csv('weatherAUS_50k_indonesian.csv', index=False)

print("Column names have been successfully translated to Indonesian.")