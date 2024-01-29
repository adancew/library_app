from datetime import date, timedelta
from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.messages import get_messages

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