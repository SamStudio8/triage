from django import forms
import task.models as TaskModels

class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self._user_id = user_id
        del self.fields['creation_date']
        del self.fields['modified_date']
        del self.fields['completed_date']
        self.fields['parent'].queryset = TaskModels.Task.objects.filter(tasklist__user_id=user_id, completed=False)
        self.fields['tasklist'].queryset = TaskModels.TaskList.objects.filter(user_id=user_id)
        self.fields['triage'].queryset = TaskModels.TaskTriageCategory.objects.filter(user_id=user_id)

    class Meta:
        model = TaskModels.Task

    def _check_user(self, field_name):
        data = self.cleaned_data[field_name]
        if data:
            if data.user_id != self._user_id:
                raise forms.ValidationError("Invalid selection for "+ field_name +"!")
        return data

    def clean_parent(self):
        return self._check_user("parent")

    def clean_tasklist(self):
        return self._check_user("tasklist")

    def clean_triage(self):
        return self._check_user("triage")

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
