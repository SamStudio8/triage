from django import forms
from django.contrib.auth.models import User
from django.utils.html import escape

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset('Basic',
                        'username',
                        'first_name',
                        'last_name',
                        'email',
                    ),
                    css_class="col-lg-6"),
                Div(
                    Fieldset('Password',
                        'password1',
                        'password2',
                    ),
                    css_class="col-lg-6"
                ),
                css_class="row"
            ),
            FormActions(
                Submit('register', 'Register'),
            )
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError('This username has already been registered.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email has already been registered.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password.")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2

