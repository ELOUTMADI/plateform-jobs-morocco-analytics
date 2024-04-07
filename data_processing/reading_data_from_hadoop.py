import json
from pyspark.sql import SparkSession


def read_json_from_hadoop_with_spark(hdfs_path):
    """
    Reads a JSON file from Hadoop HDFS using Spark, parses its content, and shows it as a DataFrame.

    Parameters:
    - spark: A SparkSession instance.
    - hdfs_path: The HDFS path to the JSON file.

    Returns:
    - The parsed JSON content as a dictionary.
    """
    # Initialize Spark configuration and context
    spark = SparkSession.builder.appName("Read JSON from Hadoop").getOrCreate()

    try:
        # Read the JSON file content as RDD
        json_rdd = spark.sparkContext.textFile(hdfs_path)

        # Perform the first parsing of the JSON content
        first_parsing = json.loads(json_rdd.first())
        # Perform the second parsing on the result of the first parsing
        second_parsing = json.loads(first_parsing)

        # Convert the result of the second parsing back into an RDD
        json_rdd = spark.sparkContext.parallelize(json.loads(second_parsing))

        # Create a DataFrame from the RDD by flattening the JSON structure into key-value pairs
        #parsed_rdd = json_rdd.flatMap(lambda job: [(key, (value)) for key, value in job.items()])

        df = spark.createDataFrame(json_rdd)

        return df

    except Exception as e:

        print(f"An error occurred in reading JSon FIle from HDFS using spark: {e}")
        return {}


