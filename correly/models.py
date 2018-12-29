from datetime import datetime
from queue import Queue
from sqlalchemy import (
    Column,
    create_engine,
    Integer,
    String,
    Float,
    DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


Base = declarative_base()


class SensorReadings(Base):
    __tablename__ = 'sensor_readings'

    timestamp = Column(DateTime, default=datetime.utcnow, primary_key=True)
    location = Column(String(200))
    temperature = Column('temp', Float)
    humidity = Column(Float)
    pressure = Column(Float)


def process_readings(uri: str, msg_queue: Queue, exiting):
    engine = create_engine(uri)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    while not exiting.is_set():
        while not msg_queue.empty():
            msg = msg_queue.get()
            reading = SensorReadings(**msg)
            session.add(reading)

        session.commit()
