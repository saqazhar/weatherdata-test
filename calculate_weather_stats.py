from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WeatherStation, WeatherData, WeatherStatistics

DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def calculate_and_store_statistics():
    stations = session.query(WeatherStation).all()

    for station in stations:
        for year in range(1985, 2015):
            results = session.query(
                func.avg(WeatherData.max_temp).label('avg_max_temp'),
                func.avg(WeatherData.min_temp).label('avg_min_temp'),
                func.sum(WeatherData.precipitation).label('total_precipitation')
            ).filter(
                WeatherData.station_id == station.id,
                func.extract('year', WeatherData.date) == year,
                WeatherData.max_temp != -9999,
                WeatherData.min_temp != -9999,
                WeatherData.precipitation != -9999
            ).one()

            avg_max_temp = results.avg_max_temp / 10 if results.avg_max_temp else None
            avg_min_temp = results.avg_min_temp / 10 if results.avg_min_temp else None
            total_precipitation = results.total_precipitation / 100 if results.total_precipitation else None

            if avg_max_temp is None and avg_min_temp is None and total_precipitation is None:
                continue

            weather_statistics = WeatherStatistics(
                station_id=station.id,
                year=year,
                avg_max_temp=avg_max_temp,
                avg_min_temp=avg_min_temp,
                total_precipitation=total_precipitation
            )
            session.merge(weather_statistics)
        session.commit()

if __name__ == "__main__":
    calculate_and_store_statistics()
