from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)


DATABASE = os.environ.get("DATABASE_URL", 'app.db')

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/weather', methods=['GET'])
def get_weather():
    station_id = request.args.get('station_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = "SELECT * FROM weather_data WHERE 1=1"
    args = []
    if station_id:
        query += " AND station_id = ?"
        args.append(station_id)
    if start_date:
        query += " AND date >= ?"
        args.append(start_date)
    if end_date:
        query += " AND date <= ?"
        args.append(end_date)
    
    weather_data = query_db(query, args)
    return jsonify(weather_data)

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    station_id = request.args.get('station_id')
    year = request.args.get('year')
    
    query = "SELECT * FROM weather_statistics WHERE 1=1"
    args = []
    if station_id:
        query += " AND station_id = ?"
        args.append(station_id)
    if year:
        query += " AND year = ?"
        args.append(year)
    
    weather_stats = query_db(query, args)
    return jsonify(weather_stats)

## Swagger setup
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
