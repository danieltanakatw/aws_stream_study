from fastapi import FastAPI
from models import ErrorMessage, PatientStats
import json
import boto3
import os
from dotenv import load_dotenv

app = FastAPI()

import boto3

# Get AWS credentials from environment variables
load_dotenv()
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
aws_session_token=os.environ.get("AWS_SESSION_TOKEN")
aws_region = os.environ.get("AWS_REGION")

# Create a boto3 session with the credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region,
    aws_session_token=aws_session_token
)

# Create a Kinesis client
kinesis_client = session.client("kinesis", aws_region)

class Router:
    @app.post("/patient_stats/")
    async def patient_stats(patient_stats: PatientStats):
        data = json.dumps(patient_stats.model_dump(), indent=4, sort_keys=True, default=str)
        records = [{"Data": bytes(data, "utf-8"), "PartitionKey": "partition_key"}]
        message = kinesis_client.put_records(StreamName="patient_stats", Records=records)
        return message

    @app.post("/error_message/")
    async def error_message(error_mesage: ErrorMessage):
        data = json.dumps(error_mesage.model_dump(), indent=4, sort_keys=True, default=str)
        records = [{"Data": bytes(data, "utf-8"), "PartitionKey": "partition_key"}]
        message = kinesis_client.put_records(StreamName="error_message", Records=records)
        return message


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
