from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base 

url = "mysql+mysqlconnector://root:%s@localhost:3306/students" % quote("Arkay@210")

engine = create_engine(url)

sesssionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()