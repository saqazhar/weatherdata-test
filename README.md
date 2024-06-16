Weather Data API

Local setup

git clone <repo_url>

pip install -r requirements.txt

chmod +x ./run_all.sh

./run_ all.sh

API Endpoints

/api/weather
This endpoint returns a paginated list of weather data records. The response includes the following fields:

id: The unique ID of the record
station_id: The ID of the weather station that recorded the data station table
date: The date of the record in YYYY-MM-DD format
max_temp: The maximum temperature for the day in degrees Celsius
min_temp: The minimum temperature for the day in degrees Celsius
precipitation: The amount of precipitation for the day in centimeters
You can filter the response by date and station ID using the date and station_id query parameters respectively.

/api/weather/stats
This endpoint returns a paginated list of weather data statistics, aggregated by year and station. The response includes the following fields:

id: The unique ID of the record
station_id: The ID of the weather station
year: The year of the statistics
avg_max_temp: The average maximum temperature for the year in degrees Celsius
avg_min_temp: The average minimum temperature for the year in degrees Celsius
total_precipitation: The total accumulated precipitation for the year in centimeters




API Documentation

To access the Swagger documentation, start the Django development server and navigate to http://localhost:5000/swagger/. This will display the Swagger UI, which allows you to interact with the API and view its documentation.



Testing

This project includes a suite of automated tests to ensure its functionality. To run the tests, activate your virtual environment and use the following command:

pytest test.py


