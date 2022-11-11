from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, WeatherReport

from settings import database_config

engine = create_engine(database_config.url, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
    
def add_user(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()

def set_user_city(tg_id, city):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = city
    session.commit()

def create_report(tg_id, temp, feels_like, wind_speed, pressure_mm, city):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    new_report = WeatherReport(temp=temp, feels_like=feels_like, wind_speed=wind_speed, pressure_mm=pressure_mm, city=city, owner=user.id)
    session.add(new_report)
    session.commit()

def get_user_city(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    return user.city

def get_reports(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    reports = user.reports
    return reports

def delete_user_report(report_id):
    session = Session()
    report = session.get(WeatherReport, report_id)
    session.delete(report)
    session.commit()

def get_all_users():
    session = Session()
    users = session.query(User).all()
    return users
