from django import forms as forms

from models import Page, MediaFile

class PageForm(forms.Form):
    name = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea())

    def clean_name(self):
        import re
        from templatetags.wiki import WIKI_WORD

        pattern = re.compile(WIKI_WORD)

        name = self.cleaned_data['name']
        if not pattern.match(name):
            raise forms.ValidationError('Must be a WikiWord.')

        return name

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
