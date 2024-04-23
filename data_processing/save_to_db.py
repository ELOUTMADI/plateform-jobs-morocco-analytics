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
        print(f"Failed to insert due to: {e}")
    finally:
        session.close()
    return iter(["Batch completed"])



