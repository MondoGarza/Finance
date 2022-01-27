import boto3
import shutil
import os
import threading

'''
HAVE TO CONFIGURE AWS CLI FIRST TO USE
SPECIFY:
    1. ACCESS KEY
    2. SECRET KEY
    3. SERVER REGION [ us-west-1]
'''

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print("%s  %s / %s  (%.2f%%)" % (self._filename, self._seen_so_far, self._size, percentage), end="\r", flush=True)
        

zipSkillFileName = 'tradingSkill'
skillLocation = '/Users/amandogarza/Desktop/School/Python VEs/skill/hello_skill_env/lib/python3.8/site-packages'
zippedSkillLocation = '/Users/amandogarza/Desktop/Amazon Skills/' + zipSkillFileName

shutil.make_archive(zippedSkillLocation, 'zip', skillLocation)

s3Resource = boto3.resource('s3')

try:
    s3Resource.meta.client.upload_file(
        '{}.zip'.format(zippedSkillLocation), 
        'alexa-skills-zip-files', 
        '{}.zip'.format(zipSkillFileName), Callback=ProgressPercentage('{}.zip'.format(zippedSkillLocation)))
    print()
    print('S3 URI: s3://alexa-skills-zip-files/{}.zip'.format(zipSkillFileName))
except Exception as exp:
    print('exp: ', exp)
