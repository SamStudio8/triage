from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

import task.models as TaskModels

class TriageSplitDateTimeWidget(forms.SplitDateTimeWidget):
    def __init__(self):
        widgets = (forms.DateInput(attrs={'type' : "date", 'data_input':"YYYY-MM-DD"}, format="%Y-%m-%d"),
               forms.TimeInput(attrs={'type': "time"}))
        super(forms.SplitDateTimeWidget, self).__init__(widgets)

def clean_colour(color):
    if color[0] == "#":
        color = color[1:]
    return color

class TaskForm(forms.ModelForm):
    def __init__(self, user_id, tasklist_id, form_type, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        del self.fields['_id']
        del self.fields['creation_date']
        del self.fields['modified_date']
        del self.fields['completed_date']
        self.fields['tasklist'].queryset = TaskModels.TaskList.objects.filter(user_id=user_id)
        self.fields['tasklist'].help_text = "* Moving a task to a different list will remove its milestone"
        self.fields['triage'].queryset = TaskModels.TaskTriageCategory.objects.filter(user_id=user_id)
        self.fields['milestone'].queryset = TaskModels.TaskMilestone.objects.filter(tasklist_id=tasklist_id)
        self.fields['due_date'].widget = TriageSplitDateTimeWidget()

        if form_type == "quick-triage":
            del self.fields['name']
            del self.fields['description']
            del self.fields['tasklist']
            del self.fields['milestone']
            del self.fields['due_date']
            del self.fields['completed']
        elif form_type == "quick-duedate":
            del self.fields['name']
            del self.fields['description']
            del self.fields['tasklist']
            del self.fields['triage']
            del self.fields['milestone']
            del self.fields['completed']
        else:
            # django-crispy-forms
            self.helper = FormHelper()
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-lg-3'
            self.helper.field_class = 'col-lg-9'
            self.helper.layout = Layout(
                Div(
                    Div(
                        Fieldset('Basic',
                            'name',
                            'description',
                            'tasklist',
                        ),
                        css_class="col-lg-6"),
                    Div(
                        Fieldset('Meta',
                            'triage',
                            'milestone',
                            AppendedText('due_date', '<span class="glyphicon glyphicon-calendar"></span>'),
                        ),
                        css_class="col-lg-6"
                    ),
                    css_class="row"
                ),
                Fieldset(
                    'Completed',
                    'completed',
                ),
                FormActions(
                    Submit('save', 'Save'),
                )
            )

    class Meta:
        model = TaskModels.Task

class TaskListForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        del self.fields['user']
        del self.fields['slug']

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            Fieldset(
                'Basic',
                'name',
                'description',
                'order',
            ),
            Fieldset(
                'Privacy',
                'public',
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TaskList

    def clean_name(self):
        name = self.cleaned_data['name']
        if not self.instance.pk:
            if TaskModels.TaskList.objects.filter(user=self._user_id, name=name).count() > 0:
                raise forms.ValidationError('You already have a tasklist with this name.')
        return name

class TaskListDeleteForm(forms.Form):
    tasklist_transfer = forms.ModelChoiceField(label="",
                                               initial="",
                                               required=True,
                                               empty_label=None,
                                               help_text=("Select a tasklist to transfer all tasks within this tasklist to."),
                                               queryset=[])

    def __init__(self, user_id, tasklist_pk, *args, **kwargs):
        super(TaskListDeleteForm, self).__init__(*args, **kwargs)
        self.fields['tasklist_transfer'].queryset = TaskModels.TaskList.objects.filter(user_id=user_id).exclude(pk=tasklist_pk).order_by("name")

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            Fieldset(
                'Transfer',
                'tasklist_transfer',
            ),
            FormActions(
                Submit('delete', 'Delete', css_class="btn-danger"),
            )
        )

class TaskTriageCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskTriageCategoryForm, self).__init__(*args, **kwargs)
        del self.fields['user']
        self.fields['bg_colour'].label = "Background"
        self.fields['fg_colour'].label = "Text"

        # Add 'color' type to colour fields, increase max_length to include hash symbol
        # NOTE The '#' is stripped out in the form validation, model still has max_length of 6
        self.fields['bg_colour'].widget = forms.TextInput(attrs={'type': 'color', 'max_length': 7})
        self.fields['fg_colour'].widget = forms.TextInput(attrs={'type': 'color', 'max_length': 7})
        self.fields['bg_colour'].validators[0].limit_value = 7
        self.fields['fg_colour'].validators[0].limit_value = 7

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Basic',
                    'name',
                    'priority',
                    css_class="col-lg-6",
                ),
                Fieldset(
                    'Label Colour Coding',
                    PrependedText('bg_colour', '#', placeholder="Background Colour"),
                    PrependedText('fg_colour', '#', placeholder="Text Colour"),
                    css_class="col-lg-6",
                ),
                css_class="row"
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TaskTriageCategory

    def clean_bg_colour(self):
        return clean_colour(self.cleaned_data['bg_colour'])

    def clean_fg_colour(self):
        return clean_colour(self.cleaned_data['fg_colour'])

class TaskLinkForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        self._user_id = user_id
        super(TaskLinkForm, self).__init__(*args, **kwargs)
        self.fields['from_task'].queryset = TaskModels.Task.objects.filter(tasklist__user_id=user_id, completed=False)
        self.fields['to_task'].queryset = TaskModels.Task.objects.filter(tasklist__user_id=user_id, completed=False)

    class Meta:
        model = TaskModels.TaskLink

    def clean(self):
        cleaned_data = super(TaskLinkForm, self).clean()
        from_task = cleaned_data.get("from_task")
        to_task = cleaned_data.get("to_task")

        if from_task == to_task:
            raise forms.ValidationError("Cannot link a Task to itself.")

        try:
            link = TaskModels.TaskLink.objects.get(from_task=to_task.pk, to_task=from_task.pk)
            raise forms.ValidationError("A link between these tasks already exists, remove the existing link and try again.")
        except TaskModels.TaskLink.DoesNotExist:
            pass
        return cleaned_data

class TaskMilestoneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskMilestoneForm, self).__init__(*args, **kwargs)
        del self.fields['tasklist']
        self.fields['bg_colour'].label = "Background"
        self.fields['fg_colour'].label = "Text"
        self.fields['due_date'].widget = TriageSplitDateTimeWidget()

        # Add 'color' type to colour fields, increase max_length to include hash symbol
        # NOTE The '#' is stripped out in the form validation, model still has max_length of 6
        self.fields['bg_colour'].widget = forms.TextInput(attrs={'type': 'color', 'max_length': 7})
        self.fields['fg_colour'].widget = forms.TextInput(attrs={'type': 'color', 'max_length': 7})
        self.fields['bg_colour'].validators[0].limit_value = 7
        self.fields['fg_colour'].validators[0].limit_value = 7

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    'Basic',
                    'name',
                    AppendedText('due_date', '<span class="glyphicon glyphicon-calendar"></span>'),
                    css_class="col-lg-6",
                ),
                Fieldset(
                    'Label Colour Coding',
                    PrependedText('bg_colour', '#', placeholder="Background Colour"),
                    PrependedText('fg_colour', '#', placeholder="Text Colour"),
                    css_class="col-lg-6",
                ),
                css_class="row"
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TaskMilestone

    def clean_bg_colour(self):
        return clean_colour(self.cleaned_data['bg_colour'])

    def clean_fg_colour(self):
        return clean_colour(self.cleaned_data['fg_colour'])


class TriageUserPreferencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TriageUserPreferencesForm, self).__init__(*args, **kwargs)
        del self.fields['user']

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.layout = Layout(
            Fieldset(
                'Tasks',
                'default_due_time',
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TriageUser

