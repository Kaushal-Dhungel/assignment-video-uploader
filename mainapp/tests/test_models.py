from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from mainapp.models import *

class TestModel(TestCase):
    
    def setUp(self):
        file = File(open('mainapp/tests/files/videoplayback.mp4', 'rb'))
        tmp_file = SimpleUploadedFile('videoplayback.mp4', file.read(),
            content_type='multipart/form-data')
        self.video = Video.objects.create(video=tmp_file, size=0.79, duration=11, extension='mp4')

    def test_instance_created(self):
        self.assertEqual(self.video.id,1)
