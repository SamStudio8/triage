from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Submit
from crispy_forms.bootstrap import FormActions

import task.models as TaskModels

class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        del self.fields['creation_date']
        del self.fields['modified_date']
        del self.fields['completed_date']
        self.fields['tasklist'].queryset = TaskModels.TaskList.objects.filter(user_id=user_id)
        self.fields['triage'].queryset = TaskModels.TaskTriageCategory.objects.filter(user_id=user_id)

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                'Basic',
                'name',
                'description',
                'tasklist',
                css_class="col-lg-6",
            ),
            Fieldset(
                'Meta',
                'triage',
                'progress',
                'due_date',
                css_class="col-lg-6",
            ),
            Fieldset(
                'Completed',
                'completed',
                css_class="col-lg-12",
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.Task

class TaskListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        del self.fields['user']

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
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TaskList

class TaskTriageCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskTriageCategoryForm, self).__init__(*args, **kwargs)
        del self.fields['user']

        # django-crispy-forms
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            Fieldset(
                'Basic',
                'name',
                'priority',
                css_class="col-lg-6",
            ),
            Fieldset(
                'Colour Coding',
                'bg_colour',
                'fg_colour',
            ),
            FormActions(
                Submit('save', 'Save'),
            )
        )

    class Meta:
        model = TaskModels.TaskTriageCategory

class TaskLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskLinkForm, self).__init__(*args, **kwargs)

    class Meta:
        model = TaskModels.TaskLink

    def clean(self):
        cleaned_data = super(TaskLinkForm, self).clean()
        from_task = cleaned_data.get("from_task")
        to_task = cleaned_data.get("to_task")

        if from_task and to_task:
            if from_task == to_task:
                raise forms.ValidationError("Cannot link a Task to itself.")
        return cleaned_data
