from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class WeatherStation(Base):
    __tablename__ = 'weather_stations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_name = Column(String(255), unique=True, nullable=False)

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('weather_stations.id'), nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Integer)
    min_temp = Column(Integer)
    precipitation = Column(Integer)

    station = relationship('WeatherStation', back_populates='weather_data')
    __table_args__ = (UniqueConstraint('station_id', 'date', name='unique_station_date'),)

WeatherStation.weather_data = relationship('WeatherData', order_by=WeatherData.id, back_populates='station')

class WeatherStatistics(Base):
    __tablename__ = 'weather_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('weather_stations.id'), nullable=False)
    year = Column(Integer, nullable=False)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)

    station = relationship('WeatherStation')
    __table_args__ = (UniqueConstraint('station_id', 'year', name='unique_station_year'),)


