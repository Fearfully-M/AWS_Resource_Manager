import boto3
import os

def main(): 
    ...

    

# list the names of all the buckets
def list_all_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        print(bucket['Name'])

 
# calculate total size of everything in the bucket
def get_bucket_size(bucket_name):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket = bucket_name)
    
    size = 0
    if 'Contents' in response:
        for content in response['Contents']:
            size += content['Size']

    return size


# uploads and adds the file to the bucket
def upload_file(bucket_name, file_path):
    s3 = boto3.client('s3')

    # obtain only base filename instead of entire filepath name
    key_name = os.path.basename(file_path)

    with open(file_path) as f:
        contents = f.read()

    s3.put_object(
        Bucket = bucket_name,
        Key = key_name,
        Body = contents
    )



def describe_instances():
    pass


if __name__ == "__main__":
    main()