import pickle
import os


#directory = os.path.dirname(__file__) + "\\"
with open('bus_data_2.pkl', 'rb') as handle:
    data = pickle.load(handle)

for stop, stop_data in data.items():
    if stop_data['total_stops'] > 0:
        print(stop_data['journey_dict'])
        # for line, count in stop_data['bus_dict']:
        #     print(line, count)