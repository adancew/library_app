from shared.models import Reader, Borrowing, Resource, Journal
MAX_RENTALS_PER_READER = 5

# for now only checks if limit of borrowings per reader has not been exceeded
def has_general_right_to_borrow(reader:Reader):
    current_rentals_count = Borrowing.objects.filter(
        status="UNDERWAY", reader_id=reader.id).count()
    return current_rentals_count < MAX_RENTALS_PER_READER


# for now it only checks if resource is not a journal, just to see if it works
def has_right_to_borrow_resource(reader:Reader, resource:Resource):
    is_not_journal = not Journal.objects.filter(resource_id=resource.id).exists()
    is_available = Resource.objects.filter(id=resource.id, status="AVAILABLE").exists()

    return (is_not_journal and is_available)
    