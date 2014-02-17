from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

from account.forms import RegistrationForm
from account.signals import user_registered

@sensitive_post_parameters('password', 'password2')
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('task:profile', kwargs={"username": request.user.username}))

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        newUser = {
            "username": form.cleaned_data["username"],
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"],
            "email": form.cleaned_data["email"],
        }
        user = User.objects.create(**newUser)
        user.set_password(form.cleaned_data["password2"])
        user.save()
        user_registered.send(sender=request.POST, post=request.POST, new_user=user, request=request)

        auth_user = authenticate(username=user.username, password=form.cleaned_data["password2"])
        if auth_user:
            login(request, auth_user)
        return HttpResponseRedirect(request.POST.get('next', '/'))

    return render(request, "register.html", {
        'form': form,
    })

