from django.test import TestCase
from django.utils import timezone
from polls.models import Poll

class PollModelTest(TestCase):
    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()

        poll.save()

        all_polls_in_database = Poll.objects.all()
        self.assertEquals(1, len(all_polls_in_database))
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(poll, only_poll_in_database)

        self.assertEquals("What's up?", only_poll_in_database.question)
        self.assertEquals(poll.pub_date, only_poll_in_database.pub_date)
