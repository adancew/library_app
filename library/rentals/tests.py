from time import sleep
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.messages import get_messages

from fees.utils import get_fees, get_fee_details
from rentals.forms import ScanCodeForm
from shared.models import Fee, Account, Reader, Employee, Card


class RentalFormTest(TestCase):
    def setUp(self):
        employee_account = Account.objects.create(username='testuser', password='testpass')
        employee = Employee.objects.create(account=employee_account)
        self.client.force_login(employee_account)
        
        reader_account = Account.objects.create(username='testuser2', password='testpass')
        reader = Reader.objects.create(account=reader_account)
        
        self.card = Card.objects.create(type="ADULT", reader=reader)
        
    def test_scan_card_form(self):
        form = ScanCodeForm(data={'Code': self.card.id})
        self.assertTrue(form.is_valid())
        
    def test_enter_card_form(self):
        form = ScanCodeForm(data={'Code': self.card.id})
        self.assertTrue(form.is_valid())

class RentalViewsTest(TestCase):
    def setUp(self):
        employee_account = Account.objects.create(username='testuser', password='testpass')
        employee = Employee.objects.create(account=employee_account)
        self.client.force_login(employee_account)
        
        reader_account = Account.objects.create(username='testuser2', password='testpass')
        reader = Reader.objects.create(account=reader_account)
        
        self.card = Card.objects.create(type="ADULT", reader=reader)
        
    def test_scan_card_view(self):
        response = self.client.get(reverse('rentals:scan-card'), data={'Code': self.card.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/scan_card.html')
        
    def test_scan_card_view_invalid_id(self):
        response = self.client.post(reverse('rentals:scan-card'), data={'Code': 100})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/scan_card.html')
        self.assertContains(response, "Wystąpił błąd")
        
    def test_scan_card_view_none_id(self):
        with self.assertRaises(TypeError):
            self.client.post(reverse('rentals:scan-card'), data={'Code': None})
            
    def test_enter_card_view(self):
        response = self.client.get(reverse('rentals:enter-card'), data={'Code': self.card.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/enter_card.html')
        
    def test_enter_card_view_invalid_id(self):
        response = self.client.post(reverse('rentals:enter-card'), data={'Code': 100})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/enter_card.html')
        self.assertContains(response, "Wystąpił błąd")
        
    def test_enter_card_view_none_id(self):
        with self.assertRaises(TypeError):
            self.client.post(reverse('rentals:enter-card'), data={'Code': None})
            
    def test_reader_menu_view(self):
        response = self.client.get(reverse('rentals:reader-menu', args=[self.card.reader.account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rentals/borrow_reader_menu.html')
        
    def test_reader_menu_view_invalid_id(self):
        with self.assertRaises(Account.DoesNotExist):
            response = self.client.get(reverse('rentals:reader-menu', args=[100]))
            
    def test_reader_menu_view_none_id(self):
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse('rentals:reader-menu', args=[None]))