from reading_data_from_hadoop import *
from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType , ArrayType

def parse_json_and_process_details(df: DataFrame, json_column_name: str, cache: bool = False, checkpoint: bool = False) -> DataFrame:
    """
    Parses a JSON column and optionally caches and/or checkpoints the DataFrame.

    :param df: Input DataFrame.
    :param json_column_name: Name of the column containing JSON strings.
    :param cache: Whether to cache the DataFrame after parsing. Default is False.
    :param checkpoint: Whether to checkpoint the DataFrame after parsing. Default is False.
    :return: Transformed DataFrame.
    """
    # Define the schema based on your JSON structure
    details_schema = StructType([
        StructField("job_title", StringType(), True),
        StructField("company_name", StringType(), True),
        StructField("location", StringType(), True),
        StructField("promoted_status", StringType(), True),
        StructField("easy_apply_status", StringType(), True),
    ])

    # Parse the JSON and expand its fields into separate columns
    df = df.withColumn("parsed_details", from_json(col(json_column_name), details_schema)) \
           .select("*", "parsed_details.*") \
           .drop("parsed_details", json_column_name)

    if cache:
        df.cache()
        # If caching, remember to perform actions (e.g., show, count) here or in subsequent code
        # and to unpersist later if necessary

    if checkpoint:
        # Check if the SparkContext has a checkpoint directory set. If not, set one.
        if df.sql_ctx.sparkSession.sparkContext.getCheckpointDir() is None:
            # Set your checkpoint directory. This should be a path in HDFS or a similar fault-tolerant storage system.
            df.sql_ctx.sparkSession.sparkContext.setCheckpointDir("/path/to/checkpoint/dir")
        df = df.checkpoint()

    return df

# Example usage:
# df = spark.read... # Load your DataFrame
# df_transformed = parse_json_and_process(df, "details", cache=True)
# Perform actions on df_transformed, e.g., df_transformed.show()
# Remember to unpersist if you cached the DataFrame
# df_transformed.unpersist()

def parse_json_and_process_hirer_infos(df: DataFrame, json_column_name: str, cache: bool = False, checkpoint: bool = False) -> DataFrame:

    hirer_infos_schema = StructType([
        StructField("hiring_team_name", StringType(), True),
        StructField("hirer_job_title", StringType(), True)
    ])

    df = df.withColumn("parsed_hirer_infos", from_json(col(json_column_name), hirer_infos_schema)) \
        .select("*", "parsed_hirer_infos.*") \
        .drop("parsed_hirer_infos", json_column_name)

    if cache:
        df.cache()

    if checkpoint:
        if df.sql_ctx.sparkSession.sparkContext.getCheckpointDir() is None:
            df.sql_ctx.sparkSession.sparkContext.setCheckpointDir("/path/to/checkpoint/dir")
        df = df.checkpoint()

    return df

def parse_json_and_process_job_insights(df: DataFrame, json_column_name: str, cache: bool = False, checkpoint: bool = False) -> DataFrame:

    job_insights_schema = StructType([
        StructField("remote_status", StringType(), True),
        StructField("job_type", StringType(), True),
        StructField("company_size", StringType(), True),
        StructField("sector", StringType(), True),
        StructField("skills", StringType(), True),
        StructField("Other", StringType(), True),

    ])

    df = df.withColumn("parsed_job_insights", from_json(col(json_column_name), job_insights_schema)) \
        .select("*",*[col(f"parsed_job_insights.{field.name}").alias(field.name) if field.name != "skills" else col("parsed_job_insights.skills").alias("expertise") for field in job_insights_schema.fields]) \
        .drop("parsed_job_insights", json_column_name)

    if cache:
        df.cache()

    if checkpoint:
        if df.sql_ctx.sparkSession.sparkContext.getCheckpointDir() is None:
            df.sql_ctx.sparkSession.sparkContext.setCheckpointDir("/path/to/checkpoint/dir")
        df = df.checkpoint()

    return df


def parse_json_and_process_skills(df: DataFrame, json_column_name: str, cache: bool = False, checkpoint: bool = False) -> DataFrame:

    skills_schema = StructType([
        StructField("skills", StringType(), True)
    ])

    df = df.withColumn("parsed_skills", from_json(col(json_column_name), skills_schema)) \
        .select("*",col("parsed_skills").getField("skills").alias("Required Skills")) \
        .drop("parsed_skills", json_column_name)

    if cache:
        df.cache()

    if checkpoint:
        if df.sql_ctx.sparkSession.sparkContext.getCheckpointDir() is None:
            df.sql_ctx.sparkSession.sparkContext.setCheckpointDir("/path/to/checkpoint/dir")
        df = df.checkpoint()

    return df


def parse_json_and_process_description(df: DataFrame, json_column_name: str, cache: bool = False, checkpoint: bool = False) -> DataFrame:

    description_schema = StructType([
        StructField("job_description", StringType(), True)
    ])

    df = df.withColumn("parsed_specific_description", from_json(col(json_column_name), description_schema)) \
        .select("*","parsed_specific_description.job_description") \
        .drop("parsed_specific_description", json_column_name)

    if cache:
        df.cache()

    if checkpoint:
        if df.sql_ctx.sparkSession.sparkContext.getCheckpointDir() is None:
            df.sql_ctx.sparkSession.sparkContext.setCheckpointDir("/path/to/checkpoint/dir")
        df = df.checkpoint()

    return df


if __name__ == "__main__":
    hdfs_path = 'hdfs://localhost:9000/data_lake/raw/jobs/health_care_research_pharmacy/2024/03/31/health_care_research_pharmacy_20240331T032123.json'
    df = read_json_from_hadoop_with_spark(hdfs_path)
    details = parse_json_and_process_details(df,"details")
    hirer = parse_json_and_process_hirer_infos(details,"hirer_infos")
    job_insight = parse_json_and_process_job_insights(hirer,"job_insights")
    skills = parse_json_and_process_skills(job_insight,"skills")
    description = parse_json_and_process_description(skills,"specific_description")
    description.show(truncate=False)

