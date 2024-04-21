from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, ARRAY
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from data_processing.models_session_orm import *
from datetime import date

Session = sessionmaker(bind=engine)
session = Session()

# Ensure the necessary location exists
location = session.query(Location).filter_by(location_id=1).first()
if not location:
    location = Location(city="CityName", region="RegionName", country="CountryName")
    session.add(location)
    session.commit()

# Ensure the necessary company exists
company = session.query(Company).filter_by(company_id=1).first()
if not company:
    company = Company(name="Example Company", industry="Software", size="100-500")
    session.add(company)
    session.commit()

# Ensure the necessary job type exists
job_type = session.query(JobType).filter_by(job_type_id=1).first()
if not job_type:
    job_type = JobType(type_description="Full-time")
    session.add(job_type)
    session.commit()

# Now add a new job posting
new_job = JobPosting(
    company_id=company.company_id,
    location_id=location.location_id,
    job_type_id=job_type.job_type_id,
    posted_date=date.today(),
    description="Software Developer needed",
    years_experience=5,
    skills=['Python', 'Django', 'JavaScript']
)
session.add(new_job)
session.commit()

session.close()