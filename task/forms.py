from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import task.models as TaskModels

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        del self.fields['tasklist']
        del self.fields['creation_date']
        del self.fields['modified_date']

    class Meta:
        model = TaskModels.Task

class TaskListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        del self.fields['user']

    class Meta:
        model = TaskModels.TaskList
