from data_processing.models_session_orm import *
def get_session():
    engine = create_engine('postgresql://admin:admin@localhost:5432/linkedin')
    Session = sessionmaker(bind=engine)
    return Session()



def insert_companies(index, iterator):
    session = get_session()
    try:
        for record in iterator:
            # Assuming you have some logic to map your record to the Company model
            company = Company(company_name=record['company_name'], company_size=record['company_size'])
            session.add(company)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to insert company DIMENSION due to: {e}")
    finally:
        session.close()
    return iter(["Batch completed of Company Records"])

def insert_location(index,iterator):
    session = get_session()
    try:
        for record in iterator:
            location = Location(city=record['city'],remote_status=record['remote_status'])
            session.add(location)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Location DIMENSION due to :{e}")
    finally:
        session.close()
    return iter(["Batch Completed of Location Records"])


def insert_hirers(index,iterator):
    session = get_session()
    try :
        for record in iterator:
            hirer = Hirer(hiring_team_name=record['hiring_team_name'],hirer_job_title=record['hirer_job_title'])
            session.add(hirer)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to Insert to Hirers DIMENSION due to : {e}")
    finally:
        session.close()
    return iter(["Batch Completed of Hirers Records"])

def insert_job_type(index , iterator):
    session = get_session()
    try :
        for record in iterator:
            job_type = JobType(job_type=record["job_type"])
            session.add(job_type)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Job TYpe DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of job type Records"])


def insert_section(index , iterator):
    session = get_session()
    try:
        for record in iterator :
            sector = Sector(sector=record["sector"])
            session.add(sector)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to section DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of Sector Records"])

def insert_expertise(index,iterator):
        session = get_session()
        try:
            for record in iterator:
                expertise = Expertise(expertise=record["expertise"])
                session.add(expertise)
            session.commit()
        except Exception as e :
            session.rollback()
            print(f"Failed to insert to expertise DIMENSION")
        finally:
            session.close()
        return iter(["Batch Completed of expertise Records"])

def insert_job_description(index,iterator):
    session = get_session()
    try:
        for record in iterator:
            job_description = JobDescription(job_description=record["job_description"] , list_of_skills=record["list_of_skills"])
            session.add(job_description)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Job Description DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of Job Description Records"])


def insert_job_condition(index, iterator):
    session = get_session()
    try:
        for record in iterator:
            # Ensure data types and formats match what's expected by the database schema
            promoted_status = str(record["promoted_status"])
            easy_apply_status = str(record["easy_apply_status"])
            is_reposted = bool(record["is_reposted"])  # Convert to boolean if it's not already
            time_posted = str(record["time_posted"])
            scrapping_date = record["scrapping_date"]  # Ensure this is a date object or correctly formatted string

            job_condition = JobCondition(
                promoted_status=promoted_status,
                easy_apply_status=easy_apply_status,
                is_reposted=is_reposted,
                time_posted=time_posted,
                scrapping_date=scrapping_date
            )
            session.add(job_condition)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to insert to Job Condition DIMENSION due to: {e}")  # Print the specific error
    finally:
        session.close()
    return iter(["Batch Completed of Job Condition Records"])


import re

def extract_number(text):
    # This function attempts to extract the first number from a string.
    if text is None:
        return 0
    if 'Over' in text:
        # Handle the 'Over 100' case or similar cases.
        return 100  # Adjust this number as appropriate for your context.
    match = re.search(r'\d+', text)
    return int(match.group()) if match else 0

def insert_job_listing(index, iterator):
    session = get_session()
    try:
        for record in iterator:
            # Convert the 'applicants' field to integer after extracting numbers
            applicants = extract_number(record["applicants"])
            years_experience = int(record["years_experience"]) if record["years_experience"] is not None else 100000

            # Retrieve or verify existence of associated entities
            company = session.query(Company).filter_by(company_name=record["company_name"]).first()
            location = session.query(Location).filter_by(city=record["city"]).first()
            hirer = session.query(Hirer).filter_by(hiring_team_name=record["hiring_team_name"]).first()
            job_type = session.query(JobType).filter_by(job_type=record["job_type"]).first()
            sector = session.query(Sector).filter_by(sector=record["sector"]).first()
            expertise = session.query(Expertise).filter_by(expertise=record["expertise"]).first()
            job_description = session.query(JobDescription).filter_by(job_description=record["job_description"]).first()
            job_condition = session.query(JobCondition).filter_by(time_posted=record["time_posted"]).first()  # Adjust according to your model

            # Create the JobListing instance with foreign key relations
            joblisting = JobListing(
                jobIDLinkedin=record["jobID"],
                applicants=applicants,
                years_experience=years_experience,
                companyID=company.companyID if company else None,
                locationID=location.locationID if location else None,
                hirerID=hirer.hirerID if hirer else None,
                jobTypeID=job_type.jobTypeID if job_type else None,
                sectorID=sector.sectorID if sector else None,
                expertiseID=expertise.expertiseID if expertise else None,
                descriptionID=job_description.descriptionID if job_description else None,
                conditionID=job_condition.conditionID if job_condition else None
            )
            session.add(joblisting)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to insert to Job Listing DIMENSION due to: {e}")
    finally:
        session.close()
    return iter(["Batch Completed of Job Listing Records"])






