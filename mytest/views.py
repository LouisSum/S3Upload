# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from boto3.session import Session
import json

def index(request):
    bucket_list = []
    down_url = 'string'
    aws_key = 'AKIAJ77C6WP4LQMH3P2A'
    aws_secret = '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'
    session = Session(aws_access_key_id=aws_key,
                      aws_secret_access_key=aws_secret, region_name='us-east-2')
    s3 = session.resource('s3')
    client = session.client('s3')
    if request.method == "POST":
        bucket = request.POST.get("bucket", None)
        objFile = str(request.FILES["btn_file"])
        data = open(objFile, 'rb')
        cre_mul_upload = client.create_multipart_upload(Bucket=bucket, Key=objFile)
        upload = client.upload_part(Bucket=bucket, Key=objFile, UploadId=cre_mul_upload["UploadId"], PartNumber=1, Body=data)
        com_mul_upload = client.complete_multipart_upload(Bucket=bucket, Key=objFile, UploadId=cre_mul_upload["UploadId"],
                                                          MultipartUpload={ 'Parts': [{'ETag': upload['ETag'], 'PartNumber': 1},]})
 #       file_obj = s3.Bucket(bucket).put_object(Key=objFile, Body=data)
        down_url = client.generate_presigned_url(
            'get_object', Params={'Bucket': bucket, 'Key': objFile}, ExpiresIn=360000
        )
    for bucket in s3.buckets.all():
        bucket_list.append(bucket.name)
    return render(request, "index.html", {"name": bucket_list, "url": json.dumps(down_url)})