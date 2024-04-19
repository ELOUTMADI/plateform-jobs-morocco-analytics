from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

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

class Skill(Base):
    __tablename__ = 'skills'
    skill_id = Column(Integer, primary_key=True)
    skill_name = Column(String)

class JobPosting(Base):
    __tablename__ = 'job_postings'
    job_id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    job_type_id = Column(Integer, ForeignKey('job_types.job_type_id'))
    posted_date = Column(Date)
    description = Column(String)
    years_experience = Column(Integer)
    company = relationship("Company")
    location = relationship("Location")
    job_type = relationship("JobType")

# Connecting to a PostgreSQL database
engine = create_engine('postgresql://admin:admin@localhost:5432/linkedin')
Base.metadata.create_all(engine)  # Creates the tables

Session = sessionmaker(bind=engine)
session = Session()

# Example to add a new company
new_company = Company(name="Example Company", industry="Software", size="100-500")
session.add(new_company)
session.commit()
