from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.conf import settings
from mainapp.models import *

class TestVideoUploadView(APITestCase):
    url = reverse('uploadView')

    def test_post(self):
        file_path = settings.BASE_DIR/'mainapp/tests/files/videoplayback.mp4'
        tmp_file = SimpleUploadedFile('videoplayback.mp4', content=open(file_path, 'rb').read(), content_type='multipart/form-data')
        data = {'video':tmp_file}
        res = self.client.post(self.url,data,format = "multipart")
        self.assertEquals(res.status_code,201)

    #TODO 
    # 1. test with different unsupported formats, videos with length < 10 minutes and size < 1GB

class CommonTestClass(APITestCase):
    def setUp(self):
        file = File(open('mainapp/tests/files/videoplayback.mp4', 'rb'))
        tmp_file = SimpleUploadedFile('video', file.read(),
            content_type='multipart/form-data')
        self.video = Video.objects.create(video=tmp_file, size=0.79, duration=11, extension='mp4')

class TestVideoListView(CommonTestClass):
    url = reverse('listView')

    def test_video_list(self):
        res = self.client.get(self.url)
        self.assertEquals(len(res.data), 1) # we have created only one instance of Video in the setUp above
        self.assertEquals(res.status_code,200)

    #TODO 
    # 1. test with different query parameters like category, date range and size range


class TestVideoChargesView(CommonTestClass):
    url = reverse('chargesView')

    # all the query parameters are mandatory to get video's charge
    def test_video_charges_without_parameters(self):
        res = self.client.get(self.url)
        self.assertEquals(res.status_code,400)

    # testing the charge provided all the parameters
    def test_video_charges_with_parameters(self):
        res = self.client.get(f"{self.url}?size=200&length=06:00&extension=mp4")
        self.assertEquals(res.data['charges'],17.5)   # the charge for a mp4 video of length 6 minutes and size 200 MB is 17.5 $
        self.assertEquals(res.status_code,200)
