import pandas as pd
from virtualclass.models import Video
import requests
import re
from django.core.files.base import ContentFile


def read_all():
    df = pd.read_excel('eye.xlsx')
    for tup in df.iterrows():
        row = tup[1]
        number = row['شماره']
        title = row['نام فایل']
        drive_link = row['لینک']
        download_url = get_download_link(drive_link)
        response = requests.get(download_url)
        f = ContentFile(response.content)
        vid = Video.objects.create(number=number, title=title)
        vid.video_file.save(vid.title, f)
        vid.save()


def get_download_link(drive_link):
    pattern = r'^https?://drive.google.com/file/d/([^/]+)'
    match = re.match(pattern, drive_link, re.M | re.I)
    if match:
        file_id = match.group(1)
        download_url = 'https://docs.google.com/uc?id={}&export=download'.format(file_id)
        return download_url


def test():
    link = 'https://drive.google.com/file/d/130tzD9ILCHlJ521vs8uBPx-6-zdhhixc/view?usp=sharing'
    pattern = r'^https?://drive.google.com/file/d/([^/]+)'
    match = re.match(pattern, link, re.M | re.I)
    if match:
        file_id = match.group(1)
        download_url = 'https://docs.google.com/uc?id={}&export=download'.format(file_id)
        response = requests.get(download_url)
        f = ContentFile(response.content)
        vid = Video.objects.create(number=1122, title='test3')
        vid.video_file.save(vid.title, f)
        vid.save()


read_all()
