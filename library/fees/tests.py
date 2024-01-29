from time import sleep
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.messages import get_messages
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from fees.forms import FeeForm, AddFeeForm
from fees.utils import get_fees, get_fee_details
from shared.models import Fee, Account, Reader, Employee



class FeeFormsTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username='testuser', password='testpass')
        self.reader = Reader.objects.create(account=self.account)
    
    def test_fee_form_valid(self):
        form = FeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': date.today(), 'is_paid': False})
        self.assertTrue(form.is_valid())
        
    def test_fee_form_invalid(self):
        form = FeeForm(data={'reason': 'Test', 'date_issued': date.today(), 'is_paid': False})
        self.assertFalse(form.is_valid())
        
    def test_add_fee_form_valid(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': date.today(), 'is_paid': False, 'reader': self.account})
        self.assertTrue(form.is_valid())
        
    def test_add_fee_form_invalid_reader(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': date.today(), 'is_paid': False, 'reader': None})
        self.assertFalse(form.is_valid())
        
    def test_add_fee_form_invalid(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': date.today(), 'is_paid': False})
        self.assertFalse(form.is_valid())

class FeeUtilsTest(TestCase):
    def setUp(self):
        account = Account.objects.create(username='testuser', password='testpass')
        reader = Reader.objects.create(account=account)
        self.fee = Fee.objects.create(amount=100, reason='Test', date_issued=date.today(), is_paid=False, reader=reader)

    def test_get_fees(self):
        fees = get_fees()
        self.assertEqual(len(fees), 1)
        self.assertEqual(fees[0]['amount'], 100)
        self.assertEqual(fees[0]['reason'], 'Test')

    def test_get_fee_details(self):
        fee_details = get_fee_details(self.fee.id)
        self.assertEqual(fee_details['amount'], 100)
        self.assertEqual(fee_details['reason'], 'Test')

class FeeViewsTest(TestCase):
    def setUp(self):
        employee_account = Account.objects.create(username='testuser', password='testpass')
        employee = Employee.objects.create(account=employee_account)
        self.client.force_login(employee_account)
        
        reader_account = Account.objects.create(username='testuser2', password='testpass')
        reader = Reader.objects.create(account=reader_account)
        
        self.fee = Fee.objects.create(amount=100, reason='Test', date_issued=date.today(), is_paid=False, reader=reader)

    def test_index_view(self):
        response = self.client.get(reverse('fees:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        
    def test_index_view_empty(self):
        self.fee.delete()
        response = self.client.get(reverse('fees:index'))
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Fee.DoesNotExist):
            Fee.objects.get(id=self.fee.id)

    def test_details_view(self):
        response = self.client.get(reverse('fees:details', args=[self.fee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        
    def test_details_view_invalid_id(self):
        with self.assertRaises(Fee.DoesNotExist):
            self.client.get(reverse('fees:details', args=[self.fee.id + 1]))
            
    def test_details_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fees:details', args=[None]))
    
    def test_register_payment_view(self):
        response = self.client.get(reverse('fees:register-payment', args=[self.fee.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Uiszczenie opłaty zostało zarejestrowane')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Fee.objects.get(id=self.fee.id).is_paid, True)
    
    def test_register_payment_view_invalid_id(self):
        response = self.client.get(reverse('fees:register-payment', args=[self.fee.id + 1]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nie można zarejestrować uiszczenia opłaty')
        
    def test_register_payment_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fees:register-payment', args=[None]))
        
    def test_add_view(self):
        response = self.client.get(reverse('fees:add'))
        self.assertEqual(response.status_code, 200)

    def test_edit_view(self):
        response = self.client.get(reverse('fees:edit', args=[self.fee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        
    def test_edit_view_invalid_id(self):
        with self.assertRaises(Fee.DoesNotExist):
            self.client.get(reverse('fees:edit', args=[self.fee.id + 1]))
    
    def test_edit_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fees:edit', args=[None]))
            
    def test_delete_view(self):
        response = self.client.get(reverse('fees:delete', args=[self.fee.id]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Opłata została anulowana')
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Fee.DoesNotExist):
            Fee.objects.get(id=self.fee.id)
            
    def test_delete_view_invalid_id(self):
        response = self.client.get(reverse('fees:delete', args=[self.fee.id + 1]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Nie można anulować opłaty')
        
    def test_delete_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('fees:delete', args=[None]))
            
# class FeeAutomatedTest(StaticLiveServerTestCase):
#     def setUp(self):
#         employee_account = Account.objects.create(username='testuser', password='pbkdf2_sha256$720000$GwSeQQbcUOnUJncqvncWBs$thTtjJ0ftMCdwQdSDi8LKyFiDhBOBKvV24CeuJY9tyc=')
#         employee = Employee.objects.create(account=employee_account)
        
#         reader_account = Account.objects.create(username='testuser2', password='pbkdf2_sha256$720000$GwSeQQbcUOnUJncqvncWBs$thTtjJ0ftMCdwQdSDi8LKyFiDhBOBKvV24CeuJY9tyc=')
#         reader = Reader.objects.create(account=reader_account)
        
#         self.fee = Fee.objects.create(amount=100.00, reason='Test', date_issued=date.today(), is_paid=False, reader=reader)
#         self.browser = webdriver.Edge()  # or webdriver.Chrome(), depending on your browser of choice
        
#         self.browser.get(self.live_server_url + '/accounts/login')
#         username_input = self.browser.find_element(By.NAME, 'username')
#         password_input = self.browser.find_element(By.NAME, 'password')

#         username_input.send_keys('testuser')
#         sleep(0.5)
#         password_input.send_keys('haslo')
#         sleep(0.5)
#         password_input.send_keys(Keys.RETURN)
#         sleep(1)

#     def tearDown(self):
#         self.browser.quit()
        
#     def test_index_view(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
        
        
#         amount = self.browser.find_element(By.ID, 'amount')
#         reason = self.browser.find_element(By.ID, 'reason')
#         self.assertEqual(amount.text, '100.00')
#         self.assertEqual(reason.text, 'Test')
        
#     def test_index_view_empty(self):
#         self.fee.delete()
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
        
#         with self.assertRaises(NoSuchElementException):
#             amount = self.browser.find_element(By.ID, 'amount')

#     def test_details_view(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.find_element(By.ID, 'details').click()
#         sleep(1)

#         keys = self.browser.find_elements(By.CLASS_NAME, 'key')
#         values = self.browser.find_elements(By.CLASS_NAME, 'values')
        
#         for key, value in zip(keys, values):
#             if key.text == 'id':
#                 self.assertEqual(value.text, str(self.fee.id))
#             elif key.text == 'amount':
#                 self.assertEqual(value.text, str(self.fee.amount))
#             elif key.text == 'reason':
#                 self.assertEqual(value.text, self.fee.reason)
#             elif key.text == 'date_issued':
#                 self.assertEqual(value.text, self.fee.date_issued.strftime('%Y-%m-%d'))
#             elif key.text == 'is_paid':
#                 self.assertEqual(value.text, 'nie')
                
#     def test_details_view_invalid_id(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.get(f'{str(self.live_server_url)}/fees/{str(self.fee.id + 1)}/details')
#         sleep(1)
        
#         error = self.browser.find_element(By.TAG_NAME, 'h1')
#         self.assertEqual(error.text, 'Server Error (500)')
        
#     def test_details_view_none_id(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.get(f'{str(self.live_server_url)}/fees/{None}/details')
#         sleep(1)
        
#         error = self.browser.find_element(By.TAG_NAME, 'h1')
#         self.assertEqual(error.text, 'Not Found')

#     def test_register_payment_view(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.find_element(By.ID, 'register-payment').click()
#         sleep(1)
        
#         messages = self.browser.find_elements(By.CLASS_NAME, 'success')
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(messages[0].text, 'Uiszczenie opłaty zostało zarejestrowane')
        
#         self.assertEqual(Fee.objects.get(id=self.fee.id).is_paid, True)
        
#     def test_register_payment_view_invalid_id(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.get(f'{str(self.live_server_url)}/fees/{self.fee.id + 1}/register-payment')
#         sleep(1)
        
#         messages = self.browser.find_elements(By.CLASS_NAME, 'failure')
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(messages[0].text, 'Nie można zarejestrować uiszczenia opłaty')
        
#     def test_register_payment_view_none_id(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.get(f'{str(self.live_server_url)}/fees/{None}/register-payment')
#         sleep(1)
        
#         error = self.browser.find_element(By.TAG_NAME, 'h1')
#         self.assertEqual(error.text, 'Not Found')
        
#     def test_delete_view(self):
#         self.browser.get(f'{str(self.live_server_url)}/fees/')
#         sleep(1)
#         self.browser.find_element(By.ID, 'delete').click()
#         sleep(1)

#         messages = self.browser.find_elements(By.CLASS_NAME, 'success')
#         self.assertEqual(len(messages), 1)
#         self.assertEqual(messages[0].text, 'Opłata została anulowana')     