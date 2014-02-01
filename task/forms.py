from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

import task.models as TaskModels

class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        del self.fields['_id']
        del self.fields['creation_date']
        del self.fields['modified_date']
        del self.fields['completed_date']
        self.fields['tasklist'].queryset = TaskModels.TaskList.objects.filter(user_id=user_id)
        self.fields['triage'].queryset = TaskModels.TaskTriageCategory.objects.filter(user_id=user_id)
        self.fields['milestone'].queryset = TaskModels.TaskMilestone.objects.filter(user_id=user_id)

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
                        'progress',
                        'milestone',
                        AppendedText('due_date', '<span class="glyphicon glyphicon-calendar"></span>', data_format="YYYY-MM-DD H:mm"),
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

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()

        if cleaned_data.get('progress') == None:
            cleaned_data["progress"] = 0
        return cleaned_data

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
        if TaskModels.TaskList.objects.filter(user=self._user_id, name=name).count() > 0:
            raise forms.ValidationError('You already have a tasklist with this name.')
        return name

class TaskTriageCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskTriageCategoryForm, self).__init__(*args, **kwargs)
        del self.fields['user']
        self.fields['bg_colour'].label = "Background"
        self.fields['fg_colour'].label = "Text"

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
        del self.fields['user']
        self.fields['bg_colour'].label = "Background"
        self.fields['fg_colour'].label = "Text"

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
                    AppendedText('due_date', '<span class="glyphicon glyphicon-calendar"></span>', data_format="YYYY-MM-DD H:mm"),
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
