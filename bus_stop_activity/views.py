from django.shortcuts import render
import pickle
import os

# Create your views here.

# directory = os.path.dirname(__file__) + "\\"
# bus_stop_data_raw = pd.read_pickle(directory + 'complete_bus_stop_data.pkl')
# max_count = max(bus_stop_data_raw['bus_count'])
# bus_stop_data = []
# for index, bus_stop in bus_stop_data_raw.iterrows():
#     bus_stop_dict = {
#         'name': bus_stop['name'],
#         'longitude': bus_stop['longitude'],
#         'latitude': bus_stop['latitude'],
#         'bus_count': int(bus_stop['bus_count']),
#         'opacity': min((bus_stop['bus_count']*4)/max_count, 1)
#     }
#     bus_stop_data.append(bus_stop_dict.copy())
#
# buses_data_raw = pd.read_pickle(directory + 'bus_data.pkl')
# buses_data = []
# for index, bus in buses_data_raw.iterrows():
#     if bus['speed'] < 2:
#         buses_dict = {
#             'longitude': bus['longitude'],
#             'latitude': bus['latitude'],
#             'direction': bus['direction']
#         }
#         buses_data.append(buses_dict.copy())

directory = os.path.dirname(__file__) + "\\..\\"
with open(directory + 'bus_data.pkl', 'rb') as handle:
    data = pickle.load(handle)

max_stop_count = 0
for stop, stop_data in data.items():
    if stop_data['total_stops'] > max_stop_count:
        max_stop_count = stop_data['total_stops']
    if stop_data['total_stops'] > 0:
        data[stop]['bus_dict'] = {k: v for k, v in sorted(stop_data['bus_dict'].items(), key=lambda item: item[1], reverse=True)}

max_stop_count

def index(response):
    content = {
        'data': data,
        'max_stop_count': max_stop_count
    }
    return render(response, 'bus_stop_activity/index.html', content)
