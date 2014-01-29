from markdown import markdown

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test.client import Client

TEST_DATA = {
    "user": {
        "username": "testlo",
        "email": "captaintest@example.org",
        "password": "testeration"
    },
    "user2": {
        "username": "darkhat",
        "email": "shady@example.org",
        "password": "secretspls"
    },
    "tasklist": {
        "name": "General",
        "description": "A generic task list for your dull existence.",
        "order": 0
    },
    "tasklist_2": {
        "name": "Specific",
        "description": "A task list for your life's particulars.",
        "order": 0
    },
    "task": {
        "tasklist": 1,
        "name": "Create a todo list manager",
        "description": "Procrastinate by writing a todo list manager.",
    },
    "task_edit": {
        "tasklist": 1,
        "name": "Become a watermelon farmer",
        "description": "Give up on everything and farm for watermelons.",
    },
    "task_evil_assign": {
        "tasklist": 1,
        "name": "Become a supervillain",
        "description": "Defend metrocity.",
    },
    "task_edit_triage": {
        "triage": 1,
        "tasklist": 1,
        "name": "Become a watermelon farmer",
        "description": "Give up on everything and farm for watermelons.",
    },
    "tasklist_edit": {
        "name": "Life Goals",
        "description": "A detailed task list for your adventures.",
        "order": 0
    },
    "triage_category_low": {
        "name": "Expectant",
        "priority": -1,
        "fg_colour": "FF0000",
        "bg_colour": "000",
    },
    "triage_category_low_edit": {
        "name": "Minor",
        "priority": 3,
        "fg_colour": "FFF",
        "bg_colour": "006600",
    },
    "triage_category_high": {
        "name": "Immediate",
        "priority": 10,
        "fg_colour": "000",
        "bg_colour": "FF0000",
    },
    "task_edit_for_history": {
        "tasklist": 2,
        "name": "Write witty diary entry",
        "description": "Maintain a record of exciting happenings.",
        "progress": 10
    },
    "task_edit_for_markdown": {
        "tasklist": 1,
        "name": "Write a marked down diary entry",
        "description": "This is [an example](http://triage.ironowl.io/ 'Title') inline link.",
        "progress": 50
    },
}
class SimpleTaskTest(TestCase):
    def setUp(self):
        User.objects.create_user(
                TEST_DATA['user']['username'],
                TEST_DATA['user']['email'],
                TEST_DATA['user']['password'])
        User.objects.create_user(
                TEST_DATA['user2']['username'],
                TEST_DATA['user2']['email'],
                TEST_DATA['user2']['password'])

    def test_login_required(self):
        url = reverse("task:view_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=/')

        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:complete_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:add_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:edit_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:list_triage_category", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:add_triage_category", kwargs={
            "username": TEST_DATA['user']['username']
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

        url = reverse("task:edit_triage_category", kwargs={
            "username": TEST_DATA['user']['username'],
            "triage_category_id": 1
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next='+url)

    def test_view_permissions(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )
        url = reverse("home")
        response = self.client.get(url)
        self.assertContains(response, "Hello, "+TEST_DATA['user2']['username'])
        self.assertContains(response, "0 task lists")

    def test_edit_list_permission(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )
        url = reverse("task:edit_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_edit_task_permission(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )
        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_evil_assign_to_other_list(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )
        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user2']['username'],
        })
        response = self.client.post(url, TEST_DATA['task_evil_assign'], follow=True)
        self.assertContains(response, "Select a valid choice. That choice is not one of the available choices")

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
        url = reverse("task:add_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        response = self.client.post(url, TEST_DATA['tasklist'], follow=True)
        self.assertContains(response, "1 task lists")
        self.assertContains(response, TEST_DATA['tasklist']['name'])
        self.assertContains(response, TEST_DATA['tasklist']['description'])

    def test_add_task(self):
        self.test_add_tasklist()
        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task']['name'])

    def test_view_task(self):
        self.test_add_task()
        url = reverse("task:view_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/view.html')

        self.assertContains(response, TEST_DATA['task']['name'])
        self.assertContains(response, TEST_DATA['task']['description'])

    def test_edit_task(self):
        self.test_add_task()
        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task_edit'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task_edit']['name'])

    def test_task_markdown(self):
        self.test_add_task()

        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.post(url, TEST_DATA['task_edit_for_markdown'], follow=True)

        url = reverse("task:view_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)

        self.assertContains(response, markdown(TEST_DATA['task_edit_for_markdown']['description']))

    def test_task_history(self):
        self.test_add_task()

        url = reverse("task:add_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.post(url, TEST_DATA['tasklist_2'], follow=True)

        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.post(url, TEST_DATA['task_edit_for_history'], follow=True)

        url = reverse("task:view_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)

        self.assertContains(response, TEST_DATA['task']['name'])
        self.assertContains(response, TEST_DATA['task']['description'])
        self.assertContains(response, TEST_DATA['task_edit_for_history']['name'])
        self.assertContains(response, TEST_DATA['task_edit_for_history']['description'])
        self.assertContains(response, TEST_DATA['tasklist']['name'])
        self.assertContains(response, TEST_DATA['tasklist_2']['name'])

    def test_edit_tasklist(self):
        self.test_add_tasklist()
        url = reverse("task:edit_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        response = self.client.post(url, TEST_DATA['tasklist_edit'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, TEST_DATA['tasklist_edit']['name'])
        self.assertContains(response, TEST_DATA['tasklist_edit']['description'])

    def test_complete_task(self):
        self.test_add_task()
        url = reverse("task:complete_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1
        })

        response = self.client.post(url, TEST_DATA['tasklist_edit'], follow=True)
        # Redirects to home
        self.assertRedirects(response, '/')
        self.assertTemplateUsed(response, 'task/list.html')

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "0 tasks")
        self.assertContains(response, "(1 completed)")

    def test_add_triage_category(self):
        self.client.login(
                username=TEST_DATA['user']['username'],
                password=TEST_DATA['user']['password']
        )
        url = reverse("task:add_triage_category", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetriage.html')
        response = self.client.post(url, TEST_DATA['triage_category_low'], follow=True)

        self.assertEqual(len(response.context['triages']), 1)
        self.assertContains(response, TEST_DATA['triage_category_low']['name'])
        self.assertContains(response, "style=\"background-color:#"+TEST_DATA['triage_category_low']['bg_colour']+"; color:#"+TEST_DATA['triage_category_low']['fg_colour'])

    def test_edit_triage_category(self):
        self.test_add_triage_category()
        url = reverse("task:edit_triage_category", kwargs={
            "username": TEST_DATA['user']['username'],
            "triage_category_id": 1
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetriage.html')
        response = self.client.post(url, TEST_DATA['triage_category_low_edit'], follow=True)

        self.assertEqual(len(response.context['triages']), 1)
        self.assertContains(response, TEST_DATA['triage_category_low_edit']['name'])
        self.assertContains(response, "style=\"background-color:#"+TEST_DATA['triage_category_low_edit']['bg_colour']+"; color:#"+TEST_DATA['triage_category_low_edit']['fg_colour'])

#    def test_triage_category_priority(self):
#        self.test_add_triage_category()
#        url = reverse("task:add_triage_category")
#        response = self.client.post(url, TEST_DATA['triage_category_high'], follow=True)

#        self.assertEqual(len(response.context['triages']), 2)

    def test_triage_task(self):
        self.test_add_triage_category()
        self.test_add_task()
        url = reverse("task:edit_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.post(url, TEST_DATA['task_edit_triage'], follow=True)

        self.assertContains(response, TEST_DATA['triage_category_low']['name'])
        self.assertContains(response, "style=\"background-color:#"+TEST_DATA['triage_category_low']['bg_colour']+"; color:#"+TEST_DATA['triage_category_low']['fg_colour'])
