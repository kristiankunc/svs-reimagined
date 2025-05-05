from django import forms
from web.models import TemplateChoices


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=255, label="Project Name")
    git_url = forms.URLField(label="Git URL")
    git_branch = forms.CharField(max_length=255, label="Git Branch", initial="main")
    template = forms.ChoiceField(
        choices=TemplateChoices.choices,
        label="Template",
        initial=TemplateChoices.NONE,
    )
