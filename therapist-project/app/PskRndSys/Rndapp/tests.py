from urllib import response
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from requests import request
from .views import anasayfa

# Create your tests here.

class HomePageTest(TestCase):
  def test_root_url_resolves_to_homepage_view(self):
    found = resolve("/")
    self.assertEqual(found.func, anasayfa)
  
