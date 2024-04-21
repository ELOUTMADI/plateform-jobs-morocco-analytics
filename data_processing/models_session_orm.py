from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Define your models as previously done
class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    name = Column(String)
    industry = Column(String)
    size = Column(String)

class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    city = Column(String)
    region = Column(String)
    country = Column(String)

class JobType(Base):
    __tablename__ = 'job_types'
    job_type_id = Column(Integer, primary_key=True)
    type_description = Column(String)

class JobPosting(Base):
    __tablename__ = 'job_postings'
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    job_type_id = Column(Integer, ForeignKey('job_types.job_type_id'))
    posted_date = Column(Date)
    description = Column(String)
    years_experience = Column(Integer)
    skills = Column(ARRAY(String))

engine = create_engine('postgresql://admin:admin@localhost:5432/linkedin')
Base.metadata.create_all(engine)

