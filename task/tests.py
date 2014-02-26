import datetime
from markdown import markdown

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.test.client import Client
from django.utils.timezone import utc

import task.models as TaskModels
import task.utils as TaskUtils

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
    "register": {
        "username": "hootle",
        "first_name": "Hoot",
        "last_name": "McHootleson",
        "email": "hootle@ironowl.io",
        "password1": "secrets",
        "password2": "secrets"
    },
    "register2": {
        "username": "hoota",
        "first_name": "Hoota",
        "last_name": "O'Wise",
        "email": "hoota@ironowl.io",
        "password1": "wisewords",
        "password2": "wisewords"
    },
    "tasklist": {
        "name": "General",
        "description": "A generic task list for your dull existence.",
        "order": 0
    },
    "tasklist_2": {
        "name": "Specific",
        "description": "A task list for your life based particulars.",
        "order": 0
    },
    "public_tasklist": {
        "name": "Global List",
        "description": "A globally visible task list to share your dull existence.",
        "order": 0,
        "public": True
    },
    "another_tasklist": {
        "name": "Another List",
        "description": "A task list that is not yours.",
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
    "tasklist_delete": {
        "tasklist_transfer": 2,
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
    },
    "task_edit_for_markdown": {
        "tasklist": 1,
        "name": "Write a marked down diary entry",
        "description": "This is [an example](http://triage.ironowl.io/ 'Title') inline link.",
    },
    "milestone": {
        "name": "Major Milestone",
        "fg_colour": "FF0000",
        "bg_colour": "000",
    },
    "milestone_edit": {
        "name": "Minor Milestone",
        "fg_colour": "000",
        "bg_colour": "FF0000",
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
        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
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

    def test_add_tasklist(self, user=TEST_DATA['user'], tasklist=TEST_DATA['tasklist'], number=1):
        self.client.login(
                username=user['username'],
                password=user['password']
        )
        url = reverse("task:add_tasklist", kwargs={
            "username": user['username'],
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        response = self.client.post(url, tasklist, follow=True)
        self.assertContains(response, str(number) + " task lists")
        self.assertContains(response, tasklist['name'])
        self.assertContains(response, tasklist['description'])

    def test_add_non_unique_tasklist(self):
        self.test_add_tasklist()
        url = reverse("task:add_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)
        response = self.client.post(url, TEST_DATA['tasklist'], follow=True)
        self.assertContains(response, "You already have a tasklist with this name")

    def test_add_public_tasklist(self):
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
        response = self.client.post(url, TEST_DATA['public_tasklist'], follow=True)
        self.assertContains(response, TEST_DATA['public_tasklist']['name'])
        self.assertContains(response, TEST_DATA['public_tasklist']['description'])

    def test_view_public_tasklist(self):
        self.test_add_public_tasklist()

        url = reverse("task:view_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['public_tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/tasklist.html')
        self.assertContains(response, TEST_DATA['public_tasklist']['name'])
        self.assertContains(response, TEST_DATA['public_tasklist']['description'])

    def test_view_tasklist(self):
        self.test_add_task()

        url = reverse("task:view_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name'])
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/tasklist.html')
        self.assertContains(response, TEST_DATA['tasklist']['name'])
        self.assertContains(response, TEST_DATA['tasklist']['description'])

    def test_evil_view_tasklist(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:view_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name'])
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_evil_edit_public_tasklist(self):
        self.test_add_public_tasklist()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:edit_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['public_tasklist']['name']),
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_evil_delete_public_tasklist(self):
        self.test_add_public_tasklist()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:delete_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['public_tasklist']['name']),
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

    def test_globalview_public_tasklist(self):
        self.test_add_public_tasklist()

        self.client.logout()
        url = reverse("task:view_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['public_tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/tasklist.html')
        tasklist_expected = TEST_DATA['user']['username'] + "</a> / " + TEST_DATA['public_tasklist']['name']
        self.assertContains(response, tasklist_expected)

    def test_add_task(self):
        self.test_add_tasklist()
        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        response = self.client.post(url, TEST_DATA['task'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertContains(response, "1 tasks")
        self.assertContains(response, TEST_DATA['task']['name'])

    def test_add_task_prefill_list(self):
        self.test_add_tasklist()
        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
        }) + "?tasklist=" + slugify(TEST_DATA['tasklist']['name'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changetask.html')
        self.assertContains(response, "selected=\"selected\">"+TEST_DATA['tasklist']['name']+"</option>")

    def test_evil_add_task_prefill_list(self):
        self.test_add_tasklist()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:new_task", kwargs={
            "username": TEST_DATA['user']['username'],
        }) + "?tasklist=" + slugify(TEST_DATA['tasklist']['name'])
        response = self.client.get(url)
        self.assertRedirects(response, '/')

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

    def test_evil_view_task(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:view_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

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

    def test_edit_tasklist_redirect(self):
        self.test_add_tasklist()
        view_url = reverse("task:view_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name'])
        })
        url = reverse("task:edit_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        }) + "?next=" + view_url

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changelist.html')
        self.assertContains(response, "<input type=\"hidden\" name=\"next\" value=\"" + view_url + "\"")

        TEST_DATA_PLUS_HIDDEN = TEST_DATA['tasklist_edit']
        TEST_DATA_PLUS_HIDDEN["next"] = view_url
        response = self.client.post(url, TEST_DATA_PLUS_HIDDEN, follow=True)
        new_url = reverse("task:view_tasklist", kwargs={"username": TEST_DATA['user']['username'],
                                                    "listslug": slugify(TEST_DATA['tasklist_edit']['name'])})
        self.assertRedirects(response, new_url)

    def test_delete_tasklist(self):
        self.test_add_task()
        self.test_add_public_tasklist()

        url = reverse("task:delete_tasklist", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/deletelist.html')
        response = self.client.post(url, TEST_DATA['tasklist_delete'], follow=True)

        self.assertContains(response, "1 task lists")
        self.assertNotContains(response, TEST_DATA['tasklist']['name'])
        self.assertNotContains(response, TEST_DATA['tasklist']['description'])
        self.assertContains(response, TEST_DATA['public_tasklist']['name'])
        self.assertContains(response, TEST_DATA['public_tasklist']['description'])

        # Check task was transferred
        task = TaskModels.Task.objects.filter(pk=1)
        self.assertEquals(task.count(), 1)
        self.assertEquals(task[0].tasklist.slug, slugify(TEST_DATA['public_tasklist']['name']))

    def test_view_profile(self):
        self.test_add_tasklist()
        self.test_add_public_tasklist()
        self.client.logout()

        url = reverse("task:profile", kwargs={
            "username": TEST_DATA['user']['username'],
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/profile.html')

        self.assertContains(response, TEST_DATA['user']['username'])
        self.assertContains(response, TEST_DATA['public_tasklist']['name'])
        self.assertNotContains(response, TEST_DATA['tasklist']['name'])

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

    def test_evil_complete_task(self):
        self.test_add_task()
        self.client.logout()
        self.client.login(
                username=TEST_DATA['user2']['username'],
                password=TEST_DATA['user2']['password']
        )

        url = reverse("task:complete_task", kwargs={
            "username": TEST_DATA['user']['username'],
            "task_id": 1,
        })
        response = self.client.get(url)
        self.assertRedirects(response, '/')

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

    def test_util_create_default_triages(self):
        user = User.objects.get(username=TEST_DATA['user']['username'])
        TaskUtils.create_default_triage_categories(user.pk)
        defaults = TaskUtils._DEFAULT_TRIAGE

        for triage in user.triages.all():
            self.assertIn(triage.name, defaults)

    def test_task_due_date(self):
        self.test_add_tasklist()

        today = datetime.datetime.utcnow().replace(tzinfo=utc)

        #  0   Not Due
        not_due_date = today + datetime.timedelta(days=7)
        not_due = TaskModels.Task.objects.create(name="Not Due",
                                                tasklist_id=1,
                                                due_date=not_due_date)
        self.assertEquals(not_due.is_due, 0)

        #  1   Due Today
        due_today_date = today + datetime.timedelta(seconds=10)
        due_today = TaskModels.Task.objects.create(name="Due Today",
                                                  tasklist_id=1,
                                                  due_date=due_today_date)
        self.assertEquals(due_today.is_due, 1)

        # -1   Overdue
        overdue_date = today
        overdue = TaskModels.Task.objects.create(name="Overdue",
                                                tasklist_id=1,
                                                due_date=overdue_date)
        self.assertEquals(overdue.is_due, -1)

    def test_task_local_id_ordering(self):
        self.test_add_tasklist(TEST_DATA['user'], TEST_DATA['tasklist'])
        self.test_add_tasklist(TEST_DATA['user2'], TEST_DATA['another_tasklist'])

        task_user1_1 = TaskModels.Task.objects.create(name="T1",
                                                tasklist_id=1)
        task_user1_2 = TaskModels.Task.objects.create(name="T2",
                                                tasklist_id=1)
        task_user2_1 = TaskModels.Task.objects.create(name="T1",
                                                tasklist_id=2)
        task_user1_3 = TaskModels.Task.objects.create(name="T3",
                                                tasklist_id=1)

        self.assertEquals(task_user2_1.local_id, 1)
        self.assertEquals(task_user1_3.local_id, 3)

    def test_dashboard(self):
        self.test_add_tasklist()
        self.test_add_tasklist(TEST_DATA['user'], TEST_DATA['tasklist_2'], 2)

        today = datetime.datetime.utcnow().replace(tzinfo=utc)
        this_week_date = today + datetime.timedelta(days=5)
        this_month_date = today + datetime.timedelta(days=30)

        thisweek_1 = TaskModels.Task.objects.create(name="This Week (1)",
                                                tasklist_id=1,
                                                due_date=this_week_date)
        thisweek_2 = TaskModels.Task.objects.create(name="This Week (2)",
                                                tasklist_id=2,
                                                due_date=this_week_date)
        overdue_date = today
        overdue = TaskModels.Task.objects.create(name="Overdue",
                                                tasklist_id=1,
                                                due_date=overdue_date)

        not_due = TaskModels.Task.objects.create(name="Later This Month",
                                                tasklist_id=2,
                                                due_date=this_month_date)

        url = reverse("task:dashboard", kwargs={
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/dashboard.html')
        self.assertEqual(len(response.context['overdue']), 1)
        self.assertEqual(len(response.context['upcoming_week']), 2)
        self.assertEqual(len(response.context['upcoming_month']), 1)

    def test_add_milestone(self):
        self.test_add_tasklist()
        url = reverse("task:new_milestone", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changemilestone.html')
        response = self.client.post(url, TEST_DATA['milestone'], follow=True)
        self.assertEqual(len(response.context['tasklist'].milestones.all()), 1)
        self.assertContains(response, TEST_DATA['milestone']['name'])
        self.assertContains(response, "style=\"background-color:#"+TEST_DATA['milestone']['bg_colour']+"; color:#"+TEST_DATA['milestone']['fg_colour'])

    def test_edit_milestone(self):
        self.test_add_milestone()
        url = reverse("task:edit_milestone", kwargs={
            "username": TEST_DATA['user']['username'],
            "listslug": slugify(TEST_DATA['tasklist']['name']),
            "milestone_id": 1
        })
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/changemilestone.html')
        response = self.client.post(url, TEST_DATA['milestone_edit'], follow=True)

        self.assertEqual(len(response.context['tasklist'].milestones.all()), 1)
        self.assertContains(response, TEST_DATA['milestone_edit']['name'])
        self.assertContains(response, "style=\"background-color:#"+TEST_DATA['milestone_edit']['bg_colour']+"; color:#"+TEST_DATA['milestone_edit']['fg_colour'])

    def test_register(self):
        url = reverse("account:register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        response = self.client.post(url, TEST_DATA['register'], follow=True)
        self.assertRedirects(response, '/')
        self.assertContains(response, "Hello, "+TEST_DATA['register']['username'])
        self.assertContains(response, "0 task lists")

        user = User.objects.get(username=TEST_DATA['register']['username'])
        defaults = TaskUtils._DEFAULT_TRIAGE

        for triage in user.triages.all():
            self.assertIn(triage.name, defaults)

        self.client.logout()

    def test_register_login(self):
        self.test_register()

        # Triage defaults to forwarding user to / after login
        # Note that django will actually try to forward to "accounts/profile"
        url = reverse("account:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        login_data = {
            "username": TEST_DATA["register"]["username"],
            "password": TEST_DATA["register"]["password1"],
            "next": "/" # Hidden next field
        }
        response = self.client.post(url, login_data, follow=True)
        self.assertRedirects(response, '/')
        self.assertContains(response, "Hello, "+TEST_DATA['register']['username'])
        self.assertContains(response, "0 task lists")

    def test_register_missing(self):
        url = reverse("account:register")
        pops = ["username", "first_name", "last_name", "email"]
        for pop in pops:
            reg_data = TEST_DATA["register"].copy()
            del reg_data[pop]
            response = self.client.post(url, reg_data, follow=True)
            self.assertContains(response, "field is required")

    def test_register_duplicate_username(self):
        self.test_register()
        url = reverse("account:register")
        reg_data = TEST_DATA["register2"].copy()
        reg_data["username"] = TEST_DATA["register"]["username"]

        response = self.client.post(url, reg_data, follow=True)
        self.assertContains(response, "username has already been registered")

    def test_register_duplicate_email(self):
        self.test_register()
        url = reverse("account:register")

        reg_data = TEST_DATA["register2"].copy()
        reg_data["email"] = TEST_DATA["register"]["email"]

        response = self.client.post(url, reg_data, follow=True)
        self.assertContains(response, "email has already been registered")

    def test_register_password_match(self):
        url = reverse("account:register")

        reg_data = TEST_DATA["register2"].copy()
        reg_data["password2"] = "not the password..."

        response = self.client.post(url, reg_data, follow=True)
        self.assertContains(response, "passwords do not match")
