from django import forms
import task.models as TaskModels

class TaskForm(forms.ModelForm):
    def __init__(self, user_id=0, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        del self.fields['creation_date']
        del self.fields['modified_date']
        del self.fields['completed_date']
        self.fields['parent'].queryset = TaskModels.Task.objects.filter(tasklist__user_id=user_id, completed=False)
        self.fields['triage'].queryset = TaskModels.TaskTriageCategory.objects.filter(user_id=user_id)

    class Meta:
        model = TaskModels.Task

class TaskListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskListForm, self).__init__(*args, **kwargs)
        del self.fields['user']

    class Meta:
        model = TaskModels.TaskList

class TaskTriageCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskTriageCategoryForm, self).__init__(*args, **kwargs)
        del self.fields['user']

    class Meta:
        model = TaskModels.TaskTriageCategory
