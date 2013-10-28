from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test.client import Client

TEST_DATA = {
    "user": {
        "username": "testlo",
        "email": "captaintest@example.org",
        "password": "testeration"
    },
    "tasklist": {
        "name": "General",
        "description": "A generic task list for your dull existence."
    },
    "task": {
        "name": "Create a todo list manager",
        "description": "Procrastinate by writing a todo list manager.",
        "priority": 0,
        "progress": 0
    }
}
class SimpleTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                TEST_DATA['user']['username'],
                TEST_DATA['user']['email'],
                TEST_DATA['user']['password'])

    def test_first_listing(self):
        self.client.login(
                username=TEST_DATA['user']['username'],
                password=TEST_DATA['user']['password']
        )
        url = reverse("task:list_tasks")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/list.html')
        self.assertContains(response, "Hello, "+TEST_DATA['user']['username'])
        self.assertContains(response, "0 task lists")

    def test_add_tasklist(self):
        self.client.login(
                username=TEST_DATA['user']['username'],
                password=TEST_DATA['user']['password']
        )
        url = reverse("task:add_tasklist")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        response = self.client.post(url, TEST_DATA['tasklist'], follow=True)
        self.assertContains(response, "1 task lists")
        self.assertContains(response, TEST_DATA['tasklist']['name'])
        self.assertContains(response, TEST_DATA['tasklist']['description'])

    def test_add_task(self):
        self.test_add_tasklist()
        self.client.login(
                username=TEST_DATA['user']['username'],
                password=TEST_DATA['user']['password']
        )
        url = reverse("task:add_task", kwargs={"tasklist_id":1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task']['name'])
        self.assertContains(response, TEST_DATA['task']['description'])
