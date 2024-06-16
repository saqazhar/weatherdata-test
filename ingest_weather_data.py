import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WeatherStation, WeatherData

# Database setup
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def parse_line(line):
    parts = line.strip().split('\t')
    date = datetime.datetime.strptime(parts[0], '%Y%m%d').date()
    max_temp = int(parts[1])
    min_temp = int(parts[2])
    precipitation = int(parts[3])
    return date, max_temp, min_temp, precipitation

def ingest_file(file_path, station_name):
    station = session.query(WeatherStation).filter_by(station_name=station_name).first()
    if not station:
        station = WeatherStation(station_name=station_name)
        session.add(station)
        session.commit()

    with open(file_path, 'r') as file:
        for line in file:
            date, max_temp, min_temp, precipitation = parse_line(line)
            if session.query(WeatherData).filter_by(station_id=station.id, date=date).first():
                continue
            weather_record = WeatherData(
                station_id=station.id,
                date=date,
                max_temp=max_temp,
                min_temp=min_temp,
                precipitation=precipitation
            )
            session.add(weather_record)
        session.commit()

def main(data_dir):
    start_time = datetime.datetime.now()
    print(f"Ingestion started at {start_time}")

    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_dir, filename)
            station_name = os.path.splitext(filename)[0]
            ingest_file(file_path, station_name)
    
    end_time = datetime.datetime.now()
    print(f"Ingestion completed at {end_time}")
    print(f"Total time taken: {end_time - start_time}")

if __name__ == "__main__":
    data_dir = 'wx_data'
    main(data_dir)
