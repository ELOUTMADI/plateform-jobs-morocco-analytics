from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY , BigInteger , Boolean , Text
from sqlalchemy.orm import declarative_base , relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Define your models as previously done
class Company(Base):
    __tablename__ = 'companies'
    companyID = Column(Integer, primary_key=True)
    company_name = Column(String)
    company_size = Column(String)
    job_listings = relationship("JobListing", back_populates="company")

class Location(Base):
    __tablename__ = 'locations'
    locationID = Column(Integer, primary_key=True)
    city = Column(String)
    remote_status = Column(String)
    job_listings = relationship("JobListing", back_populates="location")

class Hirer(Base):
    __tablename__ = 'hirers'
    hirerID = Column(Integer, primary_key=True)
    hiring_team_name = Column(String)
    hirer_job_title = Column(String)
    job_listings = relationship("JobListing", back_populates="hirer")

class JobType(Base):
    __tablename__ = 'job_types'
    jobTypeID = Column(Integer, primary_key=True)
    job_type = Column(String)
    job_listings = relationship("JobListing", back_populates="job_type")

class Sector(Base):
    __tablename__ = 'sectors'
    sectorID = Column(Integer, primary_key=True)
    sector = Column(String)
    job_listings = relationship("JobListing", back_populates="sector")

class Expertise(Base):
    __tablename__ = 'expertise'
    expertiseID = Column(Integer, primary_key=True)
    expertise = Column(String)
    job_listings = relationship("JobListing", back_populates="expertise")

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    descriptionID = Column(Integer, primary_key=True)
    job_description = Column(Text)
    list_of_skills = Column(ARRAY(String))
    job_listings = relationship("JobListing", back_populates="job_description")

class JobCondition(Base):
    __tablename__ = 'job_conditions'
    conditionID = Column(Integer, primary_key=True, autoincrement=True)
    promoted_status = Column(String)
    easy_apply_status = Column(String)
    is_reposted = Column(Boolean)
    time_posted = Column(String)
    scrapping_date = Column(Date)
    job_listings = relationship("JobListing", back_populates="job_condition")

class JobListing(Base):
    __tablename__ = 'job_listings'
    JobID = Column(BigInteger, primary_key=True)
    companyID = Column(Integer, ForeignKey('companies.companyID'))
    locationID = Column(Integer, ForeignKey('locations.locationID'))
    hirerID = Column(Integer, ForeignKey('hirers.hirerID'))
    jobTypeID = Column(Integer, ForeignKey('job_types.jobTypeID'))
    sectorID = Column(Integer, ForeignKey('sectors.sectorID'))
    expertiseID = Column(Integer, ForeignKey('expertise.expertiseID'))
    descriptionID = Column(Integer, ForeignKey('job_descriptions.descriptionID'))
    conditionID = Column(Integer, ForeignKey('job_conditions.conditionID'))
    jobIDLinkedin = Column(BigInteger)
    applicants = Column(Integer)
    years_experience = Column(Integer)

    # Back-populates for easy access from both directions
    company = relationship("Company", back_populates="job_listings")
    location = relationship("Location", back_populates="job_listings")
    hirer = relationship("Hirer", back_populates="job_listings")
    job_type = relationship("JobType", back_populates="job_listings")
    sector = relationship("Sector", back_populates="job_listings")
    expertise = relationship("Expertise", back_populates="job_listings")
    job_description = relationship("JobDescription", back_populates="job_listings")
    job_condition = relationship("JobCondition", back_populates="job_listings")

engine = create_engine('postgresql://admin:admin@localhost:5432/linkedin')
Base.metadata.create_all(engine)




