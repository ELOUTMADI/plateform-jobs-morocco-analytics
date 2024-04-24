from hdfs import InsecureClient, HdfsError
import datetime
import json

def save_to_hdfs(client, job_category, data):
    # Format the current date
    date_path = datetime.datetime.now().strftime("%Y/%m/%d")
    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    dir_path = f"/data_lake/raw/jobs/{job_category}/{date_path}"
    file_path = f"{dir_path}/{job_category}_{timestamp}.json"

    # Ensure the directory exists, trying to create it if necessary
    try:
        client.makedirs(dir_path, permission=755)  # Including an example permission
    except HdfsError as e:
        # If an error other than the directory already exists occurs, it will be raised here
        if "FileAlreadyExistsException" not in str(e):
            raise  # Re-raise the exception if it's not about the directory existing

    # Attempt to write data to HDFS
    try:
        with client.write(file_path, encoding='utf-8', overwrite=True) as writer:
            # Ensure the data is in JSON format as a string
            writer.write(json.dumps(data))
        print(f"Data saved to HDFS at {file_path}")
    except HdfsError as e:
        print(f"Failed to write data to HDFS: {e}")


from pyspark.sql import SparkSession
import datetime


def save_processed_dataframe_to_hdfs(df, job_category):
    """
    Saves a Spark DataFrame to HDFS in a directory structured by job category and date.

    Args:
    df (DataFrame): The Spark DataFrame to save.
    job_category (str): The category of the job to help organize the saved files.

    Returns:
    None
    """
    # Initialize a Spark session if not already done
    #spark = SparkSession.builder \
    #   .appName("Save DataFrame to HDFS with Directories") \
     #   .config("spark.hadoop.fs.defaultFS", "hdfs://localhost:9000") \
    #    .getOrCreate()

    # Define the base path using the current date and job category
    date_path = datetime.datetime.now().strftime("%Y/%m/%d")
    dir_path = f"hdfs://localhost:9000/data_lake/processed/jobs/{job_category}/{date_path}"

    # Save the DataFrame to HDFS, creating the directory if it does not exist
    df.write.mode("overwrite").json(dir_path)

    # Log the location where the data was saved
    print(f"DataFrame saved to HDFS at: {dir_path}")
    return dir_path
    # Stop the Spark session if it will no longer be used (optional)
