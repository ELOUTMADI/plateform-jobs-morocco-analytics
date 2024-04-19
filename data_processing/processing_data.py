from data_processing.defining_schema import *
from data_processing.reading_data_from_hadoop import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, explode, regexp_extract, trim , udf , lower , regexp_replace
from pyspark.sql.types import StringType
import re
from pyspark.sql.types import IntegerType


def fill_missing_values(df):
    """
    Fill missing values for specific columns.
    """
    return df.fillna({"hiring_team_name": "Unknown", "hirer_job_title": "Unknown"})

def standardize_column_names(df):
    """
    Replace spaces in column names with underscores.
    """
    return df.select([col(c).alias(c.replace(' ','_')) for c in df.columns])

def convert_dates(df, column_name, format_string):
    """
    Convert date columns to a specified format.
    """
    return df.withColumn(column_name, to_date(col(column_name), format_string))

def clean_string_columns(df):
    """
    Trim spaces and correct capitalization in string columns.
    """
    string_fields = [field.name for field in df.schema.fields if isinstance(field.dataType, StringType)]
    return df.select([trim(col(c)).alias(c) for c in string_fields])

def extract_experience_udf():
    """ Define a UDF to extract years of experience based on a regex pattern """
    return udf(lambda text: int(re.search(r'(\d+)\s+(years|ans)', text, re.IGNORECASE).group(1)) if re.search(r'(\d+)\s+(years|ans)', text, re.IGNORECASE) else None, IntegerType())

def add_experience_column(df, source_col='job_description', new_col='years_experience'):
    """ Add a new column to DataFrame that extracts years of experience from job descriptions """
    extract_experience = extract_experience_udf()
    return df.withColumn(new_col, extract_experience(col(source_col)))

if __name__ == "__main__":
    hdfs_path = 'hdfs://localhost:9000/data_lake/raw/jobs/health_care_research_pharmacy/2024/04/08/health_care_research_pharmacy_20240408T050556.json'
    df = read_json_from_hadoop_with_spark(hdfs_path)
    details = parse_json_and_process_details(df,"details")
    hirer = parse_json_and_process_hirer_infos(details,"hirer_infos")
    job_insight = parse_json_and_process_job_insights(hirer,"job_insights")
    skills = parse_json_and_process_skills(job_insight,"skills")
    df = parse_json_and_process_description(skills,"specific_description")
    df.show()