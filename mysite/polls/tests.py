from django.test import TestCase
from django.utils import timezone
from polls.models import Poll, Choice

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

    def test_verbose_name_for_pub_date(self):
        for field in Poll._meta.fields:
	    if field.name == 'pub_date':
	        self.assertEquals('Date published', field.verbose_name)

    def test_poll_objects_are_named_after_their_question(self):
        p = Poll()
	p.question = "How is babby formed?"
	self.assertEquals("How is babby formed?", unicode(p))
	
    def test_poll_can_tell_you_its_total_number_of_votes(self):
        p = Poll(question='where', pub_date=timezone.now())
	p.save()

	c1 = Choice(poll=p, choice='here', votes=0)
	c1.save()
	c2 = Choice(poll=p, choice='there', votes=0)
	c2.save()

	self.assertEquals(0, p.total_votes())

class ChoiceModelTest(TestCase):
    def test_creating_some_choices_for_a_poll(self):
        poll = Poll()
	poll.question = "What's up?"
	poll.pub_date = timezone.now()
	poll.save()

	choice = Choice()
	choice.poll = poll
	choice.choice = "doin' fine..."
	choice.votes = 3
	choice.save()

	poll_choices = poll.choice_set.all()
	self.assertEquals(1, poll_choices.count())

	choice_from_db = poll_choices[0]
	self.assertEquals(choice, choice_from_db)
	self.assertEquals("doin' fine...", choice_from_db.choice)
	self.assertEquals(3, choice_from_db.votes)

    def test_choice_defaults(self):
        choice = Choice()
	self.assertEquals(0, choice.votes)

    def test_choice_can_calculate_its_own_percentage_of_votes(self):
        poll = Poll(question='who?', pub_date=timezone.now())
	poll.save()
	choice1 = Choice(poll=poll, choice='me', votes=2)
	choice1.save()
	choice2 = Choice(poll=poll, choice='you', votes=1)
	choice2.save()

	self.assertEquals(100 * 2 / 3.0, choice1.percentage())
	self.assertEquals(100 * 1 / 3.0, choice2.percentage())

	choice1.votes = 0
	choice1.save()
	choice2.votes = 0
	choice2.save()
	self.assertEquals(0, choice1.percentage())
	self.assertEquals(0, choice2.percentage())
