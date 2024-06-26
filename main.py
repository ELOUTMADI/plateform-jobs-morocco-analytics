# PySpark related imports

from pyspark.sql.functions import to_date, regexp_extract, trim, udf, lower, regexp_replace, when
from pyspark.sql.types import IntegerType

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
    return df.select([col(c).alias(c.replace(' ', '_')) for c in df.columns])


def fill_missing_values_remote_status(df):
    return df.fillna({"remote_status": "Unknown"})


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


def process_job_stats(df):
    """
    Processes the 'stats' column of a job DataFrame to extract structured information.
    Adds columns for company, location, repost status, time posted without 'Reposted', and applicants.
    Removes the original 'stats' column.

    Parameters:
        df (DataFrame): Input DataFrame containing a column 'stats'.

    Returns:
        DataFrame: Transformed DataFrame with new columns and without the 'stats' column.
    """
    # Define the regular expression patterns
    company_pattern = r"^(.*?) ·"
    location_pattern = r"· (.*?) ·"
    repost_time_pattern = r"Reposted (\d+ \w+ ago) ·"  # Extracts just the time portion after "Reposted"
    time_posted_pattern = r"· (\d+ \w+ ago) ·"
    applicants_pattern = r"· (\d+ applicants|Over 100 applicants)$"

    # Transform the DataFrame
    transformed_df = df.withColumn("company", regexp_extract("stats", company_pattern, 1)) \
        .withColumn("location", regexp_extract("stats", location_pattern, 1)) \
        .withColumn("is_reposted", when(regexp_extract("stats", repost_time_pattern, 1) != "", "Yes").otherwise("No")) \
        .withColumn("time_posted", when(regexp_extract("stats", repost_time_pattern, 1) != "",
                                        regexp_extract("stats", repost_time_pattern, 1)) \
                    .otherwise(regexp_extract("stats", time_posted_pattern, 1))) \
        .withColumn("applicants", regexp_extract("stats", applicants_pattern, 1))

    # Drop the original 'stats' column
    transformed_df = transformed_df.drop("stats")

    return transformed_df


def extract_city(location: str) -> str:
    """
    Extracts the primary city name from a location string.
    The function uses a regex that captures multiple words in the city name,
    continuing until it encounters a comma, dash, or ends the input.

    Args:
    location (str): The full location string from which to extract the city.

    Returns:
    str: The extracted city name or None if not applicable.
    """
    if location is None:
        return None

    # Convert to lower case to standardize the input
    location = location.lower()

    # Define special handling for certain phrases
    if 'metropolitan area' in location and 'casablanca' in location:
        return 'Casablanca'

    # Define a regular expression pattern to extract the city name
    # This pattern aims to capture city names more precisely before common descriptors.
    pattern = re.compile(r"([\w\s]+?)(?:,|-| metropolitan area|$)")
    # Attempt to match the pattern
    match = pattern.match(location)
    if match:
        # Return the matched group, stripped of trailing spaces and capitalized
        city = match.group(1).strip()
        return ' '.join([word.capitalize() for word in city.split()])

    # Default to None if no match is found
    return None


def process_location_column(df):
    """
    Processes the location column of a DataFrame to extract city names,
    using a generalized pattern to handle a variety of location formats.

    Args:
    df (DataFrame): DataFrame with a column named 'location' containing location strings.

    Returns:
    DataFrame: A new DataFrame with an added column 'city' containing the extracted city names.
    """
    # Register the UDF
    extract_city_udf = udf(extract_city, StringType())

    # Apply the UDF to the location column
    df_with_city = df.withColumn("city", extract_city_udf(df["location"]))
    df_with_city = df_with_city.drop("location")

    return df_with_city


def extract_skills(skill_string):
    """
    Cleans the skills data in the 'Required_Skills' column by converting the string
    representation of a list into an actual list and removing unnecessary conjunctions.

    Args:
    skill_string (str): A string that represents a list of skills, including some conjunctions like 'and'.

    Returns:
    list: A clean list of skills without the conjunction 'and'.
    """
    try:
        # Convert the string to a list using json.loads after replacing single quotes
        skills = json.loads(skill_string.replace("'", '"'))
        # Remove 'and' which is not required and strip any surrounding whitespace
        clean_skills = [skill.replace("and", "").strip() for skill in skills if skill.lower() != 'and']
        return clean_skills
    except json.JSONDecodeError:
        return []


def process_skills_column(df):
    """
    Processes the 'Required_Skills' column of a DataFrame to extract and clean the skills data.

    Args:
    df (DataFrame): DataFrame with a column named 'Required_Skills' containing strings of list data.

    Returns:
    DataFrame: A new DataFrame with an updated 'Required_Skills' column containing cleaned lists of skills.
    """
    # Register the UDF
    extract_skills_udf = udf(extract_skills, ArrayType(StringType()))

    # Apply the UDF to the 'Required_Skills' column
    df_with_clean_skills = df.withColumn("list_of_skills", extract_skills_udf(col("Required_Skills")))
    df_with_clean_skills = df_with_clean_skills.drop("Required_Skills")

    return df_with_clean_skills


def process_initial_data(hdfs_path):
    df = read_json_from_hadoop_with_spark(hdfs_path)

    # Process JSON data through various stages
    details = parse_json_and_process_details(df, "details")
    hirer = parse_json_and_process_hirer_infos(details, "hirer_infos")
    job_insight = parse_json_and_process_job_insights(hirer, "job_insights")
    skills = parse_json_and_process_skills(job_insight, "skills")
    df = parse_json_and_process_description(skills, "specific_description")
    df = fill_missing_values_hiring(df)
    df = standardize_column_names(df)
    df = clean_string_columns(df)
    return df


def enhance_data_with_experience_and_titles(df):
    """Enhances data with experience and cleaned job titles."""
    df = add_experience_column(df)
    df = clean_job_titles(df)
    return df


def perform_advanced_data_processing(df):
    """Performs advanced data processing like extracting job stats and locations."""
    df = process_job_stats(df)
    df = process_location_column(df)
    df = process_skills_column(df)
    df = df.drop("Other")

    return df


from pyspark.sql.functions import col

def filter_and_prepare_data_for_db(df):
    """
    Optimized version of data filtering and preparation for database insertion.
    Applies transformations in a chained manner to minimize computational overhead.
    """
    filters = {
        "companies": (df.company_size.isNotNull(), ["company_name", "company_size"]),
        "job_type": (col("job_type") != "", ["job_type"]),
        "sectors": (col("sector") != "", ["sector"]),
        "hirers": (col("hiring_team_name") != "", ["hiring_team_name", "hirer_job_title"]),
        "location": ((col("remote_status") != "") & (col("city") != ""), ["city", "remote_status"]),
        "job_condition": (
            (col("promoted_status").isNotNull()) & (col("easy_apply_status").isNotNull()) &
            (col("is_reposted").isNotNull()) & (col("time_posted").isNotNull()) &
            (col("scrapping_date").isNotNull()), ["promoted_status", "easy_apply_status", "is_reposted", "time_posted", "scrapping_date"]
        ),
        "expertise": (col("expertise") != "", ["expertise"]),
        "job_description": (None, ["job_description", "list_of_skills"]),
        "job_listing": (None, df.columns)
    }

    result = {}
    for key, (condition, columns) in filters.items():
        if condition is not None:
            # Chain filter, dropDuplicates, and select operations together
            temp_df = df.filter(condition).dropDuplicates(columns).select(columns)
        else:
            # For cases with no condition, directly drop duplicates and select
            temp_df = df.dropDuplicates(columns).select(columns)

        result[key] = temp_df

    return result


def insert_data_into_db(filtered_data):
    results = {}
    for key, df in filtered_data.items():
        rdd = df.rdd
        func = globals().get(f"insert_{key}")
        results[key] = rdd.mapPartitionsWithIndex(func).collect() if func else None
    return results


#########################     SAVING TO DB     ######################################################
from data_processing.save_to_db import *

if __name__ == "__main__":
    job_category = "health_care_research_pharmacy"
    hdfs_path = f'hdfs://localhost:9000/data_lake/raw/jobs/{job_category}/2024/04/08/health_care_research_pharmacy_20240408T050556.json'
    df = process_initial_data(hdfs_path)
    df = enhance_data_with_experience_and_titles(df)
    df = perform_advanced_data_processing(df)

    filtered_data = filter_and_prepare_data_for_db(df)
    results = insert_data_into_db(filtered_data)
