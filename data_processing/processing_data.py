from data_processing.defining_schema import *
from data_processing.reading_data_from_hadoop import *
from pyspark.sql.functions import col, to_date, explode, regexp_extract
import spacy









if __name__ == "__main__":
    hdfs_path = 'hdfs://localhost:9000/data_lake/raw/jobs/health_care_research_pharmacy/2024/04/08/health_care_research_pharmacy_20240408T050556.json'
    df = read_json_from_hadoop_with_spark(hdfs_path)
    details = parse_json_and_process_details(df,"details")
    hirer = parse_json_and_process_hirer_infos(details,"hirer_infos")
    job_insight = parse_json_and_process_job_insights(hirer,"job_insights")
    skills = parse_json_and_process_skills(job_insight,"skills")
    df = parse_json_and_process_description(skills,"specific_description")
    # Extract years of experience from job_description
    experience_regex = r"(?i)\b(\d+)[+]* ans"
    df = df.withColumn("Experience_Required", regexp_extract(col("job_description"), experience_regex, 1))
    df.select("Experience_Required").show()