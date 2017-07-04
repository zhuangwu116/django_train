# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from djangtestdemo.models import Author
# Create your tests here.
class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(name="庄武",email="562669088@qq.com")
        Author.objects.create(name="小明", email="444561981@qq.com")
    def test_author(self):
        author=Author.objects.get(name="庄武")
        self.assertEqual(author.email,'562669088@qq.com')
