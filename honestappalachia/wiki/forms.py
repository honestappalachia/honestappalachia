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


class BulkUploadForm(forms.Form):
    upload = forms.FileField(help_text=
        "A zip archive of .md files, or a single .md file")
    overwrite_exisiting = forms.BooleanField(required=False, help_text=
        "If checked, uploaded files with the same name as existing Wiki pages \
        will overwrite the content of the existing pages")

    def clean_upload(self):
        """Verify the upload file is a .zip or .md file"""
        import re
        upload = self.cleaned_data['upload']
        valid = lambda f: re.compile(r'\.(zip|md)$', re.IGNORECASE).search(f)
        if not valid(upload.name):
            raise forms.ValidationError('Must be a .zip or a .md file')

        return upload
