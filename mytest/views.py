# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from boto3.session import Session
import json

def index(request):
    bucket_list = []
    down_url = 'string'
    aws_key = 'xxx'
    aws_secret = 'xxx'
    session = Session(aws_access_key_id=aws_key,
                      aws_secret_access_key=aws_secret, region_name='xxx')
    s3 = session.resource('s3')
    client = session.client('s3')
    if request.method == 'POST':
        bucket = request.POST.get('bucket', None)
#        objFile = request.FILES["btn_file"]
        objFile = request.FILES.get('btn_file', None)
        if objFile is None:
            return HttpResponse('没有需要上传的文件！')
        else:
            cre_mul_upload = client.create_multipart_upload(Bucket=bucket, Key=str(objFile))
            upload = client.upload_part(Bucket=bucket, Key=str(objFile), UploadId=cre_mul_upload["UploadId"], PartNumber=1, Body=objFile)
            com_mul_upload = client.complete_multipart_upload(Bucket=bucket, Key=str(objFile), UploadId=cre_mul_upload["UploadId"],
                                                              MultipartUpload={ 'Parts': [{'ETag': upload['ETag'], 'PartNumber': 1},]})
 #       file_obj = s3.Bucket(bucket).put_object(Key=objFile, Body=data)
            down_url = client.generate_presigned_url(
                'get_object', Params={'Bucket': bucket, 'Key': str(objFile)}, ExpiresIn=360000
            )
    for bucket in s3.buckets.all():
        bucket_list.append(bucket.name)
    return render(request, "index.html", {"name": bucket_list, "url": json.dumps(down_url)})