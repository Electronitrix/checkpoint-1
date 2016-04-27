from rooms import Room, Office, LivingSpace
from persons import Person, Staff, Fellow
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///app.db', echo=True)
Session = sessionmaker(bind=engine)
