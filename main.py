import typer
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

app = typer.Typer()

engine = create_engine("sqlite:///top_drives.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True)
    car_name = Column(String)
    year = Column(Integer)
    max_speed = Column(Float)
    acceleration = Column(Float)
    handling = Column(Float)
    drive_type = Column(String)
    tires = Column(String)
    abs = Column(Integer)
    traction_control = Column(Integer)
    torque = Column(Float)
    power = Column(Float)
    clearance = Column(Float)
    engine_upgrade = Column(String)
    weight_upgrade = Column(Integer)
    handling_upgrade = Column(Integer)

class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True)
    track_name = Column(String)
    weather = Column(String)
    surface = Column(String)

class Race(Base):
    __tablename__ = "races"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    track_id = Column(Integer, ForeignKey("tracks.id"))
    lap_time = Column(Float)
    car = relationship("Car")
    track = relationship("Track")

Base.metadata.create_all(engine)

@app.command()
def add_car():
    """Добавить новую машину."""
    car_name = typer.prompt("Название машины")
    year = typer.prompt("Год производства", type=int)
    max_speed = typer.prompt("Максимальная скорость (км/ч)", type=float)
    acceleration = typer.prompt("Ускорение (сек до 100 км/ч)", type=float)
    handling = typer.prompt("Управляемость (баллы, 1-100)", type=float)
    drive_type = typer.prompt("Тип привода (AWD/FWD/RWD)")
    tires = typer.prompt("Тип шин (Dry/Wet/Snow)")
    abs_system = typer.prompt("Наличие АБС (1 - есть, 0 - нет)", type=int)
    traction_control = typer.prompt("Наличие тракшн-контроля (1 - есть, 0 - нет)", type=int)
    torque = typer.prompt("Максимальный крутящий момент (Нм)", type=float)
    power = typer.prompt("Максимальная мощность (л.с.)", type=float)
    clearance = typer.prompt("Клиренс (мм)", type=float)
    engine_upgrade = typer.prompt("Улучшение двигателя (1.1 - 3.3)")
    weight_upgrade = typer.prompt("Улучшение веса (1 - 3)", type=int)
    handling_upgrade = typer.prompt("Улучшение управления (1 - 3)", type=int)

    car = Car(
        car_name=car_name, year=year, max_speed=max_speed, acceleration=acceleration,
        handling=handling, drive_type=drive_type, tires=tires, abs=abs_system,
        traction_control=traction_control, torque=torque, power=power, clearance=clearance,
        engine_upgrade=engine_upgrade, weight_upgrade=weight_upgrade, handling_upgrade=handling_upgrade
    )
    session.add(car)
    session.commit()
    typer.echo(f"Машина '{car_name}' добавлена!")

@app.command()
def add_track():
    """Добавить новую трассу."""
    track_name = typer.prompt("Название трассы")
    weather = typer.prompt("Погода (Dry/Rain/Snow)")
    surface = typer.prompt("Тип покрытия (dirt/asphalt/mixed/snow/ice/grass)")  # Ввод типа покрытия
    
    track = Track(track_name=track_name, weather=weather, surface=surface)
    session.add(track)
    session.commit()
    typer.echo(f"Трасса '{track_name}' добавлена!")

@app.command()
def record_race():
    """Записать результат гонки."""
    typer.echo("Список машин:")
    cars = pd.read_sql("SELECT * FROM cars", engine)
    typer.echo(cars)
    car_id = typer.prompt("ID машины", type=int)
    
    typer.echo("Список трасс:")
    tracks = pd.read_sql("SELECT * FROM tracks", engine)
    typer.echo(tracks)
    track_id = typer.prompt("ID трассы", type=int)
    
    lap_time = typer.prompt("Время прохождения трассы (сек)", type=float)

    race = Race(car_id=car_id, track_id=track_id, lap_time=lap_time)
    session.add(race)
    session.commit()
    typer.echo("Результат гонки добавлен!")

@app.command()
def view_data():
    """Показать данные."""
    typer.echo("Машины:")
    cars = pd.read_sql("SELECT * FROM cars", engine)
    typer.echo(cars)

    typer.echo("\nТрассы:")
    tracks = pd.read_sql("SELECT * FROM tracks", engine)
    typer.echo(tracks)

    typer.echo("\nГонки:")
    races = pd.read_sql("""
    SELECT races.id, cars.car_name, tracks.track_name, tracks.surface, races.lap_time
    FROM races
    JOIN cars ON races.car_id = cars.id
    JOIN tracks ON races.track_id = tracks.id
    """, engine)
    typer.echo(races)

# Запуск приложения
if __name__ == "__main__":
    app()
