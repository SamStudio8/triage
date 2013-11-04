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
        "tasklist": 1,
        "name": "Create a todo list manager",
        "description": "Procrastinate by writing a todo list manager.",
        "priority": 0,
        "progress": 0
    },
    "task_edit": {
        "tasklist": 1,
        "name": "Become a watermelon farmer",
        "description": "Give up on everything and farm for watermelons.",
        "priority": 0,
        "progress": 0
    },
    "tasklist_edit": {
        "name": "Life Goals",
        "description": "A detailed task list for your adventures.",
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

    def test_login_required(self):
        url = reverse("task:add_tasklist")
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/list/')

        url = reverse("task:add_task", kwargs={"tasklist_id":1})
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/add/1/')

        url = reverse("task:edit_task", kwargs={"task_id":1})
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/edit/1/')

        url = reverse("task:complete_task", kwargs={"task_id":1})
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/complete/1/')

        url = reverse("task:add_tasklist")
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/list/')

        url = reverse("task:edit_tasklist", kwargs={"tasklist_id":1})
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/task/list/1/')

    def test_first_listing(self):
        self.client.login(
                username=TEST_DATA['user']['username'],
                password=TEST_DATA['user']['password']
        )
        url = reverse("home")
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
        url = reverse("task:add_task", kwargs={"tasklist_id":1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task']['name'])
        self.assertContains(response, TEST_DATA['task']['description'])

    def test_edit_task(self):
        self.test_add_task()
        url = reverse("task:edit_task", kwargs={"task_id":1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task_edit'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task_edit']['name'])
        self.assertContains(response, TEST_DATA['task_edit']['description'])

    def test_edit_tasklist(self):
        self.test_add_tasklist()
        url = reverse("task:edit_tasklist", kwargs={"tasklist_id":1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        response = self.client.post(url, TEST_DATA['tasklist_edit'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, TEST_DATA['tasklist_edit']['name'])
        self.assertContains(response, TEST_DATA['tasklist_edit']['description'])

    def test_complete_task(self):
        self.test_add_task()
        url = reverse("task:complete_task", kwargs={"task_id":1})
        response = self.client.get(url)

        response = self.client.post(url, TEST_DATA['tasklist_edit'], follow=True)
        # Redirects to home
        self.assertRedirects(response, '/')
        self.assertTemplateUsed(response, 'task/list.html')

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "0 tasks")
        self.assertContains(response, "(1 completed)")
