from django.dispatch import receiver

from account.signals import user_registered

import task.utils as TaskUtils

@receiver(user_registered)
def handle_user_registered(sender, **kwargs):
    post = kwargs.get("post")
    request = kwargs.get("request")
    new_user = kwargs.get("new_user")
    if post:
        TaskUtils.create_default_triage_categories(new_user.pk)
