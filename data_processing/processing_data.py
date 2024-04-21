# Standard library imports
import re

# PySpark related imports
from data_ingestion.data_lake import *
from pyspark.sql.functions import col, to_date, explode, regexp_extract, trim, udf, lower, regexp_replace
from pyspark.sql.types import StringType, IntegerType

# Importing custom modules
from data_processing.defining_schema import *
from data_processing.reading_data_from_hadoop import *

# Function Definitions

def fill_missing_values_hiring(df):
    """
    Fill missing values for specific columns.
    """
    return df.fillna({"hiring_team_name": "Unknown", "hirer_job_title": "Unknown"})


def standardize_column_names(df):
    """
    Replace spaces in column names with underscores.
    """
    return df.select([col(c).alias(c.replace(' ','_')) for c in df.columns])

def fill_missing_values_remote_status(df):
    return df.fillna({"remote_status": "Unknown"})

def convert_dates(df, column_name, format_string):
    """
    Convert date columns to a specified format.
    """
    return df.withColumn(column_name,to_date(col(column_name),format_string))
def clean_string_columns(df):
    """
    Trim spaces and correct capitalization in string columns.
    """
    string_fields = [field.name for field in df.schema.fields if isinstance(field.dataType, StringType)]
    return df.select([trim(col(c)).alias(c) for c in string_fields])


def extract_experience_udf():
    """
    Define a UDF to extract years of experience based on a regex pattern.
    """
    return udf(lambda text: int(re.search(r'(\d+)\s+(years|ans)', text, re.IGNORECASE).group(1)) if re.search(
        r'(\d+)\s+(years|ans)', text, re.IGNORECASE) else None, IntegerType())


def add_experience_column(df, source_col='job_description', new_col='years_experience'):
    """
    Add a new column to DataFrame that extracts years of experience from job descriptions.
    """
    extract_experience = extract_experience_udf()
    return df.withColumn(new_col, extract_experience(col(source_col)))

def clean_job_titles(df):
    """
    Cleans the 'hirer_job_title' column in the provided DataFrame.
    """
    # Convert to lowercase
    df = df.withColumn("hirer_job_title", lower(col("hirer_job_title")))

    # Remove special characters and emojis
    df = df.withColumn("hirer_job_title", regexp_replace(col("hirer_job_title"), "[^a-zA-Z0-9\\s]", ""))

    # Trim spaces
    df = df.withColumn("hirer_job_title", trim(col("hirer_job_title")))

    return df

# Main Execution Block
if __name__ == "__main__":
    job_category = "health_care_research_pharmacy"
    hdfs_path = f'hdfs://localhost:9000/data_lake/raw/jobs/{job_category}/2024/04/08/health_care_research_pharmacy_20240408T050556.json'
    df = read_json_from_hadoop_with_spark(hdfs_path)

    # Process JSON data through various stages
    details = parse_json_and_process_details(df, "details")
    hirer = parse_json_and_process_hirer_infos(details, "hirer_infos")
    job_insight = parse_json_and_process_job_insights(hirer, "job_insights")
    skills = parse_json_and_process_skills(job_insight, "skills")
    df = parse_json_and_process_description(skills, "specific_description")

    # Clean and transform the DataFrame
    df = fill_missing_values_hiring(df)
    df = standardize_column_names(df)
    df = clean_string_columns(df)
    df = add_experience_column(df)
    df = clean_job_titles(df)
    # Display the DataFrame
    path = save_processed_dataframe_to_hdfs(df, job_category)
    dg = read_processed_data_from_hadoop_with_spark(path)
    dg.show()
