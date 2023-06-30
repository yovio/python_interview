from interview import weather
import io
from datetime import datetime, date
import pandas as pd
import os

def test_full_using_pandas():    
    writer = io.StringIO()
    with open("./data/chicago_beach_weather.csv") as file:
        weather.process_csv(file, writer)
    writer.seek(0)
    results = writer.readlines()[1:]

    df = pd.read_csv("./data/chicago_beach_weather.csv")
    df.insert(1, 'timestamp', df.apply(lambda x: datetime.strptime(x['Measurement Timestamp'], "%m/%d/%Y %I:%M:%S %p"), axis=1))
    df.insert(1, 'date', df.apply(lambda x: x.timestamp.date(), axis=1))
    
    grouped_df =  df.groupby(['Station Name', 'date'], sort=False)

    res_idx = 0
    for key, _ in grouped_df:
        print(f"Asserting {key}")

        gdf = grouped_df.get_group(key)

        res_splits = results[res_idx].split(',')
               
        sorted_df = gdf.sort_values(by=['timestamp'])
        assert res_splits[0] == sorted_df['Station Name'].iloc[0]
        assert res_splits[1] == datetime.strftime(sorted_df['date'].iloc[0], "%m/%d/%Y")

        assert float(res_splits[2]) == sorted_df['Air Temperature'].min()
        assert float(res_splits[3]) == sorted_df['Air Temperature'].max()
        assert float(res_splits[4]) == sorted_df['Air Temperature'].iloc[0]
        assert float(res_splits[5]) == sorted_df['Air Temperature'].iloc[-1]
        
        res_idx += 1

        # if res_idx > 10:
        #     break

def test_weather_data_line_cls():
    wdl = weather.WeatherDataLine("63rd Street Weather Station,12/31/2016 11:00:00 PM,-1.3,-2.8,73,0,0,39.3,0,264,2.2,3.2,992.3,5,354,11.8,12/31/2016 11:00 PM,63rdStreetWeatherStation201612312300")

    assert wdl.station == "63rd Street Weather Station"
    assert wdl.timestamp == datetime(2016, 12, 31, 23)
    assert wdl.date == date(2016, 12, 31)
    assert wdl.air_temp == -1.3

    assert wdl.summary_key == "63rd Street Weather Station-2016-12-31"
