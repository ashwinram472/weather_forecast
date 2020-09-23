##########################################
########## ASHWIN BALASUBRAMANIAM ########
######### PYTHON WEATHER ASSIGNMENT ######
##########################################

# Importing the required packages
import requests as re
import pandas as pd
import datetime
import csv
from statistics import mean


def get_temp(city):
    # Getting the JSON Data
    # Enter your API key
    api_key = ''
    data = re.get('http://api.openweathermap.org/data/2.5/forecast?q=' +
                  city+'‘&units=metric&appid='+api_key).json()['list']
    # Converting to DataFrame
    df = pd.DataFrame(data)
    # Converting the Timestamp to datetime format and extracting the day
    df['dt'] = df['dt'].apply(lambda x: (
        datetime.datetime.fromtimestamp(x)).day)
    today = datetime.datetime.now().day
    # Substting the days from today
    df = df[df['dt'] != today]
    # Appedning the Min and Max temperatures of each day for each 3 hours
    temp_min = []
    temp_max = []
    for i in df['main']:
        d = dict(i)
        temp_min.append(d['temp_min'])
        temp_max.append(d['temp_max'])
    df['temp_low'] = temp_min
    df['temp_high'] = temp_max
    # Aggregating the data to get the minimum and maximum of each day!
    df1 = df.groupby('dt').agg({'temp_low': 'min', 'temp_high': 'max'})
    low = df1['temp_low'].to_list()
    high = df1['temp_high'].to_list()
    temp = []
    for i, j in zip(low, high):
        temp.append(i)
        temp.append(j)
    # Getting the mean of min and max temperatures
    temp.append(mean(low))
    temp.append(mean(high))
    tem = [round(i, 2) for i in temp]

    return tem


if __name__ == "__main__":

    cities = ['Anchorage, USA',
              'Buenos Aires, Argentina',
              'São José dos Campos, Brazil',
              'San José, Costa Rica',
              'Nanaimo, Canada',
              'Ningbo, China',
              'Giza, Egypt',
              'Mannheim, Germany',
              'Hyderabad, India',
              'Tehran, Iran',
              'Bishkek, Kyrgyzstan',
              'Riga, Latvia',
              'Quetta, Pakistan',
              'Warsaw, Poland',
              'Dhahran, Saudia Arabia',
              'Madrid, Spain',
              'Oldham, England']
    # Writing to CSV file
    with open('temp.csv', 'w', newline='') as file:
        fields = ['City', 'Min 1', 'Max 1', 'Min 2', 'Max 2',
                  'Min 3', 'Max 3', 'Min 4', 'Max 4', 'Min 5', 'Max 5', 'Min Avg', 'Max Avg']
        writer = csv.writer(file, delimiter=',')
        writer.writerow(fields)
        for city in cities:
            writer.writerow([city] + get_temp(city))
    print('The output is written to temp.csv')
