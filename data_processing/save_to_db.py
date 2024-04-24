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
            job_description = JobDescription(job_description=record["job_description"])
            session.add(job_description)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Job Description DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of Job Description Records"])


def insert_job_condition(index,iterator):
    session = get_session()
    try:
        for record in iterator :
            job_condition = JobCondition(promoted_status=record["promoted_status"],easy_apply_status=record["easy_apply_status"],
                                         is_reposted=record["is_reposted"] , time_posted=record["time_posted"] ,
                                         scrapping_date=record["scrapping_date"])
            session.add(job_condition)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Job Condition DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of Job Condition Records"])

def insert_job_listing(index,iterator):
    session = get_session()
    try :
        for record in iterator:
            joblisting = JobListing(jobIDLinkedin=record["jobID"],applicants = record["applicants"],years_experience=record["years_experience"])
            session.add(joblisting)
        session.commit()
    except Exception as e :
        session.rollback()
        print(f"Failed to insert to Job Listing DIMENSION")
    finally:
        session.close()
    return iter(["Batch Completed of Job Listing Records"])



