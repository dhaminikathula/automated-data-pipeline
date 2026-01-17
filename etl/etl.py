import os
import boto3
import pandas as pd
from io import StringIO

BUCKET = os.environ["S3_BUCKET_NAME"]
ENDPOINT = os.environ["AWS_ENDPOINT_URL"]

s3 = boto3.client(
    "s3",
    endpoint_url=ENDPOINT,
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name="us-east-1"
)

# Read CSV from raw/
obj = s3.get_object(Bucket=BUCKET, Key="raw/input.csv")
df = pd.read_csv(obj["Body"])

# Transform: keep trips with distance > 1 mile
df = df[df["trip_distance"] > 1]

# Add computed column
df["fare_per_mile"] = df["fare_amount"] / df["trip_distance"]


# Write to processed/
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=BUCKET,
    Key="processed/output.csv",
    Body=csv_buffer.getvalue()
)

print("ETL completed successfully")
