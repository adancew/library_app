from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from fees.forms import FeeForm, AddFeeForm

from fees.utils import get_fees, get_fee_details
from shared.models import Fee, Account, Reader, Employee


class FeeFormsTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(username='testuser', password='testpass')
        self.reader = Reader.objects.create(account=self.account)
    
    def test_fee_form_valid(self):
        form = FeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': datetime.today(), 'is_paid': False})
        self.assertTrue(form.is_valid())
        
    def test_fee_form_invalid(self):
        form = FeeForm(data={'reason': 'Test', 'date_issued': datetime.today(), 'is_paid': False})
        self.assertFalse(form.is_valid())
        
    def test_add_fee_form_valid(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': datetime.today(), 'is_paid': False, 'reader': self.account})
        self.assertTrue(form.is_valid())
        
    def test_add_fee_form_invalid_reader(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': datetime.today(), 'is_paid': False, 'reader': None})
        self.assertFalse(form.is_valid())
        
    def test_add_fee_form_invalid(self):
        form = AddFeeForm(data={'amount': 100, 'reason': 'Test', 'date_issued': datetime.today(), 'is_paid': False})
        self.assertFalse(form.is_valid())

class FeeUtilsTest(TestCase):
    def setUp(self):
        account = Account.objects.create(username='testuser', password='testpass')
        reader = Reader.objects.create(account=account)
        self.fee = Fee.objects.create(amount=100, reason='Test', date_issued=datetime.today(), is_paid=False, reader=reader)

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
        
        self.fee = Fee.objects.create(amount=100, reason='Test', date_issued=datetime.today(), is_paid=False, reader=reader)

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
        