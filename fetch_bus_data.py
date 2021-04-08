import pickle
from datetime import datetime as dt
from datetime import timedelta
import urllib.request as ur
import json
from haversine import haversine

# Config
duration = 60 * 60 * 4
max_dist = 0.1  # in km
fetch_interval = 5  # in seconds

# 1) Initiate data and fill in bus stop ids, names and locations
data = {}
bus_stop_json = json.load(
    ur.urlopen('http://data.itsfactory.fi/journeys/api/1/stop-points')
)
for stop in bus_stop_json['body']:
    locations = str(stop['location']).split(',')
    data[stop['shortName']] = {
            'name': stop['name'],
            'latitude': locations[0],
            'longitude': locations[1],
            'total_stops': 0,
            'bus_dict': {},
            'journey_dict': {}
    }


# 2) Fetch bus data
start_time = dt.now()
time = start_time
# makes sure we go to a loop right away
fetch_begun = dt.now() - timedelta(seconds=(fetch_interval + 1))
while (time - start_time).total_seconds() < duration:
    time = dt.now()
    time_passed = (time - fetch_begun).total_seconds()
    if time_passed > fetch_interval:
        print(time_passed)
        fetch_begun = dt.now()
        buses_json = json.load(
            ur.urlopen('http://data.itsfactory.fi/journeys/api/1/vehicle-activity')
        )
        for bus in buses_json['body']:
            line = bus['monitoredVehicleJourney']['journeyPatternRef']
            journey = bus['monitoredVehicleJourney']['journeyPatternRef'] + \
                      bus['monitoredVehicleJourney']['originAimedDepartureTime'] + \
                      bus['monitoredVehicleJourney']['originShortName']
            latitude = float(bus['monitoredVehicleJourney']['vehicleLocation']
                             ['latitude'])
            longitude = float(bus['monitoredVehicleJourney']['vehicleLocation']
                              ['longitude'])
            speed = float(bus['monitoredVehicleJourney']['speed'])
            stop_id = str(bus['monitoredVehicleJourney']['onwardCalls'][0]
                         ['stopPointRef']).split('/')[-1]
            if speed < 3.0:
                dist = haversine((float(data[stop_id]['latitude']),
                     float(data[stop_id]['longitude'])), (float(latitude),
                     float(longitude)))
                if dist < max_dist:
                    if journey not in data[stop_id]['journey_dict'].keys():
                        print(line)
                        data[stop_id]['journey_dict'][journey] = {
                            'latitude': latitude,
                            'longitude': longitude
                        }
                        data[stop_id]['total_stops'] += 1
                        if line not in data[stop_id]['bus_dict'].keys():
                            data[stop_id]['bus_dict'][line] = 1
                        else:
                            data[stop_id]['bus_dict'][line] += 1


with open('bus_data_2.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
