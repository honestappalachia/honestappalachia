import re

from django.db import models
from django.utils.translation import ugettext_lazy as _

from templatetags.wiki import wikify

# Create your models here.
class Page(models.Model):
    '''
    A Wiki page 
    '''
    name = models.CharField(max_length=100)
    content = models.TextField()
    rendered = models.TextField(editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def render(self):
        '''
        Renders body into body_html, as Markdown for now
        Escapes any HTML added by the user.
        Converts any WikiWords into links
        '''
        import markdown
        from toc import genTOC, header_permalinks

        # render self.content as Markdown
        md = markdown.Markdown(
                safe_mode="escape",
                extensions = ['toc'],
                extension_configs = {
                    'toc': [
                        ('anchorlink', True),
                        ('title', 'Table of Contents'),
                    ],
                },
            )
        rend = md.convert(self.content)
        # convert WikiWords to links, save in self.rendered
        self.rendered = wikify(rend)

    def save(self, *args, **kwargs):
        '''
        Override save to add preprocessing
        '''
        self.render()
        super(Page, self).save(*args, **kwargs)

class MediaFile(models.Model):
    '''
    A file that may be uploaded and used in a Wiki page
    '''
    name = models.CharField(max_length=255)
    file = models.FileField(max_length=255, upload_to='wiki')

    # Based on code from FeinCMS's MediaLibrary
    filetypes = (
        ('image', _('Image'), lambda f: re.compile(r'\.(bmp|jpe?g|jp2|jxr|gif|png|tiff?)$', re.IGNORECASE).search(f)),
        ('video', _('Video'), lambda f: re.compile(r'\.(mov|m[14]v|mp4|avi|mpe?g|qt|ogv|wmv)$', re.IGNORECASE).search(f)),
        ('audio', _('Audio'), lambda f: re.compile(r'\.(au|mp3|m4a|wma|oga|ram|wav)$', re.IGNORECASE).search(f)),
        ('pdf', _('PDF document'), lambda f: f.lower().endswith('.pdf')),
        ('swf', _('Flash'), lambda f: f.lower().endswith('.swf')),
        ('txt', _('Text'), lambda f: f.lower().endswith('.txt')),
        ('rtf', _('Rich Text'), lambda f: f.lower().endswith('.rtf')),
        ('zip', _('Zip archive'), lambda f: f.lower().endswith('.zip')),
        ('doc', _('Microsoft Word'), lambda f: re.compile(r'\.docx?$', re.IGNORECASE).search(f)),
        ('xls', _('Microsoft Excel'), lambda f: re.compile(r'\.xlsx?$', re.IGNORECASE).search(f)),
        ('ppt', _('Microsoft PowerPoint'), lambda f: re.compile(r'\.pptx?$', re.IGNORECASE).search(f)),
        ('other', _('Binary'), lambda f: True), # Must be last
    )
    # Build 2-tuple for choices=
    filetypes_choices = tuple([ t[0:2] for t in filetypes ])

    type = models.CharField(max_length=12, editable=False,
            choices=filetypes_choices)

    def determine_filetype(self):
        '''
        Determine the filetype of self.file
        '''
        for type_key, type_name, type_test in self.filetypes:
            if type_test(self.file.name):
                return type_key
        return self.filetypes[-1][0] # otherwise, filetype is 'other'

    def save(self, *args, **kwargs):
        '''
        Override size to determine filetype
        '''
        self.type = self.determine_filetype()
        super(MediaFile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.file.name
