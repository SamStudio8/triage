import django.dispatch
user_registered = django.dispatch.Signal(providing_args=["post","request"])
