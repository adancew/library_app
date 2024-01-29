from time import sleep
from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.messages import get_messages
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from shared.models import Account, Reader, Borrowing, Resource


class UserViewsTest(TestCase):
    def setUp(self):
        reader_account = Account.objects.create(username='testuser', password='testpass')
        reader = Reader.objects.create(account=reader_account)
        self.client.force_login(reader_account)
        
        self.resource = Resource.objects.create(title='Test', date_published=date.today())
        self.borrowing = Borrowing.objects.create(
            resource=self.resource, 
            reader=reader, 
            date_borrowed=date.today(),
            date_due=date.today(),
            times_renewed=0,
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('user:user-dash'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        
    def test_index_view_empty(self):
        self.borrowing.delete()
        response = self.client.get(reverse('user:user-dash'))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Borrowing.DoesNotExist):
            Borrowing.objects.get(id=self.borrowing.id)
            
    def test_renew_view(self):
        previous_date = self.borrowing.date_due
        response = self.client.get(reverse('user:renew', args=(self.borrowing.id,)))
        messages = list(get_messages(response.wsgi_request))
        borrowing = Borrowing.objects.get(id=self.borrowing.id)
        
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wypożyczenie zostało przedłużone')
        self.assertNotEqual(borrowing.date_due, previous_date)
        self.assertEqual(borrowing.date_due, date.today()+timedelta(days=7))
        self.assertEqual(borrowing.times_renewed, 1)
        
    def test_renew_view_invalid_id(self):
        response = self.client.get(reverse('user:renew', args=(self.borrowing.id+1,)))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Wystąpił błąd - nie można przedłużyć wypożyczenia')
        
    def test_renew_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('user:renew', args=[None]))
        
    def test_renew_view_limit_exceeded(self):
        self.borrowing.times_renewed = 2
        self.borrowing.save()
        response = self.client.get(reverse('user:renew', args=(self.borrowing.id,)))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nie można przedłużyć wypożyczenia - przekroczono limit 2 przedłużeń')
        
# class UserAutomatedTest(StaticLiveServerTestCase):
#     def setUp(self):
#         reader_account = Account.objects.create(username='testuser2', password='pbkdf2_sha256$720000$GwSeQQbcUOnUJncqvncWBs$thTtjJ0ftMCdwQdSDi8LKyFiDhBOBKvV24CeuJY9tyc=')
#         reader = Reader.objects.create(account=reader_account)
        
#         self.resource = Resource.objects.create(title='Test', date_published=date.today())
#         self.borrowing = Borrowing.objects.create(
#             resource=self.resource, 
#             reader=reader, 
#             date_borrowed=date.today(),
#             date_due=date.today(),
#             times_renewed=0,
#         )
#         self.browser = webdriver.Edge()  # or webdriver.Chrome(), depending on your browser of choice
        
#         self.browser.get(self.live_server_url + '/accounts/login')
#         username_input = self.browser.find_element(By.NAME, 'username')
#         password_input = self.browser.find_element(By.NAME, 'password')

#         username_input.send_keys('testuser2')
#         sleep(0.5)
#         password_input.send_keys('haslo')
#         sleep(0.5)
#         password_input.send_keys(Keys.RETURN)
#         sleep(1)
        
#     def tearDown(self):
#         self.browser.quit()
        
#     def test_renew_view(self):
#         self.browser.get(self.live_server_url + '/user/dashboard')
#         sleep(1)
#         self.browser.find_element(By.ID, 'renew').click()
#         sleep(1)
        
#         messages = self.browser.find_elements(By.CLASS_NAME, 'success')
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(messages[0].text, 'Wypożyczenie zostało przedłużone')
        
#     def test_renew_view_limit_exceeded(self):
#         self.borrowing.times_renewed = 2
#         self.borrowing.save()
#         self.browser.get(self.live_server_url + '/user/dashboard')
#         sleep(1)
#         self.browser.find_element(By.ID, 'renew').click()
#         sleep(1)
        
#         messages = self.browser.find_elements(By.CLASS_NAME, 'failure')
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(messages[0].text, 'Nie można przedłużyć wypożyczenia - przekroczono limit 2 przedłużeń')