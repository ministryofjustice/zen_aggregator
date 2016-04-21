from django.test import TestCase
from selenium import webdriver


class TitleTest(TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def test_title_contents(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('test_view', self.browser.title)







