from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from mainapp.views import  *

class TestMainappUrls(SimpleTestCase):

    def test_list_view(self):
        url = resolve(reverse("listView"))
        self.assertEquals(url.func.view_class,VideoListView) 

    def test_upload_details(self):
        url = resolve(reverse("uploadView"))
        self.assertEquals(url.func.view_class,VideoUploadView) 

    def test_charges_view(self):
        url = resolve(reverse("chargesView"))
        self.assertEquals(url.func.view_class,VideoChargesView) 

