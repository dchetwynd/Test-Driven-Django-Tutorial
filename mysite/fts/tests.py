from collections import namedtuple
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

PollInfo = namedtuple('PollInfo', ['question', 'choices'])

POLL1 = PollInfo(
    question = "How awesome is Test-Driven Development?",
    choices = [
        'Very awesome',
	'Quite awesome',
	'Moderately awesome',
    ],
)

class AdminSiteTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_create_new_poll_via_admin_site(self):
        self.browser.get(self.live_server_url + '/admin/')

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
        
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        body = WebDriverWait(self.browser, 10).until(lambda browser: browser.find_element_by_tag_name('body'))

        self.assertIn('Site administration', body.text)

        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)

	polls_links[1].click()

	body = self.browser.find_element_by_tag_name('body')
	self.assertIn('0 polls', body.text)
	
	new_poll_link = self.browser.find_element_by_link_text('Add poll')
	new_poll_link.click()

	body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
	self.assertIn('Date published:', body.text)
	
	question_field = self.browser.find_element_by_name('question')
	question_field.send_keys("How awesome is Test-Driven Development?")

	date_field = self.browser.find_element_by_name('pub_date_0')
	date_field.send_keys('01/01/12')
	time_field = self.browser.find_element_by_name('pub_date_1')
	time_field.send_keys('00:00')

	choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
	choice_1.send_keys('Very awesome')
	choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
	choice_2.send_keys('Quite awesome')
	choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
	choice_3.send_keys('Moderately awesome')

        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
	save_button.click()

	new_poll_links = self.browser.find_elements_by_link_text(
	    "How awesome is Test-Driven Development?"
	)
	self.assertEquals(len(new_poll_links), 1)

    def _setup_polls_via_admin(self):
        self.browser.get(self.live_server_url + '/admin')
	username_field = self.browser.find_element_by_name('username')
	username_field.send_keys('admin')
	password_field = self.browser.find_element_by_name('password')
	password_field.send_keys('admin')
	password_field.send_keys(Keys.RETURN)

	for poll_info in [POLL1]:
	    self.browser.find_elements_by_link_text('Polls')[1].click()
	    self.browser.find_element_by_link_text('Add poll').click()

	    question_field = self.browser.find_element_by_name('question')
	    question_field.send_keys(poll_info.question)
	    self.browser.find_element_by_link_text('Today').click()
	    self.browser.find_element_by_link_text('Now').click()

	    for i, choice_text in enumerate(poll_info.choices):
	        choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
		choice_field.send_keys(choice_text)

            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
	    save_button.click()

	    new_poll_links = self.browser.find_elements_by_link_text(
	        poll_info.question
	    )
	    self.assertEquals(len(new_poll_links), 1)

	    self.browser.get(self.live_server_url + '/admin/')
	
	self.browser.find_element_by_link_text('Log out').click()
