from django import forms as forms
from wanted.models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('created', 'approved',)
