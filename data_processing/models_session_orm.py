from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY , BigInteger , Boolean , Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Define your models as previously done
class Company(Base):
    __tablename__ = 'companies'
    companyID = Column(Integer, primary_key=True)
    company_name = Column(String)
    company_size = Column(String)

class Location(Base):
    __tablename__ = 'locations'
    locationID = Column(Integer, primary_key=True)
    city = Column(String)
    remote_status = Column(String)

class Hirer(Base):
    __tablename__ = 'hirers'
    hirerID = Column(Integer, primary_key=True)
    hiring_team_name = Column(String)
    hirer_job_title = Column(String)

class JobType(Base):
    __tablename__ = 'job_types'
    jobTypeID = Column(Integer, primary_key=True)
    job_type = Column(String)

class Sector(Base):
    __tablename__ = 'sectors'
    sectorID = Column(Integer, primary_key=True)
    sector = Column(String)

class Expertise(Base):
    __tablename__ = 'expertise'
    expertiseID = Column(Integer, primary_key=True)
    expertise = Column(String)

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    descriptionID = Column(Integer, primary_key=True)
    job_description = Column(Text)
    list_of_skills = Column(ARRAY(String))

class JobCondition(Base):
    __tablename__ = 'job_conditions'
    conditionID = Column(Integer, primary_key=True, autoincrement=True)
    promoted_status = Column(String)
    easy_apply_status = Column(String)
    is_reposted = Column(Boolean)
    time_posted = Column(String)
    scrapping_date = Column(Date)

class JobListing(Base):
    __tablename__ = 'job_listings'
    JobID = Column(BigInteger, primary_key=True)
    jobIDLinkedin = Column(BigInteger)
    companyID = Column(Integer, ForeignKey('companies.companyID'))
    locationID = Column(Integer, ForeignKey('locations.locationID'))
    hirerID = Column(Integer, ForeignKey('hirers.hirerID'))
    jobTypeID = Column(Integer, ForeignKey('job_types.jobTypeID'))
    sectorID = Column(Integer, ForeignKey('sectors.sectorID'))
    expertiseID = Column(Integer, ForeignKey('expertise.expertiseID'))
    descriptionID = Column(Integer, ForeignKey('job_descriptions.descriptionID'))
    applicants = Column(Integer)
    years_experience = Column(Integer)

engine = create_engine('postgresql://admin:admin@localhost:5432/linkedin')
Base.metadata.create_all(engine)

Base = declarative_base()

class jobDescription(Base):
    __tablename__ = "jobdescrition"
    id = Column(Integer , primary_key = True)
    descritpin = Column(Text)
    list_of_skills = Column(ARRAY(String))


