from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters

from account.forms import RegistrationForm

@sensitive_post_parameters('password', 'password2')
def register(request):
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
        return HttpResponseRedirect(request.POST.get('next', '/'))

    return render(request, "register.html", {
        'form': form,
    })

