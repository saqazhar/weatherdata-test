import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

def lambda_handler_query_weather_data(event, context):
    station_id = event.get('queryStringParameters', {}).get('station_id')
    start_date = event.get('queryStringParameters', {}).get('start_date')
    end_date = event.get('queryStringParameters', {}).get('end_date')

    query = "SELECT * FROM weather_data WHERE 1=1"
    params = []
    if station_id:
        query += " AND station_id = %s"
        params.append(station_id)
    if start_date:
        query += " AND date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND date <= %s"
        params.append(end_date)
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }

def lambda_handler_query_weather_stats(event, context):
    station_id = event.get('queryStringParameters', {}).get('station_id')
    year = event.get('queryStringParameters', {}).get('year')

    query = "SELECT * FROM weather_stats WHERE 1=1"
    params = []
    if station_id:
        query += " AND station_id = %s"
        params.append(station_id)
    if year:
        query += " AND year = %s"
        params.append(year)
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(results, default=str)
    }
