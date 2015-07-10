### Problem Set 5: MapReduce on Subway Data

1. Ridership per station
    - mapper: [riders_per_station_mapper.py](riders_per_station_mapper.py)
    - reducer: [riders_per_station_reducer.py](riders_per_station_reducer.py)
    - running the code:

          cat ../ps4/turnstile_data_master_with_weather.csv | python riders_per_station_mapper.py | sort | python riders_per_station_reducer.py

2. Ridership by Weather Type
    - mapper: [ridership_by_weather_mapper.py](ridership_by_weather_mapper.py)
    - reducer: [ridership_by_weather_reducer.py](ridership_by_weather_reducer.py)
    - running the code:

          cat ../ps4/turnstile_data_master_with_weather.csv | python ridership_by_weather_mapper.py | sort | python ridership_by_weather_reducer.py

          fog-norain      1315.57980681
          fog-rain	      1115.13151799
          nofog-norain	  1078.54679697
          nofog-rain	    1098.95330076

3. Busiest Hour
    - mapper: [busiest_hour_mapper.py](busiest_hour_mapper.py)
    - reducer: [busiest_hour_reducer.py](busiest_hour_reducer.py)
    - running the code:

          cat ../ps4/turnstile_data_master_with_weather.csv | python busiest_hour_mapper.py | sort | python busiest_hour_reducer.py
