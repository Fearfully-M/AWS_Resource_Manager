import boto3
import os
import json
from datetime import datetime as dt


def main():
    # generate_report() # generate the a JSON report to the project directory
    ...


# list the names of all the buckets
def list_all_buckets():
    """
    Prints to the screen the name of all buckets
    for the s3 client
    """
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    buckets = []
    for bucket in response["Buckets"]:
        buckets.append(bucket["Name"])

    return buckets


# calculate total size of everything in the bucket
def get_bucket_size(bucket_name):
    """
    Returns the total size of a bucket when given the name of the bucket
    """
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)

    size = 0
    if "Contents" in response:
        for content in response["Contents"]:
            size += content["Size"]

    return size


# uploads and adds the file to the bucket
def upload_file(bucket_name, file_path):
    """
    Uploads a file from defined file path destination and puts it in
    an s3 bucket
    """
    s3 = boto3.client("s3")

    # obtain only base filename instead of entire filepath name
    key_name = os.path.basename(file_path)

    # open file into memory, close
    with open(file_path) as f:
        contents = f.read()

    # upload the file to s3 bucket
    s3.put_object(Bucket=bucket_name, Key=key_name, Body=contents)


def describe_instances():
    """
    Returns a list of dicts, one per EC2 instance, each containing
    InstanceId, InstanceType, and State.
    """

    ec2 = boto3.client("ec2")

    instances = []  # list of all instances
    metaData = {}  # list the above metadata within an instance

    # get the metadata of InstanceId, InstanceType, and state of instance
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            metaData = {
                "InstanceId": instance["InstanceId"],
                "InstanceType": instance["InstanceType"],
                "State": instance["State"]["Name"],
            }
            instances.append(metaData)

    # return the list of instance dicts
    return instances


def generate_report():
    """
    Gets all bucket names, all current instances and the
    InstanceId, InstanceType, and State of all current instances
    and prints them in a json file
    """

    instance_data = describe_instances()
    bucket_names = list_all_buckets()
    buckets = []
    bucket_meta = {}

    # Put names of buckets and their respective sizes in a list of dicts
    for bucket in bucket_names:
        bucket_meta = {"Name": bucket, "Size": get_bucket_size(bucket)}
        buckets.append(bucket_meta)

    # insert report into a dict
    report = {"Bucket": buckets, "Instance": instance_data}

    # format report as json
    report_json = json.dumps(report, indent=2, default=str)

    # use datetime to save timestamped file
    reportFile = dt.now().strftime(f"ResourceManagerResults_%Y-%m-%d_%H-%M-%S.json")

    # save json to a file
    with open(reportFile, "w") as f:
        f.write(report_json)


if __name__ == "__main__":
    main()
