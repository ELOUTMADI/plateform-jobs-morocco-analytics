import json
import subprocess

def read_json_from_hadoop(hdfs_path):
    """
    Reads a JSON file from Hadoop HDFS and returns the parsed JSON.

    Parameters:
    - hdfs_path: The HDFS path to the JSON file (e.g., '/user/hadoop/data.json').

    Returns:
    - A Python dictionary or list parsed from the JSON content.
    """
    # Command to read the file from HDFS
    hadoop_command = ["/usr/local/hadoop/bin/hadoop", "fs", "-cat", hdfs_path]

    # Use subprocess to execute the command and capture the output
    try:
        process = subprocess.Popen(hadoop_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        # Check for errors in reading the file
        if process.returncode == 0:
            # Parse JSON content
            json_content = json.loads(output)
            return json.loads(json_content)
        else:
            # Handle errors (e.g., file not found, access denied)
            raise Exception(f"Error reading from HDFS: {error.decode('utf-8')}")

    except Exception as e:
        print(f"Failed to read JSON from HDFS: {e}")
        return None

# Example usage
hdfs_path = 'hdfs://localhost:9000/data_lake/raw/jobs/health_care_research_pharmacy/2024/03/31/health_care_research_pharmacy_20240331T032123.json'
json_data = read_json_from_hadoop(hdfs_path)
if json_data is not None:
    print(json_data)

file_path = '/home/aa/PycharmProjects/Linkedin/script-auto-proc/junk/jobs_data.json'
with open(file_path, 'r') as file:
    data = json.load(file)
    print(data)
