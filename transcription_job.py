import boto3
import time
import pandas as pd
import os


class TranscriptionJob:
    def __init__(self, filename):
        self.filename = filename

    def upload_audio_s3(self, bucket_name):
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        s3.upload_file(self.filename, bucket_name, self.filename)

    def transcribe_job(self, job_name, job_uri, media_format):
        transcribe = boto3.client('transcribe')
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat= media_format,
            LanguageCode='en-US'
        )
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(10)
        print(status)
        new_link = pd.read_json(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        return new_link
