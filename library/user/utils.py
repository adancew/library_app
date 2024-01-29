from datetime import timedelta
from shared.models import Reader, Borrowing


def get_user_borrowings(user):
    reader = Reader.objects.get(account_id=user.id)
    borrowings = Borrowing.objects.filter(reader=reader)
    return borrowings

def renew_borrowing(borrowing_id):
    borrowing = Borrowing.objects.get(id=borrowing_id)
    if borrowing.times_renewed >= 2:
        raise Exception
    borrowing.times_renewed += 1
    borrowing.date_due = borrowing.date_due + timedelta(days=7)
    borrowing.save()
        