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

