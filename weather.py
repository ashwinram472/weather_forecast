import requests as re
import pandas as pd
import datetime
import csv
import os


def get_temp(city):
    data = re.get('http://api.openweathermap.org/data/2.5/forecast?q=' +
                  city+'&appid=f6239495a3d267c31944a2930487d78c').json()['list']
    df = pd.DataFrame(data)
    df['dt'] = df['dt'].apply(lambda x: (
        datetime.datetime.fromtimestamp(x)).day)
    today = datetime.datetime.now().day
    df = df[df['dt'] != today]

    temp_min = []
    temp_max = []
    for i in df['main']:
        d = dict(i)
        temp_min.append(d['temp_min'] - 273.15)
        temp_max.append(d['temp_max'] - 273.15)
    df['temp_low'] = temp_min
    df['temp_high'] = temp_max

    df1 = df.groupby('dt').mean()
    low = df1['temp_low']
    high = df1['temp_high']
    f = low.to_list()
    g = high.to_list()
    temp = []
    for i, j in zip(f, g):
        temp.append(i)
        temp.append(j)
    temp.append(min(temp))
    temp.append(max(temp))
    tem = [round(i, 2) for i in temp]

    return tem


if __name__ == "__main__":
    print('Hello')
    n = int(input('Enter number of cities:'))
    cities = []
    for i in range(n):
        print('Enter city ', i, ':')
        cities.append(input())

    with open('temp.csv', 'w', newline='') as file:
        fields = ['City', 'Min 1', 'Max 1', 'Min 2', 'Max 2',
                  'Min 3', 'Max 3', 'Min 4', 'Max 4', 'Min 5', 'Max 5', 'Min Avg', 'Max Avg']
        writer = csv.writer(file, delimiter=',')
        writer.writerow(fields)
        for city in cities:
            writer.writerow([city] + get_temp(city))
    print('The output is written to temp.csv')
