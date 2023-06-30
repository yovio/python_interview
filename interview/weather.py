from datetime import datetime, date


class WeatherDataLine:
    def __init__(self, line: str):
        self._line_items = line.split(',')
    
    @property
    def station(self):
        return self._line_items[0]

    @property
    def timestamp(self):
        return datetime.strptime(self._line_items[1], "%m/%d/%Y %I:%M:%S %p")

    @property
    def air_temp(self):
        return float(self._line_items[2])

    @property
    def date(self):
        return self.timestamp.date()

    @property
    def summary_key(self):
        return f"{self.station}-{self.timestamp.date():%Y-%m-%d}"

    def __repr__(self):
        return f"WeatherDataLine({self.station}, {self.timestamp}, {self.air_temp})"
        
class SummaryWeatherData:
    def __init__(self, data: WeatherDataLine):
        self.station = data.station
        self.date = data.date
        self.min = data.air_temp
        self.max = data.air_temp
        self.first = data.air_temp
        self.last = data.air_temp

    def add_data(self, data: WeatherDataLine):
        if self.min > data.air_temp:
            self.min = data.air_temp
        if self.max < data.air_temp:
            self.max = data.air_temp

        self.first = data.air_temp # We do this because the data shown that it was written in descending timeline. If data is unordered, we need to keep timestamp and compare it so we know 1st and last


    def __str__(self):
        return f"{self.station},{self.date:%m/%d/%Y},{self.min},{self.max},{self.first},{self.last}"

def process_csv(reader, writer):
    summary_data = {}
    line = reader.readline().strip()
    while line:
        line = reader.readline()        
        if 'Station Name,Measurement Timestamp' in line: # last line contains this
            break
        
        if line:
            try:
                wd = WeatherDataLine(line)
                
                cur_data = summary_data.get(wd.summary_key, None)        
                if cur_data is None:
                    cur_data = SummaryWeatherData(wd)
                    summary_data[wd.summary_key] = cur_data
                else:
                    cur_data.add_data(wd)
            except Exception as ex:
                print(f"exception on line: {line} Ex: {ex}")
                break

    writer.write("Station Name,Date,Min Temp,Max Temp,First Temp,Last Temp\n")
    
    for sum_val in summary_data.values():
        writer.write(f"{sum_val}\n")